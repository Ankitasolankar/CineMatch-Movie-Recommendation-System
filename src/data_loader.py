
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")

print("Movies loaded successfully!")
print(movies.head())

print("\nRatings loaded successfully!")
print(ratings.head())

print("\nTotal movies:", len(movies))
print("Total ratings:", len(ratings))