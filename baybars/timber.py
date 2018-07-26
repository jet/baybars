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



import logging
import sys


def get_logger(name):
  logger = logging.getLogger(name)
  stream_stdout = logging.StreamHandler(sys.stdout)
  stream_stdout.setLevel(logging.INFO)
  stream_stderr = logging.StreamHandler(sys.stderr)
  stream_stderr.setLevel(logging.ERROR)
  formatter = logging.Formatter('[baybars][%(name)s][%(asctime)s][%(levelname)s]:%(message)s')
  stream_stdout.setFormatter(formatter)
  stream_stderr.setFormatter(formatter)
  logger.addHandler(stream_stdout)
  logger.addHandler(stream_stderr)
  logger.setLevel(logging.INFO)

  return logger 