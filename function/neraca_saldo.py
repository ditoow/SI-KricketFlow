import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_neraca_saldo_data():

    
    
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo.csv')
    
    
    if os.path.exists(csv_path):
        
        if os.path.getsize(csv_path) == 0:
            return pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])
        
        
        try:
            df = pd.read_csv(csv_path)
            
            if df.empty or len(df.columns) < 3:
                return pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])
            return df
        except Exception as e:
            st.error(f"Error membaca file neraca_saldo.csv: {e}")
            return pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])
    else:
        
        df = pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])
        df.to_csv(csv_path, index=False)
        return df

def save_neraca_saldo_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo.csv')
    df.to_csv(csv_path, index=False)



def show_neraca_saldo():

    st.subheader("Neraca Saldo")
    
    
    if 'ns_show_add_form' not in st.session_state:
        st.session_state.ns_show_add_form = False
    if 'ns_show_edit_form' not in st.session_state:
        st.session_state.ns_show_edit_form = False
    if 'ns_show_delete_form' not in st.session_state:
        st.session_state.ns_show_delete_form = False
    if 'ns_edit_index' not in st.session_state:
        st.session_state.ns_edit_index = 0
    if 'ns_delete_index' not in st.session_state:
        st.session_state.ns_delete_index = 0
    
    
    try:
        
        df_neraca = load_neraca_saldo_data()
        
        if not df_neraca.empty:
            
            display_df = df_neraca.copy()
            
            
            
            currency_cols = ['Debet', 'Kredit']
            for col in currency_cols:
                
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            st.table(display_df)
            
            
            
            df_neraca['Debet'] = pd.to_numeric(df_neraca['Debet'], errors='coerce').fillna(0)
            df_neraca['Kredit'] = pd.to_numeric(df_neraca['Kredit'], errors='coerce').fillna(0)
            
            total_debet = df_neraca['Debet'].sum()
            total_kredit = df_neraca['Kredit'].sum()
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
        else:
            
            st.warning("Data neraca saldo tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca_saldo.csv")
            
            
            st.markdown("---")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Nama Akun, Debet, Kredit)")
        
        
        st.markdown("---")
    
    
    if st.session_state.ns_show_add_form:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("ns_add_form"):
                nama_akun = st.text_input("Nama Akun")
                debet = st.number_input("Debet", min_value=0.0, format="%f")
                kredit = st.number_input("Kredit", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
                if submitted:
                    add_data(nama_akun, debet, kredit)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.ns_show_add_form = False
                    st.rerun()  
    
    
    if st.session_state.ns_show_edit_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key="ns_edit_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.ns_edit_index = index
                
                with st.form("ns_edit_form"):
                    nama_akun = st.text_input("Nama Akun", value=df_neraca.loc[index, 'Nama Akun'])
                    
                    current_debet = pd.to_numeric(df_neraca.loc[index, 'Debet'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_neraca.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debet = st.number_input("Debet", min_value=0.0, value=float(current_debet), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(index, nama_akun, debet, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.ns_show_edit_form = False
                        st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    
    if st.session_state.ns_show_delete_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="ns_delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.ns_delete_index = index
                
                
                if st.button("Hapus", key="ns_delete_confirm"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.ns_show_delete_form = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")