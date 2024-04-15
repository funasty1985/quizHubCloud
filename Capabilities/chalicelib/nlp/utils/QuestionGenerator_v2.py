from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re


class QuestionGenerator():

    def __init__(self):

        # self.pipe = pipeline("text2text-generation", model="iarfmoose/t5-base-question-generator")
        self.question_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
        self.question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')

    def get_question(self, sentence, answer, mdl, tknizer):
        text = "context: {} answer: {}".format(sentence, answer)
        print(text)
        max_len = 256
        encoding = tknizer.encode_plus(text, max_length=max_len, pad_to_max_length=False, truncation=True,
                                       return_tensors="pt")

        input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

        outs = mdl.generate(input_ids=input_ids,
                            attention_mask=attention_mask,
                            early_stopping=True,
                            num_beams=5,
                            num_return_sequences=1,
                            no_repeat_ngram_size=2,
                            max_length=300)

        dec = [tknizer.decode(ids, skip_special_tokens=True) for ids in outs]

        Question = dec[0].replace("question:", "")
        Question = Question.strip()
        return Question

    def generate_question(self, keyphrase, context):
        '''
        Invokes the pipeline to generate the question and return the question as a string
        '''
        question = self.get_question(context, keyphrase, self.question_model, self.question_tokenizer)
        question = re.sub(r'\?\s*', '', question) + '?'
        return question

if __name__ == '__main__':
    
    q_gen = QuestionGenerator()

    answer_test = "Maxwell Perkins"
    context_test= "The novel was inspired by a youthful romance Fitzgerald had with socialite Ginevra King, and the riotous parties he attended on Long Island's North Shore in 1922. Following a move to the French Riviera, Fitzgerald completed a rough draft of the novel in 1924. He submitted it to editor Maxwell Perkins, who persuaded Fitzgerald to revise the work over the following winter. After making revisions, Fitzgerald was satisfied with the text, but remained ambivalent about the book's title and considered several alternatives. Painter Francis Cugat's dust jacket art greatly impressed Fitzgerald, and he incorporated its imagery into the novel"
    questions = q_gen.generate_question(answer_test, context=context_test)

    print(questions)



