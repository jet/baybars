# Copyright 2018 Jet.com 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import os
# Local Imports
from ..data_types import FloatVector, StringVector, Float2DVector
# 3rd Party Imports
import gensim



class Word2VecModel(object):

  """
  Lightweight wrapper around word2vec model so that we can use to get vector representation of words
  """

  def __init__(self, model_file_path: str):
    self.model_file_path = model_file_path
    self.model = None

  @property
  def model_file_path(self) -> str:
    return self._model_file_path

  @model_file_path.setter
  def model_file_path(self, model_file_path: str) -> None:
    self._model_file_path = model_file_path

  @property
  def model(self):
    if self._model is None:
      self._model = gensim.models.KeyedVectors.load_word2vec_format(self.model_file_path)
    return self._model

  @model.setter
  def model(self, model: str) -> None:
    self._model = model

  def get_vector(self, word: str) -> FloatVector:
    """ Returns the vector representation of the word which has 300 dimensions based on the training data
    We then convert into a Python list
    This will be an endpoint which will provide a vector for a single text
    """
    out = []
    if word in self.model.wv:
      out = self.model.word_vec(word).tolist()

    return out

  def get_vectors(self, words: StringVector) -> Float2DVector:
    """ Returns a two dimensional vector representation for multiple words
    If word is not present in the dictionary, it is going to be an empty list
    """
    return [self.get_vector(ii) for ii in words]