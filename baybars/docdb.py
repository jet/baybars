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

from copy import deepcopy

# 3rd Party
from pydocumentdb import document_client


DEFAULT_COLLECTION_OPTIONS = {
  'offerEnableRUPerMinuteThroughput': True,
  'offerVersion': "V2",
  'offerThroughput': 400
}


class DocDB(object):

  def __init__(self, endpoint: str, master_key: str, database_name: str, collection_name: str):
    self.endpoint = endpoint
    self.master_key = master_key
    self.database_name = database_name
    self.collection_name = collection_name
    self.client = document_client.DocumentClient(self.endpoint, {'masterKey': self.master_key})
    self.database = None
    self.collection = None

  @property 
  def database_link(self):
    return 'dbs/{}'.format(self.database_name)

  @property
  def collection_link(self):
    return '{}/colls/{}'.format(self.database_link, self.collection_name)

  @property
  def client(self):
    return self._client

  @client.setter
  def client(self, value):
    self._client = value

  @property
  def endpoint(self):
    return self._endpoint

  @endpoint.setter
  def endpoint(self, value: str):
    self._endpoint = value

  @property
  def master_key(self):
    return self._master_key

  @master_key.setter
  def master_key(self, value: str):
    self._master_key = value

  @property
  def database_name(self):
    return self._database_name

  @database_name.setter
  def database_name(self, value):
    self._database_name = value

  @property
  def collection_name(self):
    return self._collection_name

  @collection_name.setter
  def collection_name(self, value):
    self._collection_name = value

  @property
  def database(self):
    if self._database is None:
      resp = [ii for ii in self.get_databases()
              if ii['id'] == self.database_name]
      if resp:
        self._database = resp[0]
      else:
        self._database = self.client.CreateDatabase({'id': self.database_name})
    return self._database

  @database.setter
  def database(self, value):
    self._database = value

  @property
  def collection(self, options=None):
    if self._collection is None:
      if options is None:
        options = deepcopy(DEFAULT_COLLECTION_OPTIONS)
      collections = self.get_collections()
      for collection in collections:
        if collection['id']  == self.collection_name:
          self._collection = collection

      if self._collection is None:
        self._collection = self.client.CreateCollection(self.database['_self'],
                                                        {'id': self.collection_name},
                                                        options)

    return self._collection

  @collection.setter
  def collection(self, value):
    self._collection = value

  def insert_doc(self, doc: dict):
    return self.client.CreateDocument(self.collection['_self'], doc)

  def upsert_doc(self, doc: dict):
    return self.client.UpsertDocument(self.collection['_self'], doc)

  def query_docs(self, query: str, max_number_of_items: int):
    options = {
      'enableCrossPartitionQuery': True,
      'maxItemCount': max_number_of_items,
    }
    return self.client.QueryDocuments(self.collection['_self'], query, options)

  def get_all_docs_in_collection(self, enable_cross_partition_query=True) -> list:
    options = {
      'enableCrossPartitionQuery': enable_cross_partition_query,
    }
    return self.client.QueryDocuments(self.collection['_self'], self.all_query, options)

  def get_by_id(self, doc_id: str) -> dict:
    out = None
    options = {
      'enableCrossPartitionQuery': False,
      'maxItemCount': 1,
    }
    query = { 
      "query": "SELECT * FROM c WHERE c.id='{}'".format(doc_id) 
    } 

    response = list(self.client.QueryDocuments(self.collection['_self'], query, options))
    if len(response) != 0:
      out = response[0]

    return out

  @property
  def all_query(self):
    return 'SELECT * FROM c'

  def all_ids(self):
    query = 'SELECT c.id FROM c'
    options = {
      'enableCrossPartitionQuery': True,
    }
    response = self.client.QueryDocuments(self.collection['_self'], query, options)

    return response

  def get_databases(self):
    return [ii for ii in self.client.ReadDatabases()]

  def get_collections(self):
    return [ii for ii in self.client.QueryCollections(self.database['_self'],
                                                      self.all_query)]
