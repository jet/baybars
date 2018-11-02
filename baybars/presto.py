
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

# 3rd Party Imports
from pyhive import presto


class Presto(object):

  def __init__(self, host: str, port: str, username: str, catalog: str):
    self.host = host
    self.port = port 
    self.username = username
    self.catalog = catalog
    self.connection = None

  @property
  def host(self) -> str:
    return self._host

  @host.setter
  def host(self, value):
    self._host = value

  @property
  def port(self) -> str:
    return self._port

  @port.setter
  def port(self, value):
    self._port = value

  @property
  def username(self) -> str:
    return self._username

  @username.setter
  def username(self, value):
    self._username = value

  @property
  def catalog(self) -> str:
    return self._catalog

  @catalog.setter
  def catalog(self, value):
    self._catalog = value

  @property
  def connection(self):
    if self._connection is None:
      self.connection = presto.connect(host=self.host, 
                                       port=self.port,
                                       username=self.username,
                                       catalog=self.catalog) 

    return self._connection

  @connection.setter
  def connection(self, value):
    self._connection = value 