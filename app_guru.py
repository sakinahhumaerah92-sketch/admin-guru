import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# --- 1. KONFIGURASI HALAMAN & CSS ---
st.set_page_config(
    page_title="Admin Guru - UPT SMPN 1 Watang Pulu",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan Warna-warni dan Menarik
st.markdown("""
    <style>
    /* Background utama */
    .stApp {
        background-color: #f4f7f6;
    }
    /* Header Style */
    h1 {
        color: #1e3799;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        text-transform: uppercase;
        font-weight: 800;
        text-shadow: 2px 2px 0px #a4b0be;
    }
    h2 {
        color: #e58e26;
        border-bottom: 2px solid #e58e26;
        padding-bottom: 10px;
    }
    h3 {
        color: #0c2461;
    }
    /* Tombol */
    .stButton>button {
        background-color: #38ada9;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #079992;
        transform: scale(1.02);
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dcdde1;
    }
    /* Kotak Info */
    .info-box {
        padding: 15px;
        background-color: #dff9fb;
        border-left: 5px solid #22a6b3;
        border-radius: 5px;
        color: #130f40;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INISIALISASI STATE (MEMORY SEMENTARA) ---
if 'data_guru' not in st.session_state:
    st.session_state['data_guru'] = {'Nama': '', 'NIP': '', 'Mapel': ''}
if 'kelas_list' not in st.session_state:
    st.session_state['kelas_list'] = [] 
if 'siswa_data' not in st.session_state:
    st.session_state['siswa_data'] = {} 
if 'jurnal_guru' not in st.session_state:
    st.session_state['jurnal_guru'] = pd.DataFrame(columns=['No', 'Tanggal', 'Kelas', 'Tujuan Pembelajaran', 'Keterangan'])

# --- 3. JUDUL ---
st.markdown("<h1>🏫 UPT SMP NEGERI 1 WATANG PULU</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #535c68;'>Aplikasi Administrasi Guru & Rekap Nilai Terpadu</p>", unsafe_allow_html=True)
st.divider()

# --- 4. SIDEBAR MENU ---
with st.sidebar:
    st.markdown("### 🧭 MENU UTAMA")
    menu = st.radio("", 
        ["🏠 Identitas Guru", 
         "👥 Data Siswa & Kelas", 
         "📘 Jurnal Mengajar", 
         "📅 Daftar Hadir", 
         "📊 Daftar Nilai", 
         "🖨️ Cetak Laporan"],
        index=0
    )
    st.markdown("---")
    st.caption("Developed for UPT SMPN 1 Watang Pulu")

# --- 5. LOGIKA MENU ---

# === MENU 1: IDENTITAS ===
if menu == "🏠 Identitas Guru":
    st.header("👤 Profil Pengajar")
    st.markdown('<div class="info-box">Silahkan lengkapi data diri Anda sebelum memulai administrasi.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap", st.session_state['data_guru']['Nama'])
        nip = st.text_input("NIP / NUPTK", st.session_state['data_guru']['NIP'])
    with col2:
        mapel = st.text_input("Mata Pelajaran", st.session_state['data_guru']['Mapel'])
        tahun = st.text_input("Tahun Pelajaran", "2024/2025")
    
    if st.button("💾 Simpan Identitas"):
        st.session_state['data_guru'] = {'Nama': nama, 'NIP': nip, 'Mapel': mapel}
        st.toast('Identitas berhasil disimpan!', icon='✅')

# === MENU 2: SISWA & KELAS ===
elif menu == "👥 Data Siswa & Kelas":
    st.header("📂 Kelola Kelas & Siswa")
    
    # --- Bagian A: Buat Kelas ---
    with st.expander("➕ Tambah Kelas Baru", expanded=False):
        c1, c2 = st.columns([3, 1])
        new_class = c1.text_input("Nama Kelas (Contoh: 7A)")
        if c2.button("Buat Kelas"):
            if new_class and new_class not in st.session_state['kelas_list']:
                st.session_state['kelas_list'].append(new_class)
                st.session_state['kelas_list'].sort()
                # Init empty dataframe
                st.session_state['siswa_data'][new_class] = pd.DataFrame(columns=['Nama Siswa'])
                st.toast(f"Kelas {new_class} berhasil dibuat!", icon='🎉')
                st.rerun()

    # --- Bagian B: Kelola Siswa ---
    if st.session_state['kelas_list']:
        selected_class = st.selectbox("Pilih Kelas untuk Diedit:", st.session_state['kelas_list'])
        df_current = st.session_state['siswa_data'][selected_class]
        
        st.info(f"Mengelola Kelas: **{selected_class}** | Jumlah Siswa: **{len(df_current)}/35**")

        tab_input, tab_import, tab_edit = st.tabs(["📝 Input Manual", "📤 Import Excel/CSV", "🗑️ Hapus/Edit Data"])

        # TAB 1: Input Manual
        with tab_input:
            nama_baru = st.text_input("Nama Siswa Baru:")
            if st.button("Tambahkan Siswa"):
                if len(df_current) < 35:
                    if nama_baru:
                        new_row = pd.DataFrame({'Nama Siswa': [nama_baru]})
                        st.session_state['siswa_data'][selected_class] = pd.concat([df_current, new_row], ignore_index=True)
                        st.toast("Siswa berhasil ditambahkan!", icon='✅')
                        st.rerun()
                else:
                    st.error("Gagal: Kelas sudah penuh (Maks 35 Siswa).")

        # TAB 2: Import
        with tab_import:
            st.markdown("Upload file **Excel** atau **CSV** yang memiliki header kolom **'Nama'**.")
            uploaded_file = st.file_uploader("Pilih File", type=['xlsx', 'csv'])
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df_upload = pd.read_csv(uploaded_file)
                    else:
                        df_upload = pd.read_excel(uploaded_file)
                    
                    if 'Nama' in df_upload.columns:
                        names = df_upload['Nama'].dropna().tolist()
                        sisa_slot = 35 - len(df_current)
                        
                        if sisa_slot > 0:
                            to_add = names[:sisa_slot]
                            new_rows = pd.DataFrame({'Nama Siswa': to_add})
                            st.session_state['siswa_data'][selected_class] = pd.concat([df_current, new_rows], ignore_index=True)
                            st.toast(f"Berhasil import {len(to_add)} siswa!", icon='✅')
                            if len(names) > sisa_slot:
                                st.warning(f"Hanya {sisa_slot} siswa yang masuk karena batas maksimal 35.")
                            st.rerun()
                        else:
                            st.error("Kelas sudah penuh.")
                    else:
                        st.error("Tidak ditemukan kolom 'Nama' pada file.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan file: {e}")

        # TAB 3: Edit / Hapus (Fitur Data Editor)
        with tab_edit:
            st.markdown("Anda dapat **mengedit nama** atau **menghapus siswa** (pilih baris lalu tekan tombol delete/hapus di keyboard atau gunakan fitur hapus bawaan tabel).")
            
            edited_df = st.data_editor(
                df_current,
                num_rows="dynamic", # Mengizinkan tambah/hapus baris langsung di tabel
                key=f"editor_{selected_class}",
                use_container_width=True
            )

            if st.button("Simpan Perubahan Data Siswa"):
                # Validasi Max 35 setelah edit
                if len(edited_df) <= 35:
                    st.session_state['siswa_data'][selected_class] = edited_df
                    st.toast("Data siswa diperbarui!", icon='💾')
                else:
                    st.error("Gagal simpan: Data melebihi 35 siswa. Hapus beberapa baris.")

    else:
        st.warning("Belum ada kelas. Silahkan buat kelas terlebih dahulu.")

# === MENU 3: JURNAL GURU ===
elif menu == "📘 Jurnal Mengajar":
    st.header("📘 Jurnal Harian Guru")
    
    with st.form("form_jurnal"):
        c1, c2, c3 = st.columns([1, 2, 2])
        tgl = c1.date_input("Tanggal", datetime.date.today())
        kls_jurnal = c2.selectbox("Kelas", st.session_state['kelas_list']) if st.session_state['kelas_list'] else c2.text_input("Kelas (Manual)")
        tujuan = c3.text_area("Tujuan Pembelajaran")
        ket = st.text_input("Keterangan")
        
        if st.form_submit_button("Simpan Jurnal"):
            nomor = len(st.session_state['jurnal_guru']) + 1
            new_jurnal = pd.DataFrame({
                'No': [nomor],
                'Tanggal': [tgl],
                'Kelas': [kls_jurnal],
                'Tujuan Pembelajaran': [tujuan],
                'Keterangan': [ket]
            })
            st.session_state['jurnal_guru'] = pd.concat([st.session_state['jurnal_guru'], new_jurnal], ignore_index=True)
            st.toast("Jurnal tersimpan!", icon='✅')

    st.write("### Rekapitulasi Jurnal")
    st.dataframe(st.session_state['jurnal_guru'], use_container_width=True, hide_index=True)

# === MENU 4: DAFTAR HADIR ===
elif menu == "📅 Daftar Hadir":
    st.header("📅 Presensi Siswa (20 Pertemuan)")
    
    if st.session_state['kelas_list']:
        cls_abs = st.selectbox("Pilih Kelas:", st.session_state['kelas_list'], key='sel_abs')
        df_sis = st.session_state['siswa_data'][cls_abs]
        
        if not df_sis.empty:
            key_abs = f"absensi_{cls_abs}"
            
            # Setup Kolom: P1..P20 + S, I, A
            cols = ['Nama Siswa'] + [f'P{i}' for i in range(1, 21)] + ['S', 'I', 'A']
            
            # Inisialisasi data presensi jika belum ada
            if key_abs not in st.session_state:
                # Buat template data
                init_data = df_sis.copy()
                for c in cols[1:]: # Skip Nama
                    init_data[c] = False if c.startswith('P') else 0 # Checkbox untuk P, Angka untuk S/I/A
                st.session_state[key_abs] = init_data
            else:
                # Sinkronisasi jika ada siswa baru ditambah/dihapus
                stored_data = st.session_state[key_abs]
                # Merge logic sederhana: Ambil nama dari master siswa, gabung dengan data presensi yg ada
                merged = pd.merge(df_sis, stored_data, on='Nama Siswa', how='left')
                merged = merged.fillna(False) # Isi NaN dengan False/0
                st.session_state[key_abs] = merged

            st.markdown("**Petunjuk:** Centang kotak untuk **Hadir**. Isi angka manual untuk **S (Sakit), I (Izin), A (Alpa)**.")
            
            # Konfigurasi Kolom agar rapi
            col_config = {
                "Nama Siswa": st.column_config.TextColumn("Nama Siswa", disabled=True, width="medium"),
            }
            # Kecilkan kolom P1-P20
            for i in range(1, 21):
                col_config[f'P{i}'] = st.column_config.CheckboxColumn(f"{i}", width="small")
            
            edited_abs = st.data_editor(
                st.session_state[key_abs],
                column_config=col_config,
                hide_index=True,
                use_container_width=True
            )
            
            if st.button("💾 Simpan Presensi"):
                st.session_state[key_abs] = edited_abs
                st.toast("Presensi berhasil disimpan!", icon='✅')
        else:
            st.warning("Belum ada siswa di kelas ini.")
    else:
        st.error("Buat kelas dulu di menu Data Siswa.")

# === MENU 5: DAFTAR NILAI ===
elif menu == "📊 Daftar Nilai":
    st.header("📊 Input & Rekap Nilai")
    st.markdown("**(5 Tugas, 3 Ulangan Harian, 1 STS, 1 SAS)**")
    
    if st.session_state['kelas_list']:
        cls_nil = st.selectbox("Pilih Kelas:", st.session_state['kelas_list'], key='sel_nil')
        df_sis = st.session_state['siswa_data'][cls_nil]
        
        if not df_sis.empty:
            key_nil = f"nilai_{cls_nil}"
            
            # Struktur Kolom
            cols_tugas = [f'T{i}' for i in range(1, 6)]
            cols_uh = [f'UH{i}' for i in range(1, 4)]
            cols_ujian = ['STS', 'SAS']
            cols_all_scores = cols_tugas + cols_uh + cols_ujian
            
            if key_nil not in st.session_state:
                init_nil = df_sis.copy()
                for c in cols_all_scores:
                    init_nil[c] = 0.0
                init_nil['Nilai Akhir'] = 0.0
                st.session_state[key_nil] = init_nil
            else:
                 # Sinkronisasi nama siswa
                stored_nil = st.session_state[key_nil]
                merged = pd.merge(df_sis, stored_nil, on='Nama Siswa', how='left').fillna(0)
                st.session_state[key_nil] = merged
            
            # Tampilan Data Editor
            st.markdown("Silahkan isi nilai **0 - 100**.")
            
            edited_nil = st.data_editor(
                st.session_state[key_nil],
                column_config={
                    "Nama Siswa": st.column_config.TextColumn("Nama", disabled=True),
                    "Nilai Akhir": st.column_config.NumberColumn("Akhir", format="%.2f", disabled=True)
                },
                hide_index=True,
                use_container_width=True
            )
            
            col_act1, col_act2 = st.columns([1, 4])
            if col_act1.button("🧮 Hitung & Simpan"):
                # Konversi ke angka
                for c in cols_all_scores:
                    edited_nil[c] = pd.to_numeric(edited_nil[c], errors='coerce').fillna(0)
                
                # RUMUS REKAP NILAI (Bisa disesuaikan)
                # Rata-rata Tugas (20%) + Rata-rata UH (30%) + STS (20%) + SAS (30%)
                avg_tgs = edited_nil[cols_tugas].mean(axis=1)
                avg_uh = edited_nil[cols_uh].mean(axis=1)
                
                # Bobot Contoh: Tugas 20%, UH 30%, STS 20%, SAS 30%
                # Rumus Sederhana Rata-rata Total:
                nilai_akhir = (avg_tgs + avg_uh + edited_nil['STS'] + edited_nil['SAS']) / 4
                
                edited_nil['Nilai Akhir'] = nilai_akhir.round(2)
                
                st.session_state[key_nil] = edited_nil
                st.toast("Nilai berhasil dihitung dan disimpan!", icon='✅')
                st.balloons() # Efek visual menarik
                st.rerun()

# === MENU 6: CETAK LAPORAN ===
elif menu == "🖨️ Cetak Laporan":
    st.header("🖨️ Cetak / Download Laporan")
    st.info("Pilih data yang ingin dicetak dalam format Excel.")

    # Fungsi untuk convert DF ke Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("1. Jurnal Guru")
        if not st.session_state['jurnal_guru'].empty:
            st.download_button(
                label="⬇️ Download Jurnal (.xlsx)",
                data=to_excel(st.session_state['jurnal_guru']),
                file_name="Jurnal_Guru_SMPN1_WatangPulu.xlsx",
                mime="application/vnd.ms-excel"
            )
        else:
            st.caption("Data Jurnal Kosong")
            
    with c2:
        st.subheader("2. Laporan Kelas (Nilai & Absen)")
        if st.session_state['kelas_list']:
            cls_print = st.selectbox("Pilih Kelas:", st.session_state['kelas_list'], key='prt_cls')
            
            # Tombol Download Nilai
            key_n = f"nilai_{cls_print}"
            if key_n in st.session_state:
                st.download_button(
                    label=f"⬇️ Download Nilai {cls_print}",
                    data=to_excel(st.session_state[key_n]),
                    file_name=f"Nilai_{cls_print}.xlsx"
                )
            
            # Tombol Download Absen
            key_a = f"absensi_{cls_print}"
            if key_a in st.session_state:
                 st.download_button(
                    label=f"⬇️ Download Presensi {cls_print}",
                    data=to_excel(st.session_state[key_a]),
                    file_name=f"Presensi_{cls_print}.xlsx"
                )
        else:
            st.caption("Belum ada kelas.")

st.markdown("---")