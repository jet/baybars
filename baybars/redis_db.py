import redis


class RedisDB(object):
  def __init__(self, host: str, port: int, password: str):
    self.host = host
    self.port = port
    self.password = password
    self.client = redis.Redis(host=self.host, port=self.port, password=self.password)

  def set(self, name, value):
    return self.client.set(name, value)

  def __setattr__(self, name, value):
    return self.self.set(name, value)

  def get(self, key):
    return self.client.get(key)

  def __getattr__(self, key):
    return self.get(key)