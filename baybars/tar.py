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

from abc import (
  abstractmethod,
  ABCMeta,
)
from enum import Enum, unique
import os
import tarfile


@unique
class CompressionMode(str, Enum):
  NO_COMPRESSION = ''
  GZIP_COMPRESSION = 'gz'
  BZIP2_COMPRESSION = 'bz2'


class AbstractTarDirectory(object):
  """
  Abstract class is going to accept a directory path and output path and tars the directory
  with the compression mode method

  """
  __metaclass__ = ABCMeta

  def __init__(self, directory_path: str, file_path: str, mode: str) -> None:
    self.directory_path = directory_path
    self.file_path = file_path
    self.mode = mode

  @property
  def write_mode(self) -> str:
    return 'w:{}'.format(self.mode)

  @property
  def read_mode(self) -> str:
    return 'r:{}'.format(self.mode)

  @property
  def directory_path(self) -> str:
    return self._directory_path

  @directory_path.setter
  def directory_path(self, value: str) -> None:
    self._directory_path = value

  @property
  def file_path(self) -> str:
    return self._file_path

  @file_path.setter
  def file_path(self, value: str) -> None:
    self._file_path = value

  @property
  def mode(self) -> str:
    return self._mode

  @mode.setter
  def mode(self, value: str) -> None:
    self._mode = value

  @abstractmethod
  def create(self) -> None:
    with tarfile.open(self.file_path, self.write_mode) as tar:
      tar.add(self.directory_path, arcname=os.path.basename(self.directory_path))

  @abstractmethod
  def extract(self) -> None:
    with tarfile.open(self.file_path, self.read_mode) as tar:
      tar.extractall(path=self.directory_path)


class TarDirectory(AbstractTarDirectory):

  def __init__(self, directory_path: str, file_path: str) -> None:
    super().__init__(directory_path, file_path, CompressionMode.NO_COMPRESSION)


class TarGZDirectory(AbstractTarDirectory):

  def __init__(self, directory_path: str, file_path: str) -> None:
    super().__init__(directory_path, file_path, CompressionMode.GZIP_COMPRESSION)


class TarBZ2Directory(AbstractTarDirectory):

  def __init__(self, directory_path: str, file_path: str) -> None:
    super().__init__(directory_path, file_path, mode=CompressionMode.BZIP2_COMPRESSION)
