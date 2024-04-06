from keybert import KeyBERT

class KeyWordsExtractor:

    def __init__(self):
        self.kw_model = KeyBERT()

    def extract_key_words(self, text, keyphrase_ngram_range=(1, 1), stop_words=None):

        keyword_list = self.kw_model.extract_keywords(text, keyphrase_ngram_range=keyphrase_ngram_range, stop_words=stop_words)

        print(keyword_list)
        return [ele[0] for ele in keyword_list ]

    def batch_extract_key_words(self, test_list):
        return [dict(summary=t ,key_words=self.extract_key_words(t)) for t in test_list ]

if __name__ == "__main__":
    kwe = KeyWordsExtractor()

    '''
What Is Privacy in AI Privacy in AI (Artificial Intelligence) refers to the protection of personal data and sensitive information in the development, deployment, and use of AI systems. AI systems often rely on large datasets to train and improve their algorithms, which may contain personal information such as names, addresses, and other identifiable data. In addition, AI systems may collect and analyze personal data in real-time as part of their operations. This can raise privacy concerns, particularly if the data is used in ways that are not transparent or ethical. 


What Is Privacy in AI To address these concerns, privacy in AI involves ensuring that personal data is collected and used in ways that respect individuals' rights to privacy and data protection. This can include techniques such as anonymization and pseudonymization to protect personal data, and the implementation of data protection regulations such as the GDPR (General Data Protection Regulation) in the EU or CCPA (California Consumer Privacy Act) in the US. Privacy in AI also involves ensuring that AI systems are transparent, explainable, and accountable. This means that individuals should be able to understand how their data is being used and have the ability to control its use. Additionally, AI systems should be designed in ways that minimize the risk of bias, discrimination, and other harmful impacts on individuals or groups. Privacy in AI is an essential aspect of developing and deploying ethical and responsible AI systems that respect individuals' rights to privacy and data protection. 


Examples of how privacy is addressed in AI Anonymization and Pseudonymization: AI systems can use techniques such as anonymization and pseudonymization to protect personal data. Anonymization involves removing all identifying information from a dataset, while pseudonymization involves replacing identifying information with a pseudonym or alias. Differential Privacy: Differential privacy is a technique used to protect privacy in statistical databases. It involves adding random noise to data to prevent individuals from being re-identified from a dataset. Federated Learning: Federated learning is a machine learning technique that enables multiple parties to collaborate on the development of a shared model without sharing their data. Instead, each party trains the model on their own data and sends the updated model weights to a central server, which aggregates the updates to create a new model. 


Examples of how privacy is addressed in AI Explainable AI: Explainable AI refers to the ability of an AI system to provide a clear and understandable explanation of how it arrived at a particular decision. This can help to build trust in the system and enable individuals to understand how their personal data is being used. Privacy-Preserving Machine Learning: Privacy-preserving machine learning is a technique that enables machine learning models to be trained on encrypted data. This helps to protect the privacy of the data while still allowing the model to learn from it. These techniques help to protect personal data and enable AI systems to operate in ways that respect individuals' rights to privacy and data protection. 


Why AI Needs Data AI (Artificial Intelligence) needs data to learn and improve its performance. In order to perform tasks such as image recognition, natural language processing, or predictive modeling, an AI system must be trained on large datasets. The process of training an AI model involves feeding it large amounts of data and using algorithms to learn patterns and relationships within the data. The model then uses these patterns and relationships to make predictions or perform other tasks. The quality and quantity of the data used to train an AI model is crucial to its performance. A larger and more diverse dataset can improve the accuracy of the model and reduce the risk of bias or overfitting. 
   '''

    text = '''
The vast majority of respondents to the 2014 Future of the Internet canvassing anticipate that robotics and artificial intelligence will permeate wide segments of daily life by 2025, with huge implications for a range of industries such as health care, transport and logistics, customer service, and home maintenance. But even as they are largely consistent in their predictions for the evolution of technology itself, they are deeply divided on how advances in AI and robotics will impact the economic and employment picture over the next decade.
    '''
    word_list = kwe.extract_key_words(text)

    print(word_list)

