from sense2vec import Sense2Vec
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import itertools
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import boto3
import tempfile

class Distractor:

    SIM_WORD_NUM = 20
    DIS_NUM = 3

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'quizhubcloud'
        self.model_key = 'corpus/s2v_old'  # Adjust the path as necessary

        # Use /tmp directory in AWS Lambda for storing the model temporarily
        local_model_path = '/tmp/s2v_old'

        # Ensure the directory exists and is empty
        if not os.path.exists(local_model_path):
            os.makedirs(local_model_path, exist_ok=True)
        else:
            # Optionally clear the directory if needed
            for file in os.listdir(local_model_path):
                os.remove(os.path.join(local_model_path, file))

        # Download model from S3 to the temporary directory
        self.download_model_from_s3(self.bucket_name, self.model_key, local_model_path)

        # Loading pretrained model
        self.s2v = Sense2Vec().from_disk(local_model_path)
        self.senTransformer = SentenceTransformer('all-MiniLM-L12-v2')

    def download_model_from_s3(self, bucket, key, local_path):
        """ Download a model directory from S3 to a local path """
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=key):
            for obj in page['Contents']:
                target_path = os.path.join(local_path, obj['Key'].split('/')[-1])
                self.s3_client.download_file(bucket, obj['Key'], target_path)


    def gen_most_similar_words(self, original_word):
        word = original_word.lower()
        word = word.replace(" ", "_")

        sense = self.s2v.get_best_sense(word)
        most_similar = self.s2v.most_similar(sense, n=self.SIM_WORD_NUM)

        most_similar_words = []
        for each_word in most_similar:
            append_word = each_word[0].split("|")[0].replace("_", " ")
            if append_word not in most_similar_words and append_word != word:
                most_similar_words.append(append_word)

        return most_similar_words

    def get_answer_and_distractor_embeddings(self, answer, candidate_distractors):

        answer_embedding = self.senTransformer.encode([answer])
        distractor_embeddings = self.senTransformer.encode(candidate_distractors)

        return answer_embedding, distractor_embeddings


    def mmr(self, doc_embedding: np.ndarray,
            word_embeddings: np.ndarray,
            words: List[str],
            top_n: int = 5,
            diversity: float = 0.9) -> List[Tuple[str, float]]:
        """ Calculate Maximal Marginal Relevance (MMR)
        between candidate keywords and the document.


        MMR considers the similarity of keywords/keyphrases with the
        document, along with the similarity of already selected
        keywords and keyphrases. This results in a selection of keywords
        that maximize their within diversity with respect to the document.

        Arguments:
            doc_embedding: The document embeddings
            word_embeddings: The embeddings of the selected candidate keywords/phrases
            words: The selected candidate keywords/keyphrases
            top_n: The number of keywords/keyhprases to return
            diversity: How diverse the select keywords/keyphrases are.
                       Values between 0 and 1 with 0 being not diverse at all
                       and 1 being most diverse.

        Returns:
             List[Tuple[str, float]]: The selected keywords/keyphrases with their distances

        """

        # Extract similarity within words, and between words and the document
        word_doc_similarity = cosine_similarity(word_embeddings, doc_embedding)
        word_similarity = cosine_similarity(word_embeddings)

        # Initialize candidates and already choose best keyword/keyphras
        keywords_idx = [np.argmax(word_doc_similarity)]
        candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

        for _ in range(top_n - 1):
            # Extract similarities within candidates and
            # between candidates and selected keywords/phrases
            candidate_similarities = word_doc_similarity[candidates_idx, :]
            target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

            # Calculate MMR
            mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
            mmr_idx = candidates_idx[np.argmax(mmr)]

            # Update keywords & candidates
            keywords_idx.append(mmr_idx)
            candidates_idx.remove(mmr_idx)

        return [(words[idx], round(float(word_doc_similarity.reshape(1, -1)[0][idx]), 4)) for idx in keywords_idx]

    def gen_distractors_by_embeddings(self, ):
        return

    def gen_distractors(self, word):
        distractors = self.gen_most_similar_words(word)
        # adding the original word at the beginning of the distractors
        distractors.insert(0, word)

        answer_embedd, distractor_embedds = self.get_answer_and_distractor_embeddings(word, distractors)

        final_distractors = self.mmr(answer_embedd, distractor_embedds, distractors, self.DIS_NUM)
        filtered_distractors = []
        for dist in final_distractors:
            filtered_distractors.append(dist[0])

        return filtered_distractors

if __name__ == '__main__':

    distractor = Distractor()

    # word_list = ['nlp', 'support vector machine', 'svm', 'S3', 'storage management', 'Intelligent Tiering']

    word_list = ['pipelines', 'workflow', 'automation', 'training', 'machine']

    issue_words = []
    for word in word_list:
        try:
            print(distractor.gen_distractors(word))
        except Exception as e:
            issue_words.append(word)

    print("issue words : ", issue_words)