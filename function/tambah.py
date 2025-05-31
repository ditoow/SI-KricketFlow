import streamlit as st
import pandas as pd
import os
from datetime import datetime

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# ===== JURNAL UMUM =====
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

def add_jurnal_umum_data(tanggal, keterangan, debet, kredit):
    df = load_jurnal_umum_data()
    new_row = pd.DataFrame({'Tanggal': [tanggal], 'Keterangan': [keterangan], 'Debet': [debet], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_jurnal_umum_data(df)
    return df

# ===== BUKU BESAR =====
def get_bukubesar_dir():
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database', 'bukubesar')
    ensure_dir(database_dir)
    return database_dir

def get_filename_from_account(account):
    # Konversi nama akun ke format filename
    account = account.lower().replace(' ', '')
    
    # Khusus untuk beban
    if account.startswith('beban'):
        return f'bukbes_{account}.csv'
    
    return f'bukbes_{account}.csv'

def load_buku_besar_data(akun):
    database_dir = get_bukubesar_dir()
    
    filename = get_filename_from_account(akun)
    csv_path = os.path.join(database_dir, filename)
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=['Tanggal', 'Debet', 'Tanggal.1', 'Kredit'])

def save_buku_besar_data(df, akun):
    database_dir = get_bukubesar_dir()
    
    filename = get_filename_from_account(akun)
    csv_path = os.path.join(database_dir, filename)
    
    df.to_csv(csv_path, index=False)

def add_buku_besar_data(akun, tanggal, debet=0, kredit=0):
    df = load_buku_besar_data(akun)
    
    # Jika kolom tidak ada, tambahkan kolom yang diperlukan
    if 'Tanggal' not in df.columns:
        df['Tanggal'] = ""
    if 'Debet' not in df.columns:
        df['Debet'] = 0
    if 'Tanggal.1' not in df.columns:
        df['Tanggal.1'] = ""
    if 'Kredit' not in df.columns:
        df['Kredit'] = 0
    
    # Tentukan kolom tanggal untuk kredit
    tanggal_kredit_col = 'Tanggal.1'
    
    # Buat baris baru
    new_row = {}
    
    if debet > 0:
        new_row = {
            'Tanggal': tanggal,
            'Debet': debet,
            tanggal_kredit_col: "",
            'Kredit': 0
        }
    elif kredit > 0:
        new_row = {
            'Tanggal': "",
            'Debet': 0,
            tanggal_kredit_col: tanggal,
            'Kredit': kredit
        }
    
    # Tambahkan baris baru ke DataFrame
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Simpan perubahan
    save_buku_besar_data(df, akun)
    return df

# ===== NERACA SALDO =====
def load_neraca_saldo_data():
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo.csv')
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])

def save_neraca_saldo_data(df):
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'neraca_saldo.csv')
    df.to_csv(csv_path, index=False)

def update_neraca_saldo(akun, debet=0, kredit=0):
    df = load_neraca_saldo_data()
    
    # Cek apakah akun sudah ada di neraca saldo
    akun_exists = False
    for idx, row in df.iterrows():
        if row['Nama Akun'] == akun:
            akun_exists = True
            # Update nilai debet/kredit
            if debet > 0:
                current_debet = pd.to_numeric(df.at[idx, 'Debet'], errors='coerce')
                if pd.isna(current_debet):
                    current_debet = 0
                df.at[idx, 'Debet'] = float(current_debet) + debet
            if kredit > 0:
                current_kredit = pd.to_numeric(df.at[idx, 'Kredit'], errors='coerce')
                if pd.isna(current_kredit):
                    current_kredit = 0
                df.at[idx, 'Kredit'] = float(current_kredit) + kredit
            break
    
    # Jika akun belum ada, tambahkan baris baru
    if not akun_exists:
        new_row = {'Nama Akun': akun, 'Debet': debet, 'Kredit': kredit}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Simpan perubahan
    save_neraca_saldo_data(df)
    return df

# ===== NERACA LAJUR =====
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

def update_neraca_lajur(akun, debet=0, kredit=0):
    df = load_neraca_lajur_data()
    
    # Tentukan jenis akun untuk menentukan kolom yang akan diupdate
    jenis_akun = get_jenis_akun(akun)
    
    # Cek apakah akun sudah ada di neraca lajur
    akun_exists = False
    for idx, row in df.iterrows():
        if row['Nama Akun'] == akun:
            akun_exists = True
            # Update nilai neraca saldo
            if debet > 0:
                current_debet = pd.to_numeric(df.at[idx, 'Neraca Saldo Debet'], errors='coerce')
                if pd.isna(current_debet):
                    current_debet = 0
                df.at[idx, 'Neraca Saldo Debet'] = float(current_debet) + debet
            if kredit > 0:
                current_kredit = pd.to_numeric(df.at[idx, 'Neraca Saldo Kredit'], errors='coerce')
                if pd.isna(current_kredit):
                    current_kredit = 0
                df.at[idx, 'Neraca Saldo Kredit'] = float(current_kredit) + kredit
            
            # Update nilai laba rugi atau neraca berdasarkan jenis akun
            if jenis_akun == 'laba_rugi':
                if debet > 0:
                    current_lr_debet = pd.to_numeric(df.at[idx, 'Laba Rugi Debet'], errors='coerce')
                    if pd.isna(current_lr_debet):
                        current_lr_debet = 0
                    df.at[idx, 'Laba Rugi Debet'] = float(current_lr_debet) + debet
                if kredit > 0:
                    current_lr_kredit = pd.to_numeric(df.at[idx, 'Laba Rugi Kredit'], errors='coerce')
                    if pd.isna(current_lr_kredit):
                        current_lr_kredit = 0
                    df.at[idx, 'Laba Rugi Kredit'] = float(current_lr_kredit) + kredit
            elif jenis_akun == 'neraca':
                if debet > 0:
                    current_n_debet = pd.to_numeric(df.at[idx, 'Neraca Debet'], errors='coerce')
                    if pd.isna(current_n_debet):
                        current_n_debet = 0
                    df.at[idx, 'Neraca Debet'] = float(current_n_debet) + debet
                if kredit > 0:
                    current_n_kredit = pd.to_numeric(df.at[idx, 'Neraca Kredit'], errors='coerce')
                    if pd.isna(current_n_kredit):
                        current_n_kredit = 0
                    df.at[idx, 'Neraca Kredit'] = float(current_n_kredit) + kredit
            break
    
    # Jika akun belum ada, tambahkan baris baru
    if not akun_exists:
        new_row = {
            'Nama Akun': akun, 
            'Neraca Saldo Debet': debet, 
            'Neraca Saldo Kredit': kredit,
            'Laba Rugi Debet': debet if jenis_akun == 'laba_rugi' else 0,
            'Laba Rugi Kredit': kredit if jenis_akun == 'laba_rugi' else 0,
            'Neraca Debet': debet if jenis_akun == 'neraca' else 0,
            'Neraca Kredit': kredit if jenis_akun == 'neraca' else 0
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Simpan perubahan
    save_neraca_lajur_data(df)
    return df

# ===== JURNAL PENUTUP =====
def load_jurnal_penutup_data():
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_penutup.csv')
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=['Tanggal', 'Keterangan', 'Debet', 'Kredit'])

def save_jurnal_penutup_data(df):
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_penutup.csv')
    df.to_csv(csv_path, index=False)

def add_jurnal_penutup_data(tanggal, keterangan, debet, kredit):
    df = load_jurnal_penutup_data()
    new_row = pd.DataFrame({'Tanggal': [tanggal], 'Keterangan': [keterangan], 'Debet': [debet], 'Kredit': [kredit]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_jurnal_penutup_data(df)
    return df

# ===== JURNAL SALDO SETELAH PENUTUPAN =====
def load_jurnal_saldo_setelah_penutupan_data():
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_saldo_setelah_penutupan.csv')
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=['Nama Akun', 'Debet', 'Kredit'])

def save_jurnal_saldo_setelah_penutupan_data(df):
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    ensure_dir(database_dir)
    
    csv_path = os.path.join(database_dir, 'jurnal_saldo_setelah_penutupan.csv')
    df.to_csv(csv_path, index=False)

def update_jurnal_saldo_setelah_penutupan(akun, debet=0, kredit=0):
    # Hanya akun neraca yang masuk ke jurnal saldo setelah penutupan
    if get_jenis_akun(akun) != 'neraca':
        return None
    
    df = load_jurnal_saldo_setelah_penutupan_data()
    
    # Cek apakah akun sudah ada
    akun_exists = False
    for idx, row in df.iterrows():
        if row['Nama Akun'] == akun:
            akun_exists = True
            # Update nilai debet/kredit
            if debet > 0:
                current_debet = pd.to_numeric(df.at[idx, 'Debet'], errors='coerce')
                if pd.isna(current_debet):
                    current_debet = 0
                df.at[idx, 'Debet'] = float(current_debet) + debet
            if kredit > 0:
                current_kredit = pd.to_numeric(df.at[idx, 'Kredit'], errors='coerce')
                if pd.isna(current_kredit):
                    current_kredit = 0
                df.at[idx, 'Kredit'] = float(current_kredit) + kredit
            break
    
    # Jika akun belum ada, tambahkan baris baru
    if not akun_exists:
        new_row = {'Nama Akun': akun, 'Debet': debet, 'Kredit': kredit}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Simpan perubahan
    save_jurnal_saldo_setelah_penutupan_data(df)
    return df

# ===== FUNGSI UTILITAS =====
def get_jenis_akun(akun):
    """
    Menentukan jenis akun (neraca atau laba rugi)
    """
    akun = akun.lower()
    
    # Akun-akun neraca
    if any(item in akun for item in ['kas', 'perlengkapan', 'peralatan', 'utang', 'modal']):
        return 'neraca'
    
    # Akun-akun laba rugi
    elif any(item in akun for item in ['penjualan', 'pembelian', 'beban', 'ikhtisar laba rugi']):
        return 'laba_rugi'
    
    # Default
    return 'neraca'

def normalize_account_name(akun):
    """
    Normalisasi nama akun untuk penyimpanan file
    """
    akun = akun.lower()
    
    # Mapping untuk nama akun
    mapping = {
        'kas': 'kas',
        'perlengkapan': 'perlengkapan',
        'peralatan': 'peralatan',
        'utang bank': 'utangbank',
        'modal': 'modal',
        'penjualan': 'penjualan',
        'pembelian': 'pembelian',
        'beban gaji': 'bebangaji',
        'beban pengiriman': 'bebanpengiriman',
        'beban pemeliharaan': 'bebanpemeliharaan',
        'beban sewa': 'bebansewa',
        'beban bunga': 'bebanbunga',
        'ikhtisar laba rugi': 'ikhtisarlabarugi'
    }
    
    return mapping.get(akun, akun.replace(' ', ''))

# ===== FUNGSI UTAMA =====
def check_file_exists(file_path):
    """
    Memeriksa apakah file sudah ada
    """
    return os.path.exists(file_path)

def add_transaksi_to_all(tanggal, keterangan, akun_debet, nilai_debet, akun_kredit, nilai_kredit):
    """
    Menambahkan transaksi ke semua laporan keuangan yang sudah ada
    """
    tanggal_str = tanggal.strftime('%d/%m/%Y')
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    database_dir = os.path.join(project_root, 'database')
    
    # Daftar file yang akan diperbarui
    updated_files = []
    
    # 1. Tambahkan ke Jurnal Umum jika file sudah ada
    jurnal_umum_path = os.path.join(database_dir, 'jurnal_umum.csv')
    if check_file_exists(jurnal_umum_path):
        if nilai_debet > 0:
            # Gunakan akun sebagai keterangan jika keterangan kosong, atau gabungkan keduanya tanpa tanda "-"
            desc = akun_debet if not keterangan.strip() else f"{akun_debet} {keterangan}"
            add_jurnal_umum_data(tanggal_str, desc, nilai_debet, 0)
        if nilai_kredit > 0:
            # Gunakan akun sebagai keterangan jika keterangan kosong, atau gabungkan keduanya tanpa tanda "-"
            desc = akun_kredit if not keterangan.strip() else f"{akun_kredit} {keterangan}"
            add_jurnal_umum_data(tanggal_str, desc, 0, nilai_kredit)
        updated_files.append("Jurnal Umum")
    
    # 2. Tambahkan ke Buku Besar jika direktori dan file sudah ada
    bukubesar_dir = os.path.join(database_dir, 'bukubesar')
    if os.path.exists(bukubesar_dir):
        debet_file_path = os.path.join(bukubesar_dir, f"bukbes_{normalize_account_name(akun_debet)}.csv")
        kredit_file_path = os.path.join(bukubesar_dir, f"bukbes_{normalize_account_name(akun_kredit)}.csv")
        
        buku_besar_updated = False
        if nilai_debet > 0 and check_file_exists(debet_file_path):
            add_buku_besar_data(normalize_account_name(akun_debet), tanggal_str, debet=nilai_debet)
            buku_besar_updated = True
        
        if nilai_kredit > 0 and check_file_exists(kredit_file_path):
            add_buku_besar_data(normalize_account_name(akun_kredit), tanggal_str, kredit=nilai_kredit)
            buku_besar_updated = True
        
        if buku_besar_updated:
            updated_files.append("Buku Besar")
    
    # 3. Update Neraca Saldo jika file sudah ada
    neraca_saldo_path = os.path.join(database_dir, 'neraca_saldo.csv')
    if check_file_exists(neraca_saldo_path):
        if nilai_debet > 0:
            update_neraca_saldo(akun_debet, debet=nilai_debet)
        if nilai_kredit > 0:
            update_neraca_saldo(akun_kredit, kredit=nilai_kredit)
        updated_files.append("Neraca Saldo")
    
    # 4. Update Neraca Lajur jika file sudah ada
    neraca_lajur_path = os.path.join(database_dir, 'neraca_lajur.csv')
    if check_file_exists(neraca_lajur_path):
        if nilai_debet > 0:
            update_neraca_lajur(akun_debet, debet=nilai_debet)
        if nilai_kredit > 0:
            update_neraca_lajur(akun_kredit, kredit=nilai_kredit)
        updated_files.append("Neraca Lajur")
    
    # 5. Update Jurnal Penutup jika file sudah ada
    jurnal_penutup_path = os.path.join(database_dir, 'jurnal_penutup.csv')
    if check_file_exists(jurnal_penutup_path):
        jurnal_penutup_updated = False
        
        if get_jenis_akun(akun_debet) == 'laba_rugi' and nilai_debet > 0:
            add_jurnal_penutup_data(tanggal_str, f"Penutupan {akun_debet}", 0, nilai_debet)
            add_jurnal_penutup_data(tanggal_str, "Ikhtisar Laba Rugi", nilai_debet, 0)
            jurnal_penutup_updated = True
        
        if get_jenis_akun(akun_kredit) == 'laba_rugi' and nilai_kredit > 0:
            add_jurnal_penutup_data(tanggal_str, f"Penutupan {akun_kredit}", nilai_kredit, 0)
            add_jurnal_penutup_data(tanggal_str, "Ikhtisar Laba Rugi", 0, nilai_kredit)
            jurnal_penutup_updated = True
        
        if jurnal_penutup_updated:
            updated_files.append("Jurnal Penutup")
    
    # 6. Update Jurnal Saldo Setelah Penutupan jika file sudah ada
    jurnal_saldo_path = os.path.join(database_dir, 'jurnal_saldo_setelah_penutupan.csv')
    if check_file_exists(jurnal_saldo_path):
        jurnal_saldo_updated = False
        
        if get_jenis_akun(akun_debet) == 'neraca' and nilai_debet > 0:
            update_jurnal_saldo_setelah_penutupan(akun_debet, debet=nilai_debet)
            jurnal_saldo_updated = True
        
        if get_jenis_akun(akun_kredit) == 'neraca' and nilai_kredit > 0:
            update_jurnal_saldo_setelah_penutupan(akun_kredit, kredit=nilai_kredit)
            jurnal_saldo_updated = True
        
        if jurnal_saldo_updated:
            updated_files.append("Jurnal Saldo Setelah Penutupan")
    
    return updated_files

def show_tambah_transaksi():
    st.header("Tambah Transaksi")
    
    st.write("Gunakan form ini untuk menambahkan transaksi baru ke semua laporan keuangan.")
    
    with st.form("tambah_transaksi_form"):
        tanggal = st.date_input("Tanggal", value=datetime.now())
        keterangan = st.text_input("Keterangan Transaksi")
        
        st.subheader("Detail Akun")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Debet**")
            akun_debet = st.selectbox(
                "Pilih Akun (Debet)",
                options=[
                    "Kas", 
                    "Perlengkapan", 
                    "Peralatan", 
                    "Utang Bank", 
                    "Modal", 
                    "Penjualan", 
                    "Pembelian", 
                    "Beban Gaji", 
                    "Beban Pengiriman", 
                    "Beban Pemeliharaan", 
                    "Beban Sewa", 
                    "Beban Bunga", 
                    "Ikhtisar Laba Rugi"
                ]
            )
            nilai_debet = st.number_input("Nilai Debet (Rp)", min_value=0.0, format="%f")
        
        with col2:
            st.write("**Kredit**")
            akun_kredit = st.selectbox(
                "Pilih Akun (Kredit)",
                options=[
                    "Kas", 
                    "Perlengkapan", 
                    "Peralatan", 
                    "Utang Bank", 
                    "Modal", 
                    "Penjualan", 
                    "Pembelian", 
                    "Beban Gaji", 
                    "Beban Pengiriman", 
                    "Beban Pemeliharaan", 
                    "Beban Sewa", 
                    "Beban Bunga", 
                    "Ikhtisar Laba Rugi"
                ]
            )
            nilai_kredit = st.number_input("Nilai Kredit (Rp)", min_value=0.0, format="%f")
        
        # Tidak perlu validasi keseimbangan debet dan kredit
        
        submitted = st.form_submit_button("Simpan Transaksi")
        
        if submitted:
            if nilai_debet == 0 and nilai_kredit == 0:
                st.error("Nilai debet atau kredit harus lebih dari 0.")
            else:
                # Tambahkan transaksi ke laporan keuangan yang ada
                updated_files = add_transaksi_to_all(tanggal, keterangan, akun_debet, nilai_debet, akun_kredit, nilai_kredit)
                
                if updated_files:
                    st.success("Transaksi berhasil ditambahkan ke laporan keuangan yang tersedia!")
                    
                    # Tampilkan ringkasan transaksi
                    st.subheader("Ringkasan Transaksi")
                    
                    st.write(f"**Tanggal:** {tanggal.strftime('%d/%m/%Y')}")
                    st.write(f"**Keterangan:** {keterangan}")
                    
                    if nilai_debet > 0:
                        st.write(f"**Debet:** {akun_debet} - Rp {nilai_debet:,.2f}".replace(',', '.'))
                    
                    if nilai_kredit > 0:
                        st.write(f"**Kredit:** {akun_kredit} - Rp {nilai_kredit:,.2f}".replace(',', '.'))
                    
                    # Tampilkan informasi tentang laporan yang diperbarui
                    st.subheader("Laporan yang Diperbarui")
                    for file in updated_files:
                        st.write(f"✅ {file}")
                else:
                    st.warning("Tidak ada laporan keuangan yang tersedia untuk diperbarui. Silakan buat laporan terlebih dahulu.")