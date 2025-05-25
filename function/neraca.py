import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_neraca_data():

    
    
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca.csv')
    
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        
        return pd.DataFrame(columns=['AKTIVA', 'AKTIVA.1', 'AKTIVA.2', 'PASIVA', 'PASIVA.1', 'PASIVA.2'])

def save_neraca_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca.csv')
    df.to_csv(csv_path, index=False)




def add_data(aktiva, nilai_aktiva1, nilai_aktiva2, pasiva, nilai_pasiva1, nilai_pasiva2):
    df = load_neraca_data()
    new_row = pd.DataFrame({
        'AKTIVA': [aktiva], 
        'AKTIVA.1': [nilai_aktiva1], 
        'AKTIVA.2': [nilai_aktiva2], 
        'PASIVA': [pasiva], 
        'PASIVA.1': [nilai_pasiva1], 
        'PASIVA.2': [nilai_pasiva2]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_neraca_data(df)
    return df


def edit_data(index, aktiva, nilai_aktiva1, nilai_aktiva2, pasiva, nilai_pasiva1, nilai_pasiva2):
    df = load_neraca_data()
    df.loc[index, 'AKTIVA'] = aktiva
    df.loc[index, 'AKTIVA.1'] = nilai_aktiva1
    df.loc[index, 'AKTIVA.2'] = nilai_aktiva2
    df.loc[index, 'PASIVA'] = pasiva
    df.loc[index, 'PASIVA.1'] = nilai_pasiva1
    df.loc[index, 'PASIVA.2'] = nilai_pasiva2
    save_neraca_data(df)
    return df


def delete_data(index):
    df = load_neraca_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_neraca_data(df)
    return df

def show_neraca():

    st.subheader("Neraca")
    
    
    if 'neraca_show_add_form' not in st.session_state:
        st.session_state.neraca_show_add_form = False
    if 'neraca_show_edit_form' not in st.session_state:
        st.session_state.neraca_show_edit_form = False
    if 'neraca_show_delete_form' not in st.session_state:
        st.session_state.neraca_show_delete_form = False
    if 'neraca_edit_index' not in st.session_state:
        st.session_state.neraca_edit_index = 0
    if 'neraca_delete_index' not in st.session_state:
        st.session_state.neraca_delete_index = 0
    
    
    try:
        
        df_neraca = load_neraca_data()
        
        if not df_neraca.empty:
            
            display_df = df_neraca.copy()
            
            
            
            currency_cols = ['AKTIVA.1', 'AKTIVA.2', 'PASIVA.1', 'PASIVA.2']
            for col in currency_cols:
                if col in display_df.columns:
                    
                    display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                    
                    display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.') if x != 0 else "")
            
            
            st.table(display_df)
            
            
            
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'neraca.csv')
            raw_df = pd.read_csv(csv_path)
            
            
            for col in currency_cols:
                if col in raw_df.columns:
                    raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0)
            
            
            total_aktiva = 0
            total_pasiva = 0
            
            if 'AKTIVA.2' in raw_df.columns:
                total_aktiva = raw_df['AKTIVA.2'].sum()
            
            if 'PASIVA.2' in raw_df.columns:
                total_pasiva = raw_df['PASIVA.2'].sum()
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Aktiva", f"Rp {total_aktiva:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Pasiva", f"Rp {total_pasiva:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
            
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="neraca_add_btn"):
                    st.session_state.neraca_show_add_form = not st.session_state.neraca_show_add_form
                    st.session_state.neraca_show_edit_form = False
                    st.session_state.neraca_show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', key="neraca_edit_btn"):
                    st.session_state.neraca_show_edit_form = not st.session_state.neraca_show_edit_form
                    st.session_state.neraca_show_add_form = False
                    st.session_state.neraca_show_delete_form = False
            with col3:
                if st.button('🗑️ Hapus Data', key="neraca_delete_btn"):
                    st.session_state.neraca_show_delete_form = not st.session_state.neraca_show_delete_form
                    st.session_state.neraca_show_add_form = False
                    st.session_state.neraca_show_edit_form = False
        else:
            
            st.warning("Data neraca tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca.csv")
            
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="neraca_add_btn_empty"):
                    st.session_state.neraca_show_add_form = not st.session_state.neraca_show_add_form
                    st.session_state.neraca_show_edit_form = False
                    st.session_state.neraca_show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', key="neraca_edit_btn_empty", disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', key="neraca_delete_btn_empty", disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai dengan format neraca")
        
        
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data', key="neraca_add_btn_error"):
                st.session_state.neraca_show_add_form = not st.session_state.neraca_show_add_form
                st.session_state.neraca_show_edit_form = False
                st.session_state.neraca_show_delete_form = False
        with col2:
            if st.button('✏️ Edit Data', key="neraca_edit_btn_error", disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', key="neraca_delete_btn_error", disabled=True):
                pass
    
    
    if st.session_state.neraca_show_add_form:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("neraca_add_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Aktiva")
                    aktiva = st.text_input("Nama Aktiva")
                    nilai_aktiva1 = st.number_input("Nilai Aktiva (Kolom 1)", min_value=0.0, format="%f")
                    nilai_aktiva2 = st.number_input("Nilai Aktiva (Kolom 2)", min_value=0.0, format="%f")
                
                with col2:
                    st.subheader("Pasiva")
                    pasiva = st.text_input("Nama Pasiva")
                    nilai_pasiva1 = st.number_input("Nilai Pasiva (Kolom 1)", min_value=0.0, format="%f")
                    nilai_pasiva2 = st.number_input("Nilai Pasiva (Kolom 2)", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
                if submitted:
                    add_data(aktiva, nilai_aktiva1, nilai_aktiva2, pasiva, nilai_pasiva1, nilai_pasiva2)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.neraca_show_add_form = False
                    st.rerun()  
    
    
    if st.session_state.neraca_show_edit_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            
            options = []
            for i, row in df_neraca.iterrows():
                aktiva_label = row['AKTIVA'] if pd.notna(row['AKTIVA']) and row['AKTIVA'] != '' else "(Empty)"
                pasiva_label = row['PASIVA'] if pd.notna(row['PASIVA']) and row['PASIVA'] != '' else "(Empty)"
                options.append(f"{i} - Aktiva: {aktiva_label}, Pasiva: {pasiva_label}")
                
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key="neraca_edit_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.neraca_edit_index = index
                
                with st.form("neraca_edit_form"):
                    col1, col2 = st.columns(2)
                    
                    
                    aktiva_val = df_neraca.loc[index, 'AKTIVA'] if pd.notna(df_neraca.loc[index, 'AKTIVA']) else ""
                    aktiva_val1 = pd.to_numeric(df_neraca.loc[index, 'AKTIVA.1'], errors='coerce') or 0.0
                    aktiva_val2 = pd.to_numeric(df_neraca.loc[index, 'AKTIVA.2'], errors='coerce') or 0.0
                    pasiva_val = df_neraca.loc[index, 'PASIVA'] if pd.notna(df_neraca.loc[index, 'PASIVA']) else ""
                    pasiva_val1 = pd.to_numeric(df_neraca.loc[index, 'PASIVA.1'], errors='coerce') or 0.0
                    pasiva_val2 = pd.to_numeric(df_neraca.loc[index, 'PASIVA.2'], errors='coerce') or 0.0
                    
                    with col1:
                        st.subheader("Aktiva")
                        aktiva = st.text_input("Nama Aktiva", value=aktiva_val)
                        nilai_aktiva1 = st.number_input("Nilai Aktiva (Kolom 1)", min_value=0.0, value=float(aktiva_val1), format="%f")
                        nilai_aktiva2 = st.number_input("Nilai Aktiva (Kolom 2)", min_value=0.0, value=float(aktiva_val2), format="%f")
                    
                    with col2:
                        st.subheader("Pasiva")
                        pasiva = st.text_input("Nama Pasiva", value=pasiva_val)
                        nilai_pasiva1 = st.number_input("Nilai Pasiva (Kolom 1)", min_value=0.0, value=float(pasiva_val1), format="%f")
                        nilai_pasiva2 = st.number_input("Nilai Pasiva (Kolom 2)", min_value=0.0, value=float(pasiva_val2), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(index, aktiva, nilai_aktiva1, nilai_aktiva2, pasiva, nilai_pasiva1, nilai_pasiva2)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.neraca_show_edit_form = False
                        st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    
    if st.session_state.neraca_show_delete_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            options = []
            for i, row in df_neraca.iterrows():
                aktiva_label = row['AKTIVA'] if pd.notna(row['AKTIVA']) and row['AKTIVA'] != '' else "(Empty)"
                pasiva_label = row['PASIVA'] if pd.notna(row['PASIVA']) and row['PASIVA'] != '' else "(Empty)"
                options.append(f"{i} - Aktiva: {aktiva_label}, Pasiva: {pasiva_label}")
                
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="neraca_delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.neraca_delete_index = index
                
                
                if st.button("Hapus", key="neraca_delete_confirm"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.neraca_show_delete_form = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")