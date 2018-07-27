from collections import Mapping
from enum import Enum, unique
from types import MappingProxyType
from typing import List


FloatVector = List[float]
IntegerVector = List[int]
StringVector = List[str]
Float2DVector = List[List[float]]


@unique
class ElasticSearchStatusCode(str, Enum):
  YELLOW = 'yellow'
  GREEN = 'green'
  RED = 'red'


class DistanceMetric(str, Enum):
  CityBlock = 'cityblock'
  Cosine = 'cosine'
  Euclidean = 'euclidean'
  L1 = 'l1'
  L2 = 'l2'
  Manhattan = 'manhattan'
  BrayCurtis = 'braycurtis'
  Canberra = 'canberra'
  Chebyshev = 'chebyshev'
  Correlation = 'correlation'
  Dice = 'dice'
  Hamming = 'hamming'
  Jaccard = 'jaccard'
  Kulsinki = 'kulsinki'
  Mahalanobis = 'mahalanobis'
  Minkowski = 'minkowski'
  Rogerstanimoto = 'rogerstanimoto'
  Russellrao = 'russellrao'
  Seuclidean = 'seuclidean'
  Sokalmichener = 'sokalmichener'
  Sokalsneath = 'sokalsneath'
  SqEuclidean = 'sqeuclidean'
  Yule = 'yule'