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


from datetime import datetime, timedelta
import os
import sys

# Local Imports
from .timber import get_logger

# 3rd Party
import pysftp

logger = get_logger('ftp')

CURRENT_DIRECTORY = ''


class FTP(object):

  def __init__(self, server, username, password, timeout_in_seconds: int):
    self.cnopts = pysftp.CnOpts()
    self.cnopts.hostkeys = None
    self.server = server
    self.username = username
    self.password = password
    self.timeout_in_seconds = timeout_in_seconds

  def create_directory(self, directory_name):
    out = None
    with pysftp.Connection(host=self.server, username=self.username, password=self.password, cnopts=self.cnopts) as sftp:
      with sftp.cd(CURRENT_DIRECTORY):
        out = sftp.makedirs(directory_name)

    return out

  def upload_file(self, local_path, remote_directory_name, remote_file_name):
    remote_path = '{}/{}/{}'.format(CURRENT_DIRECTORY, remote_directory_name, remote_file_name)
    with pysftp.Connection(host=self.server, username=self.username, password=self.password, cnopts=self.cnopts) as sftp:
      with sftp.cd(CURRENT_DIRECTORY):
        out = sftp.put(local_path, remote_path)
        logger.info('local_path={} is put into remote_path={}'.format(local_path, remote_path))

    return out 