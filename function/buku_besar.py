import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys
import re


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_account_name_from_filename(filename):

    if filename.startswith('bukbes_'):
        return filename.replace('bukbes_', '').replace('.csv', '')
    elif filename.startswith('bukbes.'):
        return filename.replace('bukbes.', '').replace('.csv', '')
    else:
        return filename.replace('.csv', '')

def get_filename_from_account(account):

    
    if account.startswith('beban'):
        
        if os.path.exists(os.path.join(get_bukubesar_dir(), f'bukbes.{account}.csv')):
            return f'bukbes.{account}.csv'
    
    
    return f'bukbes_{account}.csv'

def get_bukubesar_dir():

    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database', 'bukubesar')
    ensure_dir(database_dir)
    return database_dir

def load_buku_besar_data(akun):

    database_dir = get_bukubesar_dir()
    
    
    filename = get_filename_from_account(akun)
    csv_path = os.path.join(database_dir, filename)
    
    
    if not os.path.exists(csv_path) and akun.startswith('beban'):
        alternative_filename = f'bukbes.{akun}.csv'
        alternative_path = os.path.join(database_dir, alternative_filename)
        if os.path.exists(alternative_path):
            csv_path = alternative_path
    
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        
        return pd.DataFrame(columns=['Tanggal', 'Debet', 'Tanggal', 'Kredit'])

def save_buku_besar_data(df, akun):

    database_dir = get_bukubesar_dir()
    
    
    filename = get_filename_from_account(akun)
    csv_path = os.path.join(database_dir, filename)
    
    
    if not os.path.exists(csv_path) and akun.startswith('beban'):
        alternative_filename = f'bukbes.{akun}.csv'
        alternative_path = os.path.join(database_dir, alternative_filename)
        if os.path.exists(alternative_path):
            csv_path = alternative_path
    
    df.to_csv(csv_path, index=False)


def get_bukubesar_accounts_ordered():

    database_dir = get_bukubesar_dir()
    
    
    ordered_accounts = [
        'kas', 
        'perlengkapan', 
        'peralatan', 
        'utangbank', 
        'modal', 
        'penjualan', 
        'pembelian', 
        'bebangaji', 
        'bebanpengiriman', 
        'bebanpemeliharaan', 
        'bebansewa', 
        'bebanbunga', 
        'ikhtisarlabarugi'
    ]
    
    
    available_files = os.listdir(database_dir)
    available_accounts = []
    
    
    for account in ordered_accounts:
        
        if f'bukbes_{account}.csv' in available_files:
            available_accounts.append(account)
        
        elif f'bukbes.{account}.csv' in available_files:
            available_accounts.append(account)
    
    
    for filename in available_files:
        if filename.endswith('.csv'):
            account = get_account_name_from_filename(filename)
            if account not in available_accounts:
                available_accounts.append(account)
    
    return available_accounts

def format_account_name(account_name):

    
    formatted = account_name.replace('_', ' ')
    
    
    if formatted.startswith('beban'):
        
        beban_mapping = {
            'bebangaji': 'Beban Gaji',
            'bebanpengiriman': 'Beban Pengiriman',
            'bebanpemeliharaan': 'Beban Pemeliharaan',
            'bebansewa': 'Beban Sewa',
            'bebanbunga': 'Beban Bunga'
        }
        
        if account_name in beban_mapping:
            return beban_mapping[account_name]
        else:
            
            parts = formatted.split(' ', 1)
            if len(parts) > 1:
                return f"Beban {parts[1].capitalize()}"
            else:
                return "Beban"
    
    elif formatted == 'utangbank':
        return "Utang Bank"
    
    elif formatted == 'ikhtisarlabarugi':
        return "Ikhtisar Laba Rugi"
    else:
        
        words = formatted.split()
        formatted = ' '.join(word.capitalize() for word in words)
    
    return formatted

def show_buku_besar():

    st.subheader("Buku Besar")
    
    
    accounts = get_bukubesar_accounts_ordered()
    
    if not accounts:
        st.warning("Tidak ada file buku besar yang ditemukan.")
        return
    
    
    display_accounts = [format_account_name(account) for account in accounts]
    account_dict = dict(zip(display_accounts, accounts))
    
    
    selected_display = st.selectbox(
        "Pilih Akun:",
        options=display_accounts
    )
    
    
    selected_account = account_dict[selected_display]
    
    
    if 'show_add_form_bukbes' not in st.session_state:
        st.session_state.show_add_form_bukbes = False
    if 'show_edit_form_bukbes' not in st.session_state:
        st.session_state.show_edit_form_bukbes = False
    if 'show_delete_form_bukbes' not in st.session_state:
        st.session_state.show_delete_form_bukbes = False
    if 'edit_index_bukbes' not in st.session_state:
        st.session_state.edit_index_bukbes = 0
    if 'delete_index_bukbes' not in st.session_state:
        st.session_state.delete_index_bukbes = 0
    
    
    try:
        
        df_bukbes = load_buku_besar_data(selected_account)
        
        if not df_bukbes.empty:
            
            display_df = df_bukbes.copy()
            
            
            
            currency_cols = ['Debet', 'Kredit']
            for col in currency_cols:
                if col in display_df.columns:
                    
                    display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                    
                    display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            
            tanggal_kredit_col = 'Tanggal.1' if 'Tanggal.1' in display_df.columns else 'Tanggal'
            
            
            column_mapping = {
                'Tanggal': 'Tanggal Debet',
                'Tanggal.1': 'Tanggal Kredit',
                tanggal_kredit_col: 'Tanggal Kredit'
            }
            display_df = display_df.rename(columns=column_mapping)
            
            
            st.table(display_df)
            
            
            database_dir = get_bukubesar_dir()
            filename = get_filename_from_account(selected_account)
            csv_path = os.path.join(database_dir, filename)
            raw_df = pd.read_csv(csv_path)
            
            
            if 'Debet' in raw_df.columns:
                raw_df['Debet'] = pd.to_numeric(raw_df['Debet'], errors='coerce').fillna(0)
            else:
                raw_df['Debet'] = 0
                
            if 'Kredit' in raw_df.columns:
                raw_df['Kredit'] = pd.to_numeric(raw_df['Kredit'], errors='coerce').fillna(0)
            else:
                raw_df['Kredit'] = 0
            
            total_debet = raw_df['Debet'].sum()
            total_kredit = raw_df['Kredit'].sum()
            
            
            if selected_account in ['kas', 'perlengkapan', 'peralatan']:
                saldo_debit = total_debet - total_kredit
                
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
                with col2:
                    st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                with col3:
                    st.metric("Saldo Debit", f"Rp {saldo_debit:,.2f}".replace(',', '.'))
            else:
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
                with col2:
                    st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            
            st.markdown("---")
        else:
            
            st.warning(f"Data buku besar untuk akun {selected_display} tidak tersedia atau kosong.")
            st.info(f"Path file yang diharapkan: database/bukubesar/bukbes_{selected_account}.csv")
            
            
            st.markdown("---")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info(f"Pastikan format file CSV sesuai (Tanggal, Debet, Tanggal, Kredit)")
        
        
        st.markdown("---")
    
    
    if st.session_state.show_add_form_bukbes:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("add_form_bukbes"):
                tanggal_debet = st.text_input("Tanggal Debet")
                debet = st.number_input("Debet", min_value=0.0, format="%f")
                tanggal_kredit = st.text_input("Tanggal Kredit")
                kredit = st.number_input("Kredit", min_value=0.0, format="%f")
                
                submitted = st.form_submit_button("Simpan")
                if submitted:
                    add_data(selected_account, tanggal_debet, debet, tanggal_kredit, kredit)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.show_add_form_bukbes = False
                    st.rerun()  
    
    
    if st.session_state.show_edit_form_bukbes and 'df_bukbes' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - Baris {i+1}" for i in range(len(df_bukbes))]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key=f'edit_select_bukbes_{selected_account}')
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index_bukbes = index
                
                with st.form("edit_form_bukbes"):
                    tanggal_debet = st.text_input("Tanggal Debet", value=df_bukbes.loc[index, 'Tanggal'] if pd.notna(df_bukbes.loc[index, 'Tanggal']) else "")
                    
                    current_debet = pd.to_numeric(df_bukbes.loc[index, 'Debet'], errors='coerce') or 0.0
                    debet = st.number_input("Debet", min_value=0.0, value=float(current_debet), format="%f")
                    
                    tanggal_kredit_col = 'Tanggal.1' if 'Tanggal.1' in df_bukbes.columns else 'Tanggal'
                    tanggal_kredit = st.text_input("Tanggal Kredit", value=df_bukbes.loc[index, tanggal_kredit_col] if pd.notna(df_bukbes.loc[index, tanggal_kredit_col]) else "")
                    
                    current_kredit = pd.to_numeric(df_bukbes.loc[index, 'Kredit'], errors='coerce') or 0.0
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(selected_account, index, tanggal_debet, debet, tanggal_kredit, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.show_edit_form_bukbes = False
                        st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    
    if st.session_state.show_delete_form_bukbes and 'df_bukbes' in locals():
        with st.container():
            st.markdown("---")
            
            options = [f"{i} - Baris {i+1}" for i in range(len(df_bukbes))]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key=f'delete_select_bukbes_{selected_account}')
                index = int(selected_option.split(" - ")[0])
                st.session_state.delete_index_bukbes = index
                
                
                if st.button("Hapus", key=f'confirm_delete_bukbes_{selected_account}'):
                    delete_data(selected_account, index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.show_delete_form_bukbes = False
                    st.rerun()  
            else:
                st.warning("Tidak ada data yang dapat dihapus.")