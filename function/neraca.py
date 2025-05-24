import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys

# Ensure database directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_neraca_data():
    """Load data from the Neraca CSV file if it exists"""
    # Ensure database directory existss
    # Using os.path.abspath to ensure we get the correct path even when imported
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca.csv')
    
    # Check if file exists
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Return empty DataFrame with correct columns based on neraca.csv structure
        return pd.DataFrame(columns=['AKTIVA', 'AKTIVA.1', 'AKTIVA.2', 'PASIVA', 'PASIVA.1', 'PASIVA.2'])

def save_neraca_data(df):
    """Save the Neraca DataFrame to CSV"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca.csv')
    df.to_csv(csv_path, index=False)



# Fungsi untuk menambahkan data baru
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

# Fungsi untuk mengedit data
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

# Fungsi untuk menghapus data
def delete_data(index):
    df = load_neraca_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_neraca_data(df)
    return df

def show_neraca():
    """
    Display the Neraca section with tables and forms.
    This function handles all UI elements and interactions for this section.
    """
    st.subheader("Neraca")
    
    # Initialize session state for form visibility and editing index
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
    
    # Table to display data from neraca.csv
    try:
        # Load data from CSV
        df_neraca = load_neraca_data()
        
        if not df_neraca.empty:
            # Create a copy of the dataframe for display purposes
            display_df = df_neraca.copy()
            
            # Format currency columns if data exists
            # Ensure numeric values before formatting
            currency_cols = ['AKTIVA.1', 'AKTIVA.2', 'PASIVA.1', 'PASIVA.2']
            for col in currency_cols:
                if col in display_df.columns:
                    # Convert to numeric first, coercing errors to NaN
                    display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0)
                    # Then apply currency formatting
                    display_df[col] = display_df[col].apply(lambda x: f"Rp {x:,.2f}".replace(',', '.') if x != 0 else "")
            
            # Display as a styled table with headers
            st.table(display_df)
            
            # Calculate summary
            # Load raw data for calculations
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            csv_path = os.path.join(project_root, 'database', 'neraca.csv')
            raw_df = pd.read_csv(csv_path)
            
            # Ensure numeric values before calculating sum
            for col in currency_cols:
                if col in raw_df.columns:
                    raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0)
            
            # Get the total for aktiva and pasiva columns
            total_aktiva = 0
            total_pasiva = 0
            
            if 'AKTIVA.2' in raw_df.columns:
                total_aktiva = raw_df['AKTIVA.2'].sum()
            
            if 'PASIVA.2' in raw_df.columns:
                total_pasiva = raw_df['PASIVA.2'].sum()
            
            # Display totals in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Aktiva", f"Rp {total_aktiva:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Pasiva", f"Rp {total_pasiva:,.2f}".replace(',', '.'))
                
            # Add a separator between the content and buttons
            st.markdown("---")
            
            # Add buttons for CRUD operations at the bottom
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
            # Display message when data is not available
            st.warning("Data neraca tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/neraca.csv")
            
            # Add buttons for CRUD operations at the bottom (even when there's no data)
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
        
        # Add buttons for CRUD operations at the bottom (even when there's an error)
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
    
    # Form untuk menambahkan data (pop-up)
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
                    st.rerun()  # Reload the app to show updated data
    
    # Form untuk mengedit data (pop-up) - moved to bottom
    if st.session_state.neraca_show_edit_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan diedit
            # Combine both AKTIVA and PASIVA to show in the dropdown
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
                    
                    # Default values, handle empty or NaN values
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
                        st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    # Form untuk menghapus data (pop-up)
    if st.session_state.neraca_show_delete_form and 'df_neraca' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan dihapus
            options = []
            for i, row in df_neraca.iterrows():
                aktiva_label = row['AKTIVA'] if pd.notna(row['AKTIVA']) and row['AKTIVA'] != '' else "(Empty)"
                pasiva_label = row['PASIVA'] if pd.notna(row['PASIVA']) and row['PASIVA'] != '' else "(Empty)"
                options.append(f"{i} - Aktiva: {aktiva_label}, Pasiva: {pasiva_label}")
                
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="neraca_delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.neraca_delete_index = index
                
                # Direct delete button without confirmation
                if st.button("Hapus", key="neraca_delete_confirm"):
                    delete_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.neraca_show_delete_form = False
                    st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat dihapus.")