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

import pandas as pd
import pymssql


class MsSQL:
  def __init__(self, sql_connection: str, username: str, password: str, database_name: str):
    self.connection = pymssql.connect(sql_connection, username, password, database_name)

  def get_sql_query_as_dataframe(self, query):
    return pd.read_sql(query, self.connection)

  def fetch_all(self, query):
    with self.connection.cursor(as_dict=True) as cursor:
      cursor.execute(query)
      out = cursor.fetchall()
    
    return out