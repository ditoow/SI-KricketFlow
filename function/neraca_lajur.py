
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




def add_data(nama_akun, neraca_saldo_debet, neraca_saldo_kredit, laba_rugi_debet, laba_rugi_kredit, neraca_debet, neraca_kredit):
    df = load_neraca_lajur_data()
    new_row = pd.DataFrame({
        'Nama Akun': [nama_akun], 
        'Neraca Saldo Debet': [neraca_saldo_debet], 
        'Neraca Saldo Kredit': [neraca_saldo_kredit],
        'Laba Rugi Debet': [laba_rugi_debet],
        'Laba Rugi Kredit': [laba_rugi_kredit],
        'Neraca Debet': [neraca_debet],
        'Neraca Kredit': [neraca_kredit]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_neraca_lajur_data(df)
    return df


def edit_data(index, nama_akun, neraca_saldo_debet, neraca_saldo_kredit, laba_rugi_debet, laba_rugi_kredit, neraca_debet, neraca_kredit):
    df = load_neraca_lajur_data()
    df.loc[index, 'Nama Akun'] = nama_akun
    df.loc[index, 'Neraca Saldo Debet'] = neraca_saldo_debet
    df.loc[index, 'Neraca Saldo Kredit'] = neraca_saldo_kredit
    df.loc[index, 'Laba Rugi Debet'] = laba_rugi_debet
    df.loc[index, 'Laba Rugi Kredit'] = laba_rugi_kredit
    df.loc[index, 'Neraca Debet'] = neraca_debet
    df.loc[index, 'Neraca Kredit'] = neraca_kredit
    save_neraca_lajur_data(df)
    return df


def delete_data(index):
    df = load_neraca_lajur_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_neraca_lajur_data(df)
    return df

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
            
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data'):
                    st.session_state.show_add_form = not st.session_state.show_add_form
                    st.session_state.show_edit_form = False
                    st.session_state.show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data'):
                    st.session_state.show_edit_form = not st.session_state.show_edit_form
                    st.session_state.show_add_form = False
                    st.session_state.show_delete_form = False
            with col3:
                if st.button('🗑️ Hapus Data'):
                    st.session_state.show_delete_form = not st.session_state.show_delete_form
                    st.session_state.show_add_form = False
                    st.session_state.show_edit_form = False
        else:
            
            st.warning("Data neraca lajur tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca_lajur.csv")
            
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data'):
                    st.session_state.show_add_form = not st.session_state.show_add_form
                    st.session_state.show_edit_form = False
                    st.session_state.show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Nama Akun, Neraca Saldo Debet, Neraca Saldo Kredit, Laba Rugi Debet, Laba Rugi Kredit, Neraca Debet, Neraca Kredit)")
        
        
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data'):
                st.session_state.show_add_form = not st.session_state.show_add_form
                st.session_state.show_edit_form = False
                st.session_state.show_delete_form = False
        with col2:
            if st.button('✏️ Edit Data', disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', disabled=True):
                pass
    
    
    if st.session_state.show_add_form:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("nl_add_form"):
                nama_akun = st.text_input("Nama Akun")
                neraca_saldo_debet = st.number_input("Neraca Saldo Debet", min_value=0.0, format="%f")
                neraca_saldo_kredit = st.number_input("Neraca Saldo Kredit", min_value=0.0, format="%f")
                laba_rugi_debet = st.number_input("Laba Rugi Debet", min_value=0.0, format="%f")
                laba_rugi_kredit = st.number_input("Laba Rugi Kredit", min_value=0.0, format="%f")
                neraca_debet = st.number_input("Neraca Debet", min_value=0.0, format="%f")
                neraca_kredit = st.number_input("Neraca Kredit", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
    
    
    if st.session_state.show_edit_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options)
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index = index
                
                with st.form("nl_edit_form"):
                    nama_akun = st.text_input("Nama Akun", value=df_neraca.loc[index, 'Nama Akun'])
                    
                    
                    current_neraca_saldo_debet = pd.to_numeric(df_neraca.loc[index, 'Neraca Saldo Debet'], errors='coerce') or 0.0
                    current_neraca_saldo_kredit = pd.to_numeric(df_neraca.loc[index, 'Neraca Saldo Kredit'], errors='coerce') or 0.0
                    current_laba_rugi_debet = pd.to_numeric(df_neraca.loc[index, 'Laba Rugi Debet'], errors='coerce') or 0.0
                    current_laba_rugi_kredit = pd.to_numeric(df_neraca.loc[index, 'Laba Rugi Kredit'], errors='coerce') or 0.0
                    current_neraca_debet = pd.to_numeric(df_neraca.loc[index, 'Neraca Debet'], errors='coerce') or 0.0
                    current_neraca_kredit = pd.to_numeric(df_neraca.loc[index, 'Neraca Kredit'], errors='coerce') or 0.0
                    
                    neraca_saldo_debet = st.number_input("Neraca Saldo Debet", min_value=0.0, value=float(current_neraca_saldo_debet), format="%f")
                    neraca_saldo_kredit = st.number_input("Neraca Saldo Kredit", min_value=0.0, value=float(current_neraca_saldo_kredit), format="%f")
                    laba_rugi_debet = st.number_input("Laba Rugi Debet", min_value=0.0, value=float(current_laba_rugi_debet), format="%f")
                    laba_rugi_kredit = st.number_input("Laba Rugi Kredit", min_value=0.0, value=float(current_laba_rugi_kredit), format="%f")
                    neraca_debet = st.number_input("Neraca Debet", min_value=0.0, value=float(current_neraca_debet), format="%f")
                    neraca_kredit = st.number_input("Neraca Kredit", min_value=0.0, value=float(current_neraca_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(index, nama_akun, neraca_saldo_debet, neraca_saldo_kredit, laba_rugi_debet, laba_rugi_kredit, neraca_debet, neraca_kredit)
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
                
                
                if st.button("Hapus"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.show_delete_form = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")

