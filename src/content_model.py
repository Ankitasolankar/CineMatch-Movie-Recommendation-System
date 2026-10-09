from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def build_content_model():
    movies = pd.read_csv(DATA_DIR / "movies.csv")

    # Replace missing genres with empty text
    movies["genres"] = movies["genres"].fillna("")

    # Convert movie genres into numerical features
    vectorizer = TfidfVectorizer(token_pattern=r"[^|]+")
    genre_matrix = vectorizer.fit_transform(movies["genres"])

    # Calculate similarity between movies
    similarity_matrix = cosine_similarity(genre_matrix)

    return movies, similarity_matrix


def recommend_movies(movie_title, number_of_recommendations=5):
    movies, similarity_matrix = build_content_model()

    matches = movies[
        movies["title"].str.contains(
            movie_title, case=False, regex=False, na=False
        )
    ]

    if matches.empty:
        print("Movie not found. Please try another title.")
        return

    movie_index = matches.index[0]

    scores = list(enumerate(similarity_matrix[movie_index]))
    scores = sorted(scores, key=lambda item: item[1], reverse=True)

    # Skip the selected movie itself
    scores = [
        item for item in scores if item[0] != movie_index
    ][:number_of_recommendations]

    print(f"\nBecause you selected: {movies.iloc[movie_index]['title']}")
    print("\nRecommended movies:")

    for index, score in scores:
        print(f"- {movies.iloc[index]['title']} (similarity: {score:.2f})")


if __name__ == "__main__":
    recommend_movies("Toy Story")