# 🎬 CineMatch — Movie Recommendation System

## 1. Project Overview

CineMatch is a movie recommendation system developed using Python and Machine Learning. It recommends movies based on genre similarity and user ratings, helping users discover movies that match their interests.

The application provides an interactive interface where users can search for movies, filter by genre, view movie posters, and explore popular movies.

## 2. Features

* **Movie Recommendations:** Suggests similar movies using content-based filtering.
* **Hybrid Recommendation:** Combines movie similarity scores with rating information.
* **Movie Search:** Search for movies by title.
* **Genre Filter:** Filter recommendations by selected genres.
* **Movie Posters:** Displays posters using the TMDB API.
* **Ratings and Popular Movies:** Shows average ratings and popular titles.
* **Activity History:** Stores recommendation activity in an SQLite database.
* **Interactive Interface:** Built using Streamlit for a simple user experience.

## 3. Technologies Used

* **Programming Language:** Python
* **Frontend / UI:** Streamlit
* **Machine Learning:** Scikit-learn
* **Data Processing:** Pandas, NumPy
* **Recommendation Technique:** TF-IDF and Cosine Similarity
* **Database:** SQLite
* **Movie Poster API:** The Movie Database (TMDB)
* **Dataset:** MovieLens

## 4. How It Works

1. The system loads movie information and ratings from the MovieLens dataset.
2. TF-IDF converts movie genre information into numerical features.
3. Cosine similarity calculates how similar movies are to one another.
4. The recommendation logic combines similarity and rating information to rank movies.
5. Users can search for a movie and receive recommendations through the Streamlit interface.
6. Recommendation activity is stored in an SQLite database.

## 5. Project Structure

```text
Movie_recommendation_system/
│
├── app.py
├── requirements.txt
├── .env
│
├── data/
│   ├── movies.csv
│   └── ratings.csv
│
├── database/
│   └── cinematch.db
│
├── models/
├── notebooks/
│
└── src/
    ├── tmdb_api.py
    └── activity_db.py
```

The SQLite database file is generated when the application initializes the activity database. The `models` and `notebooks` folders may contain additional project files.

## 6. Installation and Setup

### Step 1: Clone or download the project

Download the project files to your computer and open the project folder in VS Code.

### Step 2: Install dependencies

Open the VS Code terminal and run:

```bash
pip install -r requirements.txt
```

### Step 3: Configure the API key

Create a `.env` file in the main project folder and add your own TMDB API key:

```text
TMDB_API_KEY=your_tmdb_api_key
```

Keep your actual API key private. Do not upload the `.env` file to GitHub.

### Step 4: Run the application

Run the following command in the project folder:

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL where you can open CineMatch in your browser.

## 7. Dataset

CineMatch uses the MovieLens dataset, which contains movie metadata and user ratings. The movie and rating CSV files are used to calculate similarity and rating-based recommendation scores.

## 8. Future Enhancements

* Personalized recommendations based on individual user preferences.
* User login and profile management.
* Improved recommendation evaluation.
* Deployment as a public web application.

## 9. Conclusion

CineMatch demonstrates how machine learning, data processing, APIs, and database management can be combined to build an interactive movie recommendation application. It provides practical experience in recommendation systems and Python application development.
