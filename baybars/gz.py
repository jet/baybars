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

from abc import (abstractmethod,ABCMeta,)
import os
import gzip


class AbstractGZDirectory(object):
  """
  Abstract class is going to accept a directory path and output path and gz the directory

  """
  __metaclass__ = ABCMeta

  def __init__(self, input_file_path: str, output_file_path: str, compress_level=0) -> None:
    self.input_file_path = input_file_path
    self.output_file_path = output_file_path
    self.compress_level = compress_level

  @property
  def input_file_path(self) -> str:
    return self._input_file_path

  @input_file_path.setter
  def input_file_path(self, value: str) -> None:
    self._input_file_path = value

  @property
  def output_file_path(self) -> str:
    return self._output_file_path

  @output_file_path.setter
  def output_file_path(self, value: str) -> None:
    self._output_file_path = value

  @property
  def read_mode(self):
    return 'rb'

  @property
  def write_mode(self):
    return 'wb'

  # Need to get the following two functions working for gz file
  @abstractmethod
  def read_from_gzip(self) -> None:
    out = []
    with gzip.open(self.input_file_path, mode=self.read_mode, compresslevel=self.compress_level) as input_file, open(self.output_file_path, self.write_mode) as output_file:
      for line in input_file:
        resp = output_file.write(line)
        out.append(resp)

    return out

  @abstractmethod
  def write_to_gzip(self) -> None:
    with gzip.open(self.output_file_path, self.write_mode) as output_file, open(self.input_file_path, self.read_mode) as input_file:
      output_file.write(input_file)


class GZDirectory(AbstractGZDirectory):
  def __init__(self, input_file_path: str, output_file_path: str) -> None:
    super().__init__(input_file_path, output_file_path)