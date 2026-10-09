
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.tmdb_api import get_movie_poster
from src.activity_db import get_activities, init_db, log_activity

init_db()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_movies():
    movies = pd.read_csv(DATA_DIR / "movies.csv")
    movies["genres"] = movies["genres"].fillna("")
    return movies

@st.cache_resource
def build_similarity_model():
    movies = load_movies()
    vectorizer = TfidfVectorizer(token_pattern=r"[^|]+")
    genre_matrix = vectorizer.fit_transform(movies["genres"])
    similarity = cosine_similarity(genre_matrix)
    return similarity

movies = load_movies()
@st.cache_data
def load_ratings():
    return pd.read_csv(DATA_DIR / "ratings.csv")

ratings = load_ratings()

average_ratings = (
    ratings.groupby("movieId")["rating"]
    .agg(["mean", "count"])
    .reset_index()
)

average_ratings.columns = [
    "movieId", "average_rating", "rating_count"
]

movies = movies.merge(average_ratings, on="movieId", how="left")
movies["average_rating"] = movies["average_rating"].fillna(0)
movies["rating_count"] = movies["rating_count"].fillna(0)

similarity = build_similarity_model()

st.title("🎬 CineMatch")
st.subheader("Discover your next favourite movie")
st.write("Choose a movie you enjoy and we'll find similar movies for you.")

# Popular movies section
with st.expander("🎥 Explore Popular Movies"):
    popular_movies = movies.sort_values(
        by=["rating_count", "average_rating"],
        ascending=[False, False]
    ).head(10)

    st.write("Movies with the most user ratings:")

    for _, movie in popular_movies.iterrows():
        st.write(
            f"🍿 {movie['title']} — "
            f"⭐ {movie['average_rating']:.1f}/5 "
            f"({int(movie['rating_count'])} ratings)"
        )

# Search movies by title
st.subheader("🔎 Find a Movie")

search_query = st.text_input(
    "Search by movie name",
    placeholder="Type a movie name, e.g. Toy Story"
)

if search_query.strip():
    matching_movies = movies[
        movies["title"].str.contains(
            search_query.strip(),
            case=False,
            na=False,
            regex=False
        )
    ]["title"].sort_values().tolist()
else:
    matching_movies = movies["title"].sort_values().tolist()

if matching_movies:
    movie_title = st.selectbox(
        "Select a movie",
        matching_movies
    )
else:
    st.warning("No movies found. Try another title.")
    st.stop()

# Genre filter
all_genres = sorted({
    genre
    for genre_list in movies["genres"]
    for genre in genre_list.split("|")
    if genre and genre != "(no genres listed)"
})

selected_genres = st.multiselect(
    "Filter recommendations by genre",
    options=all_genres,
    placeholder="Choose one or more genres"
)

number = st.slider(
    "Number of recommendations",
    min_value=3,
    max_value=10,
    value=5
)

log_activity(
    action="requested_recommendations",
    movie_title=movie_title,
    genre=", ".join(selected_genres) if selected_genres else "All genres"
)



if st.button("✨ Find Recommendations"):
    movie_index = movies.index[
        movies["title"] == movie_title
    ][0]

    # Get genre similarity scores
    similarity_scores = similarity[movie_index]

    # Normalize ratings
    normalized_ratings = movies["average_rating"] / 5.0

    # Reduce the influence of movies with few ratings
    rating_confidence = (
        movies["rating_count"]
        / (movies["rating_count"] + 20)
    )

    adjusted_ratings = (
        normalized_ratings * rating_confidence
    )

    # Combine similarity and adjusted ratings
    hybrid_scores = (
        0.7 * similarity_scores
        + 0.3 * adjusted_ratings
    )

    scores = list(enumerate(hybrid_scores))
    scores.sort(key=lambda item: item[1], reverse=True)

    # Apply genre filter
    recommendations = [
        (index, score)
        for index, score in scores
        if index != movie_index
        and (
            not selected_genres
            or any(
                genre in movies.iloc[index]["genres"].split("|")
                for genre in selected_genres
            )
        )
    ][:number]

    if recommendations:
        st.subheader("Recommended for you")

        for index, score in recommendations:
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                poster_url = get_movie_poster(
                    movies.iloc[index]["title"]
                )

                if poster_url:
                    st.image(poster_url, width=110)
                else:
                    st.write("🎬 Poster unavailable")

            with col2:
                st.markdown(
                    f"### 🍿 {movies.iloc[index]['title']}"
                )
                st.write(
                    f"Genres: {movies.iloc[index]['genres']}"
                )
                st.write(
                    f"⭐ Average rating: "
                    f"{movies.iloc[index]['average_rating']:.1f}/5"
                )

            with col3:
                st.metric("Recommendation Score", f"{score:.0%}")

            st.divider()
    else:
        st.warning("No matching movies found. Try another genre.")


st.subheader("📊 User Activity History")

if st.button("View Activity"):
    activities = get_activities()

    if activities.empty:
        st.info("No activity recorded yet.")
    else:
        st.dataframe(activities, use_container_width=True)