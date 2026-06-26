#!/bin/bash
# ============================================================
#  ELTON VIDEO MAKER - Abrir (macOS)
#  Duplo-clique para abrir o programa no navegador.
# ============================================================
cd "$(dirname "$0")"

PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  echo "[X] Python 3 nao encontrado. Rode o INSTALAR.command primeiro."
  read -r -p "Pressione Enter para fechar..."
  exit 1
fi

echo "Abrindo o ELTON VIDEO MAKER... (a janela do navegador abre sozinha)"
echo "Para fechar o programa, feche esta janela do Terminal."
"$PY" elton_video_maker.py
