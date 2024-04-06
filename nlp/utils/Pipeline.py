from Distractor import Distractor
from QuestionGenerator import QuestionGenerator
from Summarizer import Summarizer

import sys
import os

# Get the current directory of Pipeline.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Traverse two directories up to get to project_directory
project_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

module_dir = os.path.join(project_dir, 'Capabilities/chalicelib')
sys.path.append(module_dir)

from comprehend_service import ComprehendService ### module importing not working


# Expected Output: 
'''
{
prompt: "some question?",
answers: ['answer1', 'answer2', 'answer3', 'answer4']
answer: indexOfAnswer, e.g. 0
}
'''

class Pipeline():

    def __init__(self):
        self.qa_gen = QuestionGenerator()
        self.summmarizer = Summarizer()
        self.keyword_gen = ComprehendService()
        self.distractor = Distractor()
        
    
    def generate_context(self, texts):
        '''
        Returns a list containing a summary of each text.

        Inputs:
        List containing strings. 
        '''

        contexts = []
        for text in texts:
            contexts.append(self.summmarizer.gen_summaries(text))
        
        return contexts

    def generate_keyphrases(self, contexts):
        '''
        Returns a dictionary containing all keyphrases for a string of text

        Inputs:
        List containing strings.
        '''
        keyphrases_dict_list = []
        for context in contexts:
            keyphrases_dict_list.append(self.keyword_gen.extract_key_phrases(context))
        
        return keyphrases_dict_list

    def generate_distractors(self, keyphrases_dict_list):
         '''
        Returns a dictionary containing all keyphrases for a string of text

        Inputs:
        List containing strings.
        '''
         answers_distractors = []
         for item in keyphrases_dict_list:
            context_id = item['context_id']
            for keyphrase in item['keyPhrases']:
                answer_distractor_dict = {}
                try:
                    answer_distractor_dict[keyphrase] = self.distractor.gen_distractors(keyphrase)
                    answer_distractor_dict['context_id'] = context_id
                    answers_distractors.append(answer_distractor_dict)
                except Exception as e:
                    answer_distractor_dict[keyphrase] = "Error"
                    answer_distractor_dict['context_id'] = -1  
                    answers_distractors.append(answer_distractor_dict)    
         return answers_distractors


    def generate_questions(self,keyphrases_dict, context):
        '''
        Returns a dictionary containing a summary of each text.

        Inputs:
        List containing strings. 
        '''
        qa_dict = self.qa_gen.generate_questions(keyphrases_dict, context)
        return qa_dict
    
    def pipeline(self, texts):
        '''
        Returns a dictionary containing the prompt, answer, and distractors.

        Inputs:
        List containing strings.
        '''
        contexts = self.generate_context(texts) #creating the context (summarization of the texts)
        keyphrases = self.generate_keyphrases(contexts) #extracting keyphrases from each context \
        
        #getting a list of dictionaries" {Keyphrases: abc, cde, efg, ...}
        #need to link it to each context to generate questions
        #generate questions only if distractors were able to be generated, else, skip generating the question. 

        context_keyphrase_dict = {}
        
        for i in len(contexts):
            keyphrase_context_id = {'keyphrases': keyphrases[i], 'context_id': i}
            context_keyphrase_dict[contexts[i]] = keyphrase_context_id 
        
        #context and keywords are mapped. Now generate distractors
        keyphrase_distractor_dict_list = self.generate_distractors(keyphrases)

        #all keyphrases have their distractors,they are not linked to their context 
        # {'blablabla' : keyphrases: { 1, 2, 3}, id : 0}
        return keyphrase_distractor_dict_list

        

if __name__ == '__main__':
    
   
    pipe = Pipeline()
    
    texts = ["The cell is the basic structural and functional unit of all forms of life. Every cell consists of cytoplasm enclosed within a membrane; many cells contain organelles, each with a specific function. The term comes from the Latin word cellula meaning 'small room'. Most cells are only visible under a microscope. Cells emerged on Earth about 4 billion years ago. All cells are capable of replication, protein synthesis, and motility.",
             "Cells are broadly categorized into two types: eukaryotic cells, which possess a nucleus, and prokaryotic cells, which lack a nucleus but have a nucleoid region. Prokaryotes are single-celled organisms such as bacteria, whereas eukaryotes can be either single-celled, such as amoebae, or multicellular, such as some algae, plants, animals, and fungi. Eukaryotic cells contain organelles including mitochondria, which provide energy for cell functions; chloroplasts, which create sugars by photosynthesis, in plants; and ribosomes, which synthesise proteins.",
             "Cells were discovered by Robert Hooke in 1665, who named them for their resemblance to cells inhabited by Christian monks in a monastery. Cell theory, developed in 1839 by Matthias Jakob Schleiden and Theodor Schwann, states that all organisms are composed of one or more cells, that cells are the fundamental unit of structure and function in all living organisms, and that all cells come from pre-existing cells.",
             "Organelles are parts of the cell that are adapted and/or specialized for carrying out one or more vital functions, analogous to the organs of the human body (such as the heart, lung, and kidney, with each organ performing a different function).[6] Both eukaryotic and prokaryotic cells have organelles, but prokaryotic organelles are generally simpler and are not membrane-bound."]
    results = pipe.pipeline(texts)
    print(results)