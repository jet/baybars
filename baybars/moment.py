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

import time


class timer(object):
  def __init__(self, name, logger):
    self.name = name
    self.logger = logger
    self.duration = None

  def __enter__(self):
    self.start = time.time()

    return self

  def __exit__(self,ty,val,tb):
    end = time.time()
    self.duration = 1000 * (end - self.start)
    self.logger.info("{} : {} milliseconds".format(self.name, self.duration))

  @property
  def duration(self):
    return self._duration

  @duration.setter
  def duration(self, value):
    self._duration = value
