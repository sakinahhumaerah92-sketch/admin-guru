<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Administrasi Guru - UPT SMPN 1 Watang Pulu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        body { font-family: 'Poppins', sans-serif; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        @media print {
            .no-print { display: none !important; }
            .print-only { display: block !important; }
            body { background: white; padding: 0; }
            .container { max-width: 100%; width: 100%; }
            table { font-size: 10pt; }
        }
        .custom-scrollbar::-webkit-scrollbar { height: 8px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen">

    <header class="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white p-6 shadow-xl no-print">
        <div class="container mx-auto flex flex-col md:flex-row justify-between items-center">
            <div class="text-center md:text-left mb-4 md:mb-0">
                <h1 class="text-3xl font-extrabold tracking-tight">UPT SMP Negeri 1 Watang Pulu</h1>
                <p class="text-blue-100 italic">"Mencerdaskan Bangsa dengan Teknologi"</p>
            </div>
            <div class="bg-white/20 p-3 rounded-xl backdrop-blur-md border border-white/30 text-center">
                <span id="currentDate" class="font-semibold"></span>
            </div>
        </div>
    </header>

    <nav class="container mx-auto mt-6 px-4 no-print">
        <div class="flex flex-wrap gap-2 justify-center">
            <button onclick="switchTab('tab-profil')" class="nav-btn bg-white px-4 py-2 rounded-lg shadow-sm border-b-4 border-blue-500 hover:bg-blue-50 transition-all font-semibold"><i class="fas fa-user-tie mr-2 text-blue-500"></i>Profil & Kelas</button>
            <button onclick="switchTab('tab-siswa')" class="nav-btn bg-white px-4 py-2 rounded-lg shadow-sm border-b-4 border-emerald-500 hover:bg-emerald-50 transition-all font-semibold"><i class="fas fa-users mr-2 text-emerald-500"></i>Data Siswa</button>
            <button onclick="switchTab('tab-jurnal')" class="nav-btn bg-white px-4 py-2 rounded-lg shadow-sm border-b-4 border-purple-500 hover:bg-purple-50 transition-all font-semibold"><i class="fas fa-book mr-2 text-purple-500"></i>Jurnal</button>
            <button onclick="switchTab('tab-absensi')" class="nav-btn bg-white px-4 py-2 rounded-lg shadow-sm border-b-4 border-amber-500 hover:bg-amber-50 transition-all font-semibold"><i class="fas fa-calendar-check mr-2 text-amber-500"></i>Absensi</button>
            <button onclick="switchTab('tab-nilai')" class="nav-btn bg-white px-4 py-2 rounded-lg shadow-sm border-b-4 border-rose-500 hover:bg-rose-50 transition-all font-semibold"><i class="fas fa-star mr-2 text-rose-500"></i>Nilai</button>
            <button onclick="preparePrint()" class="bg-slate-800 text-white px-4 py-2 rounded-lg shadow-md hover:bg-slate-900 transition-all font-semibold"><i class="fas fa-print mr-2"></i>Cetak Laporan</button>
        </div>
    </nav>

    <main class="container mx-auto p-4 md:p-6">
        
        <section id="tab-profil" class="tab-content active space-y-6 animate-fade-in">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-2xl shadow-lg border-l-8 border-blue-500">
                    <h2 class="text-xl font-bold mb-4 text-blue-700">Identitas Guru & Mapel</h2>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-600">Nama Guru</label>
                            <input type="text" id="guru-nama" onchange="saveData()" class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" placeholder="Contoh: Budi Santoso, S.Pd">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-600">Mata Pelajaran</label>
                            <input type="text" id="guru-mapel" onchange="saveData()" class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" placeholder="Contoh: Matematika">
                        </div>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-2xl shadow-lg border-l-8 border-indigo-500">
                    <h2 class="text-xl font-bold mb-4 text-indigo-700">Manajemen Kelas</h2>
                    <div class="flex gap-2 mb-4">
                        <input type="text" id="input-kelas" class="flex-1 p-2 border rounded-lg" placeholder="Nama Kelas Baru (Contoh: VII-A)">
                        <button onclick="tambahKelas()" class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">Tambah</button>
                    </div>
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-600">Pilih Kelas Aktif:</label>
                        <select id="select-kelas" onchange="gantiKelasActive(this.value)" class="w-full p-2 border-2 border-indigo-100 rounded-lg font-bold text-indigo-700 outline-none"></select>
                    </div>
                </div>
            </div>
        </section>

        <section id="tab-siswa" class="tab-content bg-white p-6 rounded-2xl shadow-lg border-t-8 border-emerald-500">
            <div class="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                <h2 class="text-2xl font-bold text-emerald-700">Daftar Siswa (Maks 35)</h2>
                <div class="flex flex-wrap gap-2">
                    <label class="bg-emerald-100 text-emerald-700 px-4 py-2 rounded-lg cursor-pointer hover:bg-emerald-200 font-semibold transition">
                        <i class="fas fa-file-import mr-2"></i>Import CSV (Nama)
                        <input type="file" id="csv-file" accept=".csv" class="hidden" onchange="importCSV(this)">
                    </label>
                    <button onclick="hapusSemuaSiswa()" class="bg-rose-100 text-rose-600 px-4 py-2 rounded-lg hover:bg-rose-200 font-semibold"><i class="fas fa-trash-alt mr-2"></i>Kosongkan</button>
                </div>
            </div>
            
            <div class="flex gap-2 mb-6">
                <input type="text" id="input-nama-siswa" class="flex-1 p-2 border rounded-lg" placeholder="Masukkan Nama Siswa Manual">
                <button onclick="tambahSiswaManual()" class="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 font-bold">Tambah</button>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full border-collapse">
                    <thead class="bg-emerald-50">
                        <tr>
                            <th class="border p-3 text-left w-16">No</th>
                            <th class="border p-3 text-left">Nama Lengkap</th>
                            <th class="border p-3 text-center w-24 no-print">Aksi</th>
                        </tr>
                    </thead>
                    <tbody id="tabel-siswa-body"></tbody>
                </table>
            </div>
        </section>

        <section id="tab-jurnal" class="tab-content bg-white p-6 rounded-2xl shadow-lg border-t-8 border-purple-500">
            <h2 class="text-2xl font-bold text-purple-700 mb-6">Jurnal Mengajar Guru</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 no-print bg-purple-50 p-4 rounded-xl">
                <input type="date" id="jurnal-tgl" class="p-2 border rounded-lg">
                <input type="text" id="jurnal-tp" class="p-2 border rounded-lg" placeholder="Tujuan Pembelajaran">
                <input type="text" id="jurnal-ket" class="p-2 border rounded-lg" placeholder="Keterangan">
                <button onclick="tambahJurnal()" class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 font-bold col-span-1 md:col-span-3">Simpan Jurnal</button>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full border-collapse">
                    <thead class="bg-purple-100">
                        <tr>
                            <th class="border p-3 w-12">No</th>
                            <th class="border p-3 w-32">Tanggal</th>
                            <th class="border p-3">Tujuan Pembelajaran</th>
                            <th class="border p-3">Keterangan</th>
                            <th class="border p-3 w-12 no-print"></th>
                        </tr>
                    </thead>
                    <tbody id="tabel-jurnal-body"></tbody>
                </table>
            </div>
        </section>

        <section id="tab-absensi" class="tab-content bg-white p-6 rounded-2xl shadow-lg border-t-8 border-amber-500">
            <h2 class="text-2xl font-bold text-amber-700 mb-2">Presensi Kehadiran Siswa</h2>
            <p class="text-xs text-amber-600 mb-4">* Ketik: <span class="font-bold">A</span> (Alfa), <span class="font-bold">I</span> (Izin), <span class="font-bold">S</span> (Sakit), atau <span class="font-bold">H</span> (Hadir)</p>
            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full border-collapse text-xs">
                    <thead class="bg-amber-100">
                        <tr>
                            <th class="border p-2 sticky left-0 bg-amber-100 z-10 w-40">Nama Siswa</th>
                            <script>for(let i=1; i<=20; i++) document.write(`<th class="border p-1 w-8">${i}</th>`);</script>
                            <th class="border p-1 bg-amber-200">Rekap</th>
                        </tr>
                    </thead>
                    <tbody id="tabel-absensi-body"></tbody>
                </table>
            </div>
        </section>

        <section id="tab-nilai" class="tab-content bg-white p-6 rounded-2xl shadow-lg border-t-8 border-rose-500">
            <h2 class="text-2xl font-bold text-rose-700 mb-4">Daftar Nilai Siswa</h2>
            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full border-collapse text-xs">
                    <thead class="bg-rose-100">
                        <tr class="text-center">
                            <th rowspan="2" class="border p-2 sticky left-0 bg-rose-100 z-10 w-40">Nama Siswa</th>
                            <th colspan="5" class="border p-1">Tugas (T)</th>
                            <th colspan="3" class="border p-1">UH</th>
                            <th rowspan="2" class="border p-1 bg-yellow-100">STS</th>
                            <th rowspan="2" class="border p-1 bg-yellow-100">SAS</th>
                            <th rowspan="2" class="border p-1 bg-rose-600 text-white">RATA2</th>
                        </tr>
                        <tr>
                            <script>for(let i=1; i<=5; i++) document.write(`<th class="border p-1 w-10">T${i}</th>`);</script>
                            <script>for(let i=1; i<=3; i++) document.write(`<th class="border p-1 w-10">UH${i}</th>`);</script>
                        </tr>
                    </thead>
                    <tbody id="tabel-nilai-body"></tbody>
                </table>
            </div>
        </section>

    </main>

    <div id="toast" class="fixed bottom-5 right-5 hidden bg-emerald-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all animate-bounce">
        <i class="fas fa-check-circle mr-2"></i> <span id="toast-msg">Data berhasil disimpan!</span>
    </div>

    <div class="print-only hidden p-8">
        <div class="text-center border-b-4 border-double border-black pb-4 mb-6">
            <h1 class="text-2xl font-bold">LAPORAN HASIL ADMINISTRASI GURU</h1>
            <h2 class="text-xl font-bold uppercase" id="print-sekolah">UPT SMP NEGERI 1 WATANG PULU</h2>
            <p id="print-meta" class="mt-2"></p>
        </div>
        <div id="print-area"></div>
    </div>

    <script>
        // --- State Management ---
        let db = JSON.parse(localStorage.getItem('db_smpn1watangpulu')) || {
            profil: { nama: '', mapel: '' },
            kelas: {}, // Format: { 'VIIA': { siswa: [], jurnal: [], absensi: {}, nilai: {} } }
            activeKelas: ''
        };

        const toast = document.getElementById('toast');
        function showToast(msg) {
            document.getElementById('toast-msg').innerText = msg;
            toast.classList.remove('hidden');
            setTimeout(() => toast.classList.add('hidden'), 3000);
        }

        function saveData() {
            db.profil.nama = document.getElementById('guru-nama').value;
            db.profil.mapel = document.getElementById('guru-mapel').value;
            localStorage.setItem('db_smpn1watangpulu', JSON.stringify(db));
            renderAll();
        }

        // --- Tabs ---
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            renderAll();
        }

        // --- Kelas Logic ---
        function tambahKelas() {
            const namaKelas = document.getElementById('input-kelas').value.trim();
            if (namaKelas && !db.kelas[namaKelas]) {
                db.kelas[namaKelas] = {
                    siswa: [],
                    jurnal: [],
                    absensi: {},
                    nilai: {}
                };
                db.activeKelas = namaKelas;
                document.getElementById('input-kelas').value = '';
                saveData();
                showToast("Kelas " + namaKelas + " ditambahkan!");
            }
        }

        function gantiKelasActive(val) {
            db.activeKelas = val;
            saveData();
        }

        // --- Siswa Logic ---
        function tambahSiswaManual() {
            if(!db.activeKelas) return alert("Pilih kelas terlebih dahulu!");
            const nama = document.getElementById('input-nama-siswa').value.trim();
            const listSiswa = db.kelas[db.activeKelas].siswa;
            if(nama && listSiswa.length < 35) {
                listSiswa.push(nama);
                document.getElementById('input-nama-siswa').value = '';
                saveData();
                showToast("Siswa ditambahkan!");
            } else if (listSiswa.length >= 35) {
                alert("Maksimal 35 siswa!");
            }
        }

        function importCSV(input) {
            if(!db.activeKelas) return alert("Pilih kelas terlebih dahulu!");
            const file = input.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                const text = e.target.result;
                const rows = text.split('\n');
                rows.forEach(row => {
                    const nama = row.trim();
                    if(nama && db.kelas[db.activeKelas].siswa.length < 35) {
                        db.kelas[db.activeKelas].siswa.push(nama);
                    }
                });
                saveData();
                showToast("Import CSV Berhasil!");
            };
            reader.readAsText(file);
        }

        function hapusSiswa(index) {
            if(confirm("Hapus siswa ini?")) {
                db.kelas[db.activeKelas].siswa.splice(index, 1);
                saveData();
            }
        }

        function hapusSemuaSiswa() {
            if(confirm("Hapus semua siswa di kelas ini?")) {
                db.kelas[db.activeKelas].siswa = [];
                saveData();
            }
        }

        // --- Jurnal Logic ---
        function tambahJurnal() {
            if(!db.activeKelas) return alert("Pilih kelas dulu!");
            const tgl = document.getElementById('jurnal-tgl').value;
            const tp = document.getElementById('jurnal-tp').value;
            const ket = document.getElementById('jurnal-ket').value;
            if(tgl && tp) {
                db.kelas[db.activeKelas].jurnal.push({ tgl, tp, ket });
                saveData();
                showToast("Jurnal tersimpan!");
            }
        }

        // --- Render Functions ---
        function renderAll() {
            // Profil
            document.getElementById('guru-nama').value = db.profil.nama || '';
            document.getElementById('guru-mapel').value = db.profil.mapel || '';

            // Dropdown Kelas
            const selectKelas = document.getElementById('select-kelas');
            selectKelas.innerHTML = "";
            Object.keys(db.kelas).forEach(k => {
                const opt = document.createElement('option');
                opt.value = k;
                opt.innerText = k;
                if(k === db.activeKelas) opt.selected = true;
                selectKelas.appendChild(opt);
            });

            if(!db.activeKelas) return;

            const dataKelas = db.kelas[db.activeKelas];

            // Render Tabel Siswa
            const tBodySiswa = document.getElementById('tabel-siswa-body');
            tBodySiswa.innerHTML = "";
            dataKelas.siswa.forEach((s, i) => {
                tBodySiswa.innerHTML += `
                    <tr class="hover:bg-slate-50 border-b">
                        <td class="p-3 border">${i+1}</td>
                        <td class="p-3 border font-semibold">${s}</td>
                        <td class="p-3 border text-center no-print">
                            <button onclick="hapusSiswa(${i})" class="text-rose-500 hover:scale-110 transition"><i class="fas fa-trash"></i></button>
                        </td>
                    </tr>`;
            });

            // Render Tabel Jurnal
            const tBodyJurnal = document.getElementById('tabel-jurnal-body');
            tBodyJurnal.innerHTML = "";
            dataKelas.jurnal.forEach((j, i) => {
                tBodyJurnal.innerHTML += `
                    <tr class="border-b">
                        <td class="p-2 border text-center">${i+1}</td>
                        <td class="p-2 border">${j.tgl}</td>
                        <td class="p-2 border">${j.tp}</td>
                        <td class="p-2 border italic">${j.ket}</td>
                        <td class="p-2 border no-print">
                            <button onclick="db.kelas[db.activeKelas].jurnal.splice(${i},1); saveData();" class="text-rose-400">X</button>
                        </td>
                    </tr>`;
            });

            // Render Absensi
            const tBodyAbsen = document.getElementById('tabel-absensi-body');
            tBodyAbsen.innerHTML = "";
            dataKelas.siswa.forEach((s) => {
                let inputs = "";
                let count = {A:0, I:0, S:0};
                for(let i=1; i<=20; i++) {
                    const key = `absen-${s}-${i}`;
                    const val = dataKelas.absensi[key] || '';
                    if(val === 'A') count.A++;
                    if(val === 'I') count.I++;
                    if(val === 'S') count.S++;
                    inputs += `<td class="border p-0"><input type="text" maxlength="1" onchange="updateAbsensi('${s}', ${i}, this.value)" class="w-full h-8 text-center uppercase outline-none focus:bg-amber-50" value="${val}"></td>`;
                }
                tBodyAbsen.innerHTML += `
                    <tr>
                        <td class="border p-2 sticky left-0 bg-white font-medium">${s}</td>
                        ${inputs}
                        <td class="border p-1 bg-amber-50 text-[10px] text-center">A:${count.A} I:${count.I} S:${count.S}</td>
                    </tr>`;
            });

            // Render Nilai
            const tBodyNilai = document.getElementById('tabel-nilai-body');
            tBodyNilai.innerHTML = "";
            dataKelas.siswa.forEach((s) => {
                const n = dataKelas.nilai[s] || { t:[0,0,0,0,0], uh:[0,0,0], sts:0, sas:0 };
                let tCols = "";
                let uhCols = "";
                n.t.forEach((val, i) => tCols += `<td class="border p-0"><input type="number" onchange="updateNilai('${s}', 't', ${i}, this.value)" class="w-full h-8 text-center outline-none" value="${val}"></td>`);
                n.uh.forEach((val, i) => uhCols += `<td class="border p-0"><input type="number" onchange="updateNilai('${s}', 'uh', ${i}, this.value)" class="w-full h-8 text-center outline-none" value="${val}"></td>`);
                
                // Kalkulasi Rata-rata
                const totalNilai = [...n.t, ...n.uh, n.sts, n.sas].reduce((a, b) => Number(a) + Number(b), 0);
                const rata = (totalNilai / 10).toFixed(1);

                tBodyNilai.innerHTML += `
                    <tr>
                        <td class="border p-2 sticky left-0 bg-white font-medium">${s}</td>
                        ${tCols} ${uhCols}
                        <td class="border p-0 bg-yellow-50"><input type="number" onchange="updateNilai('${s}', 'sts', 0, this.value)" class="w-full h-8 text-center outline-none bg-transparent" value="${n.sts}"></td>
                        <td class="border p-0 bg-yellow-50"><input type="number" onchange="updateNilai('${s}', 'sas', 0, this.value)" class="w-full h-8 text-center outline-none bg-transparent" value="${n.sas}"></td>
                        <td class="border p-2 text-center font-bold bg-rose-50 text-rose-700">${rata}</td>
                    </tr>`;
            });
        }

        function updateAbsensi(siswa, pertemuan, val) {
            db.kelas[db.activeKelas].absensi[`absen-${siswa}-${pertemuan}`] = val.toUpperCase();
            saveData();
            showToast("Absensi diperbarui");
        }

        function updateNilai(siswa, tipe, idx, val) {
            if(!db.kelas[db.activeKelas].nilai[siswa]) {
                db.kelas[db.activeKelas].nilai[siswa] = { t:[0,0,0,0,0], uh:[0,0,0], sts:0, sas:0 };
            }
            const node = db.kelas[db.activeKelas].nilai[siswa];
            if(tipe === 't' || tipe === 'uh') node[tipe][idx] = val;
            else node[tipe] = val;
            saveData();
            showToast("Nilai diperbarui");
        }

        // --- Print Logic ---
        function preparePrint() {
            const printMeta = document.getElementById('print-meta');
            printMeta.innerText = `Guru: ${db.profil.nama} | Mata Pelajaran: ${db.profil.mapel} | Kelas: ${db.activeKelas}`;
            
            // Gabungkan tabel-tabel penting ke print-area
            const activeTabId = document.querySelector('.tab-content.active').id;
            const content = document.querySelector(`#${activeTabId} table`).cloneNode(true);
            
            // Hilangkan kolom aksi di hasil print
            content.querySelectorAll('.no-print').forEach(el => el.remove());
            
            const area = document.getElementById('print-area');
            area.innerHTML = "";
            area.appendChild(content);
            
            window.print();
        }

        // --- Init ---
        document.getElementById('currentDate').innerText = new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        renderAll();

    </script>
</body>
</html>
