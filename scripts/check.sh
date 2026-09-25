#!/usr/bin/env bash
# check.sh — gerbang kualitas benchmark Sabotaged Tools.
# Dipakai oleh hook pre-push dan bisa dijalankan manual: bash scripts/check.sh
#
# Tahapan:
#   1. py_compile semua modul Python
#   2. pytest lintas-seed (90 test, 20 seed) — fallback ke smoke test jika
#      pytest tidak tersedia
#   3. Smoke test local_run.py
#   4. Regenerasi kaggle-notebook.ipynb harus bebas diff (artefak selalu segar)

set -uo pipefail
cd "$(dirname "$0")/.."

FAIL=0
PY="${PYTHON:-python3}"

step() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m[OK]\033[0m %s\n' "$*"; }
err()  { printf '\033[1;31m[GAGAL]\033[0m %s\n' "$*"; FAIL=1; }

# 1) Sintaks ------------------------------------------------------------
step "1/4 Sintaks semua modul"
if "$PY" -m py_compile sabotaged_tools/*.py local_run.py gen_notebook.py conftest.py tests/*.py; then
    ok "semua file valid"
else
    err "ada file yang gagal compile"
fi

# 2) pytest lintas-seed (fallback smoke test) ---------------------------
step "2/4 pytest lintas-seed (20 seed)"
if "$PY" -c "import pytest" >/dev/null 2>&1; then
    "$PY" -m pytest -q && ok "pytest lulus" || err "pytest gagal"
elif [ -x .venv/bin/pytest ]; then
    .venv/bin/pytest -q && ok "pytest (venv) lulus" || err "pytest (venv) gagal"
else
    err "pytest tidak tersedia (pasang: python3 -m venv .venv && .venv/bin/pip install pytest) — fallback ke smoke test"
    "$PY" local_run.py >/dev/null 2>&1 && ok "smoke test (fallback) lulus" || err "smoke test (fallback) gagal"
fi

# 3) Smoke test ----------------------------------------------------------
step "3/4 Smoke test local_run.py"
"$PY" local_run.py >/tmp/st_run.log 2>&1 && ok "semua suite lulus (tail: $(tail -1 /tmp/st_run.log))" || {
    err "smoke test gagal — lihat /tmp/st_run.log"; tail -5 /tmp/st_run.log; }

# 4) Notebook harus up-to-date -------------------------------------------
step "4/4 kaggle-notebook.ipynb up-to-date"
cp kaggle-notebook.ipynb /tmp/nb_before.ipynb
"$PY" gen_notebook.py >/dev/null 2>&1
if cmp -s kaggle-notebook.ipynb /tmp/nb_before.ipynb; then
    ok "notebook sinkron dengan paket"
else
    err "notebook basi — jalankan 'python3 gen_notebook.py' dan commit ulang"
fi

printf '\n'
if [ "$FAIL" -eq 0 ]; then
    printf '\033[1;32mSEMUA TAHAPAN LULUS ✅\033[0m\n'
    exit 0
fi
printf '\033[1;31mADA TAHAPAN GAGAL ❌ — push diblokir\033[0m\n'
exit 1
