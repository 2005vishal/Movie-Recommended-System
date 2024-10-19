import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the pickle file for movies
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

# Load the split similarity files
similarity_parts = []
for i in range(5):  # Assuming you have 5 parts: similarity_part_0.pkl to similarity_part_4.pkl
    try:
        similarity_part = pickle.load(open(f'similarity_part_{i}.pkl', 'rb'))
        similarity_parts.append(similarity_part)
    except FileNotFoundError:
        st.error(f"File similarity_part_{i}.pkl not found. Please check the file path.")
        break  # Stop loading if a file is not found

# Combine the parts into a single similarity matrix
if similarity_parts:
    similarity = np.vstack(similarity_parts)  # Combine arrays vertically
else:
    st.error("No similarity parts were loaded. Please check your files.")

# Check if the data structure is valid for DataFrame
if isinstance(movies_dict, dict):
    movies = pd.DataFrame(movies_dict)
elif isinstance(movies_dict, list):
    movies = pd.DataFrame(movies_dict)
else:
    st.error("The structure of movies_dict is invalid for DataFrame creation!")

# Fetching movie names
def recommender(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:  # Get top 5 recommendations
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App with Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the options below to interact with the app.")
page = st.sidebar.selectbox("Choose a page", ["Home", "About"])

if page == "Home":
    st.title("🎬 Movie Recommender System 🍿")
    st.markdown("Get movie recommendations based on your favorite movies! Just select a movie and hit **Recommend**.")

    selected_movie_name = st.selectbox(
        "Choose a movie",
        movies['title'].values  # Assuming 'title' column exists in the DataFrame
    )

    if st.button('Recommend'):
        with st.spinner('Finding recommendations...'):
            recommended_movies = recommender(selected_movie_name)
            st.subheader(f"Movies similar to {selected_movie_name}:")
            for movie in recommended_movies:
                st.write(f"🎥 {movie}")
else:
    st.title("About")
    st.markdown(
        """
        Vishal Patwa
        """
    )

    st.markdown(
        """
        This is a simple movie recommender system that helps you find movies similar to your favorites!
        It uses a precomputed similarity matrix to suggest films based on the movie you select.
        """
    )
