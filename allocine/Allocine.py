from .AllocineApi import AllocineQuery
from .Elements import Movie, Person, Review
from .settings import DEFAULT_PROFILE

import json

class Allocine(object):
  class SearchResults(object):
    def __init__(self, d, parent):
      self.movies = [Movie(parent=parent, **i) for i in d.get("movie",[])]
      self.persons = [Person(parent=parent, **i) for i in d.get("person",[])]
      self.medias = d.get("media",[])

  def __init__(self, profile="small"):
    self.query = AllocineQuery(reply_format="json", profile=profile)

  def search(self, qry, count = 10, **args):
    reply = self.query.search(qry, count=count, **args)
    d = json.loads(reply)
    return self.SearchResults(d["feed"], parent=self)
  
  def search_movies(self, keywords, count = 10):
    return self.search(keywords, count, filter="movie")
  
  def search_people(self, keywords, count = 10):
    return self.search(keywords, count, filter="person")
  
  def getMovie(self, code, profile=DEFAULT_PROFILE):
    retval = Movie(code = code, parent=self)
    retval.getInfo(profile)
    return retval

  def getPerson(self, code, profile=DEFAULT_PROFILE):
    retval = Person(code = code, parent=self)
    retval.getInfo(profile)
    return retval

  def reviewList(self, movie_code):
    reply = self.query.query_reviewlist(movie_code)
    d = json.loads(reply)
    return [Review(parent=self, **i) for i in d["feed"]["review"]]
  
  def getInfo(self, type, code, **args):  # ignore **profile arg
    query_func = getattr(self.query, "query_" + type)
    return json.loads(query_func(code))
