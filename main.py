import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict=pickle.load(open('movies_dic.pkl','rb'))

movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('simi.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get(url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data=response.json()
    poster_path=data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movies_index=movies[movies['title']==movie].index[0]
    distances=similarity[movies_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster form api

        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies,posters


st.title("Movie Recommender System")
selected_movies=st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

# if st.button('Recommend'):
#     recommendation,posters=recommend(selected_movies)
#     col1,col2,col3,col4,col5=st.beta_columns(3)
#     with col1:
#         st.header(recommendation[0])
#         st.image(posters[0])
#     with col2:
#         st.header(recommendation[1])
#         st.image(posters[1])
#     with col3:
#         st.header(recommendation[2])
#         st.image(posters[2])
#     with col4:
#         st.header(recommendation[3])
#         st.image(posters[3])
#     with col5:
#         st.header(recommendation[4])
#         st.image(posters[4])

if st.button('Recommend'):
    recommendation, posters = recommend(selected_movies)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.header(recommendation[i])
            st.image(posters[i])