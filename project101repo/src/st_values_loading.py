#backend for the Streamlit app to load the values and display results
import streamlit as st

import pickle
import pandas as pd
import numpy as np
from src.get_data import get_data, read_params
import argparse
from transformers import pipeline
from pages.navbar import render_navbar

def get_emotion_scores(text):
    classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", return_all_scores=True)
    results = classifier(text)
    emotion_dict = {emotion['label']: round(emotion['score'] * 100, 2) for emotion in results[0]}
    return emotion_dict

def get_or_create_mapping(value, mapping_dict):
    """Returns the mapped ID if exists, else creates a new one."""
    if value in mapping_dict:
        return mapping_dict[value]
    else:
        new_id = max(mapping_dict.values(), default=0) + 1  # Assign next ID
        mapping_dict[value] = new_id
        return new_id


def st_values_load():
    render_navbar()

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='./params.yaml')
    args = parser.parse_args()
    config_file=args.config
    config = get_data(config_file)

    with open(config['models']['multiple_regression'] ,"rb") as file:
        model = pickle.load(file)
    # Access the stored session state values
    if "query" in st.session_state:
        query = st.session_state.query
        product_category = st.session_state.product_category
        platform = st.session_state.platform
        followers = int(st.session_state.followers)
        age_range = st.session_state.age_range

        #preprocessing the inputs
        start_age, end_age = age_range
        avg_age = (start_age + end_age) / 2

        platform_mapping = {
        "Twitter": 1,
        "Instagram": 2,
        "Linkedin": 3,
        "LinkedIn": 3,
        "Meta": 4,
        "Reddit": 5,
        "YouTube": 6,
        "Facebook":7,
        "TikTok":8
        }
        mapped_platform_value=get_or_create_mapping(platform, platform_mapping)

        category_mapping={
        'Food': 1,
        "Beverages": 1,
        "Fast Food": 1,
        "Budget Meals": 1,
        "Snacks":1,
        'Electronics': 2,
        "Audio Equipment": 2,
        "Mobile Accessories": 2,
        'Clothing': 3,
        "Athletic Footwear": 3,
        "Fashion": 3,
        'Sports': 4,
        "Health": 5,
        "Nutrition": 5,
        "Health Supplements": 5,
        "Fitness Equipment": 5,
        "Beauty": 6,
        "Cosmetics": 6,
        "Skincare": 6,
        "Makeup":6,
        "Vehicle": 7,
        "Home": 8,
        "Home & Garden": 8,
        "Kitchenware": 8,
        "Dorm Essentials": 8,
        "Education": 9,
        "Study Aids": 9,
        "School Supplies": 9,
        "Stationery": 9,
        "Creatives": 9,
        "Kids": 10,
        "Finance": 11,
        "Tech": 12,
        "Technology": 12,
        "HR Software": 12,
        "Project Management Software": 12,
        "Audio Software": 12,
        "Travel": 13,
        "Camping Gear": 13,
        "Travel Gear": 13,
        "Educational":14,
        "Gaming": 15,
        "Gaming Accessories": 15,
        "Entertainment": 16,
        "Investment": 17
        }
        product_category_value=get_or_create_mapping(product_category, category_mapping)
    
        emotions_dict=get_emotion_scores(query)
        
        # input data
        new_data = pd.DataFrame({
        'admiration':[emotions_dict.get('admiration', 0)],
        'amusement':[emotions_dict.get('amusement', 0)],
        'anger':[emotions_dict.get('anger', 0)],
        'annoyance':[emotions_dict.get('annoyance', 0)],
        'approval':[emotions_dict.get('approval', 0)],
        'caring':[emotions_dict.get('caring', 0)],
        'confusion':[emotions_dict.get('confusion', 0)],
        'curiosity':[emotions_dict.get('curiosity', 0)],
        'desire':[emotions_dict.get('desire', 0)],
        'disappointment':[emotions_dict.get('disappointment', 0)],
        'disapproval':[emotions_dict.get('disapproval', 0)],
        'disgust':[emotions_dict.get('disgust', 0)],
        'embarrassment':[emotions_dict.get('embarrassment', 0)],
        'excitement':[emotions_dict.get('excitement', 0)],

        'fear':[emotions_dict.get('fear', 0)],
        'gratitude':[emotions_dict.get('gratitude', 0)],
        'grief':[emotions_dict.get('grief', 0)],
        'joy':[emotions_dict.get('joy', 0)],
        'love':[emotions_dict.get('love', 0)],
        'nervousness':[emotions_dict.get('nervousness', 0)],
        'optimism':[emotions_dict.get('optimism', 0)],
        'pride':[emotions_dict.get('pride', 0)],
        'realization':[emotions_dict.get('realization', 0)],
        'relief':[emotions_dict.get('relief', 0)],
        'remorse':[emotions_dict.get('remorse', 0)],
        'sadness':[emotions_dict.get('sadness', 0)],
        'surprise':[emotions_dict.get('surprise', 0)],
        'neutral':[emotions_dict.get('neutral', 0)],
        'Followers': [followers],
        'Platform_mapped': [mapped_platform_value],
        'AgeRange': [avg_age],
        'ProductCategory_numeric': [product_category_value] 
        })
    
        predictions =model.predict(new_data)
        
        st.session_state.prediction_result = predictions[0]

        st.markdown(f"""
        <div style="text-align: center; margin-top: 60px;">
            <h1 style="color: #ffffff; font-size: 40px;">Success Rate</h1>
            <p style="color: #ffffff; font-size: 20px;">{round(st.session_state.prediction_result[0],2)} %</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: center; margin-top: 60px;">
            <h1 style="color: #ffffff; font-size: 40px;">Trend Score</h1>
            <p style="color: #ffffff; font-size: 20px;">{round(st.session_state.prediction_result[1],2)} %</p>
        </div>
        """, unsafe_allow_html=True)
        
        print("Predicted Values:", predictions)






