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
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors


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
    self.client = cosmos_client.CosmosClient(self.endpoint, {'masterKey': self.master_key})

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

  def insert_doc(self, doc: dict):
    return self.client.CreateItem(self.collection_link, doc)

  def upsert_doc(self, doc: dict):
    return self.client.UpsertItem(self.collection_link, doc)

  def get_by_id(self, doc_id: str, options=None) -> dict:
    if options is None:
      options = {'partitionKey': doc_id}
    out = None
    doc_link = '{}/docs/{}'.format(self.collection_link, doc_id)  
    response = self.client.ReadItem(doc_link, options=options)
    
    if response:
      out = response

    return out

  def all_ids(self):
    return [ii['id'] for ii in self.get_all_documents()]

  def get_all_documents(self):
    return self.client.ReadItems(self.collection_link)

  def get_databases(self):
    return list(self.client.ReadDatabases())