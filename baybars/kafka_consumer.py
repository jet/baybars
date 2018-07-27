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

import json
import time

# Local Imports
from .timber import get_logger

# 3rd Party
from confluent_kafka import Consumer, KafkaError

DEFAULT_BATCH_SIZE = 1000
SLEEP_TIME_IN_SECONDS = .1


class KafkaListener:
  def __init__(self, 
               kafka_endpoint, 
               kafka_topic_name, 
               kafka_group_name, 
               sleep_time_in_seconds=SLEEP_TIME_IN_SECONDS):
    self.kafka_endpoint = kafka_endpoint
    self.kafka_topic_name = kafka_topic_name
    self.kafka_group_name = kafka_group_name
    self.consumer = Consumer({
      'bootstrap.servers': self.kafka_endpoint, 
      'group.id': self.kafka_group_name,
      'default.topic.config': {'auto.offset.reset': 'smallest'}
    })
    self.consumer.subscribe([self.kafka_topic_name])
    self.sleep_time_in_seconds = sleep_time_in_seconds
    self.logger = get_logger('{}-{}'.format(self.kafka_topic_name, self.kafka_group_name))

  def consume(self, batch_function, batch_size=DEFAULT_BATCH_SIZE):
    batch = []
    is_running = True
    while is_running:
      time.sleep(self.sleep_time_in_seconds)
      message = self.consumer.poll()
      if not message.error():
        msg = json.loads(message.value())
        batch.append(msg)
        if len(batch) == batch_size:
          out = batch_function(batch)
          self.logger.info('In consume function; total_number_of_messages_produced={}'.format(len(batch)))
          batch = []
      elif message.error().code() != KafkaError._PARTITION_AOF:
        self.logger.error("KafkaListener had the following problem in the consume function={}".format(message.error()))
        is_running = False

    if batch:
      out = batch_function(batch)
      self.logger.info('In consume function; total_number_of_messages_consumed={}'.format(len(batch)))

    self.consumer.close()