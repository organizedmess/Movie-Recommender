import streamlit as st
import pickle
import pandas as pd 
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=17e44de3f11cca492a4396496f44d7c2&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


#we load the data 
movies_df = pickle.load(open('movies_new.pkl','rb'))

#we load similarity matrix
similarity = pickle.load(open('similarity.pkl','rb'))

#now we will reconstruct df from it
movies_df = pd.DataFrame(movies_df)

server = app.server

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distance)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    movie_poster = []
    for i in similar_movies:
        movie_id = movies_df.iloc[i[0]].id
        movie_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies_df.iloc[i[0]].title)
    
    return recommended_movies,movie_poster

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Enter The Movie ',
    movies_df['title'].values)

if st.button('Recommend'):
        names, poster = recommend(selected_movie)
        
        cols = st.columns(5)
        
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(poster[i])
