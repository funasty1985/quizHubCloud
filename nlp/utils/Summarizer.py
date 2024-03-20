import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import spacy

class Summarizer():

    SUMMARY_LENGTH = 50

    def __init__(self):
        self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")
        return

    def gen_summaries(self, text):

        paragraphs = self.split_paragraphs(text)
        summaries = self.summarizer(paragraphs, max_length=200, min_length=50, do_sample=False)
        results = [ele['summary_text'] for ele in summaries]
        return results

    def split_paragraphs(self, text):
        # ref : https://stackoverflow.com/questions/38852712/python-split-on-empty-new-line
        blank_line_regex = r"(?:\r?\n){2,}"
        paragraphs = re.split(blank_line_regex, text.strip())
        return paragraphs

if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")

    text = '''
    With the situation in Europe and Asia relatively stable, Germany, Japan, and the Soviet Union made preparations for war. 
    With the Soviets wary of mounting tensions with Germany, and the Japanese planning to take advantage of the European War by 
    seizing resource-rich European possessions in Southeast Asia, the two powers signed the Soviet–Japanese Neutrality Pact in April 1941.[130] 
    By contrast, the Germans were steadily making preparations for an attack on the Soviet Union, massing forces on the Soviet border.[131]

    Hitler believed that the United Kingdom's refusal to end the war was based on the hope that the United States and 
    the Soviet Union would enter the war against Germany sooner or later.[132] On 31 July 1940, Hitler decided that the 
    Soviet Union should be eliminated and aimed for the conquest of Ukraine, the Baltic states and Byelorussia.[133] 
    However, other senior German officials like Ribbentrop saw an opportunity to create a Euro-Asian bloc against the 
    British Empire by inviting the Soviet Union into the Tripartite Pact.[134] In November 1940, negotiations took place to 
    determine if the Soviet Union would join the pact. The Soviets showed some interest but asked for concessions from Finland, 
    Bulgaria, Turkey, and Japan that Germany considered unacceptable. On 18 December 1940, Hitler issued the directive to prepare for an invasion of the Soviet Union.[135]    '''

    summarizer = Summarizer()
    paras = summarizer.gen_summaries(text)

    for p in paras:
        doc = nlp(p)
        sentences = [sent.text.strip() for sent in doc.sents]

        # Print the tokenized sentences
        for idx, sentence in enumerate(sentences, start=1):
            print(sentence)

        print()
        print()
