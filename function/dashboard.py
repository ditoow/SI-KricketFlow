import streamlit as st
import os
from PIL import Image

def show_dashboard():
    """
    Display the dashboard with image, heading and description centered
    """
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Centered title using HTML
    st.markdown("<h1 style='text-align: center;'>KricketFlow Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add an image to the dashboard
    image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'jangkrik.png')
    
    # Check if image exists and display it centered
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.markdown(
            f"<div style='text-align: center;'><img src='data:image/png;base64,{image_to_base64(image)}' width='300'/></div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Image not found. Please check the path: " + image_path)

    st.write("")
    st.write("")
    
    # Centered header
    st.markdown("<h2 style='text-align: center;'>Selamat Datang di KricketFlow App</h2>", unsafe_allow_html=True)

    # Centered description
    st.markdown("""
    <div style='text-align: center; max-width: 700px; margin: 0 auto;'>
        <p>KricketFlow adalah aplikasi manajemen keuangan untuk membantu Anda mengelola dan 
        menganalisis data keuangan dengan mudah. </p>
    </div>
    """, unsafe_allow_html=True)

# Helper function to convert image to base64
import base64
from io import BytesIO

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()