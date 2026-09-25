# Panduan Run Pertama di Kaggle — Sabotaged Tools

> Tujuan: menjalankan task utama (dunia teracaukan) + kontrol kalibrasi (dunia jujur)
> dengan model pilihan Anda, lalu mengambil angka untuk mengisi `[FILL: ...]` di
> `DEV_SUBMISSION_DRAFT.md`. Perkiraan durasi per model: 5–15 menit (~12 prompt LLM).

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
   `print_breakdown()` → `sabotaged_tools_calibration_task.run()` → `print_breakdown()`.
   Anda akan melihat agen memanggil tool; biarkan sampai selesai (jangan interupsi).
3. Baca dua tabel breakdown yang tercetak — itulah bahan angka artikel:

   ```
   skenario                             total  C1  C2  C3
   S1_currency [racuan]                 6/6    2   2   2
   ...
   TOTAL [racuan]                     xx/36
   TOTAL [jujur]                      yy/36
   ```

4. **Sel terakhir**: `%choose sabotaged_tools_task` — WAJIB dijalankan setelah run
   agar task utama yang terdaftar di leaderboard (bukan task per-skenario).

## 4. Simpan sebagai versi resmi
- **Save Version → Save & Run All (Commit)**. Run inilah yang menghasilkan artefak
  task/run resmi dan URL task di Kaggle (untuk syarat eligibility DEV).
- Setelah selesai: halaman **Task Detail** menampilkan leaderboard run Anda.
  Salin URL-nya → `[FILL: kaggle benchmark URL]`.

## 5. Model kedua, ketiga, dst.
Cara paling sederhana untuk run pertama: **ganti model default** (panel model → set
sebagai default) → jalankan ulang sel 2 → catat tabel breakdown per model.
Cara resmi yang lebih rapi (setelah run pertama berhasil): dari Task Detail page,
gunakan **Add Models** untuk menjadwalkan model lain pada task yang sama.

## 6. Kontrol kalibrasi & varian (untuk artikel)
- `sabotaged_tools_calibration_task` sudah berjalan di sel 2 (dunia jujur, C2 murni).
- Opsional, untuk bagian "robustness" artikel: sebelum sel run, eksekusi
  `world.apply_variant(7)` (atau seed lain) lalu jalankan ulang kedua task — soal
  berubah total, skor agen teliti tetap harus 36/36.
- Catatan: leaderboard kbench hanya mendukung **satu task per notebook**. Task
  kalibrasi tetap valid sebagai data artikel; jika ingin leaderboard-nya sendiri,
  duplikat notebook dan `%choose sabotaged_tools_calibration_task` di sana.

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
| Hasil aneh di satu skenario | Periksa tabel breakdown C1/C2/C3 — komponen memisahkan "salah jawab" vs "tidak sadar racun" vs "tidak verifikasi" |

## 9. Sebelum publikasi
1. Semua `[FILL: ...]` di `DEV_SUBMISSION_DRAFT.md` terisi angka nyata.
2. Link Kaggle benar dan task sudah di-Save Version.
3. Tag `#kagglechallenge` ada di postingan.
4. Jalankan `bash scripts/check.sh` sekali lagi (notebook harus sinkron).
5. Submit sebelum **11 Oktober 2026, 23:59 PDT** — sisa waktu Anda: cukup, tapi jangan tunggu hari terakhir.
