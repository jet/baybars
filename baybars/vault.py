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

from enum import Enum
import os

# 3rd Party
import hvac


class Vault:
  def __init__(self, vault_address: str, vault_token: str):
    self.vault_address = vault_address 
    self.vault_token = vault_token 
    self.client = hvac.Client(url=self.vault_address, token=self.vault_token)

  @classmethod
  def deserialize_data(cls, d: dict):
    key, value = None, None
    data = d.get('data', {})
    if data and len(data) == 1:
      key, value = list(data.items())[0]

    return key, value

  def get(self, key):
    return self.deserialize_data(self.client.read(key))