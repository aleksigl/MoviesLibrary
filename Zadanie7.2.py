class Movies:
    def __init__(self, title: str, release_year: int, genre: str, views: int, library):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.views = views
        self.add_to_library(library)

        if not isinstance(release_year, int) or release_year < 1880 or release_year > 2100:
            raise ValueError("Release year must be a valid integer between 1880 and 2100")

    def play(self):
        self.views += 1

    def __str__(self) -> str:
        return f'\n{self.title} ({self.release_year})'

    def add_to_library(self, library):
        if isinstance(library, Library):
            library.add_to_library(self)
        else:
            print("Invalid library instance.")


class TvSeries(Movies):
    def __init__(self, title: str, release_year: int, genre: str, views: int, episode_no: int, season_no: int, library):
        super().__init__(title, release_year, genre, views, library)
        self.episode_no = episode_no
        self.season_no = season_no

    def __str__(self) -> str:
        return f'\n{self.title} S{self.season_no:02d}E{self.episode_no:02d}'


class Library:
    def __init__(self):
        self.library = []

    def add_to_library(self, instance):
        if isinstance(instance, (Movies, TvSeries)):
            self.library.append(instance)
        else:
            print("Only instances of Movies or TvSeries can be added.")

    def display_library(self):
        for item in self.library:
            print(item)

    def get_movies(self):
        movies_list = [item for item in self.library if isinstance(item, Movies) and not isinstance(item, TvSeries)]
        return sorted(movies_list, key=lambda x: x.title)

    def get_series(self):
        series_list = [item for item in self.library if isinstance(item, TvSeries)]
        return sorted(series_list, key=lambda x: x.title)


my_library = Library()

movie_1 = Movies("Inception", 2010, "Sci-Fi", 1000000, my_library)
tv_series_1 = TvSeries("Stranger Things", 2016, "Horror", 5000000, 3, 1, my_library)
movie_2 = Movies("The Matrix", 1999, "Action", 2000000, my_library)
tv_series_2 = TvSeries("Breaking Bad", 2008, "Crime", 4000000, 12, 5, my_library)

my_library.display_library()

movies = my_library.get_movies()
print("\nMovies in the library:")
for movie in movies:
    print(movie)

tv_series = my_library.get_series()
print("\nTV series in the library:")
for series in tv_series:
    print(series)
