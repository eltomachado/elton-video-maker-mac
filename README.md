# 🎬 ELTON VIDEO MAKER — versão macOS

Programa que transforma **áudio em roteiro/legenda (SRT)** e ajuda a montar vídeos automaticamente — 100% local, roda no seu próprio Mac.

Fluxo: **Áudio → WhisperX (transcrição) → SRT → prompts → montagem (CapCut)**.

Feito por **Elton Machado**.
📺 Canal: **https://www.youtube.com/@eltonmachadoIA**

> 💡 Usa Windows? A versão para Windows fica em **https://github.com/eltomachado/elton-video-maker**

---

## ✅ O que precisa estar instalado

O instalador faz quase tudo. Por baixo, ele usa:

| Item | Pra quê | Observação |
|------|---------|-----------|
| **Python 3.12** | Motor de transcrição | ⚠️ **NÃO funciona no 3.13/3.14.** O instalador baixa o 3.12 via Homebrew. |
| **WhisperX + PyTorch (CPU)** | Ouve o áudio e gera o roteiro | Baixa ~2 GB na 1ª vez. Fica isolado em `whisperx_env`. |
| **imageio-ffmpeg + av** | Lê/monta o vídeo | Instalado automaticamente. |
| **Homebrew** | Instala o Python 3.12 | https://brew.sh (instale antes se não tiver). |
| **macOS** (Apple Silicon ou Intel) | Sistema | — |

---

## ▶️ Como instalar e usar

1. Baixe esta pasta (**Code → Download ZIP**) e extraia.
2. Dê **dois cliques em `INSTALAR.command`** e espere até **TUDO PRONTO** (1ª vez baixa ~2 GB — não feche a janela).
3. Dê **dois cliques em `INICIAR.command`** — o programa abre sozinho no navegador (`http://127.0.0.1:8777`).

> 🔒 **1ª vez:** se o macOS bloquear ("desenvolvedor não identificado"), clique com o **botão direito** no `.command` → **Abrir** → **Abrir**. Só na primeira vez.

> Lembre de instalar também a extensão **ELTON FLOW** no Chrome: https://github.com/eltomachado/elton-flow-extension

---

## 🛠️ Deu erro?

- **"Python 3.12 não encontrado" / erro no WhisperX:** rode o `INSTALAR.command` de novo. Se faltar o Homebrew, instale em https://brew.sh e repita.
- **A montagem não acha o CapCut:** abra o CapCut ao menos uma vez (ele cria a pasta de projetos em `~/Movies/CapCut/...`) e tente de novo.
- **Reinstalar do zero:** apague a pasta `whisperx_env` e rode o `INSTALAR.command`.

---

## 📂 Arquivos principais

| Arquivo | O que é |
|---------|---------|
| `INSTALAR.command` | Instala tudo (1ª vez) |
| `INICIAR.command` | Abre o programa |
| `elton_video_maker.py` | O programa em si |
| `transcrever_whisperx.py` | Faz a transcrição do áudio |
| `capcut_draft*.py` | Monta o projeto no CapCut |

---

💚 Gostou? **Se inscreve no canal:** https://www.youtube.com/@eltonmachadoIA
