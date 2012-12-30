from allocine import Allocine, Movie

def main():
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

if __name__ == "__main__":
  main()