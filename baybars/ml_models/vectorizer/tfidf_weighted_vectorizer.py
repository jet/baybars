from collections import defaultdict

# 3rd Party
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFEmbeddingVectorizer(object):
  def __init__(self, word2vec: dict):
    self.word2vec = word2vec
    self.word2weight = None
    self.dim = len(word2vec)

  @classmethod
  def get_tfidf_weights(cls, X):
    tfidf = TfidfVectorizer(analyzer=lambda x: x)
    tfidf.fit(X)
    max_idf = max(tfidf.idf_)
    return defaultdict(lambda: max_idf,
                       [(w, tfidf.idf_[i]) 
                        for w, i in tfidf.vocabulary_.items()])

  def transform(self, X):
    self.word2weight = self.get_tfidf_weights(X)
    return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                    for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])