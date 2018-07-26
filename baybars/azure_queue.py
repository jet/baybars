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
This module has a very light wrapper to interact Azure Queue
"""

import os
# 3rd Party Imports
from azure.storage.queue import QueueService, QueueMessage


BATCH_NUMBER = 16
TIMEOUT_IN_SECONDS = 300


class AzureQueue(object):

  def __init__(self, account_name, account_key, queue_name):
    self.queue_name = queue_name
    self.queue_service = QueueService(account_name=account_name, account_key=account_key)
    self.queue_service.create_queue(self.queue_name)

  def put_message_into_queue(self, content) -> QueueMessage:
    """
    Publishes a message with `content`
    
    :param content: The queue message 

    :returns: A QueueMessage that has the message as well as metadata 
    :rtype: QueueMessage 
    """
    return self.queue_service.put_message(self.queue_name, content)

  def get_messages(self) -> list:
    """
    Retrieves all of the messages that have been published into queue 
    
    :param content: The queue message 

    :returns: List of Queue messages
    :rtype: list 
    """

    return self.queue_service.get_messages(self.queue_name)

  def delete_message_from_queue(self, message_id, pop_receipt):
    self.queue_service.delete_message(self.queue_name, message_id, pop_receipt)

  def get_message_count(self):
    queue_metadata = self.queue_service.get_queue_metadata(self.queue_name)
    return queue_metadata.approximate_message_count

  def delete(self):
    return self.queue_service.delete_queue(self.queue_name)

  def empty(self):
    messages = queue_service.get_messages(self.queue_name, 
                                          num_messages=BATCH_NUMBER, 
                                          visibility_timeout=TIMEOUT_IN_SECONDS) 
    for message in messages:
      self.queue_service.delete_message(self.queue_name, message.id, message.pop_receipt)