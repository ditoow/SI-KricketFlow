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
    
    csv_path = os.path.join(database_dir, 'neraca_saldo_periode_sebelumnya.csv')
    
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        
        return pd.DataFrame(columns=['Nama Akun', 'Debit', 'Kredit'])

def save_neraca_saldo_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo_periode_sebelumnya.csv')
    df.to_csv(csv_path, index=False)



def add_data(nama_akun, debit, kredit):
    df = load_neraca_saldo_data()
    new_row = pd.DataFrame({'Nama Akun': [nama_akun], 'Debit': [debit], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_neraca_saldo_data(df)
    return df


def edit_data(index, nama_akun, debit, kredit):
    df = load_neraca_saldo_data()
    df.loc[index, 'Nama Akun'] = nama_akun
    df.loc[index, 'Debit'] = debit
    df.loc[index, 'Kredit'] = kredit
    save_neraca_saldo_data(df)
    return df


def delete_data(index):
    df = load_neraca_saldo_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_neraca_saldo_data(df)
    return df

def show_neraca_saldo_periode_sebelumnya():

    st.subheader("Neraca Saldo Periode Sebelumnya")
    
    
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
        
        df_neraca = load_neraca_saldo_data()
        
        if not df_neraca.empty:
            
            display_df = df_neraca.copy()
            
            
            
            currency_cols = ['Debit', 'Kredit']
            for col in currency_cols:
                
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            st.table(display_df)
            
            
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'neraca_saldo_periode_sebelumnya.csv')
            raw_df = pd.read_csv(csv_path)
            
            
            raw_df['Debit'] = pd.to_numeric(raw_df['Debit'], errors='coerce').fillna(0)
            raw_df['Kredit'] = pd.to_numeric(raw_df['Kredit'], errors='coerce').fillna(0)
            
            total_debit = raw_df['Debit'].sum()
            total_kredit = raw_df['Kredit'].sum()
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Debit", f"Rp {total_debit:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
            
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="nps_add_btn"):
                    st.session_state.show_add_form = not st.session_state.show_add_form
                    st.session_state.show_edit_form = False
                    st.session_state.show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', key="nps_edit_btn"):
                    st.session_state.show_edit_form = not st.session_state.show_edit_form
                    st.session_state.show_add_form = False
                    st.session_state.show_delete_form = False
            with col3:
                if st.button('🗑️ Hapus Data', key="nps_delete_btn"):
                    st.session_state.show_delete_form = not st.session_state.show_delete_form
                    st.session_state.show_add_form = False
                    st.session_state.show_edit_form = False
        else:
            
            st.warning("Data neraca saldo tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca_saldo_periode_sebelumnya.csv")
            
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="nps_add_btn_empty"):
                    st.session_state.show_add_form = not st.session_state.show_add_form
                    st.session_state.show_edit_form = False
                    st.session_state.show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', key="nps_edit_btn_empty", disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', key="nps_delete_btn_empty", disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Nama Akun, Debit, Kredit)")
        
        
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data', key="nps_add_btn_error"):
                st.session_state.show_add_form = not st.session_state.show_add_form
                st.session_state.show_edit_form = False
                st.session_state.show_delete_form = False
        with col2:
            if st.button('✏️ Edit Data', key="nps_edit_btn_error", disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', key="nps_delete_btn_error", disabled=True):
                pass
    
    
    if st.session_state.show_add_form:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("nps_add_form"):
                nama_akun = st.text_input("Nama Akun")
                debit = st.number_input("Debit", min_value=0.0, format="%f")
                kredit = st.number_input("Kredit", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
                if submitted:
                    add_data(nama_akun, debit, kredit)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.show_add_form = False
                    st.rerun()  
    
    
    if st.session_state.show_edit_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options)
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index = index
                
                with st.form("nps_edit_form"):
                    nama_akun = st.text_input("Nama Akun", value=df_neraca.loc[index, 'Nama Akun'])
                    
                    current_debit = pd.to_numeric(df_neraca.loc[index, 'Debit'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_neraca.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debit = st.number_input("Debit", min_value=0.0, value=float(current_debit), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(index, nama_akun, debit, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.show_edit_form = False
                        st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    
    if st.session_state.show_delete_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options)
                index = int(selected_option.split(" - ")[0])
                st.session_state.delete_index = index
                
                
                if st.button("Hapus", key="nps_delete_confirm"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.show_delete_form = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")
