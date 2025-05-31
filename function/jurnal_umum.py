import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_jurnal_umum_data():

    
    
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_umum.csv')
    
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        
        return pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])

def save_jurnal_umum_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_umum.csv')
    df.to_csv(csv_path, index=False)



def show_jurnal_umum():

    st.subheader("Jurnal Umum")
    
    
    if 'jurnal_show_add_form' not in st.session_state:
        st.session_state.jurnal_show_add_form = False
    if 'jurnal_show_edit_form' not in st.session_state:
        st.session_state.jurnal_show_edit_form = False
    if 'jurnal_show_delete_form' not in st.session_state:
        st.session_state.jurnal_show_delete_form = False
    if 'jurnal_edit_index' not in st.session_state:
        st.session_state.jurnal_edit_index = 0
    if 'jurnal_delete_index' not in st.session_state:
        st.session_state.jurnal_delete_index = 0
    
    
    try:
        
        df_jurnal = load_jurnal_umum_data()
        
        if not df_jurnal.empty:
            
            display_df = df_jurnal.copy()
            
            
            
            currency_cols = ['Debet', 'Kredit']
            for col in currency_cols:
                
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            st.table(display_df)
            
            
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'jurnal_umum.csv')
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
            
            st.warning("Data jurnal umum tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/jurnal_umum.csv")
            
            
            st.markdown("---")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Tanggal, Keterangan, Debet, Kredit)")
        
        
        st.markdown("---")
    
    
    if st.session_state.jurnal_show_add_form:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("jurnal_add_form"):
                tanggal = st.date_input("Tanggal")
                keterangan = st.text_input("Keterangan")
                debet = st.number_input("Debet", min_value=0.0, format="%f")
                kredit = st.number_input("Kredit", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
                if submitted:
                    add_jurnal_data(tanggal.strftime('%d/%m/%Y'), keterangan, debet, kredit)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.jurnal_show_add_form = False
                    st.rerun()  
    
    
    if st.session_state.jurnal_show_edit_form and 'df_jurnal' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Keterangan']}" for i, row in df_jurnal.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key="jurnal_edit_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.jurnal_edit_index = index
                
                with st.form("jurnal_edit_form"):
                    
                    try:
                        date_value = pd.to_datetime(df_jurnal.loc[index, 'Tanggal'])
                    except:
                        date_value = pd.Timestamp.now()
                    
                    tanggal = st.date_input("Tanggal", value=date_value)
                    keterangan = st.text_input("Keterangan", value=df_jurnal.loc[index, 'Keterangan'])
                    
                    
                    current_debet = pd.to_numeric(df_jurnal.loc[index, 'Debet'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_jurnal.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debet = st.number_input("Debet", min_value=0.0, value=float(current_debet), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_jurnal_data(index, tanggal.strftime('%d/%m/%Y'), keterangan, debet, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.jurnal_show_edit_form = False
                        st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    
    if st.session_state.jurnal_show_delete_form and 'df_jurnal' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - {row['Keterangan']}" for i, row in df_jurnal.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="jurnal_delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.jurnal_delete_index = index
                
                
                if st.button("Hapus", key="jurnal_delete_confirm"):
                    delete_jurnal_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.jurnal_show_delete_form = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")