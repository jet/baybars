import consul


class ConsulValue(object):

  def __init__(self, base_url=None):
    self.base_url = base_url or self.CONSUL_BASE_URL
    self.consul_obj = None

  @property
  def base_url(self):
    return self._base_url

  @base_url.setter
  def base_url(self, value):
    if ':' in value:
      value, _ = value.split(':')
    self._base_url = value

  @property
  def consul_obj(self):
    if self._consul_obj is None:
      self._consul_obj = consul.Consul(self.base_url)
    return self._consul_obj

  @consul_obj.setter
  def consul_obj(self, value):
    self._consul_obj = value

  def get(self, key):
    out = None
    _, data = self.consul_obj.kv.get(key)
    if data is not None:
      out = data.get('Value').decode("utf-8")

    return out

  def put(self, key, value):
    return self.consul_obj.kv.put(key, value)

  @classmethod
  def try_get_int(cls, val):
    out = None 
    try:
      out = int(val)
    except TypeError:
      pass
      
    return out