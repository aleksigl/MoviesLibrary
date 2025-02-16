import random
from datetime import date


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
        return f'{self.title} ({self.release_year})'

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

    @classmethod
    def add_entire_season(cls, title, release_year, genre, season_no, episodes_to_add: int, library):
        if episodes_to_add > 0:
            for episode in range(1, episodes_to_add + 1):
                tv_series = TvSeries(title, release_year, genre, 0, episode, season_no, library)
                library.add_to_library(tv_series)
            print(f"{episodes_to_add} episodes of tv series {title} season {season_no} successfully added to library.")
        else:
            print("Number of episodes needs to be larger than 0.")

    def __str__(self) -> str:
        return f'{self.title} S{self.season_no:02d}E{self.episode_no:02d}'

    def count_episodes(self, library):
        return library.count_series_episodes(self.title)


class Library:
    def __init__(self):
        self.library = []

    def add_to_library(self, instance):
        if isinstance(instance, Movies):
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

    def search(self, title: str):
        matching_content = [item for item in self.library if item.title == title]
        if matching_content:
            result = f"\nBelow you will find all positions matching {title}:\n"
            result += "\n".join(str(item) for item in matching_content)
            return result
        else:
            return f"No positions found matching {title}."

    def generate_views(self):
        item = random.choice(self.library)
        item.views += random.choice(range(1, 101))
        return item

    def ten_generated_views(self):
        results = []
        for item in range(10):
            result = self.generate_views()
            results.append((result.title, result.views))
        return results

    def top_titles(self, content_type: str, number_of_titles: int):
        top_titles_list = []
        if content_type.lower() == "movie":
            movies = self.get_movies()
            top_titles_list = sorted(movies, key=lambda x: x.views, reverse=True)
        elif content_type.lower() == "tv series":
            series = self.get_series()
            top_titles_list = sorted(series, key=lambda x: x.views, reverse=True)
        else:
            print("Invalid content type. Please choose 'movie' or 'tv series'.")
        top_titles = top_titles_list[:number_of_titles]
        return top_titles

    def count_series_episodes(self, title: str) -> int:
        series_not_movies = self.get_series()
        result = len([item for item in series_not_movies if title == item.title])
        return result


movie_titles = [
    "Inception", "The Matrix", "Avatar", "Interstellar", "The Dark Knight",
    "The Godfather", "Pulp Fiction", "Forrest Gump", "The Shawshank Redemption",
    "The Lord of the Rings"
]
tv_series_titles = [
    "Stranger Things", "Game of Thrones", "The Office", "Friends", "The Crown",
    "Sherlock", "The Witcher", "Black Mirror", "Peaky Blinders",
    "The Big Bang Theory", "Chernobyl"
]
genres = ["Sci-Fi", "Action", "Drama", "Comedy", "Thriller", "Adventure", "Crime", "Horror", "Fantasy"]


def create_random_movie(library):
    title = random.choice(movie_titles)
    release_year = random.randint(1980, 2025)
    genre = random.choice(genres)
    views = random.randint(1_000_000, 50_000_000)
    return Movies(title, release_year, genre, views, library)


def fill_library_with_random_movies(library: Library) -> None:
    for _ in range(6):
        create_random_movie(library)


def create_random_tv_series(library):
    title = random.choice(tv_series_titles)
    release_year = random.randint(1980, 2025)
    genre = random.choice(genres)
    views = random.randint(1_000_000, 50_000_000)
    season_no = random.randint(1, 10)
    episode_no = random.randint(1, 12)
    return TvSeries(title, release_year, genre, views, episode_no, season_no, library)


def fill_library_with_random_tv_series(library: Library) -> None:
    for _ in range(6):
        create_random_tv_series(library)


def generate_views(library: Library):
    generated_view = library.generate_views()
    print(f"\nAdding randomly generated number of views for: {generated_view.title}\n"
          f"Number of views after random increase: {generated_view.views}")


def generate_top_3(library: Library) -> None:
    today = date.today()
    print(f"\nMost popular movies and TV series as of {today.strftime("%d.%m.%Y")}:")

    top_movie_titles = library.top_titles("movie", 3)
    print("\n1. Top three movies:")
    for movie in top_movie_titles:
        print(f"'{movie.title}' - {movie.views} views")

    top_tv_series_titles = library.top_titles("tv series", 3)
    print("\n2. Top three TV series:")
    for tv_series in top_tv_series_titles:
        print(f"'{tv_series.title}' - {tv_series.views} views")


my_library = Library()
print("___MOVIES AND TV SERIES LIBRARY___")
fill_library_with_random_movies(my_library)
fill_library_with_random_tv_series(my_library)
my_library.display_library()
generate_views(my_library)
generate_top_3(my_library)
