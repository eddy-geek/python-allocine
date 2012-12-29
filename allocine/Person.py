from AllocineObject import *
import Movie
import sys

if sys.version_info[0] >= 3: # Python 3
  stringtype = str
else:
  stringtype = basestring

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
        m = Movie.Movie(code, parent=self.parent, **(i["movie"]))
        self.__dict__["filmography"].append(self.Participation(i["activity"], m))

    # return d