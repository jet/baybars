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

import os

NOMAD_META_REGION = os.environ.get('NOMAD_META_REGION')
NOMAD_META_ENV = os.environ.get('NOMAD_META_ENV')
NOMAD_META_GIT_COMMIT = os.environ.get('NOMAD_META_GIT_COMMIT')
NOMAD_META_BUILD_TIMESTAMP = os.environ.get('NOMAD_META_BUILD_TIMESTAMP')
NOMAD_META_VERSION = os.environ.get('NOMAD_META_VERSION')
CONSUL_ADDR = os.environ.get('CONSUL_ADDR')
