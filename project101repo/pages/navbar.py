import streamlit as st
import base64

def render_navbar():
    st.markdown("""
    <style>
        /* Remove default Streamlit styling */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Reset ALL padding & margin */
        .main .block-container {
            padding-top: 0 !important;
            padding-right: 0 !important;
            padding-left: 0 !important;
            padding-bottom: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        /* Hide streamlit header */
        header {visibility: hidden !important;}
        
        /* Full width navbar */
        .custom-navbar {
            width: 100vw;
            background-color: #f8f9fa;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            border-bottom: 1px solid #ddd;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            box-sizing: border-box;
        }
        
        .left-section {
            display: flex;
            align-items: center;
        }
        .left-link {
            font-size: 24px !important;
            font-weight: 650 !important;
            color: #333 !important;
            text-decoration: none !important;
        }
        
        .logo {
            width: 25px;
            height: 25px;
            background-color: #ccc;
            border-radius: 50%;
            margin-right: 10px;
        }
        
        .right-section {
            display: flex;
            align-items: center;
            color: #000000;
            gap: 30px;
        }
        
        .nav-link {
            color: #000000 !important;
            text-decoration: none !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            font-size: 22px !important;
        }
        
        .profile-icon {
            width: 25px;
            height: 25px;
            background-color: #000000;
            border-radius: 50%;
        }
        
        /* Push page content down to account for navbar height */
        .spacer {
            height: 70px;
            width: 100%;
        }

    </style>
    
    <div class="custom-navbar">
        <div class="left-section">
            <div class="logo"></div>
            <a class="left-link" href="./home"  target='_self'>AdElevate AI</a>
        </div>
        <div class="right-section">
            <a class="nav-link" href="#"  target='_self'>Contact Us</a>
            <a class="nav-link" href="#"  target='_self'>About Us</a>
            <div class="profile-icon"></div>
        </div>
    </div>
    
    <div class="spacer"></div>
    """, unsafe_allow_html=True)


    # Background image setup
    def get_base64_img(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # Path to image in the same folder
    img_base64 = get_base64_img("pages/bgimg.jpg")

    # Injecting background CSS
    bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;    
    }}
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)