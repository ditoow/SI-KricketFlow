import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import sys

# Ensure database directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_jurnal_umum_data():
    """Load data from the Jurnal Umum CSV file if it exists"""
    # Ensure database directory exists
    # Using os.path.abspath to ensure we get the correct path even when imported
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_umum.csv')
    
    # Check if file exists
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])

def save_jurnal_umum_data(df):
    """Save the Jurnal Umum DataFrame to CSV"""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_umum.csv')
    df.to_csv(csv_path, index=False)

# Fungsi untuk menambahkan data baru
def add_jurnal_data(tanggal, keterangan, debet, kredit):
    df = load_jurnal_umum_data()
    new_row = pd.DataFrame({'Tanggal': [tanggal], 'Keterangan': [keterangan], 'Debet': [debet], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_jurnal_umum_data(df)
    return df

# Fungsi untuk mengedit data
def edit_jurnal_data(index, tanggal, keterangan, debet, kredit):
    df = load_jurnal_umum_data()
    df.loc[index, 'Tanggal'] = tanggal
    df.loc[index, 'Keterangan'] = keterangan
    df.loc[index, 'Debet'] = debet
    df.loc[index, 'Kredit'] = kredit
    save_jurnal_umum_data(df)
    return df

# Fungsi untuk menghapus data
def delete_jurnal_data(index):
    df = load_jurnal_umum_data()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_jurnal_umum_data(df)
    return df

def show_jurnal_umum():
    """
    Display the Jurnal Umum section with tables and forms.
    This function handles all UI elements and interactions for this section.
    """
    st.subheader("Jurnal Umum")
    
    # Initialize session state for form visibility and editing index
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
    
    # Table to display data from jurnal_umum.csv
    try:
        # Load data from CSV
        df_jurnal = load_jurnal_umum_data()
        
        if not df_jurnal.empty:
            # Create a copy of the dataframe for display purposes
            display_df = df_jurnal.copy()
            
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
            csv_path = os.path.join(project_root, 'database', 'jurnal_umum.csv')
            raw_df = pd.read_csv(csv_path)
            
            # Ensure numeric values before calculating sum
            raw_df['Debet'] = pd.to_numeric(raw_df['Debet'], errors='coerce').fillna(0)
            raw_df['Kredit'] = pd.to_numeric(raw_df['Kredit'], errors='coerce').fillna(0)
            
            total_debet = raw_df['Debet'].sum()
            total_kredit = raw_df['Kredit'].sum()
            
            # Display totals in two columns
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
                if st.button('➕ Tambah Data', key="jurnal_add_btn"):
                    st.session_state.jurnal_show_add_form = not st.session_state.jurnal_show_add_form
                    st.session_state.jurnal_show_edit_form = False
                    st.session_state.jurnal_show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', key="jurnal_edit_btn"):
                    st.session_state.jurnal_show_edit_form = not st.session_state.jurnal_show_edit_form
                    st.session_state.jurnal_show_add_form = False
                    st.session_state.jurnal_show_delete_form = False
            with col3:
                if st.button('🗑️ Hapus Data', key="jurnal_delete_btn"):
                    st.session_state.jurnal_show_delete_form = not st.session_state.jurnal_show_delete_form
                    st.session_state.jurnal_show_add_form = False
                    st.session_state.jurnal_show_edit_form = False
        else:
            # Display message when data is not available
            st.warning("Data jurnal umum tidak tersedia. Silakan gunakan tombol 'Tambah Data' untuk menambahkan data baru.")
            st.info("Path file yang diharapkan: database/jurnal_umum.csv")
            
            # Add buttons for CRUD operations at the bottom (even when there's no data)
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button('➕ Tambah Data', key="jurnal_add_btn_empty"):
                    st.session_state.jurnal_show_add_form = not st.session_state.jurnal_show_add_form
                    st.session_state.jurnal_show_edit_form = False
                    st.session_state.jurnal_show_delete_form = False
            with col2:
                if st.button('✏️ Edit Data', key="jurnal_edit_btn_empty", disabled=True):
                    pass
            with col3:
                if st.button('🗑️ Hapus Data', key="jurnal_delete_btn_empty", disabled=True):
                    pass
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Tanggal, Keterangan, Debet, Kredit)")
        
        # Add buttons for CRUD operations at the bottom (even when there's an error)
        st.markdown("---")
        st.subheader("Menu Aksi")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('➕ Tambah Data', key="jurnal_add_btn_error"):
                st.session_state.jurnal_show_add_form = not st.session_state.jurnal_show_add_form
                st.session_state.jurnal_show_edit_form = False
                st.session_state.jurnal_show_delete_form = False
        with col2:
            if st.button('✏️ Edit Data', key="jurnal_edit_btn_error", disabled=True):
                pass
        with col3:
            if st.button('🗑️ Hapus Data', key="jurnal_delete_btn_error", disabled=True):
                pass
    
    # Form untuk menambahkan data (pop-up)
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
                    st.rerun()  # Reload the app to show updated data
    
    # Form untuk mengedit data (pop-up) - moved to bottom
    if st.session_state.jurnal_show_edit_form and 'df_jurnal' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan diedit
            options = [f"{i} - {row['Keterangan']}" for i, row in df_jurnal.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan diedit:", options, key="jurnal_edit_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.jurnal_edit_index = index
                
                with st.form("jurnal_edit_form"):
                    # Parse the date string
                    try:
                        date_value = pd.to_datetime(df_jurnal.loc[index, 'Tanggal'])
                    except:
                        date_value = pd.Timestamp.now()
                    
                    tanggal = st.date_input("Tanggal", value=date_value)
                    keterangan = st.text_input("Keterangan", value=df_jurnal.loc[index, 'Keterangan'])
                    
                    # Convert to float to handle any string or formatting issues
                    current_debet = pd.to_numeric(df_jurnal.loc[index, 'Debet'], errors='coerce') or 0.0
                    current_kredit = pd.to_numeric(df_jurnal.loc[index, 'Kredit'], errors='coerce') or 0.0
                    
                    debet = st.number_input("Debet", min_value=0.0, value=float(current_debet), format="%f")
                    kredit = st.number_input("Kredit", min_value=0.0, value=float(current_kredit), format="%f")
                    
                    submitted = st.form_submit_button("Perbarui")
                    if submitted:
                        edit_jurnal_data(index, tanggal.strftime('%d/%m/%Y'), keterangan, debet, kredit)
                        st.success("Data berhasil diperbarui!")
                        st.session_state.jurnal_show_edit_form = False
                        st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat diedit.")
    
    # Form untuk menghapus data (pop-up) - moved to bottom and removed confirmation
    if st.session_state.jurnal_show_delete_form and 'df_jurnal' in locals():
        with st.container():
            st.markdown("---")
            # Dropdown untuk memilih data yang akan dihapus
            options = [f"{i} - {row['Keterangan']}" for i, row in df_jurnal.iterrows()]
            if options:
                selected_option = st.selectbox("Pilih data yang akan dihapus:", options, key="jurnal_delete_select")
                index = int(selected_option.split(" - ")[0])
                st.session_state.jurnal_delete_index = index
                
                # Direct delete button without confirmation
                if st.button("Hapus", key="jurnal_delete_confirm"):
                    delete_jurnal_data(index)
                    st.success("Data berhasil dihapus!")
                    st.session_state.jurnal_show_delete_form = False
                    st.rerun()  # Reload the app to show updated data
            else:
                st.warning("Tidak ada data yang dapat dihapus.")