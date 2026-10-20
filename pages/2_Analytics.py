
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="CineMatch Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CineMatch Data Analytics")
st.write(
    "Explore movie ratings, genres, popularity, "
    "and relationships in the CineMatch dataset."
)

# Locate the project data folder
BASE_DIR = Path(__file__).resolve().parent.parent
movies_path = BASE_DIR / "data" / "movies.csv"
ratings_path = BASE_DIR / "data" / "ratings.csv"

# Load datasets
@st.cache_data
def load_data():
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    return movies_df, ratings_df

try:
    movies, ratings = load_data()

    # Validate required columns
    if not {"movieId", "genres"}.issubset(movies.columns):
        st.error("movies.csv must contain movieId and genres columns.")
        st.stop()

    if not {"movieId", "rating"}.issubset(ratings.columns):
        st.error("ratings.csv must contain movieId and rating columns.")
        st.stop()

    # Prepare per-movie rating statistics
    movie_stats = ratings.groupby("movieId")["rating"].agg(
        average_rating="mean",
        rating_count="count",
        rating_std="std"
    ).reset_index()

    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Movies", f"{movies['movieId'].nunique():,}")
    col2.metric("Total Rating Records", f"{len(ratings):,}")
    col3.metric("Movies with Ratings", f"{movie_stats['movieId'].nunique():,}")

    sns.set_theme(style="whitegrid")

    # 1. Histogram
    st.subheader("1. Distribution of Movie Ratings")

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.histplot(data=ratings, x="rating", bins=10, ax=ax)
    ax.set_title("Distribution of User Ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of Ratings")
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "This histogram shows how frequently each rating value occurs."
    )

    # 2. Genre bar chart
    st.subheader("2. Most Common Movie Genres")

    genres = (
        movies["genres"]
        .dropna()
        .str.split("|")
        .explode()
    )
    genres = genres[genres != "(no genres listed)"]
    top_genres = genres.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(
        x=top_genres.values,
        y=top_genres.index,
        ax=ax
    )
    ax.set_title("Top 10 Movie Genres")
    ax.set_xlabel("Number of Movies")
    ax.set_ylabel("Genre")
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "The bar chart identifies the most common genres in the dataset."
    )

    # 3. Scatter plot
    st.subheader("3. Average Rating vs. Rating Count")

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(
        data=movie_stats,
        x="rating_count",
        y="average_rating",
        alpha=0.6,
        ax=ax
    )
    ax.set_title("Movie Ratings and Rating Counts")
    ax.set_xlabel("Number of Ratings")
    ax.set_ylabel("Average Rating")
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Each point represents a movie. "
        "The chart compares its average rating with its rating count."
    )

    # 4. Correlation heatmap
    st.subheader("4. Movie Statistics Correlation Heatmap")

    heatmap_data = movie_stats[
        ["average_rating", "rating_count", "rating_std"]
    ].dropna()

    if len(heatmap_data) >= 2:
        correlation = heatmap_data.corr()

        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            fmt=".2f",
            ax=ax
        )
        ax.set_title("Correlation Between Movie Statistics")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Not enough rating data to calculate correlations.")

    st.caption(
        "The heatmap shows correlations between average rating, "
        "rating count, and rating standard deviation. "
        "Correlation does not imply causation."
    )

    # Optional: show summary table
    with st.expander("View Movie Rating Statistics"):
        st.dataframe(
            movie_stats.sort_values(
                "rating_count", ascending=False
            ),
            use_container_width=True
        )

except FileNotFoundError:
    st.error(
        "Dataset files were not found. Check that movies.csv and "
        "ratings.csv are inside the project's data folder."
    )
except Exception as e:
    st.error(f"Could not load analytics: {e}")