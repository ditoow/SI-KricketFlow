import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu

# Ensure function directory exists before trying to import from it
function_dir = os.path.join(os.path.dirname(__file__), 'function')
if not os.path.exists(function_dir):
    os.makedirs(function_dir)
    # Create an __init__.py file to make it a proper package
    with open(os.path.join(function_dir, '__init__.py'), 'w') as f:
        pass

# Only try to import after ensuring the directory exists
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
    
except ImportError:
    # This will happen on first run before we've created the file
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

# Ensure database directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Define fallback for profile function if module not loaded
def show_profile_fallback():
    """Fallback function for profile page if module not loaded"""
    st.title("Profile")
    st.error("Profile module not found. Please restart the application after the files have been created.")

def show_home():
    """Create a sidebar navigation menu using option_menu"""
    with st.sidebar:
        selected = option_menu("🦗KricketFlow",
                              ["Dashboard", "Profil", "Keuangan"],
                              icons=["house", "person", "cash-coin"],
                              default_index=0)
        
        # Add logout button to sidebar at line 66 as requested
        st.sidebar.button("Logout", on_click=logout, key="logout_button")
    
    return selected

def show_content(selected):
    """Display content based on the selected menu item"""
    if selected == "Dashboard":
        # Call the dashboard function if available, otherwise display fallback
        if show_dashboard:
            show_dashboard()
        else:
            st.title("Dashboard")
            st.error("Dashboard module not found. Please restart the application after the files have been created.")
    
    elif selected == "Profil":
        # Display the profile page
        if show_profile:
            show_profile()
        else:
            show_profile_fallback()
        
    elif selected == "Keuangan":
        st.title("Keuangan")
        
        # Add dropdown menu for Keuangan options
        keuangan_option = st.selectbox(
            "Pilih jenis laporan keuangan:",
            options=["Siklus", "Laporan"]
        )
        
        # Display content based on selected dropdown option
        if keuangan_option == "Siklus":
            st.subheader("Laporan Keuangan per Siklus")
            
            # Add tab selection for different report types
            tabs = st.tabs(["Neraca Saldo Periode Sebelumnya", "Jurnal Umum", "Buku Besar", "Neraca Saldo", "Neraca Lajur", "Jurnal Penutup", "Jurnal Saldo Setelah Penutupan", "Neraca", "Laporan Laba Rugi"])
            with tabs[0]:  # Neraca Saldo Periode Sebelumnya tab
                if show_neraca_saldo_periode_sebelumnya:
                    show_neraca_saldo_periode_sebelumnya()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[1]:  # Jurnal Umum tab
                if show_jurnal_umum:
                    show_jurnal_umum()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[2]:  # Buku Besar tab
                if show_buku_besar:
                    show_buku_besar()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[3]:  # Neraca Saldo tab
                if show_neraca_saldo:
                    show_neraca_saldo()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[4]:  # Neraca Lajur tab
                if show_neraca_lajur:
                    show_neraca_lajur()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[5]:  # Jurnal Penutup tab
                if show_jurnal_penutup:
                    show_jurnal_penutup()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[6]:  # Jurnal Saldo Setelah Penutupan tab
                if show_jurnal_saldo_setelah_penutupan:
                    show_jurnal_saldo_setelah_penutupan()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[7]:  # Neraca tab
                if show_neraca:
                    show_neraca()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
                
            with tabs[8]:  # Laporan Laba Rugi tab
                if show_lap_labarugi:
                    show_lap_labarugi()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
        elif keuangan_option == "Laporan":
            
            # Add second dropdown specific to Laporan with 3 options
            st.subheader("Laporan Keuangan per Siklus")
            
            # Add tab selection for different report types
            tabs = st.tabs(["Laporan Laba Rugi", "Laporan Perubahan Modal"])
           
            with tabs[0]:  # Laporan Laba Rugi tab
                if show_lap_labarugi:
                    show_lap_labarugi()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")
            
            with tabs[1]:  # Laporan Perubahan Modal tab
                if show_lap_perubahanmodal:
                    show_lap_perubahanmodal()
                else:
                    st.error("Module not found. Please restart the application after the files have been created.")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="KricketFlow App",
        page_icon="🦗",
        layout="wide"
    )
    
    # Check if the user is logged in
    if not is_logged_in:
        # If the module is not imported yet, show a simple login page
        st.title("🦗 KricketFlow")
        st.error("Authentication module not found. Please restart the application.")
        return
    
    # Check if the user is logged in
    if not is_logged_in():
        # Show login page (without sidebar)
        show_login()
    else:
        # User is logged in, show the main application with sidebar
        selected = show_home()
        show_content(selected)

if __name__ == "__main__":
    main()