import gensim
from gensim import corpora


def analyze_topics(texts):
    # Create a dictionary from the texts
    dictionary = corpora.Dictionary(texts)
    # Create a corpus from the texts
    corpus = [dictionary.doc2bow(text) for text in texts]
    # Train the LDA model on the corpus
    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus, id2word=dictionary, num_topics=5, passes=10
    )
    # Return the topics
    return lda_model.print_topics()
