
class AllocineObject(object):
  _cache = dict()

  def __new__(cls, code, parent, **kwargs):
    AllocineObject._cache.setdefault(cls.__name__,{})
    if code in AllocineObject._cache[cls.__name__]:
      obj = AllocineObject._cache[cls.__name__][code]
      obj.__init__(code, parent, **kwargs)
    else:
      obj = super(AllocineObject, cls).__new__(cls)
      AllocineObject._cache[cls.__name__][code] = obj
    return obj

  def __init__(self, code, parent, **kwargs):
    self.code = code
    self.parent = parent
    for k,v in kwargs.items():
      self.__dict__[k] = v

  def __unicode__(self):
    return self.__class__.__name__

  def __repr__(self):
    return ("<%s #%s: %s>" % (
      self.__class__.__name__,
      self.code,
      self.__unicode__()
    ))

  def getInfo(self, **args):
    d = self.parent.getInfo(self.__class__.__name__.lower(), self.code, **args)
    for k,v in d[self.__class__.__name__.lower()].items():
      self.__dict__[k] = v
