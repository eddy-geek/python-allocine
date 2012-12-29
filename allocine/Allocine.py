from AllocineApi import AllocineQuery
from Movie import Movie
from Person import Person
from Review import Review

import json

class Allocine(object):
  class SearchResults(object):
    def __init__(self, d, parent):
      self.movies = [Movie(parent=parent, **i) for i in d.get("movie",[])]
      self.persons = [Person(parent=parent, **i) for i in d.get("person",[])]

  def __init__(self, profile = "small"):
    self.query = AllocineQuery(reply_format="json", profile=profile)

  def search(self, qry, count = 10):
    reply = self.query.search(qry, count=count)
    d = json.loads(reply)
    return self.SearchResults(d["feed"], parent=self)

  def getMovie(self, code):
    retval = Movie(code = code, parent=self)
    retval.getInfo(profile)
    return retval

  def getPerson(self, code):
    retval = Person(code = code, parent=self)
    retval.getInfo(profile)
    return retval

  def reviewList(self, movie_code):
    reply = self.query.query_reviewlist(movie_code)
    d = json.loads(reply)
    return [Review(parent=self, **i) for i in d["feed"]["review"]]
  
  def getInfo(self, type, code):
    query_func = getattr(self.query, "query_" + type)
    return json.loads(query_func(code))

if __name__ == "__main__":
  p = Allocine().search("robert de niro").persons[0]
  p.getFilmography()
  for m in p.filmography:
    print("%s played in %s" % (p, m.movie))
  m = Movie(code=32070, parent=Allocine(profile = "large"))
  m.getInfo()
  print("searching 'le parrain'")
  results = Allocine().search("the godfather")
  movie = results.movies[0]
  print("first result is %s" % movie)
  movie.getInfo()
  print("synopsis of %s : %s" % (movie, movie.synopsisShort))