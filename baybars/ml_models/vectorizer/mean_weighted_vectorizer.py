import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


class MeanEmbeddingVectorizer(object):
  def __init__(self, word2vec):
    self.word2vec = word2vec
    self.dim = len(word2vec)

  def transform(self, X):
    return np.array([
        np.mean([self.word2vec[w] for w in words.split(' ') if w in self.word2vec]
                or [np.zeros(self.dim)], axis=0)
        for words in X
    ])