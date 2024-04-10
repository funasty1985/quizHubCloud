from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re


class QuestionGenerator():

    def __init__(self):

        self.pipe = pipeline("text2text-generation", model="iarfmoose/t5-base-question-generator")

        # self.question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
        # self.question_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
    
    def format_input(self, answer, context):
        '''
        Formats the answer and context with the expected tags for loaded model. Answer and Context are of type string
        '''
        model_input = '<answer> ' + answer + ' <context> ' + context
        return model_input

    def generate_question(self, answer, context):
        '''
        Invokes the pipeline to generate the question and return the question as a string
        '''
        formatted_input = self.format_input(answer, context)
        results = self.pipe(formatted_input)
        question = re.sub(r'\?\s*', '', results[0]['generated_text'])
        question = question + '?'

        return question
    
    def generate_questions(self, keyphrases_dict, context):
        '''
        Invokes the pipeline and generates questions for all keyphrases passed.
        Keyphrases must be in a list and mapped to 'KeyPhrases' in a dictionary. 
        '''
        qa_dict = {}
        keyphrases = keyphrases_dict['keyPhrases']
        
        for keyphrase in keyphrases:
            formatted_input = self.format_input(keyphrase, context)
            results = self.pipe(formatted_input)
            question = results[0]['generated_text'][:-2]
            #print('Generated question is', question)
            qa_dict[keyphrase] = question
        
        return qa_dict

if __name__ == '__main__':
    
    answer_test = "Maxwell Perkins"
    context_test= "The novel was inspired by a youthful romance Fitzgerald had with socialite Ginevra King, and the riotous parties he attended on Long Island's North Shore in 1922. Following a move to the French Riviera, Fitzgerald completed a rough draft of the novel in 1924. He submitted it to editor Maxwell Perkins, who persuaded Fitzgerald to revise the work over the following winter. After making revisions, Fitzgerald was satisfied with the text, but remained ambivalent about the book's title and considered several alternatives. Painter Francis Cugat's dust jacket art greatly impressed Fitzgerald, and he incorporated its imagery into the novel"

    q_gen = QuestionGenerator()
    
    #Get single question from Key Phrase
    question = q_gen.generate_question(answer_test, context_test)
    print(question)

    #Get multiple questions from Key Phrases
    keyphrases = {
    "keyPhrases": ["The vast majority", "respondents", "the 2014 Future", "the Internet", "robotics", "artificial intelligence", "wide segments", "daily life", "2025"]
    }
    context = "The vast majority of respondents to the 2014 Future of the Internet canvassing anticipate that robotics and artificial intelligence will permeate wide segments of daily life by 2025, with huge implications for a range of industries such as health care, transport and logistics, customer service, and home maintenance. But even as they are largely consistent in their predictions for the evolution of technology itself, they are deeply divided on how advances in AI and robotics will impact the economic and employment picture over the next decade."
    questions = q_gen.generate_questions(keyphrases_dict=keyphrases, context=context)

    print(questions)



