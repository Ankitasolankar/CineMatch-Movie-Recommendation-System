
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def get_movie_poster(title):
    if not API_KEY:
        return None

    clean_title = title.rsplit(" (", 1)[0]

    try:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            params={
                "api_key": API_KEY,
                "query": clean_title
            },
            timeout=10
        )
        response.raise_for_status()

        results = response.json().get("results", [])

        if results and results[0].get("poster_path"):
            return (
                "https://image.tmdb.org/t/p/w500"
                + results[0]["poster_path"]
            )

    except requests.RequestException:
        return None

    return None