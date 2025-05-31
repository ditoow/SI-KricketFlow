import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu


function_dir = os.path.join(os.path.dirname(__file__), 'function')
if not os.path.exists(function_dir):
    os.makedirs(function_dir)
    
    with open(os.path.join(function_dir, '__init__.py'), 'w') as f:
        pass


try:
    from function.neraca_periode_sebelumnya import (
        show_neraca_saldo_periode_sebelumnya,
        load_neraca_saldo_data,
        save_neraca_saldo_data,
        add_data,
        edit_data,
        delete_data
    )
    from function.jurnal_umum import show_jurnal_umum
    from function.neraca_saldo import show_neraca_saldo
    from function.jurnal_penutup import show_jurnal_penutup
    from function.jurnal_saldo_setelah_penutupan import show_jurnal_saldo_setelah_penutupan
    from function.neraca import show_neraca
    from function.buku_besar import show_buku_besar
    from function.neraca_lajur import show_neraca_lajur
    from function.lap_labarugi import show_lap_labarugi
    from function.lap_perubahanmodal import show_lap_perubahanmodal
    from function.dashboard import show_dashboard
    from function.profile import show_profile
    from function.auth import show_login, is_logged_in, logout
    from function.tambah import show_tambah_transaksi
    
except ImportError:
    
    show_neraca_saldo_periode_sebelumnya = None
    show_jurnal_umum = None
    show_neraca_saldo = None
    show_jurnal_penutup = None
    show_jurnal_saldo_setelah_penutupan = None
    show_neraca = None
    show_buku_besar = None
    show_neraca_lajur = None
    show_lap_labarugi = None
    show_lap_perubahanmodal = None
    show_dashboard = None
    show_profile = None
    show_login = None
    is_logged_in = None
    logout = None
    show_tambah_transaksi = None


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def show_profile_fallback():
    st.title("Profile")
    st.error("Profile module not found. Please restart the application after the files have been created.")

def show_home():

    with st.sidebar:
        selected = option_menu("🦗KricketFlow",
                              ["Dashboard", "Profil", "Keuangan", "Tambah Transaksi"],
                              icons=["house", "person", "cash-coin", "plus-circle"],
                              default_index=0)
        
        
        st.sidebar.button("Logout", on_click=logout, key="logout_button")
    
    return selected

def show_content(selected):

    if selected == "Dashboard":
        
        if show_dashboard:
            show_dashboard()
        else:
            st.title("Dashboard")
            st.error("Dashboard module not found. Please restart the application after the files have been created.")
    
    elif selected == "Profil":
        
        if show_profile:
            show_profile()
        else:
            show_profile_fallback()
    
    elif selected == "Tambah Transaksi":
        
        if show_tambah_transaksi:
            show_tambah_transaksi()
        else:
            st.title("Tambah Transaksi")
            st.error("Modul Tambah Transaksi tidak ditemukan. Silakan restart aplikasi setelah file dibuat.")
        
    elif selected == "Keuangan":
        st.title("Keuangan")
        
        
        keuangan_option = st.selectbox(
            "Pilih jenis laporan keuangan:",
            options=["Siklus", "Laporan"]
        )
        
        
        if keuangan_option == "Siklus":
            st.subheader("Laporan Keuangan per Siklus")
            
            
            tabs = st.tabs(["Neraca Saldo Periode Sebelumnya", "Jurnal Umum", "Buku Besar", "Neraca Saldo", "Neraca Lajur", "Jurnal Penutup", "Jurnal Saldo Setelah Penutupan", "Neraca", ])
            with tabs[0]:  
                if show_neraca_saldo_periode_sebelumnya:
                    show_neraca_saldo_periode_sebelumnya()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[1]:  
                if show_jurnal_umum:
                    show_jurnal_umum()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[2]:  
                if show_buku_besar:
                    show_buku_besar()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[3]:  
                if show_neraca_saldo:
                    show_neraca_saldo()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[4]:  
                if show_neraca_lajur:
                    show_neraca_lajur()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[5]:  
                if show_jurnal_penutup:
                    show_jurnal_penutup()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[6]:  
                if show_jurnal_saldo_setelah_penutupan:
                    show_jurnal_saldo_setelah_penutupan()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[7]:  
                if show_neraca:
                    show_neraca()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            
        elif keuangan_option == "Laporan":
            
            
            st.subheader("Laporan Keuangan")
            
            
            tabs = st.tabs(["Laporan Laba Rugi", "Laporan Perubahan Modal"])
           
            with tabs[0]:  
                if show_lap_labarugi:
                    show_lap_labarugi()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[1]:  
                if show_lap_perubahanmodal:
                    show_lap_perubahanmodal()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")

def main():

    st.set_page_config(
        page_title="KricketFlow App",
        page_icon="🦗",
        layout="wide"
    )
    
    
    if not is_logged_in:
        
        st.title("🦗 KricketFlow")
        st.error("Authentication module not found. Please restart the application.")
        return
    
    
    if not is_logged_in():
        
        show_login()
    else:
        
        selected = show_home()
        show_content(selected)

if __name__ == "__main__":
    main()