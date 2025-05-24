import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys
import re

# Ensure database directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_account_name_from_filename(filename):
    """Extract account name from the filename format bukbes_XXX.csv or bukbes.XXX.csv"""
    if filename.startswith('bukbes_'):
        return filename.replace('bukbes_', '').replace('.csv', '')
    elif filename.startswith('bukbes.'):
        return filename.replace('bukbes.', '').replace('.csv', '')
    else:
        return filename.replace('.csv', '')

def get_filename_from_account(account):
    """Convert account name to filename"""
    # Check if the account includes 'beban' at the start
    if account.startswith('beban'):
        # Some files use bukbes.bebanXXX.csv format
        if os.path.exists(os.path.join(get_bukubesar_dir(), f'bukbes.{account}.csv')):
            return f'bukbes.{account}.csv'
    
    # Default format is bukbes_XXX.csv
    return f'bukbes_{account}.csv'

def get_bukubesar_dir():
    """Get the path to the bukubesar directory"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database', 'bukubesar')
    ensure_dir(database_dir)
    return database_dir

def load_buku_besar_data(akun):
    """Load data from the Buku Besar CSV file for a specific account"""
    database_dir = get_bukubesar_dir()
    
    # Determine the correct filename based on the account name
    filename = get_filename_from_account(akun)
    csv_path = os.path.join(database_dir, filename)
    
    # If file doesn't exist with the standard naming, try alternative format
    if not os.path.exists(csv_path) and akun.startswith('beban'):
        alternative_filename = f'bukbes.{akun}.csv'
        alternative_path = os.path.join(database_dir, alternative_filename)
        if os.path.exists(alternative_path):
            csv_path = alternative_path
    
    # Check if file exists
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=['Tanggal', 'Debet', 'Tanggal', 'Kredit'])

def save_buku_besar_data(df, akun):
    """Save the Buku Besar DataFrame to CSV"""
    database_dir = get_bukubesar_dir()
    
    # Determine the correct filename based on the account name
    filename = get_filename_from_account(akun)
    csv_path = os.path.join(database_dir, filename)
    
    # If file doesn't exist with the standard naming, try alternative format
    if not os.path.exists(csv_path) and akun.startswith('beban'):
        alternative_filename = f'bukbes.{akun}.csv'
        alternative_path = os.path.join(database_dir, alternative_filename)
        if os.path.exists(alternative_path):
            csv_path = alternative_path
    
    df.to_csv(csv_path, index=False)

def add_data(akun, tanggal_debet, debet, tanggal_kredit, kredit):
    df = load_buku_besar_data(akun)
    
    # Determine the correct column names
    tanggal_kredit_col = 'Tanggal.1' if 'Tanggal.1' in df.columns else 'Tanggal'
    
    new_row = pd.DataFrame({
        'Tanggal': [tanggal_debet], 
        'Debet': [debet], 
        tanggal_kredit_col: [tanggal_kredit], 
        'Kredit': [kredit]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_buku_besar_data(df, akun)
    return df

def edit_data(akun, index, tanggal_debet, debet, tanggal_kredit, kredit):
    df = load_buku_besar_data(akun)
    
    # Determine the correct column names
    tanggal_kredit_col = 'Tanggal.1' if 'Tanggal.1' in df.columns else 'Tanggal'
    
    df.loc[index, 'Tanggal'] = tanggal_debet
    df.loc[index, 'Debet'] = debet
    df.loc[index, tanggal_kredit_col] = tanggal_kredit
    df.loc[index, 'Kredit'] = kredit
    save_buku_besar_data(df, akun)
    return df

def delete_data(akun, index):
    df = load_buku_besar_data(akun)
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_buku_besar_data(df, akun)
    return df

def get_bukubesar_accounts_ordered():
    """Get list of all available buku besar accounts in specified order"""
    database_dir = get_bukubesar_dir()
    
    # Custom ordering of accounts as specified
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
    
    # Get all the files that actually exist
    available_files = os.listdir(database_dir)
    available_accounts = []
    
    # Check each ordered account and add it if file exists
    for account in ordered_accounts:
        # Check for standard format (bukbes_xxx.csv)
        if f'bukbes_{account}.csv' in available_files:
            available_accounts.append(account)
        # Check for alternative format (bukbes.xxx.csv) - especially for beban accounts
        elif f'bukbes.{account}.csv' in available_files:
            available_accounts.append(account)
    
    # Get any additional accounts that weren't in the ordered list but exist in the directory
    for filename in available_files:
        if filename.endswith('.csv'):
            account = get_account_name_from_filename(filename)
            if account not in available_accounts:
                available_accounts.append(account)
    
    return available_accounts

def format_account_name(account_name):
    """Format account name for display (capitalize and replace underscores with spaces)"""
    # Replace underscores with spaces
    formatted = account_name.replace('_', ' ')
    
    # Special handling for account names with "beban"
    if formatted.startswith('beban'):
        # Map beban accounts to their proper display names
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
            # Fallback for any other beban accounts
            parts = formatted.split(' ', 1)
            if len(parts) > 1:
                return f"Beban {parts[1].capitalize()}"
            else:
                return "Beban"
    # Special handling for "utangbank" 
    elif formatted == 'utangbank':
        return "Utang Bank"
    # Special handling for "ikhtisarlabarugi"
    elif formatted == 'ikhtisarlabarugi':
        return "Ikhtisar Laba Rugi"
    else:
        # Capitalize each word
        words = formatted.split()
        formatted = ' '.join(word.capitalize() for word in words)
    
    return formatted

def show_buku_besar():
    """
    Display the Buku Besar section with tables for different accounts.
    This function handles all UI elements and interactions for this section.
    """
    st.subheader("Buku Besar")
    
    # Get list of all accounts in specified order
    accounts = get_bukubesar_accounts_ordered()
    
    if not accounts:
        st.warning("Tidak ada file buku besar yang ditemukan.")
        return
    
    # Create formatted account names for display
    display_accounts = [format_account_name(account) for account in accounts]
    account_dict = dict(zip(display_accounts, accounts))
    
    # Select account to display
    selected_display = st.selectbox(
        "Pilih Akun:",
        options=display_accounts
    )
    
    # Convert display name back to actual account name
    selected_account = account_dict[selected_display]
    
    # Initialize session state for form visibility and editing index
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
    
    # Table to display data from the selected buku besar file
    try:
        # Load data from CSV
        df_bukbes = load_buku_besar_data(selected_account)
        
        if not df_bukbes.empty:
            # Create a copy of the dataframe for display purposes
            display_df = df_bukbes.copy()
            
            # Format currency columns if data exists
            # Ensure numeric values before formatting
            currency_cols = ['Debet', 'Kredit']
            for col in currency_cols:
                if col in display_df.columns:
                    # Convert to numeric first, coercing errors to NaN
                    display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                    # Then apply currency formatting
                    display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            # Identify the correct column names
            tanggal_kredit_col = 'Tanggal.1' if 'Tanggal.1' in display_df.columns else 'Tanggal'
            
            # Rename columns for better display
            column_mapping = {
                'Tanggal': 'Tanggal Debet',
                'Tanggal.1': 'Tanggal Kredit',
                tanggal_kredit_col: 'Tanggal Kredit'
            }
            display_df = display_df.rename(columns=column_mapping)
            
            # Display as a styled table with headers
            st.table(display_df)
            
            # Calculate summary
            database_dir = get_bukubesar_dir()
            filename = get_filename_from_account(selected_account)
            csv_path = os.path.join(database_dir, filename)
            raw_df = pd.read_csv(csv_path)
            
            # Ensure numeric values before calculating sum
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
            
            # Check if the account is one of the ones that should display Saldo Debit
            if selected_account in ['kas', 'perlengkapan', 'peralatan']:
                saldo_debit = total_debet - total_kredit
                
                # Display totals in three columns with Saldo Debit
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
                with col2:
                    st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                with col3:
                    st.metric("Saldo Debit", f"Rp {saldo_debit:,.2f}".replace(',', '.'))
            else:
                # For other accounts, display only Debet and Kredit in two columns
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
                with col2:
                    st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            # Add a separator between the content and buttons
            st.markdown("---")
            
            # Add buttons for CRUD operations at the bottom
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key=f'add_bukbes_{selected_account}'):
                    st.session_state.show_add_form_bukbes = not st.session_state.show_add_form_bukbes
                    st.session_state.show_edit_form_bukbes = False
                    st.session_state.show_delete_form_bukbes = False
            with col2:
                if st.button('✏️ Edit Data', key=f'edit_bukbes_{selected_account}'):
                    st.session_state.show_edit_form_bukbes = not st.session_state.show_edit_form_bukbes
                    st.session_state.show_add_form_bukbes = False
                    st.session_state.show_delete_form_bukbes = False
            with col3:
                if st.button('🗑️ Hapus Data', key=f'delete_bukbes_{selected_account}'):
                    st.session_state.show_delete_form_bukbes = not st.session_state.show_delete_form_bukbes
                    st.session_state.show_add_form_bukbes = False
                    st.session_state.show_edit_form_bukbes = False
        else:
            # Display message when data is not available
            st.warning(f"Data buku besar untuk akun {selected_display} tidak tersedia atau kosong.")
            st.info(f"Path file yang diharapkan: database/bukubesar/bukbes_{selected_account}.csv")
            
            # Add buttons for CRUD operations at the bottom (even when there's no data)
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key=f'add_bukbes_empty_{selected_account}'):
                    st.session_state.show_add_form_bukbes = not st.session_state.show_add_form_bukbes
                    st.session_state.show_edit_form_bukbes = False
                    st.session_state.show_delete_form_bukbes = False
            with col2:
                if st.button('✏️ Edit Data', key=f'edit_bukbes_empty_{selected_account}', disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', key=f'delete_bukbes_empty_{selected_account}', disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info(f"Pastikan format file CSV sesuai (Tanggal, Debet, Tanggal, Kredit)")
        
        # Add buttons for CRUD operations at the bottom (even when there's an error)
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data', key=f'add_bukbes_error_{selected_account}'):
                st.session_state.show_add_form_bukbes = not st.session_state.show_add_form_bukbes
                st.session_state.show_edit_form_bukbes = False
                st.session_state.show_delete_form_bukbes = False
        with col2:
            if st.button('✏️ Edit Data', key=f'edit_bukbes_error_{selected_account}', disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', key=f'delete_bukbes_error_{selected_account}', disabled=True):
                pass
    
    # Form untuk menambahkan data (pop-up)
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
                    st.rerun()  # Reload the app to show updated data
    
    # Form untuk mengedit data (pop-up)
    if st.session_state.show_edit_form_bukbes and 'df_bukbes' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan diedit
            options = [f"{i} - Baris {i+1}" for i in range(len(df_bukbes))]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key=f'edit_select_bukbes_{selected_account}')
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index_bukbes = index
                
                with st.form("edit_form_bukbes"):
                    tanggal_debet = st.text_input("Tanggal Debet", value=df_bukbes.loc[index, 'Tanggal'] if pd.notna(df_bukbes.loc[index, 'Tanggal']) else "")
                    # Convert to float to handle any string or formatting issues
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
                        st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    # Form untuk menghapus data (pop-up)
    if st.session_state.show_delete_form_bukbes and 'df_bukbes' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan dihapus
            options = [f"{i} - Baris {i+1}" for i in range(len(df_bukbes))]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key=f'delete_select_bukbes_{selected_account}')
                index = int(selected_option.split(" - ")[0])
                st.session_state.delete_index_bukbes = index
                
                # Direct delete button without confirmation
                if st.button("Hapus", key=f'confirm_delete_bukbes_{selected_account}'):
                    delete_data(selected_account, index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.show_delete_form_bukbes = False
                    st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat dihapus.")