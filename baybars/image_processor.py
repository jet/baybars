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

import base64
from io import BytesIO

# 3rd Party Import
import requests
import numpy as np
from PIL import Image


async def get_as_base64_of_url(url):
    out = None
    resp = requests.get(url) 
    if resp.status_code == 200:
      out = base64.b64encode(resp.content)

    return out


def convert_image_to_rgb(image):
  image = Image.open(BytesIO(base64.b64decode(image)))
  image = image.convert('RGB')
  thefile = BytesIO()
  image.save(thefile, "jpeg")
  out = thefile.getvalue()
  thefile.close()

  return out 