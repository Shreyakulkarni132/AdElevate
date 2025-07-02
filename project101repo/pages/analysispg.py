import streamlit as st
from src.st_values_loading import st_values_load
from streamlit_extras.switch_page_button import switch_page
from pages.navbar import render_navbar

st.set_page_config(layout="wide")

from pages.navbar import render_navbar
render_navbar()

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Your custom HTML content
st.markdown("""
    <div style="text-align: center; margin-top: 5px;">
        <h1 style="color: #ffffff; font-size: 40px;">Get Performance Prediction</h1>
        <p style="color: #ffffff; font-size: 20px;">Simply enter your campaign text and we will analyze and predict how well your campaign can do based on <br> our high-tech machine learnings model and neatly gathered data.</p>
    </div>
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
/* Text area styling */
textarea {
    margin-top: 5px !important;
    min-height: 60px;
    max-height: 300px;
    padding: 12px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ccc;
    resize: vertical;
    width: 100%;
}

/* Button styling */
.stButton > button {
    height: 44px;
    padding: 0 30px;
    font-size: 16px;
    border: none;
    background-color: #10a37f;
    color: white;
    border-radius: 6px;
    cursor: pointer;
    margin: 0 auto;
    display: block;
}

.stButton > button:hover {
    background-color: #0e8a6a;
    font-weight: bold;
    color: #ffffff;
}

/* Add top margin for spacing */
.top-margin {
    margin-top: 80px;
}
</style>
""", unsafe_allow_html=True)

# Add top margin
st.markdown('<div class="top-margin"></div>', unsafe_allow_html=True)

# Create a 3-column layout with the middle column for content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Campaign Text Input
    query = st.text_area("Search", label_visibility="collapsed", 
                         placeholder="Enter your campaign text...", 
                         key="search_input")
    
    # Dropdown for Product Category
    product_category = st.selectbox(
        "Select Product Category",
        ["Fashion", "Technology", "Food & Beverage", "Fitness", "Beauty", "Travel", "Education"]
    )
    
    # Dropdown for Platform
    platform = st.selectbox(
        "Select Platform",
        ["Instagram", "YouTube", "TikTok", "Facebook", "Twitter", "LinkedIn"]
    )

    # Number input for Followers
    followers = st.number_input(
        "Number of Followers",
        min_value=0,
        step=1000
    )

    # Age Range Slider
    age_range = st.slider(
        "Select Age Range",
        13, 65, (18, 35)
    )

    # Button
    submitted = st.button("Enter")

    # Handle Submission
    if submitted:
        if query:
            # Store values in session state
            st.session_state.query = query
            st.session_state.product_category = product_category
            st.session_state.platform = platform
            st.session_state.followers = followers
            st.session_state.age_range = age_range
            
            switch_page("go_to_st_values_loading")
        else:
            st.warning("Please enter a campaign message.")
