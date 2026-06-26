#!/bin/bash
# ============================================================
#  ELTON VIDEO MAKER - Instalacao automatica (macOS)
#  Duplo-clique. Na 1a vez baixa ~2 GB (WhisperX + PyTorch).
# ============================================================
set -e
cd "$(dirname "$0")"

echo "============================================================"
echo "  ELTON VIDEO MAKER - INSTALACAO (macOS)"
echo "============================================================"

# ── 1) Python 3.12 (o 3.13/3.14 quebra o WhisperX: ctranslate2) ──
echo ""
echo ">> 1/3  Procurando o Python 3.12..."
PY312=""
for c in python3.12 /opt/homebrew/bin/python3.12 /usr/local/bin/python3.12; do
  if command -v "$c" >/dev/null 2>&1; then PY312="$(command -v "$c")"; break; fi
done

if [ -z "$PY312" ]; then
  echo "   Python 3.12 nao encontrado. Vou instalar via Homebrew."
  if ! command -v brew >/dev/null 2>&1; then
    echo "   [X] Homebrew nao instalado."
    echo "       Instale em https://brew.sh e rode o INSTALAR.command de novo."
    read -r -p "Pressione Enter para fechar..."
    exit 1
  fi
  brew install python@3.12
  PY312="$(brew --prefix)/bin/python3.12"
fi
echo "   [OK] $($PY312 --version)"

# ── 2) Componentes do app principal (montagem) ──
echo ""
echo ">> 2/3  Instalando componentes do app (imageio-ffmpeg, av)..."
python3 -m pip install --user --quiet imageio-ffmpeg av 2>/dev/null \
  || python3 -m pip install --break-system-packages --quiet imageio-ffmpeg av
echo "   [OK] Componentes instalados."

# ── 3) Motor de transcricao (WhisperX) em ambiente isolado 3.12 ──
echo ""
echo ">> 3/3  Instalando o WhisperX + PyTorch (~2 GB)... NAO feche a janela."
rm -rf whisperx_env
"$PY312" -m venv whisperx_env
whisperx_env/bin/python -m pip install --quiet --upgrade pip
whisperx_env/bin/python -m pip install whisperx av
echo "   [OK] Motor de transcricao instalado."

echo ""
echo "============================================================"
echo "  TUDO PRONTO! Abra o programa com INICIAR.command"
echo "============================================================"
read -r -p "Pressione Enter para fechar..."
