import pickle
import streamlit as st
import requests
import pandas as pd
import os


# ---------------- LOAD PICKLE ----------------

st.header("Movie Recommender System")

try:
    movies = pickle.load(open("movie_recommendation.pkl", "rb"))
    similarity = pickle.load(open("similarity_movies.pkl", "rb"))

except Exception as e:
    st.error(e)
    st.stop()


if isinstance(movies, dict):
    movies = pd.DataFrame(movies)


# ---------------- FUNCTIONS ----------------

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    data = requests.get(url).json()

    if 'poster_path' in data and data['poster_path']:

        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    else:

        return "https://via.placeholder.com/300x450?text=No+Image"



def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


movie_list = movies["title"].values


selected_movie = st.selectbox(
    "Select movie",
    movie_list
)


if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

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