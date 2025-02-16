import random


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
                tv_series = TvSeries(title, release_year, genre, views, episode, season_no, library)
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
        item.views = random.choice(range(1, 101))
        return item

    def ten_generated_views(self):
        results = []
        for item in range(10):
            result = self.generate_views()
            results.append((result.title, result.views))
        return results

    def top_titles(self, content_type: str):
        top_titles_list = []
        if content_type.lower() == "movie":
            movies = self.get_movies()
            top_titles_list = sorted(movies, key=lambda x: x.views, reverse=True)
        elif content_type.lower() == "tv series":
            series = self.get_series()
            top_titles_list = sorted(series, key=lambda x: x.views, reverse=True)
        else:
            print("Invalid content type. Please choose 'movie' or 'tv series'.")

        num_titles = random.randint(1, len(top_titles_list))
        random_titles = random.sample(top_titles_list, num_titles)
        return random_titles

    def count_series_episodes(self, title: str) -> int:
        series_not_movies = self.get_series()
        result = len([item for item in series_not_movies if title == item.title])
        return result

my_library = Library()

movie_1 = Movies("Inception", 2010, "Sci-Fi", 1000000, my_library)
tv_series_1 = TvSeries("Stranger Things", 2016, "Horror", 5000000, 3, 1, my_library)
movie_2 = Movies("The Matrix", 1999, "Action", 2000000, my_library)
tv_series_2 = TvSeries("Breaking Bad", 2008, "Crime", 4000000, 12, 5, my_library)
tv_series_3 = TvSeries("Breaking Bad", 2008, "Crime", 3450000, 11, 5, my_library)

my_library.display_library()

movies = my_library.get_movies()
print("\nMovies in the library:")
for movie in movies:
    print(movie)

tv_series = my_library.get_series()
print("\nTV series in the library:")
for series in tv_series:
    print(series)

print(my_library.search("Breaking Bad"))

generated_view = my_library.generate_views()
print(f"\nSelected title: {generated_view.title}\nNumber of views after random increase: {generated_view.views}")

generated_views = my_library.ten_generated_views()
print("\nGenerated views for 10 random items:")
for title, views in generated_views:
    print(f"Selected title: {title}\nNumber of views after random increase: {views}")

top_movie_titles = my_library.top_titles("movie")
print("\nTop movie titles:")
for movie in top_movie_titles:
    print(f"{movie.title} - {movie.views} views")

number_of_episodes = my_library.count_series_episodes("Breaking Bad")
print(f"The number of available episodes for TV Series 'Breaking Bad' is: {number_of_episodes}.")

TvSeries.add_entire_season("Vampire Diaries", 1989, "Drama", 4, 22, my_library)
