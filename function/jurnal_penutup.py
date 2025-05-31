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
        try:
            # Read the CSV file with specific column names to avoid duplicates
            df = pd.read_csv(csv_path, header=0, names=['Tanggal', 'Keterangan1', 'Debet', 'Kredit', 'Unnamed', 'Keterangan2'])
            
            # Create a new DataFrame for display
            display_df = pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])
            
            # Copy Tanggal column
            display_df['Tanggal'] = df['Tanggal']
            
            # Combine Keterangan columns - use Keterangan2 if Keterangan1 is empty
            display_df['Keterangan'] = df['Keterangan1'].copy()
            mask = (df['Keterangan1'].isna() | (df['Keterangan1'] == '')) & (~df['Keterangan2'].isna())
            display_df.loc[mask, 'Keterangan'] = df.loc[mask, 'Keterangan2']
            
            # Copy numeric columns
            display_df['Debet'] = pd.to_numeric(df['Debet'], errors='coerce').fillna(0)
            display_df['Kredit'] = pd.to_numeric(df['Kredit'], errors='coerce').fillna(0)
            
            return display_df
            
        except Exception as e:
            print(f"Error loading jurnal_penutup.csv: {e}")
            # If there's an error, return an empty DataFrame
            return pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])
    else:
        # If file doesn't exist, return an empty DataFrame
        return pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])

def save_jurnal_penutup_data(df):
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_penutup.csv')
    
    # Check if the original file exists to preserve its structure
    if os.path.exists(csv_path):
        try:
            # Read the original file to get its structure
            original_df = pd.read_csv(csv_path)
            
            # Create a new DataFrame with the original structure
            save_df = pd.DataFrame(columns=original_df.columns)
            
            # Map the display columns to the original structure
            if 'Tanggal' in df.columns:
                save_df['Tanggal'] = df['Tanggal']
            
            # Handle Keterangan columns based on the original structure
            if 'Keterangan ' in save_df.columns and 'Keterangan' in save_df.columns:
                # For rows where we have data in the second Keterangan column in the original
                # (last two rows in the example), keep that structure
                for idx, row in df.iterrows():
                    if idx >= len(original_df):
                        # For new rows, put Keterangan in the appropriate column
                        if idx >= len(save_df):
                            new_row = pd.Series(index=save_df.columns)
                            new_row['Tanggal'] = row['Tanggal']
                            new_row['Debet'] = row['Debet']
                            new_row['Kredit'] = row['Kredit']
                            
                            # Determine which Keterangan column to use based on pattern
                            if "Penutupan" in str(row['Keterangan']) or "Ikhtisar" in str(row['Keterangan']):
                                new_row['Keterangan'] = ""
                                new_row['Keterangan '] = ""
                                new_row['Keterangan'] = row['Keterangan']
                            else:
                                new_row['Keterangan '] = row['Keterangan']
                                new_row['Keterangan'] = ""
                            
                            save_df = pd.concat([save_df, pd.DataFrame([new_row])], ignore_index=True)
                    else:
                        # For existing rows, maintain the original structure
                        save_df.at[idx, 'Tanggal'] = row['Tanggal']
                        save_df.at[idx, 'Debet'] = row['Debet']
                        save_df.at[idx, 'Kredit'] = row['Kredit']
                        
                        # Keep the original Keterangan distribution
                        if pd.notna(original_df.at[idx, 'Keterangan ']):
                            save_df.at[idx, 'Keterangan '] = row['Keterangan']
                        elif pd.notna(original_df.at[idx, 'Keterangan']):
                            save_df.at[idx, 'Keterangan'] = row['Keterangan']
            else:
                # If the original structure is different, just use the first Keterangan column
                if 'Keterangan' in df.columns:
                    if 'Keterangan ' in save_df.columns:
                        save_df['Keterangan '] = df['Keterangan']
                    elif 'Keterangan' in save_df.columns:
                        save_df['Keterangan'] = df['Keterangan']
            
            # Copy numeric columns
            if 'Debet' in df.columns:
                save_df['Debet'] = pd.to_numeric(df['Debet'], errors='coerce').fillna(0)
            
            if 'Kredit' in df.columns:
                save_df['Kredit'] = pd.to_numeric(df['Kredit'], errors='coerce').fillna(0)
            
            # Save to CSV with the original structure
            save_df.to_csv(csv_path, index=False)
            
        except Exception as e:
            print(f"Error preserving original structure: {e}")
            # Fallback to simple save if there's an error
            simple_save(df, csv_path)
    else:
        # If the original file doesn't exist, use a simple save
        simple_save(df, csv_path)

def simple_save(df, csv_path):
    """Fallback function for simple CSV save"""
    # Create a basic structure
    save_df = pd.DataFrame(columns=['Tanggal', 'Keterangan ', 'Debet', 'Kredit', 'Unnamed: 4', 'Keterangan'])
    
    # Copy data
    save_df['Tanggal'] = df['Tanggal']
    save_df['Keterangan '] = df['Keterangan']
    save_df['Debet'] = df['Debet']
    save_df['Kredit'] = df['Kredit']
    
    # Save to CSV
    save_df.to_csv(csv_path, index=False)


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
            
        else:
            
            st.warning("Data jurnal penutup tidak tersedia.")
            st.info("Path file yang diharapkan: database/jurnal_penutup.csv")
            
            
            st.markdown("---")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.info("Pastikan format file CSV sesuai (Tanggal, Keterangan, Debet, Kredit)")
        
        
        st.markdown("---")