import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Admin Guru - UPT SMPN 1 Watang Pulu",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS UNTUK TAMPILAN MENARIK ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        text-shadow: 2px 2px 4px #cccccc;
    }
    h2, h3 {
        color: #e67e22;
    }
    .success-box {
        padding: 10px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- JUDUL APLIKASI ---
st.markdown("<h1>🏫 UPT SMP NEGERI 1 WATANG PULU</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>Sistem Administrasi Guru Terpadu</h3>", unsafe_allow_html=True)
st.write("---")

# --- INISIALISASI SESSION STATE (DATABASE SEMENTARA) ---
if 'data_guru' not in st.session_state:
    st.session_state['data_guru'] = {'Nama': '', 'NIP': '', 'Mapel': ''}
if 'kelas_list' not in st.session_state:
    st.session_state['kelas_list'] = [] # List nama kelas
if 'siswa_data' not in st.session_state:
    st.session_state['siswa_data'] = {} # Dictionary {nama_kelas: dataframe_siswa}
if 'jurnal_guru' not in st.session_state:
    st.session_state['jurnal_guru'] = pd.DataFrame(columns=['Tanggal', 'Kelas', 'Tujuan Pembelajaran', 'Keterangan'])

# --- SIDEBAR MENU ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429149.png", width=100)
    st.title("Menu Navigasi")
    menu = st.radio("Pilih Menu:", 
        ["🏠 Beranda & Identitas", 
         "👨‍🎓 Data Siswa & Kelas", 
         "📘 Jurnal Guru", 
         "📅 Presensi Siswa", 
         "📝 Daftar Nilai", 
         "🖨️ Cetak / Export"])

# --- FUNGSI BANTUAN ---
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# ==========================================
# 1. BERANDA & IDENTITAS
# ==========================================
if menu == "🏠 Beranda & Identitas":
    st.header("👤 Identitas Guru")
    
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap Guru", st.session_state['data_guru']['Nama'])
        nip = st.text_input("NIP / NUPTK", st.session_state['data_guru']['NIP'])
    with col2:
        mapel = st.text_input("Mata Pelajaran", st.session_state['data_guru']['Mapel'])
        tahun = st.text_input("Tahun Ajaran", "2023/2024")
    
    if st.button("Simpan Identitas"):
        st.session_state['data_guru'] = {'Nama': nama, 'NIP': nip, 'Mapel': mapel}
        st.toast('Identitas berhasil disimpan!', icon='✅')
        st.success(f"Selamat Datang, Bapak/Ibu {nama} di Aplikasi Admin Guru.")

# ==========================================
# 2. DATA SISWA & KELAS
# ==========================================
elif menu == "👨‍🎓 Data Siswa & Kelas":
    st.header("📂 Manajemen Kelas dan Siswa")
    
    # Tambah Kelas
    col_k1, col_k2 = st.columns([3, 1])
    with col_k1:
        new_class = st.text_input("Tambah Nama Kelas Baru (Contoh: 7A, 8B)")
    with col_k2:
        st.write("") # Spacer
        st.write("")
        if st.button("➕ Tambah Kelas"):
            if new_class and new_class not in st.session_state['kelas_list']:
                st.session_state['kelas_list'].append(new_class)
                # Init empty dataframe for this class
                columns_siswa = ['Nama Siswa']
                st.session_state['siswa_data'][new_class] = pd.DataFrame(columns=columns_siswa)
                st.toast(f"Kelas {new_class} berhasil dibuat!", icon='✅')
            else:
                st.warning("Nama kelas kosong atau sudah ada.")

    # Pilih Kelas
    if st.session_state['kelas_list']:
        selected_class = st.selectbox("Pilih Kelas untuk Dikelola:", st.session_state['kelas_list'])
        
        st.info(f"Mengelola Siswa untuk Kelas: **{selected_class}** (Maksimal 35 Siswa)")
        
        current_df = st.session_state['siswa_data'][selected_class]
        
        tab1, tab2 = st.tabs(["📝 Input Manual", "📤 Import Excel"])
        
        with tab1:
            nama_siswa_baru = st.text_input("Nama Siswa Baru")
            if st.button("Simpan Siswa"):
                if len(current_df) < 35:
                    if nama_siswa_baru:
                        new_row = pd.DataFrame({'Nama Siswa': [nama_siswa_baru]})
                        st.session_state['siswa_data'][selected_class] = pd.concat([current_df, new_row], ignore_index=True)
                        st.toast("Siswa berhasil ditambahkan!", icon='✅')
                        st.rerun()
                else:
                    st.error("Kuota kelas penuh (Maksimal 35 siswa).")
        
        with tab2:
            st.write("Upload file Excel dengan kolom bernama 'Nama'")
            uploaded_file = st.file_uploader("Upload Excel", type=['xlsx'])
            if uploaded_file:
                try:
                    df_upload = pd.read_excel(uploaded_file)
                    if 'Nama' in df_upload.columns:
                        names = df_upload['Nama'].tolist()
                        # Limit to remaining slots
                        remaining_slots = 35 - len(current_df)
                        names_to_add = names[:remaining_slots]
                        
                        if len(names) > remaining_slots:
                            st.warning(f"Hanya {remaining_slots} siswa pertama yang diimpor karena batas 35.")
                            
                        new_rows = pd.DataFrame({'Nama Siswa': names_to_add})
                        st.session_state['siswa_data'][selected_class] = pd.concat([current_df, new_rows], ignore_index=True)
                        st.success(f"Berhasil import {len(names_to_add)} siswa!")
                    else:
                        st.error("File Excel harus memiliki header kolom 'Nama'")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Tampilkan Data Siswa
        st.write("### Daftar Siswa")
        st.dataframe(st.session_state['siswa_data'][selected_class], use_container_width=True)
        st.caption(f"Total Siswa: {len(st.session_state['siswa_data'][selected_class])}")

    else:
        st.warning("Belum ada kelas. Silahkan tambah kelas terlebih dahulu.")

# ==========================================
# 3. JURNAL GURU
# ==========================================
elif menu == "📘 Jurnal Guru":
    st.header("📘 Jurnal Mengajar Harian")
    
    with st.form("form_jurnal"):
        col1, col2 = st.columns(2)
        with col1:
            tgl = st.date_input("Tanggal", datetime.date.today())
            kelas_jurnal = st.selectbox("Kelas", st.session_state['kelas_list']) if st.session_state['kelas_list'] else st.text_input("Kelas (Manual)")
        with col2:
            tujuan = st.text_area("Tujuan Pembelajaran")
            ket = st.text_input("Keterangan (Catatan Khusus)")
        
        submit_jurnal = st.form_submit_button("Simpan Jurnal")
        
        if submit_jurnal:
            new_jurnal = pd.DataFrame({
                'Tanggal': [tgl],
                'Kelas': [kelas_jurnal],
                'Tujuan Pembelajaran': [tujuan],
                'Keterangan': [ket]
            })
            st.session_state['jurnal_guru'] = pd.concat([st.session_state['jurnal_guru'], new_jurnal], ignore_index=True)
            st.toast("Jurnal tersimpan!", icon='✅')

    st.write("### Rekap Jurnal")
    # Tampilkan tabel jurnal dengan index dimulai dari 1
    df_show = st.session_state['jurnal_guru'].reset_index(drop=True)
    df_show.index = df_show.index + 1
    st.dataframe(df_show, use_container_width=True)

# ==========================================
# 4. PRESENSI SISWA
# ==========================================
elif menu == "📅 Presensi Siswa":
    st.header("📅 Daftar Hadir Siswa (20 Pertemuan)")
    
    if st.session_state['kelas_list']:
        selected_class_abs = st.selectbox("Pilih Kelas:", st.session_state['kelas_list'], key='presensi_kelas')
        
        # Ambil data siswa
        df_siswa = st.session_state['siswa_data'][selected_class_abs]
        
        if not df_siswa.empty:
            # Setup struktur Dataframe Presensi jika belum ada
            key_presensi = f"presensi_{selected_class_abs}"
            
            # Kolom pertemuan 1-20
            cols_pertemuan = [f'P{i}' for i in range(1, 21)]
            
            if key_presensi not in st.session_state:
                # Gabungkan nama siswa dengan kolom kosong
                df_pres = df_siswa.copy()
                for c in cols_pertemuan:
                    df_pres[c] = False # Checkbox boolean
                
                # Kolom rekap
                df_pres['Sakit'] = 0
                df_pres['Izin'] = 0
                df_pres['Alpa'] = 0
                
                st.session_state[key_presensi] = df_pres
            else:
                # Update jika ada siswa baru (sinkronisasi)
                current_pres = st.session_state[key_presensi]
                if len(current_pres) != len(df_siswa):
                    # Reset sederhana untuk demo (idealnnya merge)
                    st.warning("Terdeteksi perubahan jumlah siswa. Harap reset data presensi jika nama tidak sesuai.")
            
            st.info("Centang kotak jika siswa HADIR. Untuk S/I/A, isi manual di kolom kanan.")
            
            # Data Editor memungkinkan edit langsung seperti Excel
            edited_df = st.data_editor(
                st.session_state[key_presensi],
                column_config={
                    "Nama Siswa": st.column_config.TextColumn("Nama", disabled=True),
                },
                hide_index=True,
                use_container_width=True
            )
            
            if st.button("Simpan Data Presensi"):
                st.session_state[key_presensi] = edited_df
                st.toast("Data kehadiran berhasil disimpan!", icon='💾')
        else:
            st.warning("Belum ada data siswa di kelas ini.")
    else:
        st.warning("Buat kelas terlebih dahulu.")

# ==========================================
# 5. DAFTAR NILAI
# ==========================================
elif menu == "📝 Daftar Nilai":
    st.header("📝 Rekap Nilai Siswa")
    st.markdown("**(5 Tugas, 3 UH, 1 STS, 1 SAS)**")
    
    if st.session_state['kelas_list']:
        selected_class_nilai = st.selectbox("Pilih Kelas:", st.session_state['kelas_list'], key='nilai_kelas')
        df_siswa = st.session_state['siswa_data'][selected_class_nilai]
        
        if not df_siswa.empty:
            key_nilai = f"nilai_{selected_class_nilai}"
            
            # Definisi Kolom
            cols_tugas = [f'T{i}' for i in range(1, 6)]
            cols_uh = [f'UH{i}' for i in range(1, 4)]
            cols_ujian = ['STS', 'SAS']
            all_score_cols = cols_tugas + cols_uh + cols_ujian
            
            if key_nilai not in st.session_state:
                df_nilai = df_siswa.copy()
                for c in all_score_cols:
                    df_nilai[c] = 0 # Default nilai 0
                st.session_state[key_nilai] = df_nilai
            
            # Edit Nilai
            st.write("Silahkan input nilai (0-100):")
            edited_nilai = st.data_editor(
                st.session_state[key_nilai],
                column_config={
                    "Nama Siswa": st.column_config.TextColumn("Nama", disabled=True),
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Hitung Nilai Akhir Otomatis
            if st.button("Hitung & Simpan Nilai"):
                # Konversi ke numerik
                for col in all_score_cols:
                    edited_nilai[col] = pd.to_numeric(edited_nilai[col], errors='coerce').fillna(0)
                
                # Rumus Rata-rata (Bisa disesuaikan)
                # Misal: Rata2 Tugas + Rata2 UH + STS + SAS dibagi 4 komponen
                avg_tugas = edited_nilai[cols_tugas].mean(axis=1)
                avg_uh = edited_nilai[cols_uh].mean(axis=1)
                
                # Nilai Akhir = (Rata Tugas + Rata UH + STS + SAS) / 4 
                # (Ini hanya contoh rumus sederhana)
                edited_nilai['Nilai Akhir'] = (avg_tugas + avg_uh + edited_nilai['STS'] + edited_nilai['SAS']) / 4
                edited_nilai['Nilai Akhir'] = edited_nilai['Nilai Akhir'].round(2)
                
                st.session_state[key_nilai] = edited_nilai
                st.toast("Nilai berhasil dihitung dan disimpan!", icon='✅')
                st.dataframe(edited_nilai[['Nama Siswa', 'Nilai Akhir']].style.highlight_max(axis=0))
                
        else:
             st.warning("Belum ada siswa.")
    else:
        st.warning("Buat kelas dulu.")

# ==========================================
# 6. CETAK / EXPORT
# ==========================================
elif menu == "🖨️ Cetak / Export":
    st.header("🖨️ Cetak Laporan Akhir Semester")
    st.write("Download data dalam format Excel untuk dicetak.")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    
    # 1. Export Jurnal
    with col_c1:
        st.subheader("1. Jurnal Guru")
        if not st.session_state['jurnal_guru'].empty:
            excel_jurnal = convert_df_to_excel(st.session_state['jurnal_guru'])
            st.download_button(
                label="📥 Download Jurnal (.xlsx)",
                data=excel_jurnal,
                file_name='Jurnal_Guru_UPT_SMPN1.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            st.info("Data Jurnal Kosong")

    # 2. Export Nilai & Presensi per Kelas
    with col_c2:
        st.subheader("2. Laporan Per Kelas")
        if st.session_state['kelas_list']:
            cls_print = st.selectbox("Pilih Kelas Laporan:", st.session_state['kelas_list'], key='print_cls')
            
            # Siapkan Data Presensi
            key_pres = f"presensi_{cls_print}"
            data_pres = st.session_state.get(key_pres, pd.DataFrame())
            
            # Siapkan Data Nilai
            key_nil = f"nilai_{cls_print}"
            data_nil = st.session_state.get(key_nil, pd.DataFrame())
            
            if not data_pres.empty:
                excel_pres = convert_df_to_excel(data_pres)
                st.download_button(
                    label=f"📥 Presensi Kelas {cls_print}",
                    data=excel_pres,
                    file_name=f'Presensi_{cls_print}.xlsx'
                )
            
            if not data_nil.empty:
                excel_nil = convert_df_to_excel(data_nil)
                st.download_button(
                    label=f"📥 Nilai Kelas {cls_print}",
                    data=excel_nil,
                    file_name=f'Nilai_{cls_print}.xlsx'
                )
        else:
            st.info("Belum ada kelas.")

    with col_c3:
        st.subheader("3. Backup Data")
        st.write("Pastikan mengunduh semua data sebelum menutup browser, karena data akan hilang jika tab ditutup (Mode Demo).")

# --- FOOTER ---
st.write("---")
st.markdown("<p style='text-align: center; color: grey;'>© 2024 UPT SMP Negeri 1 Watang Pulu | Dikembangkan untuk Administrasi Guru</p>", unsafe_allow_html=True)