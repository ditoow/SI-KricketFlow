import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_jurnal_saldo_data():

    
    
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_saldo_setelah_penutupan.csv')
    
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        
        return pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])

def save_jurnal_saldo_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_saldo_setelah_penutupan.csv')
    df.to_csv(csv_path, index=False)


def show_jurnal_saldo_setelah_penutupan():

    st.subheader("Jurnal Saldo Setelah Penutupan")
    
    
    if 'jssp_show_add_form' not in st.session_state:
        st.session_state.jssp_show_add_form = False
    if 'jssp_show_edit_form' not in st.session_state:
        st.session_state.jssp_show_edit_form = False
    if 'jssp_show_delete_form' not in st.session_state:
        st.session_state.jssp_show_delete_form = False
    if 'jssp_edit_index' not in st.session_state:
        st.session_state.jssp_edit_index = 0
    if 'jssp_delete_index' not in st.session_state:
        st.session_state.jssp_delete_index = 0
    
    
    try:
        
        df_jurnal = load_jurnal_saldo_data()
        
        if not df_jurnal.empty:
            
            display_df = df_jurnal.copy()
            
            
            
            currency_cols = ['Debet', 'Kredit']
            for col in currency_cols:
                
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            st.table(display_df)
            
            
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'jurnal_saldo_setelah_penutupan.csv')
            raw_df = pd.read_csv(csv_path)
            
            
            raw_df['Debet'] = pd.to_numeric(raw_df['Debet'], errors='coerce').fillna(0)
            raw_df['Kredit'] = pd.to_numeric(raw_df['Kredit'], errors='coerce').fillna(0)
            
            total_debet = raw_df['Debet'].sum()
            total_kredit = raw_df['Kredit'].sum()
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
            
        else:
            
            st.warning("Data jurnal saldo setelah penutupan tidak tersedia.")
            st.info("Path file yang diharapkan: database/jurnal_saldo_setelah_penutupan.csv")
            
            
            st.markdown("---")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Nama Akun, Debet, Kredit)")
        
        
        st.markdown("---")