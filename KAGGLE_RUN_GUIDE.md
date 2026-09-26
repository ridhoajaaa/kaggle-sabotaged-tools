# Panduan Run Pertama di Kaggle — Sabotaged Tools

> Tujuan: menjalankan task utama (dunia teracaukan) + kontrol kalibrasi (dunia jujur)
> dengan model pilihan Anda, lalu mengambil angka untuk mengisi `[FILL: ...]` di
> `DEV_SUBMISSION_DRAFT.md`. Perkiraan durasi per model: 5–15 menit (~12 prompt LLM).
> Plus eksperimen three-arm: +2 task ≈ +24 prompt LLM per model.

## 0. Prasyarat
- Akun Kaggle **terverifikasi telepon** (syarat untuk memilih model LLM di notebook).
- File `kaggle-notebook.ipynb` dari repo ini (regenerasi terbaru: `python3 gen_notebook.py`).

## 1. Unggah notebook
1. Buka **kaggle.com/code** → **New Notebook**.
2. Menu **File → Import Notebook** → pilih `kaggle-notebook.ipynb`.
3. Alternatif (jika import bermasalah): buka **kaggle.com/benchmarks/tasks/new**
   (notebook starter dengan SDK terpasang), lalu salin isi 4 sel kita satu per satu.

## 2. Pilih model (Add Models)
1. Panel kanan → **Add Models** (ikon model / "Model picker").
2. Tambahkan 2–4 model, contoh lineup: satu flagship per lab (Gemini / GPT / Claude)
   + satu open-weight (Llama/Qwen).
3. Model **pertama** menjadi default (`kbench.llm`) untuk run pertama.
4. Kode task sudah mengikuti pola resmi (satu `llm` placeholder) — model lain bisa
   dijadwalkan dari **Task Detail page → Add Models** tanpa mengubah kode.
5. Settings notebook: **Internet ON** (butuh verifikasi telepon). GPU tidak diperlukan.

## 3. Jalankan
1. **Sel 1**: menulis paket ke `/kaggle/working/sabotaged_tools` (selalu jalan duluan).
2. **Sel 2**: guard instalasi SDK → impor task → `sabotaged_tools_task.run()` →
   `print_breakdown()` → `sabotaged_tools_calibration_task.run()` → `print_breakdown()`
   → **eksperimen three-arm** (`think_first` lalu `two_pass`) →
   `print_experiment_summary(LAST_RESULTS)`.
   Anda akan melihat agen memanggil tool; biarkan sampai selesai (jangan interupsi).
3. Baca tabel breakdown yang tercetak — itulah bahan angka artikel:

   ```
   == single-pass (baseline leaderboard) ==
   skenario                             total  C1  C2  C3
   S1_currency [racuan]                 6/6    2   2   2
   ...
   TOTAL [racuan]                     xx/36
   TOTAL [jujur]                      yy/36

   == Eksperimen verify-then-recompute (dunia teracaukan) ==
     single       total xx/36   (S1-S3: x/18)
     think_first  total xx/36   (S1-S3: x/18)
     two_pass     total xx/36   (S1-S3: x/18)
     delta two_pass vs single: +N poin
   ```

4. **Sel terakhir**: `%choose sabotaged_tools_task` — WAJIB dijalankan setelah run
   agar task utama yang terdaftar di leaderboard (bukan task per-skenario).

## 4. Simpan sebagai versi resmi
- **Save Version → Save & Run All (Commit)**. Run inilah yang menghasilkan artefak
  task/run resmi dan URL task di Kaggle (untuk syarat eligibility DEV).
- Setelah selesai: halaman **Task Detail** menampilkan leaderboard run Anda.
  Salin URL-nya → `[FILL: kaggle benchmark URL]`.

## 4b. Pola cepat: tarik paket langsung dari GitHub (anti basi)

Daripada menyalin-ulang sel "tulis paket" setiap kali repo diperbarui, ganti sel itu
 dengan sel berikut di notebook benchmark `benchmarks/tasks/new` Anda:

```python
import urllib.request, pathlib

REV = "0f1ffc1"  # pin commit — naikkan bila repo diperbarui
BASE = pathlib.Path("/kaggle/working/sabotaged_tools")
BASE.mkdir(parents=True, exist_ok=True)
FILES = ["__init__.py", "world.py", "tools.py", "ledger.py",
         "schemas.py", "scoring.py", "scenarios.py", "kbench_tasks.py", "analyze.py"]
for name in FILES:
    url = (f"https://raw.githubusercontent.com/ridhoajaaa/kaggle-sabotaged-tools/"
           f"{REV}/sabotaged_tools/{name}")
    dst = BASE / name
    urllib.request.urlretrieve(url, dst)
    print(f"  {name}: {dst.stat().st_size} bytes")
print("Paket tertarik dari GitHub @", REV)
```

Lalu: **Restart kernel → Run All** (restart wajib: modul lama ter-cache di kernel).
Sel run tetap dari notebook kita; hasil run resmi tetap tervalidasi karena kode
yang dipakai ter-pin ke commit yang jelas — cocok dikutip di postingan DEV.

## 5. Model kedua, ketiga, dst.
Cara paling sederhana untuk run pertama: **ganti model default** (panel model → set
sebagai default) → jalankan ulang sel 2 → catat tabel breakdown per model.
Cara resmi yang lebih rapi (setelah run pertama berhasil): dari Task Detail page,
gunakan **Add Models** untuk menjadwalkan model lain pada task yang sama.

## 6. Kontrol kalibrasi & varian (untuk artikel)
- `sabotaged_tools_calibration_task` sudah berjalan di sel 2 (dunia jujur, C2 murni).
- Eksperimen three-arm (`sabotaged_tools_think_first_task`,
  `sabotaged_tools_two_pass_task`) juga sudah berjalan di sel 2 — outputnya
  diringkas `print_experiment_summary`. Baseline pembandingnya adalah run
  `sabotaged_tools_task` yang sudah ada di run yang sama (dunia default identik).
  Tabel hasilnya = bahan seksi "Update: a reader's hypothesis, tested" artikel DEV.
- Opsional, untuk bagian "robustness" artikel: sebelum sel run, eksekusi
  `world.apply_variant(7)` (atau seed lain) lalu jalankan ulang task — soal
  berubah total, skor agen teliti tetap harus 36/36. Untuk eksperimen three-arm
  pada varian ber-seed: `world.apply_variant(7)` lalu jalankan ketiga task
  berturut-turut (baseline single-pass boleh diwakili run terpisah asal seed sama).
- Catatan: leaderboard kbench hanya mendukung **satu task per notebook**. Task
  kalibrasi/eksperimen tetap valid sebagai data artikel; jika ingin leaderboard-nya
  sendiri, duplikat notebook dan `%choose` task tersebut di sana.

## 7. Isi draf DEV dari hasil
Per model, catat dari dua tabel breakdown:
1. Total `[racuan]` dan `[jujur]` → isi "calibration split" (gap-nya = cerita utama).
2. C2 per skenario `[racuan]` → skenario mana yang paling/least terdeteksi.
3. C3 → perilaku verifikasi (retry, paginasi, cross-check) per model.
4. 1–2 anekdot konkret: buka run di Task Detail → transkrip prompt/tool-call per
   run (platform merekam semuanya) — mis. model yang menuruti instruksi S6.

## 8. Troubleshooting
| Gejala | Solusi |
|---|---|
| Add Models kosong / error 403 | Verifikasi nomor telepon di akun Kaggle |
| `pip install kaggle-benchmarks` gagal | Nyalakan Internet di Settings notebook |
| Output task kosong di leaderboard | Pastikan sel `%choose sabotaged_tools_task` dijalankan SETELAH run |
| Run berhenti di tengah | Jalankan ulang sel 2 (state racuan di-reset otomatis tiap run skenario) |
| `VersionError: Protobuf Gencode/Runtime` saat import SDK | Sudah ditangani otomatis oleh sel 2 versi terbaru (upgrade protobuf lalu restart kernel sekali — jalankan ulang Run All setelahnya). Manual: `!pip install -q -U "protobuf>=5.29.6"` → Restart kernel → Run All |
| `ValueError: Missing environment variables ... MODEL_PROXY_URL / MODEL_PROXY_API_KEY` | Notebook biasa tidak membawa kredensial model proxy. Jalankan dari pintu resmi: buka **kaggle.com/benchmarks/tasks/new** (notebook pre-wired), tempel isi sel kita di sana (jangan File→Import agar wiring utuh), lalu Add Model & Run. Uji cepat sesi lama: `!kaggle benchmarks auth` (tidak tahan untuk Save Version) |
| Hasil aneh di satu skenario | Periksa tabel breakdown C1/C2/C3 — komponen memisahkan "salah jawab" vs "tidak sadar racun" vs "tidak verifikasi" |

## 9. Sebelum publikasi
1. Semua `[FILL: ...]` di `DEV_SUBMISSION_DRAFT.md` terisi angka nyata.
2. Link Kaggle benar dan task sudah di-Save Version.
3. Tag `#kagglechallenge` ada di postingan.
4. Jalankan `bash scripts/check.sh` sekali lagi (notebook harus sinkron).
5. Submit sebelum **11 Oktober 2026, 23:59 PDT** — sisa waktu Anda: cukup, tapi jangan tunggu hari terakhir.
