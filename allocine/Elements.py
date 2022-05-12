import datetime
import sys
from .AllocineObject import *

if sys.version_info[0] >= 3: # Python 3
  stringtype = str
else:
  stringtype = basestring

class Movie(AllocineObject):

  class Participation(object):
    def __init__(self, activity, person):
      self.activity = activity
      self.person = person

  def __str__(self):
    try:
      return self.title
    except:
      try:
        return self.originalTitle
      except:
        return "untitled"
  
  __unicode__ = __str__

  def getInfo(self, **args):
    super(Movie, self).getInfo(**args)
    if "castMember" in self.__dict__:
      castMember = []
      for i in self.castMember:
        if "person" in i:
          code = i["person"]["code"]
          i["person"].pop("code")
          p = Person(code, parent=self.parent, **(i["person"]))
          castMember.append(self.Participation(i["activity"], p))
      self.castMember = castMember

class Person(AllocineObject):
  
  class Participation(object):
    def __init__(self, activity, movie):
      self.activity = activity
      self.movie = movie

  def __str__(self):
    if hasattr(self, "name"):
      if isinstance(self.name, stringtype):
        return self.name
      elif "given" in self.name and "family" in self.name:
        return "{:s} {:s}".format(self.name["given"], self.name["family"])
      elif "given" in self.name:
        return self.name["given"]
      elif "family" in self.name:
        return self.name["family"]
      else:
        return str(self.__dict__.keys())
    else:
      return str(self.__dict__.keys())
  
  __unicode__ = __str__

  def getFilmography(self):
    d = self.parent.getInfo("filmography", self.code)["person"]["participation"]
    self.__dict__["filmography"] = []
    for i in d:
      if "movie" in i:
        code = i["movie"]["code"]
        i["movie"].pop("code")
        m = Movie(code, parent=self.parent, **(i["movie"]))
        self.__dict__["filmography"].append(self.Participation(i["activity"], m))

    # return d

class Review(AllocineObject):

  def __init__(self, **kwargs):
    super(Review, self).__init__(**kwargs)
    self.creationDate = datetime.datetime.strptime(self.creationDate, "%Y-%m-%dT%H:%M:%S")

  def __unicode__(self):
    return "%s : %s..." % (
      self.__dict__.get("author","Unknown").encode("utf8"),
      self.__dict__.get("body","Unknown")[:40].encode("utf8")
    )

