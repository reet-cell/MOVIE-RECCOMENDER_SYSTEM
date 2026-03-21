import pandas as pd
import streamlit as st
import pickle
import os
import requests
import gdown

# ---------------- GOOGLE DRIVE DOWNLOAD FUNCTION ----------------
def download_file(file_id, filename):
    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, filename, quiet=False)

# ---------------- DOWNLOAD FILES ----------------
download_file("1w9X0e7EXcW-zVl5Yp7st85blIUotc0t7", "similarity.pkl")
download_file("1EMhqpUsfSO2iGOUO5432es8eRuTHqg3Q", "movie_list.pkl")

# ---------------- DEBUG (OPTIONAL) ----------------

# ---------------- LOAD FILES ----------------
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie = pickle.load(open('movie_list.pkl', 'rb'))
    movie = pd.DataFrame(movie)

except Exception as e:
    st.error(f"❌ Failed to load model files: {e}")
    st.stop()

# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox('Select movie', movie['title'].values)

# ---------------- FETCH POSTER ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f07164adf1a7def0170eeafeeb6bb25a"
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie_name):
    movie_index = movie[movie['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movie.append(movie.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie, recommended_movie_posters

# ---------------- BUTTON ----------------
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
