from utils import Distractor, KeyWordsExtractor, Summarizer
import time
import pprint

para_list = [
    '''In this first chapter, we will introduce machine learning pipelines and outline all the
steps that go into building them. We’ll explain what needs to happen to move your
machine learning model from an experiment to a robust production system. We’ll
also introduce our example project that we will use throughout the rest of the book to
demonstrate the principles we describe.''',
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

if __name__ == '__main__':


    # instantiation
    distractor = Distractor.Distractor()
    key_word_extractor = KeyWordsExtractor.KeyWordsExtractor()
    summarizer = Summarizer.Summarizer()

    # summarization
    start_time = time.time()
    context_list = summarizer.gen_summary_per_paragraph(para_list)
    print("--- %s summarization time (seconds) ---" % (time.time() - start_time))

    # key words extraction
    start_time = time.time()
    key_words_by_context = key_word_extractor.batch_extract_key_words(context_list)
    pprint.pprint(key_words_by_context)
    print("--- %s key words extraction time (seconds) ---" % (time.time() - start_time))
