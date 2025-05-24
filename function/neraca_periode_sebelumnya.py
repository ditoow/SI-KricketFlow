import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys

# Ensure database directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_neraca_saldo_data():
    """Load data from the Neraca Saldo CSV file if it exists"""
    # Ensure database directory exists
    # Using os.path.abspath to ensure we get the correct path even when imported
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo_periode_sebelumnya.csv')
    
    # Check if file exists
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=['Nama Akun', 'Debit', 'Kredit'])

def save_neraca_saldo_data(df):
    """Save the Neraca Saldo DataFrame to CSV"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo_periode_sebelumnya.csv')
    df.to_csv(csv_path, index=False)


# Fungsi untuk menambahkan data baru
def add_data(nama_akun, debit, kredit):
    df = load_neraca_saldo_data()
    new_row = pd.DataFrame({'Nama Akun': [nama_akun], 'Debit': [debit], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_neraca_saldo_data(df)
    return df

# Fungsi untuk mengedit data
def edit_data(index, nama_akun, debit, kredit):
    df = load_neraca_saldo_data()
    df.loc[index, 'Nama Akun'] = nama_akun
    df.loc[index, 'Debit'] = debit
    df.loc[index, 'Kredit'] = kredit
    save_neraca_saldo_data(df)
    return df

# Fungsi untuk menghapus data
def delete_data(index):
    df = load_neraca_saldo_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_neraca_saldo_data(df)
    return df

def show_neraca_saldo_periode_sebelumnya():
    """
    Display the Neraca Saldo Periode Sebelumnya section with tables and forms.
    This function handles all UI elements and interactions for this section.
    """
    st.subheader("Neraca Saldo Periode Sebelumnya")
    
    # Initialize session state for form visibility and editing index
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
    
    # Table to display data from neraca_saldo_periode_sebelumnya.csv
    try:
        # Load data from CSV
        df_neraca = load_neraca_saldo_data()
        
        if not df_neraca.empty:
            # Create a copy of the dataframe for display purposes
            display_df = df_neraca.copy()
            
            # Format currency columns if data exists
            # Ensure numeric values before formatting
            currency_cols = ['Debit', 'Kredit']
            for col in currency_cols:
                # Convert to numeric first, coercing errors to NaN
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                # Then apply currency formatting
                display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.'))
            
            # Display as a styled table with headers
            st.table(display_df)
            
            # Calculate summary
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'neraca_saldo_periode_sebelumnya.csv')
            raw_df = pd.read_csv(csv_path)
            
            # Ensure numeric values before calculating sum
            raw_df['Debit'] = pd.to_numeric(raw_df['Debit'], errors='coerce').fillna(0)
            raw_df['Kredit'] = pd.to_numeric(raw_df['Kredit'], errors='coerce').fillna(0)
            
            total_debit = raw_df['Debit'].sum()
            total_kredit = raw_df['Kredit'].sum()
            
            # Display totals in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Debit", f"Rp {total_debit:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
                
            # Add a separator between the content and buttons
            st.markdown("---")
            
            # Add buttons for CRUD operations at the bottom
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
            # Display message when data is not available
            st.warning("Data neraca saldo tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca_saldo_periode_sebelumnya.csv")
            
            # Add buttons for CRUD operations at the bottom (even when there's no data)
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
        
        # Add buttons for CRUD operations at the bottom (even when there's an error)
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
    
    # Form untuk menambahkan data (pop-up)
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
                    st.rerun()  # Reload the app to show updated data
    
    # Form untuk mengedit data (pop-up) - moved to bottom
    if st.session_state.show_edit_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan diedit
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options)
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index = index
                
                with st.form("nps_edit_form"):
                    nama_akun = st.text_input("Nama Akun", value=df_neraca.loc[index, 'Nama Akun'])
                    # Convert to float to handle any string or formatting issues
                    current_debit = pd.to_numeric(df_neraca.loc[index, 'Debit'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_neraca.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debit = st.number_input("Debit", min_value=0.0, value=float(current_debit), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_data(index, nama_akun, debit, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.show_edit_form = False
                        st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    # Form untuk menghapus data (pop-up) - moved to bottom and removed confirmation
    if st.session_state.show_delete_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan dihapus
            options = [f"{i} - {row['Nama Akun']}" for i, row in df_neraca.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options)
                index = int(selected_option.split(" - ")[0])
                st.session_state.delete_index = index
                
                # Direct delete button without confirmation
                if st.button("Hapus", key="nps_delete_confirm"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.show_delete_form = False
                    st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat dihapus.")