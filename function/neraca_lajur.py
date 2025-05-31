
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_neraca_lajur_data():

    
    
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_lajur.csv')
    
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        
        return pd.DataFrame(columns=[
            'Nama Akun', 
            'Neraca Saldo Debet', 
            'Neraca Saldo Kredit',
            'Laba Rugi Debet',
            'Laba Rugi Kredit',
            'Neraca Debet',
            'Neraca Kredit'
        ])

def save_neraca_lajur_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_lajur.csv')
    df.to_csv(csv_path, index=False)





def show_neraca_lajur():

    st.subheader("Neraca Lajur")
    
    
    if 'show_add_form' not in st.session_state:
        st.session_state.show_add_form = False
    if 'show_edit_form' not in st.session_state:
        st.session_state.show_edit_form = False
    if 'show_delete_form' not in st.session_state:
        st.session_state.show_delete_form = False
    if 'edit_index' not in st.session_state:
        st.session_state.edit_index = 0
    if 'delete_index' not in st.session_state:
        st.session_state.delete_index = 0
    
    
    try:
        
        df_neraca = load_neraca_lajur_data()
        
        if not df_neraca.empty:
            
            display_df = df_neraca.copy()
            
            
            
            currency_cols = ['Neraca Saldo Debet', 'Neraca Saldo Kredit', 
                            'Laba Rugi Debet', 'Laba Rugi Kredit', 
                            'Neraca Debet', 'Neraca Kredit']
            for col in currency_cols:
                
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            st.table(display_df)
            
            
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'neraca_lajur.csv')
            raw_df = pd.read_csv(csv_path)
            
            
            for col in currency_cols:
                raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0)
            
            
            total_neraca_saldo_debet = raw_df['Neraca Saldo Debet'].sum()
            total_neraca_saldo_kredit = raw_df['Neraca Saldo Kredit'].sum()
            total_laba_rugi_debet = raw_df['Laba Rugi Debet'].sum()
            total_laba_rugi_kredit = raw_df['Laba Rugi Kredit'].sum()
            total_neraca_debet = raw_df['Neraca Debet'].sum()
            total_neraca_kredit = raw_df['Neraca Kredit'].sum()
            
            
            st.markdown("Totals")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Neraca Saldo Debet", f"Rp {total_neraca_saldo_debet:,.2f}".replace(',', '.'))
                st.metric("Total Laba Rugi Debet", f"Rp {total_laba_rugi_debet:,.2f}".replace(',', '.'))
                st.metric("Total Neraca Debet", f"Rp {total_neraca_debet:,.2f}".replace(',', '.'))
            
            with col2:
                st.metric("Total Neraca Saldo Kredit", f"Rp {total_neraca_saldo_kredit:,.2f}".replace(',', '.'))
                st.metric("Total Laba Rugi Kredit", f"Rp {total_laba_rugi_kredit:,.2f}".replace(',', '.'))
                st.metric("Total Neraca Kredit", f"Rp {total_neraca_kredit:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
        else:
            
            st.warning("Data neraca lajur tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca_lajur.csv")
            
            
            st.markdown("---")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Nama Akun, Neraca Saldo Debet, Neraca Saldo Kredit, Laba Rugi Debet, Laba Rugi Kredit, Neraca Debet, Neraca Kredit)")
        
        
        st.markdown("---")
    
    
    
