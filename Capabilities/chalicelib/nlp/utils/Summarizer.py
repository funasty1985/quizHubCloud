import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import spacy
import pprint


class Summarizer():
    SUMMARY_LENGTH = 50

    def __init__(self):
        self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")
        return

    def gen_summaries_from_text(self, t):
        paragraphs = self.split_paragraphs(t)
        summaries = self.summarizer(paragraphs, max_length=200, min_length=50, do_sample=False)
        results = [ele['summary_text'] for ele in summaries]
        return results

    def gen_summary_per_paragraph(self, text_list):
        summaries = self.summarizer(text_list, max_length=200, min_length=50, do_sample=False)
        results = [ele['summary_text'] for ele in summaries]
        return results

    def split_paragraphs(self, t):
        # ref : https://stackoverflow.com/questions/38852712/python-split-on-empty-new-line
        blank_line_regex = r"(?:\r?\n){2,}"
        paragraphs = re.split(blank_line_regex, t.strip())
        return paragraphs


if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")

    paras = [
        '''
What Is Privacy in AI To address these concerns, privacy in AI involves ensuring that personal data is collected and used in ways that respect individuals' rights to privacy and data protection. This can include techniques such as anonymization and pseudonymization to protect personal data, and the implementation of data protection regulations such as the GDPR (General Data Protection Regulation) in the EU or CCPA (California Consumer Privacy Act) in the US. Privacy in AI also involves ensuring that AI systems are transparent, explainable, and accountable. This means that individuals should be able to understand how their data is being used and have the ability to control its use. Additionally, AI systems should be designed in ways that minimize the risk of bias, discrimination, and other harmful impacts on individuals or groups. Privacy in AI is an essential aspect of developing and deploying ethical and responsible AI systems that respect individuals' rights to privacy and data protection. ''',
        '''
Why Machine Learning Pipelines?
The key benefit of machine learning pipelines lies in the automation of the model life
cycle steps. When new training data becomes available, a workflow which includes
data validation, preprocessing, model training, analysis, and deployment should be
triggered. We have observed too many data science teams manually going through
these steps, which is costly and also a source of errors. Let’s cover some details of the
benefits of machine learning pipelines:
''',
        '''
Ability to focus on new models, not maintaining existing models
Automated machine learning pipelines will free up data scientists from maintain‐
ing existing models. We have observed too many data scientists spending their
days on keeping previously developed models up to date. They run scripts man‐
ually to preprocess their training data, they write one-off deployment scripts, or
they manually tune their models. Automated pipelines allow data scientists to
develop new models, the fun part of their job. Ultimately, this will lead to higher
job satisfaction and retention in a competitive job market.
''',
        '''
Prevention of bugs
Automated pipelines can prevent bugs. As we will see in later chapters, newly
created models will be tied to a set of versioned data and preprocessing steps will
be tied to the developed model. This means that if new data is collected, a new
model will be generated. If the preprocessing steps are updated, the training data
will become invalid and a new model will be generated. In manual machine
learning workflows, a common source of bugs is a change in the preprocessing
step after a model was trained. In this case, we would deploy a model with differ‐
ent processing instructions than what we trained the model with. These bugs
might be really difficult to debug since an inference of the model is still possible,
but simply incorrect. With automated workflows, these errors can be prevented.
''',
        '''
Useful paper trail
The experiment tracking and the model release management generate a paper
trail of the model changes. The experiment will record changes to the model’s
hyperparameters, the used datasets, and the resulting model metrics (e.g., loss or
accuracy). The model release management will keep track of which model was
ultimately selected and deployed. This paper trail is especially valuable if the data
science team needs to re-create a model or track the model’s performance.
''',
        '''
Standardization
Standardized machine learning pipelines improve the experience of a data sci‐
ence team. Due to the standardized setups, data scientists can be onboarded
quickly or move across teams and find the same development environments.
This improves efficiency and reduces the time spent getting set up on a new
project. The time investment of setting up machine learning pipelines can also
lead to an improved retention rate.
The business case for pipelines
The implementation of automated machine learning pipelines will lead to three
key impacts for a data science team:
• More development time for novel models
• Simpler processes to update existing models
• Less time spent to reproduce models
All these aspects will reduce the costs of data science projects. But furthermore, auto‐
mated machine learning pipelines will:
• Help detect potential biases in the datasets or in the trained models. Spotting bia‐
ses can prevent harm to people who interact with the model. For example, Ama‐
zon’s machine learning–powered resume screener was found to be biased against
women.
• Create a paper trail (via experiment tracking and model release management)
that will assist if questions arise around data protection laws, such as Europe’s
General Data Protection Regulation (GDPR).
• Free up development time for data scientists and increase their job satisfaction.''']

    summarizer = Summarizer()
    # paras = summarizer.gen_summaries_from_text(text)
    summaries = summarizer.gen_summary_per_paragraph(paras)
    for p in summaries:
        pprint.pprint(p)
        print()
