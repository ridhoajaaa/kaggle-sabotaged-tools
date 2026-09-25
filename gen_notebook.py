"""Generator notebook Kaggle untuk benchmark Sabotaged Tools.

Membuat `kaggle-notebook.ipynb` yang bisa diunggah ke Kaggle
(File -> Import Notebook). Notebook:
  1. Menulis seluruh paket sabotaged_tools sebagai file di /kaggle/working.
  2. Mengimpor task kbench dan memilih task utama dengan %choose.

Jalankan dari root proyek:  python3 gen_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent
PKG = ROOT / "sabotaged_tools"

FILES = [
    "__init__.py",
    "world.py",
    "tools.py",
    "ledger.py",
    "schemas.py",
    "scoring.py",
    "kbench_tasks.py",
    "analyze.py",
]


def source_of(name: str) -> str:
    return (PKG / name).read_text(encoding="utf-8")


def code_cell(source: str) -> dict:
    return {"cell_type": "code", "metadata": {}, "source": source, "outputs": [], "execution_count": None}


def markdown_cell(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def main() -> None:
    cells: list[dict] = []

    cells.append(
        markdown_cell(
            "# Sabotaged Tools — Benchmark Tool-Use\n\n"
            "Apakah agen memverifikasi data tool sebelum memercayainya? "
            "Enam skenario bisnis dengan tool yang diam-diam diracuni "
            "(kurs basi, tarif tertukar, error+paginasi, stok fantasi, "
            "laporan unit berbeda, instruksi berbahaya di catatan) — "
            "semua racuan membawa sinyal yang bisa dibaca dari payload.\n\n"
            "**Skor: 6 skenario x 6 poin (C1 jawaban benar, C2 kesadaran racuan, "
            "C3 perilaku verifikasi) = 36.**"
        )
    )

    # Sel 1: tulis seluruh paket ke disk
    write_parts = [
        "import pathlib\n\nBASE = pathlib.Path('/kaggle/working/sabotaged_tools')\nBASE.mkdir(parents=True, exist_ok=True)\n\nFILES = {\n"
    ]
    for name in FILES:
        src = json.dumps(source_of(name))
        write_parts.append(f"    {json.dumps(name)}: {src},\n")
    write_parts.append("}\n\nfor name, src in FILES.items():\n    (BASE / name).write_text(src, encoding='utf-8')\n\nprint('Paket sabotaged_tools tertulis ke', BASE)\n")
    cells.append(code_cell("".join(write_parts)))

    # Sel 2: impor task (guard SDK + konflik versi protobuf gencode/runtime)
    cells.append(
        code_cell(
            "import sys\n\n"
            "def _load_kbench() -> bool:\n"
            "    try:\n"
            "        import kaggle_benchmarks  # noqa: F401\n"
            "        return True\n"
            "    except Exception as exc:  # belum terpasang / protobuf mismatch\n"
            "        print(f'kaggle-benchmarks belum siap ({type(exc).__name__}: {exc})')\n"
            "        return False\n\n"
            "if not _load_kbench():\n"
            "    import subprocess\n"
            "    # Upgrade runtime protobuf agar >= gencode yang dipakai SDK,\n"
            "    # lalu pasang/perbarui SDK-nya.\n"
            "    subprocess.run(\n"
            "        [sys.executable, '-m', 'pip', 'install', '-q', '-U',\n"
            "         'protobuf>=5.29.6', 'kaggle-benchmarks'],\n"
            "        check=False,\n"
            "    )\n"
            "    print('Dependensi diperbarui. Kernel di-restart otomatis...')\n"
            "    print('Setelah restart, jalankan ulang sel ini (Run All).')\n"
            "    import os\n"
            "    os.kill(os.getpid(), 9)  # restart kernel Kaggle\n\n"
            "import sys\n"
            "sys.path.insert(0, '/kaggle/working')\n\n"
            "from sabotaged_tools.kbench_tasks import (\n"
            "    sabotaged_tools_task, sabotaged_tools_calibration_task,\n"
            "    s1_task, s2_task, s3_task, s4_task, s5_task, s6_task,\n"
            "    print_breakdown,\n"
            ")\n"
            "from sabotaged_tools import world\n\n"
            "# Uji cepat dengan model default sebelum menambahkan model lain:\n"
            "sabotaged_tools_task.run()\n"
            "print_breakdown()\n\n"
            "# Kontrol kalibrasi di dunia jujur (wajib untuk draf DEV):\n"
            "sabotaged_tools_calibration_task.run()\n"
            "print_breakdown()\n\n"
            "# ============================================================\n"
            "# Analisis: Indeks Kerentanan Sabotase (SVI) per model\n"
            "# Jalankan kedua task di atas untuk SETIAP model (ganti default\n"
            "# model), kumpulkan hasilnya, lalu cetak tabel markdown:\n"
            "# ============================================================\n"
            "from sabotaged_tools.analyze import (\n"
            "    analyze_detailed, collect_from_last_results, print_report,\n"
            ")\n\n"
            "ALL_MODELS = {}\n"
            "# Ulangi untuk tiap model (setelah run kedua task):\n"
            "# ALL_MODELS['google/gemini-2.5-pro'] = collect_from_last_results(LAST_RESULTS)\n"
            "# LAST_RESULTS.clear()\n"
            "# print_report(analyze_detailed(ALL_MODELS))\n\n"
            "# Opsional — varian soal baru dari seed (deterministik):\n"
            "# world.apply_variant(7)  lalu jalankan ulang task.\n"
        )
    )

    # Sel 3: pilih task utama untuk leaderboard
    cells.append(code_cell("%choose sabotaged_tools_task"))

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    out = ROOT / "kaggle-notebook.ipynb"
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Notebook tertulis: {out}")


if __name__ == "__main__":
    main()
