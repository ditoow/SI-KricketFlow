
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys

# Ensure database directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_labarugi_data():
    """Load data from the Laporan Laba Rugi CSV file if it exists"""
    # Ensure database directory exists
    # Using os.path.abspath to ensure we get the correct path even when imported
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'lap_labarugi.csv')
    
    # Check if file exists
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Return empty DataFrame with correct columns for Laporan Laba Rugi
        return pd.DataFrame(columns=['Kategori', 'Akun', 'Debet', 'Kredit'])

def save_labarugi_data(df):
    """Save the Laporan Laba Rugi DataFrame to CSV"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'lap_labarugi.csv')
    df.to_csv(csv_path, index=False)


# Fungsi untuk menambahkan data baru
def add_data(kategori, akun, debet, kredit):
    df = load_labarugi_data()
    new_row = pd.DataFrame({'Kategori': [kategori], 'Akun': [akun], 'Debet': [debet], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_labarugi_data(df)
    return df

# Fungsi untuk mengedit data
def edit_data(index, kategori, akun, debet, kredit):
    df = load_labarugi_data()
    df.loc[index, 'Kategori'] = kategori
    df.loc[index, 'Akun'] = akun
    df.loc[index, 'Debet'] = debet
    df.loc[index, 'Kredit'] = kredit
    save_labarugi_data(df)
    return df

# Fungsi untuk menghapus data
def delete_data(index):
    df = load_labarugi_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_labarugi_data(df)
    return df

def show_lap_labarugi():
    """
    Display the Laporan Laba Rugi section with tables and forms.
    This function handles all UI elements and interactions for this section.
    """
    st.subheader("Laporan Laba Rugi")
    
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
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    # Table to display data from lap_labarugi.csv
    try:
        # Load data from CSV
        df_labarugi = load_labarugi_data()
        
        if not df_labarugi.empty:
            # Create a copy of the dataframe for display purposes
            display_df = df_labarugi.copy()
            
            # Format currency columns if data exists
            # Ensure numeric values before formatting
            currency_cols = ['Debet', 'Kredit']
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
            csv_path = os.path.join(project_root, 'database', 'lap_labarugi.csv')
            raw_df = pd.read_csv(csv_path)
            
            # Ensure numeric values before calculating sum
            raw_df['Debet'] = pd.to_numeric(raw_df['Debet'], errors='coerce').fillna(0)
            raw_df['Kredit'] = pd.to_numeric(raw_df['Kredit'], errors='coerce').fillna(0)
            
            total_debet = raw_df['Debet'].sum()
            total_kredit = raw_df['Kredit'].sum()
            laba_bersih = total_kredit - total_debet
            
            # Display totals in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Debet", f"Rp {total_debet:,.2f}".replace(',', '.'))
            with col2:
                st.metric("Total Kredit", f"Rp {total_kredit:,.2f}".replace(',', '.'))
            with col3:
                st.metric("Laba Bersih", f"Rp {laba_bersih:,.2f}".replace(',', '.'))
                
            # Add a separator between the content and buttons
            st.markdown("---")
            
            # Add buttons for CRUD operations at the bottom
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="lr_add_btn"):
                    st.session_state.show_add_form = True
                    st.session_state.show_edit_form = False
                    st.session_state.show_delete_form = False
                    st.session_state.form_submitted = False
                    st.rerun()
            with col2:
                if st.button('✏️ Edit Data', key="lr_edit_btn"):
                    st.session_state.show_edit_form = True
                    st.session_state.show_add_form = False
                    st.session_state.show_delete_form = False
                    st.session_state.form_submitted = False
                    st.rerun()
            with col3:
                if st.button('🗑️ Hapus Data', key="lr_delete_btn"):
                    st.session_state.show_delete_form = True
                    st.session_state.show_add_form = False
                    st.session_state.show_edit_form = False
                    st.session_state.form_submitted = False
                    st.rerun()
        else:
            # Display message when data is not available
            st.warning("Data laporan laba rugi tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/lap_labarugi.csv")
            
            # Add buttons for CRUD operations at the bottom (even when there's no data)
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="lr_add_btn_empty"):
                    st.session_state.show_add_form = True
                    st.session_state.show_edit_form = False
                    st.session_state.show_delete_form = False
                    st.session_state.form_submitted = False
                    st.rerun()
            with col2:
                if st.button('✏️ Edit Data', key="lr_edit_btn_empty", disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', key="lr_delete_btn_empty", disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Kategori, Akun, Debet, Kredit)")
        
        # Add buttons for CRUD operations at the bottom (even when there's an error)
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data', key="lr_add_btn_error"):
                st.session_state.show_add_form = True
                st.session_state.show_edit_form = False
                st.session_state.show_delete_form = False
                st.session_state.form_submitted = False
                st.rerun()
        with col2:
            if st.button('✏️ Edit Data', key="lr_edit_btn_error", disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', key="lr_delete_btn_error", disabled=True):
                pass
    
    # Form untuk menambahkan data (pop-up)
    if st.session_state.show_add_form:
        with st.expander("Form Tambah Data", expanded=True):
            st.subheader("Tambah Data Baru")
            with st.form("lr_add_form", clear_on_submit=True):
                kategori = st.selectbox("Kategori", options=["Pendapatan", "Pembelian", "Beban", "TOTAL", ""])
                akun = st.text_input("Akun")
                debet = st.number_input("Debet", min_value=0.0, format="%f")
                kredit = st.number_input("Kredit", min_value=0.0, format="%f")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Simpan")
                with col2:
                    cancelled = st.form_submit_button("Batal")
                
                if submitted:
                    add_data(kategori, akun, debet, kredit)
                    st.success("Data berhasil ditambahkan!")
                    st.session_state.show_add_form = False
                    st.session_state.form_submitted = True
                    # Use a sleep timer to give the success message time to be seen
                    import time
                    time.sleep(1)
                    st.rerun()
                
                if cancelled:
                    st.session_state.show_add_form = False
                    st.rerun()
    
    # Form untuk mengedit data (pop-up)
    if st.session_state.show_edit_form and 'df_labarugi' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan diedit
            options = [f"{i} - {row['Akun'] if pd.notna(row['Akun']) else row['Kategori']}" for i, row in df_labarugi.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key="edit_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.edit_index = index
                
                with st.form("lr_edit_form", clear_on_submit=True):
                    kategori = st.selectbox("Kategori", 
                                           options=["Pendapatan", "Pembelian", "Beban", "TOTAL", ""],
                                           index=["Pendapatan", "Pembelian", "Beban", "TOTAL", ""].index(df_labarugi.loc[index, 'Kategori']) if df_labarugi.loc[index, 'Kategori'] in ["Pendapatan", "Pembelian", "Beban", "TOTAL", ""] else 0)
                    
                    akun = st.text_input("Akun", value=df_labarugi.loc[index, 'Akun'] if pd.notna(df_labarugi.loc[index, 'Akun']) else "")
                    
                    # Convert to float to handle any string or formatting issues
                    current_debet = pd.to_numeric(df_labarugi.loc[index, 'Debet'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_labarugi.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debet = st.number_input("Debet", min_value=0.0, value=float(current_debet), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("Perbarui")
                    with col2:
                        cancelled = st.form_submit_button("Batal")
                    
                    if submitted:
                        edit_data(index, kategori, akun, debet, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.show_edit_form = False
                        st.session_state.form_submitted = True
                        # Use a sleep timer to give the success message time to be seen
                        import time
                        time.sleep(1)
                        st.rerun()
                    
                    if cancelled:
                        st.session_state.show_edit_form = False
                        st.rerun()
            else:
                st.warning("Tidak ada data yang dapat diedit.")
                if st.button("Kembali"):
                    st.session_state.show_edit_form = False
                    st.rerun()
    
    # Form untuk menghapus data (pop-up)
    if st.session_state.show_delete_form and 'df_labarugi' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan dihapus
            options = [f"{i} - {row['Akun'] if pd.notna(row['Akun']) else row['Kategori']}" for i, row in df_labarugi.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.delete_index = index
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Direct delete button
                    if st.button("Hapus", key="confirm_delete"):
                        delete_data(index)
                        st.success("Data berhasil dihapus!")
                        st.session_state.show_delete_form = False
                        st.session_state.form_submitted = True
                        # Use a sleep timer to give the success message time to be seen
                        import time
                        time.sleep(1)
                        st.rerun()
                
                with col2:
                    if st.button("Batal", key="cancel_delete"):
                        st.session_state.show_delete_form = False
                        st.rerun()
            else:
                st.warning("Tidak ada data yang dapat dihapus.")
                if st.button("Kembali"):
                    st.session_state.show_delete_form = False
                    st.rerun()
                    
    # Check if we need to rerun the app after form submission
    if st.session_state.form_submitted:
        st.session_state.form_submitted = False
        st.rerun()
