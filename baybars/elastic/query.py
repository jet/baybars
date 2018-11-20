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


# Local Imports
from .data_types import ElasticSearchStatusCode


# 3rd Party Imports
from elasticsearch import Elasticsearch


DEFAULT_NUMBER_OF_RESULTS_IN_BATCH = 1000


class ES(object):

  def __init__(self, 
               host: str, 
               port: int, 
               index_name: str,
               doc_type: str,
               total_number_of_results_in_batch=DEFAULT_NUMBER_OF_RESULTS_IN_BATCH):
    self.es_host = host 
    self.port = port 
    self.index_name = index_name
    self.doc_type = doc_type
    self.es = Elasticsearch(self.get_host(self.es_host, self.port))
    self.total_number_of_results_in_batch = total_number_of_results_in_batch

  @classmethod
  def get_host(cls, host: str, port: int) -> list:
    return [
      {'host': host, 'port': port},
    ]

  @property
  def es(self) -> str:
    return self._es

  @es.setter
  def es(self, es: str) -> None:
    self._es = es

  @property
  def total_number_of_results_in_batch(self) -> int:
    return self._total_number_of_results_in_batch

  @total_number_of_results_in_batch.setter
  def total_number_of_results_in_batch(self, total_number_of_results_in_batch: int) -> None:
    self._total_number_of_results_in_batch = total_number_of_results_in_batch

  @property
  def es_host(self) -> str:
    return self._es_host

  @es_host.setter
  def es_host(self, es_host: str) -> None:
    self._es_host = es_host

  @property
  def index_name(self):
    return self._index_name

  @index_name.setter
  def index_name(self, index: str) -> None:
    self._index_name = index

  @property
  def port(self):
    return self._port

  @port.setter
  def port(self, new_port: int) -> int:
    self._port = new_port

  @property
  def total_number_of_results(self):
    return self._total_number_of_results_in_batch

  @total_number_of_results.setter
  def total_number_of_results(self, new_value: int) -> None:
    self._total_number_of_results_in_batch = new_value

  def get(self, id_: str) -> dict:
    return self.es.get(self.index_name, self.doc_type, id_)

  def search(body):
    """
    For a given index name and body of the query, this function will return the matching documents
    :param body: the query that is going to be executed against

    """
    return es.search(index=self.index_name,
                     body={"query": {"match_all": {}}})

  def cluster_health(self):
    return self.es.cluster.health()

  def get_status(self):
    return self.cluster_health().get('status')

  def is_green(self):
    return self.get_status() == ElasticSearchStatusCode.GREEN.value

  def is_red(self):
    return self.get_status() == ElasticSearchStatusCode.RED.value


class CategorySearch(ES):

  def __init__(self, 
               host: str, 
               port: int, 
               index_name: str, 
               doc_type: str,
               category_id: int, 
               total_number_of_results=DEFAULT_NUMBER_OF_RESULTS_IN_BATCH):
    super().__init__(host, port, index_name, doc_type, total_number_of_results)
    self.category_id = category_id

  @property
  def category_id(self) -> int:
    return self._category_id

  @category_id.setter
  def category_id(self, category_id):
    self._category_id = category_id

  def do(self, scroll='2m', search_type='scan', track_scores=True):
    search_query = 'category_id: {}'.format(self.category_id)
    page = self.es.search(q=search_query,
                          scroll=scroll,
                          size=self.total_number_of_results_in_batch,
                          track_scores=track_scores)

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    yield page

    while scroll_size > 0:
      page = self.es.scroll(scroll_id = sid, scroll = '2m')
      if page['hits']['hits']:
        yield page
      sid = page['_scroll_id']
      scroll_size = len(page['hits']['hits'])

  @classmethod
  def get_results_in_a_list(cls, ls: list) -> list:
    out = []
    for item in ls:
      hits = item.get('hits', {}).get('hits', [])
      if hits:
        out.extend(hits)

    return out

    
class KeyValueLookup(ES):

  def __init__(self, host: str, port: int, index_name: str, doc_type: str):
    super().__init__(host, port, index_name, doc_type)
