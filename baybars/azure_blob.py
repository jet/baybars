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

"""
This module contains a wrapper class to interact with AzureBlob 
"""

import os

# Local Imports
from .timber import get_logger

# 3rd Party Imports
from azure.storage.blob import BlockBlobService, ContentSettings

logger = get_logger('azure_blob_client')


class AzureBlob(object):

  def __init__(self, account_name, account_key, container_name, 
               max_connections=1,
               timeout_in_seconds=60):
    self.account_name = account_name
    self.account_key = account_key
    self.container_name = container_name
    self.blob_service = None
    self.max_connections = max_connections
    self.timeout_in_seconds = timeout_in_seconds

  @property
  def account_name(self) -> str:
    return self._account_name

  @account_name.setter
  def account_name(self, value):
    self._account_name = value

  @property
  def account_key(self) -> str:
    return self._account_key

  @account_key.setter
  def account_key(self, value): 
    self._account_key = value

  @property
  def container_name(self) -> str:
    return self._container_name

  @container_name.setter
  def container_name(self, value):
    self._container_name = value

  @property
  def blob_service(self) -> BlockBlobService:
    if self._blob_service is None:
      self._blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
    return self._blob_service

  @blob_service.setter
  def blob_service(self, value) :
    self._blob_service = value

  def create_container(self):
    return self.blob_service.create_container(self.container_name)

  @property
  def blob_list(self) -> list:
    return [ii.name for ii in self.blob_service.list_blobs(self.container_name)]

  @classmethod
  def progress_callback(cls, current, total) -> None:
    logger.info('{} out of {} is done'.format(current, total))

  def download_blob_to_path(self, blob_name, path) -> dict:
    """
    Downloads a blob from `blob_name` to a given file `path`
    
    :param blob_name: The blob name of the blob 
    :param path: File path where blob is going to be downloaded to 

    :returns: A dictionary that has metadata information about the blob 
    :rtype: dict 
    """
    response = self.blob_service.get_blob_to_path(self.container_name, blob_name, path, 
                                                  max_connections=self.max_connections, 
                                                  progress_callback=self.progress_callback,
                                                  timeout=self.timeout_in_seconds)
    properties = response.properties
    out = {
      'content': response.content,
      'metadata': response.metadata,
      'name': response.name,
      'properties': {
        'blob_type': properties.blob_type,
        'content_length': properties.content_length,
        'content_type': properties.content_settings.content_type,
        'etag': properties.etag,
        'last_modified': properties.last_modified,
      },
      'snapshot': response.snapshot
    }

    return out

  def create_blob(self, blob_name, path, content_settings=None) -> dict:
    """
    Uploads a blob to `blob_name` from a file using file_path: `path` 
    
    :param blob_name: The blob name of the blob 
    :param path: File path where blob is going to be uploaded from 

    :returns: A dictionary that has metadata information about the blob 
    :rtype: dict 
    """
    response = self.blob_service.create_blob_from_path(self.container_name,
                                                       blob_name,
                                                       path,
                                                       content_settings=content_settings)

    return {
      'etag': response.etag,
      'last_modified': response.last_modified,
    }

  def create_blob_from_stream(self, blob_name, stream) -> dict:
    """
    Uploads a blob to `blob_name` from `stream`
    
    :param blob_name: The blob name of the blob 
    :param stream: Stream which is going to create the blob 

    :returns: A dictionary that has metadata information about the blob 
    :rtype: dict 
    """
    response = self.blob_service.create_blob_from_stream(self.container_name,
                                                         blob_name,
                                                         stream)
    return {
      'etag': response.etag,
      'last_modified': response.last_modified,
    }

  def create_blob_from_text(self, blob_name, text) -> dict:
    """
    Uploads a blob to `blob_name` from `stream`
    
    :param blob_name: The blob name of the blob 
    :param stream: Stream which is going to create the blob 

    :returns: A dictionary that has metadata information about the blob 
    :rtype: dict 
    """
    response = self.blob_service.create_blob_from_text(self.container_name,
                                                       blob_name,
                                                       text)
    return {
      'etag': response.etag,
      'last_modified': response.last_modified,
    }

  def delete_blob(self, blob_name):
    return self.blob_service.delete_blob(self.container_name, blob_name)