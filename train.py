iimport pandas as pd
import streamlit as st
import pickle
import os
import requests
import gdown

# ---------------- GOOGLE DRIVE DOWNLOAD FUNCTION ----------------
def download_file(file_id, filename):
    if not os.path.exists(filename):
        with st.spinner(f"Downloading {filename}... ⏳"):
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, filename, quiet=True, fuzzy=True)

# ---------------- FILE IDS ----------------
SIMILARITY_ID = "1w9X0e7EXcW-zVl5Yp7st85blIUotc0t7"
MOVIE_ID = "1EMhqpUsfSO2iGOUO5432es8eRuTHqg3Q"

# ---------------- DOWNLOAD FILES ----------------
download_file(SIMILARITY_ID, "similarity.pkl")
download_file(MOVIE_ID, "movie_list.pkl")

# ---------------- LOAD FILES ----------------
try:
    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    with open("movie_list.pkl", "rb") as f:
        movie = pickle.load(f)

    movie = pd.DataFrame(movie)

except Exception as e:
    st.error(f"❌ Failed to load model files: {e}")
    st.stop()

# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie 🎥',
    movie['title'].values
)

# ---------------- FETCH POSTER ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f07164adf1a7def0170eeafeeb6bb25a"
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie_name):
    movie_index = movie[movie['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movie.append(movie.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movie, recommended_posters

# ---------------- BUTTON ----------------
if st.button('🎯 Show Recommendations'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"**{names[i]}**")
            st.image(posters[i])