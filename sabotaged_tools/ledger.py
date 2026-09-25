"""Ledger panggilan tool.

Setiap tool di tools.py mencatat pemanggilannya di sini. Ledger inilah
dasar penilaian Komponen 3 (perilaku verifikasi): retry, paginasi lengkap,
dan cross-check antar-tool semuanya terbaca dari log — tanpa perlu mengintip
API internal kaggle-benchmarks.
"""

from __future__ import annotations

import inspect
from typing import Any

_LOG: list[dict[str, Any]] = []


def record_call(tool: str, fn: Any, args: tuple, kwargs: dict[str, Any], result: Any) -> None:
    """Rekam satu panggilan tool beserta argumen terikat dan hasilnya."""
    try:
        sig = inspect.signature(fn)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        call_args = {k: v for k, v in bound.arguments.items()}
    except (TypeError, ValueError):
        call_args = dict(kwargs)
    _LOG.append({"tool": tool, "args": call_args, "result": result})


def get_log() -> list[dict[str, Any]]:
    """Salinan seluruh log panggilan (urut waktu)."""
    return [dict(entry) for entry in _LOG]


def calls(tool: str) -> list[dict[str, Any]]:
    """Semua entri log untuk satu nama tool."""
    return [dict(entry) for entry in _LOG if entry["tool"] == tool]


def reset() -> None:
    _LOG.clear()
