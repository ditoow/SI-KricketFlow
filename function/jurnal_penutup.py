import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_jurnal_penutup_data():

    
    
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_penutup.csv')
    
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        
        
        if 'Keterangan ' in df.columns:
            df = df.rename(columns={'Keterangan ': 'Keterangan'})
            
        
        new_df = pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])
        
        
        
        for col in new_df.columns:
            if col in df.columns:
                new_df[col] = df[col]
        
        return new_df
    else:
        
        return pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])

def save_jurnal_penutup_data(df):

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_penutup.csv')
    
    
    save_df = pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])
    
    
    for col in save_df.columns:
        if col in df.columns:
            save_df[col] = df[col]
    
    
    save_df.to_csv(csv_path, index=False)


def add_data(tanggal, keterangan, debet, kredit):
    df = load_jurnal_penutup_data()
    new_row = pd.DataFrame({'Tanggal': [tanggal], 'Keterangan': [keterangan], 'Debet': [debet], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_jurnal_penutup_data(df)
    return df


def edit_data(index, tanggal, keterangan, debet, kredit):
    df = load_jurnal_penutup_data()
    df.loc[index, 'Tanggal'] = tanggal
    df.loc[index, 'Keterangan'] = keterangan
    df.loc[index, 'Debet'] = debet
    df.loc[index, 'Kredit'] = kredit
    save_jurnal_penutup_data(df)
    return df


def delete_data(index):
    df = load_jurnal_penutup_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_jurnal_penutup_data(df)
    return df

def show_jurnal_penutup():

    st.subheader("Jurnal Penutup")
    
    
    if 'show_add_form_jp' not in st.session_state:
        st.session_state.show_add_form_jp = False
    if 'show_edit_form_jp' not in st.session_state:
        st.session_state.show_edit_form_jp = False
    if 'show_delete_form_jp' not in st.session_state:
        st.session_state.show_delete_form_jp = False
    if 'edit_index_jp' not in st.session_state:
        st.session_state.edit_index_jp = 0
    if 'delete_index_jp' not in st.session_state:
        st.session_state.delete_index_jp = 0
    
    
    try:
        
        df_jurnal = load_jurnal_penutup_data()
        
        if not df_jurnal.empty:
            
            display_df = df_jurnal.copy()
            
            
            
            currency_cols = ['Debet', 'Kredit']
            for col in currency_cols:
                
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            st.table(display_df)
            
            
            
            numeric_df = df_jurnal.copy()
            numeric_df['Debet'] = pd.to_numeric(numeric_df['Debet'], errors='coerce').fillna(0)
            numeric_df['Kredit'] = pd.to_numeric(numeric_df['Kredit'], errors='coerce').fillna(0)
            
            total_debet = numeric_df['Debet'].sum()
            total_kredit = numeric_df['Kredit'].sum()
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
            
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="jp_add_btn"):
                    st.session_state.show_add_form_jp = not st.session_state.show_add_form_jp
                    st.session_state.show_edit_form_jp = False
                    st.session_state.show_delete_form_jp = False
            with col2:
                if st.button('✏️ Edit Data', key="jp_edit_btn"):
                    st.session_state.show_edit_form_jp = not st.session_state.show_edit_form_jp
                    st.session_state.show_add_form_jp = False
                    st.session_state.show_delete_form_jp = False
            with col3:
                if st.button('🗑️ Hapus Data', key="jp_delete_btn"):
                    st.session_state.show_delete_form_jp = not st.session_state.show_delete_form_jp
                    st.session_state.show_add_form_jp = False
                    st.session_state.show_edit_form_jp = False
        else:
            
            st.warning("Data jurnal penutup tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/jurnal_penutup.csv")
            
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="jp_add_btn_empty"):
                    st.session_state.show_add_form_jp = not st.session_state.show_add_form_jp
                    st.session_state.show_edit_form_jp = False
                    st.session_state.show_delete_form_jp = False
            with col2:
                if st.button('✏️ Edit Data', key="jp_edit_btn_empty", disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', key="jp_delete_btn_empty", disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Tanggal, Keterangan, Debet, Kredit)")
        
        
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data', key="jp_add_btn_error"):
                st.session_state.show_add_form_jp = not st.session_state.show_add_form_jp
                st.session_state.show_edit_form_jp = False
                st.session_state.show_delete_form_jp = False
        with col2:
            if st.button('✏️ Edit Data', key="jp_edit_btn_error", disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', key="jp_delete_btn_error", disabled=True):
                pass
    
    
    if st.session_state.show_add_form_jp:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("add_form_jp"):
                tanggal = st.date_input("Tanggal")
                keterangan = st.text_input("Keterangan")
                debet = st.number_input("Debet", min_value=0.0, format="%f")
                kredit = st.number_input("Kredit", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
                if submitted:
                    add_data(tanggal.strftime('%m/%d/%Y'), keterangan, debet, kredit)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.show_add_form_jp = False
                    st.rerun()  
    
    
    if st.session_state.show_edit_form_jp and 'df_jurnal' in locals():
        with st.container():
            st.markdown("---")
            
            options = []
            for i, row in df_jurnal.iterrows():
                if pd.notna(row['Keterangan']) and row['Keterangan'] != "":
                    options.append(f"{i} - {row['Keterangan']}")
                elif pd.notna(row['Tanggal']) and row['Tanggal'] != "":
                    options.append(f"{i} - {row['Tanggal']}")
                else:
                    options.append(f"{i} - Item {i}")
                    
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key="jp_edit_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index_jp = index
                
                with st.form("edit_form_jp"):
                    
                    
                    date_str = df_jurnal.loc[index, 'Tanggal']
                    try:
                        
                        from datetime import datetime
                        if isinstance(date_str, str) and date_str.strip():
                            
                            try:
                                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                            except ValueError:
                                try:
                                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                                except ValueError:
                                    date_obj = datetime.now()
                        else:
                            date_obj = datetime.now()  
                    except:
                        date_obj = datetime.now()  
                        
                    tanggal = st.date_input("Tanggal", value=date_obj)
                    
                    
                    keterangan_value = df_jurnal.loc[index, 'Keterangan'] if pd.notna(df_jurnal.loc[index, 'Keterangan']) else ""
                    keterangan = st.text_input("Keterangan", value=keterangan_value)
                    
                    
                    current_debet = pd.to_numeric(df_jurnal.loc[index, 'Debet'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_jurnal.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debet = st.number_input("Debet", min_value=0.0, value=float(current_debet), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(index, tanggal.strftime('%m/%d/%Y'), keterangan, debet, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.show_edit_form_jp = False
                        st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    
    if st.session_state.show_delete_form_jp and 'df_jurnal' in locals():
        with st.container():
            st.markdown("---")
            
            options = []
            for i, row in df_jurnal.iterrows():
                if pd.notna(row['Keterangan']) and row['Keterangan'] != "":
                    options.append(f"{i} - {row['Keterangan']}")
                elif pd.notna(row['Tanggal']) and row['Tanggal'] != "":
                    options.append(f"{i} - {row['Tanggal']}")
                else:
                    options.append(f"{i} - Item {i}")
                    
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="jp_delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.delete_index_jp = index
                
                
                if st.button("Hapus", key="jp_delete_confirm"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.show_delete_form_jp = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")