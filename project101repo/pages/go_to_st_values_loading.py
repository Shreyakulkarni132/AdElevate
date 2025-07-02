
import streamlit as st
from src.st_values_loading import st_values_load  


st.set_page_config(layout="wide")

# Just call the function that shows the actual prediction UI
st_values_load()
