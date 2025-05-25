import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def show_profile():

    st.markdown("<h1 style='text-align: center;'>Profil Peternakan Jangkrik</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Lokasi Peternakan</h3>", unsafe_allow_html=True)

    
    m = folium.Map(location=[-7.2632127798446895, 110.23181505397224], zoom_start=20)

    
    folium.Marker(
        [-7.263212114673077, 110.23181237176333],
        popup="Peternakan Jangkrik KricketFlow",
        tooltip="Peternakan Jangkrik KricketFlow"
    ).add_to(m)

    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        folium_static(m)

    
    st.markdown("<h3 style='text-align: center;'>Tentang Kami</h3>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center;'>
            <p><strong>Nama</strong> : Jangkrik Boss Temanggung</p>
            <p><strong>Alamat</strong> : Sigran, Kemiri, Kaloran, Kab Temanggung, Jawa Tengah</p>
            <p><strong>Kontak</strong> : 085878863990</p>
            <p><strong>Sejarah</strong> : Sejak 2019 menjadi penyuplai jangkrik pakan burung mulai dari Temanggung, Sumowono, Magelang, hingga Wonosobo.</p>
            <p><strong>Produk</strong> : Jangkrik pakan burung</p>
        </div>
    """, unsafe_allow_html=True)