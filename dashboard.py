import streamlit as st
from multidash import MultiApp
from src.dashboard_pages import home_st, population_st

app = MultiApp()

st.title("Core - Mid bootcamp project")

# Add all your application here
app.add_app("Home", home_st.app)
app.add_app("Population", population_st.app)
# The main app
app.run()


