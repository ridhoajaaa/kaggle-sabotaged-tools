#!/usr/bin/env bash
# install_hooks.sh — pasang git hook pre-push yang menjalankan scripts/check.sh
# Idempoten: aman dijalankan berulang. Lepas dengan --remove.

set -euo pipefail
cd "$(dirname "$0")/.."

MARK="# sabotaged-tools pre-push hook"
HOOK_DIR="$(git config core.hooksPath 2>/dev/null || echo .git/hooks)"
HOOK="$HOOK_DIR/pre-push"
SCRIPT="scripts/check.sh"

mkdir -p "$HOOK_DIR"
chmod +x "$SCRIPT"

if [ "${1:-}" = "--remove" ]; then
    if [ -f "$HOOK" ] && grep -q "$MARK" "$HOOK" 2>/dev/null; then
        rm "$HOOK"
        echo "Hook pre-push dilepas: $HOOK"
    else
        echo "Tidak ada hook bermarker kami di $HOOK — tidak ada yang dilepas."
    fi
    exit 0
fi

if [ -f "$HOOK" ] && ! grep -q "$MARK" "$HOOK"; then
    echo "ADA hook pre-push lain di $HOOK — tidak ditimpa."
    echo "Integrasikan manual dengan menambahkan baris ini ke hook tersebut:"
    echo "  bash $SCRIPT"
    exit 1
fi

cat > "$HOOK" <<EOF
$MARK
#!/usr/bin/env bash
cd "\$(git rev-parse --show-toplevel)"
exec bash $SCRIPT
EOF
chmod +x "$HOOK"
echo "Hook pre-push terpasang di $HOOK — menjalankan bash $SCRIPT sebelum setiap push."
echo "Uji manual: bash $SCRIPT  |  Lepas: bash scripts/install_hooks.sh --remove"
