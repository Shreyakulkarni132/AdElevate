import streamlit as st
st.set_page_config(layout="wide")

from pages.navbar import render_navbar

render_navbar()

# Main content
st.markdown("""
    <div style="text-align: center; margin-top: 5px;">
        <h1 style="color: #ffffff; font-size: 40px;">Welcome to AdElevate AI</h1>
        <p style="color: #ffffff; font-size: 20px;">We help you overcome your marketing challenges and make your campaign an assured success.</p>
    </div>
""", unsafe_allow_html=True)

# Flex container and buttons
st.markdown("""
<style>
.flex-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40vh;  /* full vertical height minus navbar if needed */
    gap: 100px;
    flex-wrap: wrap;
    margin-bottom: 0px;
}

.flex-button {
    padding: 40px 60px;
    font-size: 24px;
    font-weight: bold;
    background-color: rgba(255, 255, 255, 0.1);
    color: white !important;
    text-decoration: none !important;
    border: 2px solid white;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.3s ease;
    text-align: center;
    min-width: 250px;
}

.flex-button:hover {
    background-color: rgba(255, 255, 255, 0.2);
}
</style>

<div class="flex-container">
    <a href="./analysispg"  target='_self' class="flex-button">Estimate how well your campaign can do </a>
    <a href="./generatepg"  target='_self' class="flex-button">Generate campaign strategies & enhance ideas</a>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    .fill-data-text {
        font-size: 20px;
        color: white;
        text-align: center;
        margin-top: 50px;
        margin-bottom: 5px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    .stButton>button {
        width: auto; /* Let the button size based on content */
        min-width: 100px; /* Minimum width */
        background-color: transparent;
        color: white;
        border: 1px solid white;
        padding: 5px 15px;
        font-size: 14px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 0 auto; /* Center the button */
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.1);
        color: green !important;
        border-color: green !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='fill-data-text'>For more precise interpretation,<br>enter your past campaign details</div>", unsafe_allow_html=True)

# Single centered column approach
col_left, col_middle, col_right = st.columns([1.8, 1, 1])

with col_middle:
    if st.button("Fill Data", key="fill_data_button"):
        st.session_state.show_data_form = True
