cd nlp/utils


> wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
> mkdir corpus
> tar -xvf s2v_reddit_2015_md.tar.gz -C ./corpus
> rm s2v_reddit_2015_md.tar.gz

> python -m spacy download en_core_web_sm