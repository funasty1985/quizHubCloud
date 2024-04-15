import random
from .Distractor import Distractor
from .QuestionGenerator_v2 import QuestionGenerator
from .Summarizer import Summarizer
from .KeyWordsExtractor import KeyWordsExtractor

# Expected Output: 
'''
{
prompt: "some question?",
answers: ['answer1', 'answer2', 'answer3', 'answer4']
answer: indexOfAnswer, e.g. 0
}
'''

class GenQuestionPipeline():

    def __init__(self):
        self.qa_gen = QuestionGenerator()
        self.summmarizer = Summarizer()
        self.keyword_gen = KeyWordsExtractor()
        self.distractor = Distractor()
        
    
    def generate_context(self, texts):
        '''
        Returns a list containing a summary of each text.

        Inputs:
        List containing strings. 
        '''

        contexts = []
        contexts = self.summmarizer.gen_summary_per_paragraph(texts)
        
        return contexts

    def generate_keyphrases(self, contexts):
        '''
        Returns a dictionary containing all keyphrases for a string of text

        Inputs:
        List containing strings.
        '''
        keyphrases_dict_list = []
        for i,context in enumerate(contexts):
            context_keyphrase_dict = {}
            context_keyphrase_dict[context] = self.keyword_gen.extract_key_words(context)
            context_keyphrase_dict['context_id'] = i
            keyphrases_dict_list.append(context_keyphrase_dict)
        
        return keyphrases_dict_list

    def generate_distractors(self, keyphrases_dict_list):
         '''
        Returns a dictionary containing all keyphrases for a string of text

        Inputs:
        List containing strings.
        '''
         # Receives an list of disctionaries of format   [{'context': ['keyword1', 'keyword2', 'keyword3', 'keyword4'], 'context_id': 0}
         #print('Keyphrases received:', keyphrases_dict_list)
         entries = []
         context = ''
         answer  = ''
         distractors = []
         context_id = -1


         for item in keyphrases_dict_list:
             keys = item.keys()
             context = list(keys)[0]
             keyphrases = item[context]
             context_id = item['context_id']
             #print('keyphrases to distractors:', keyphrases)
             for keyword in keyphrases:
                 #print(keyword)
                 answer = keyword
                 try:
                    distractors = self.distractor.gen_distractors(answer)
                    entry = {'entry': {'context': context, 'answer': answer, 'distractors': distractors, 'context_id':context_id}}
                    entries.append(entry)
                 except Exception as e:
                    print(f'Not possible to generate distractors for: {answer}. Skipping')                    
         return entries
             

    def generate_questions(self,keyphrases_dict):
        '''
        Returns a list of dictionaries containing an entry with context, prompt, answer, disstractor, and context_id.

        Inputs:
        Dictionary containing entries with context, answer, distractor, and context id.  
        '''
        updated_entries = []
        for item in keyphrases_dict:
            entry = item['entry']
            answer = entry['answer']
            context = entry['context']
            try:
                question = self.qa_gen.generate_question(answer, context)
                entry['prompt'] = question
                updated_entries.append({'entry':entry})
            except:
                print(f'Not able to generate question for context {context}'. Skipping)
        return updated_entries
    
    def format_output(self, updated_entries):
        '''
        Returns a list of entries containing prompt, answers, and index of answer
        
        Inputs:
        List of dictionaries containing entries with context, answer, distractors, promtps, and context id.
        '''
        formatted_entries = []
        for item in updated_entries:
            entry = item['entry']
            answer = entry['answer']
            distractors = entry['distractors']
            prompt = entry['prompt']

            print('Actual answer:', answer)
            # Generate a random index to insert the answer into the distractor list
            random_index = random.randint(0, len(distractors))

            # Insert the answer into the list at the random index
            distractors.insert(random_index, answer)

            entry = {'prompt': prompt, 'options': distractors, 'answer':random_index}
            formatted_entries.append(entry)
        
        return formatted_entries
    
    def pipeline(self, texts):
        '''
        Returns a dictionary containing the prompt, answer, and distractors.

        Inputs:
        List containing strings.
        '''
        contexts = self.generate_context(texts) #creating the context (summarization of the texts)
        keyphrases = self.generate_keyphrases(contexts) #extracting keyphrases from each context \
        
        #print('Contexts:', contexts)
        #print('Keyphrases:', keyphrases)

        #getting a list of dictionaries" [{'context': ['keyword1', 'keyword2', 'keyword3', 'keyword4'], 'context_id': 0}
        #need to link it to each context to generate questions
        #generate questions only if distractors were able to be generated, else, skip generating the question. 

        #print(context_keyphrase_dict)

        #context and keywords are mapped. Now generate distractors
        keyphrase_distractor_dict_list = self.generate_distractors(keyphrases)
        #returns a list of dictionaries of format [{'entry': 'context': context, 'answer': answer, 'distractors': ['distractor1', 'distractor2'], 'context_id: 0}]

        entry_list = self.generate_questions(keyphrase_distractor_dict_list)

        updated_entry_list = self.format_output(entry_list)
        
        return updated_entry_list
        #print(keyphrase_distractor_dict_list)
        #all keyphrases have their distractors,they are not linked to their context 
        # {'blablabla' : keyphrases: { 1, 2, 3}, id : 0}
        #return keyphrase_distractor_dict_list

        

if __name__ == '__main__':
    
    pipe = GenQuestionPipeline()
    
    texts = ["The cell is the basic structural and functional unit of all forms of life. Every cell consists of cytoplasm enclosed within a membrane; many cells contain organelles, each with a specific function. The term comes from the Latin word cellula meaning 'small room'. Most cells are only visible under a microscope. Cells emerged on Earth about 4 billion years ago. All cells are capable of replication, protein synthesis, and motility.",
             "Cells are broadly categorized into two types: eukaryotic cells, which possess a nucleus, and prokaryotic cells, which lack a nucleus but have a nucleoid region. Prokaryotes are single-celled organisms such as bacteria, whereas eukaryotes can be either single-celled, such as amoebae, or multicellular, such as some algae, plants, animals, and fungi. Eukaryotic cells contain organelles including mitochondria, which provide energy for cell functions; chloroplasts, which create sugars by photosynthesis, in plants; and ribosomes, which synthesise proteins.",
             "Cells were discovered by Robert Hooke in 1665, who named them for their resemblance to cells inhabited by Christian monks in a monastery. Cell theory, developed in 1839 by Matthias Jakob Schleiden and Theodor Schwann, states that all organisms are composed of one or more cells, that cells are the fundamental unit of structure and function in all living organisms, and that all cells come from pre-existing cells.",
             "Organelles are parts of the cell that are adapted and/or specialized for carrying out one or more vital functions, analogous to the organs of the human body (such as the heart, lung, and kidney, with each organ performing a different function).[6] Both eukaryotic and prokaryotic cells have organelles, but prokaryotic organelles are generally simpler and are not membrane-bound."]
    results = pipe.pipeline(texts)
    print(results)