"""
Transcrição com WhisperX (roda DENTRO da venv whisperx_env).
Gera timestamps por palavra precisos (forced alignment wav2vec2, ~±50ms),
resolvendo o drift que o faster-whisper com VAD causava.

Uso (chamado pelo pipeline via subprocess):
    whisperx_env\\Scripts\\python.exe transcrever_whisperx.py <video> <saida.json> [modelo]

Saída JSON: lista de {"start", "end", "text", "words": [{"word","start","end"}]}
com tempos alinhados ao tempo REAL do vídeo.
"""

import json
import sys


def carregar_audio_pyav(caminho: str, sr: int = 16000):
    """
    Carrega o áudio em float32 mono 16kHz usando PyAV (sem depender do ffmpeg CLI,
    que não está instalado). É o formato que o WhisperX espera (array numpy).
    """
    import av
    import numpy as np

    amostras = []
    with av.open(caminho) as container:
        stream = next(s for s in container.streams if s.type == "audio")
        resampler = av.AudioResampler(format="flt", layout="mono", rate=sr)
        for frame in container.decode(stream):
            for f in resampler.resample(frame):
                amostras.append(f.to_ndarray().reshape(-1))
    if not amostras:
        return np.zeros(0, dtype=np.float32)
    return np.concatenate(amostras).astype(np.float32)


def main():
    video_path = sys.argv[1]
    saida = sys.argv[2]
    modelo = sys.argv[3] if len(sys.argv) > 3 else "medium"
    idioma = sys.argv[4] if len(sys.argv) > 4 else "pt"

    import whisperx

    device = "cpu"
    compute_type = "int8"

    print(f"[WhisperX] Carregando modelo {modelo} (cpu/int8)...", flush=True)
    model = whisperx.load_model(modelo, device, compute_type=compute_type, language=idioma)

    print("[WhisperX] Carregando áudio (PyAV, sem ffmpeg)...", flush=True)
    audio = carregar_audio_pyav(video_path)

    print("[WhisperX] Transcrevendo...", flush=True)
    result = model.transcribe(audio, batch_size=4, language=idioma)

    print("[WhisperX] Carregando modelo de alinhamento (PT) e alinhando...", flush=True)
    align_model, metadata = whisperx.load_align_model(language_code=idioma, device=device)
    aligned = whisperx.align(
        result["segments"], align_model, metadata, audio, device,
        return_char_alignments=False,
    )

    segmentos = []
    for seg in aligned["segments"]:
        palavras = []
        for w in seg.get("words", []):
            # alguns tokens podem vir sem start/end (pontuação) — pula esses
            if "start" in w and "end" in w:
                palavras.append({
                    "word": w.get("word", ""),
                    "start": float(w["start"]),
                    "end": float(w["end"]),
                })
        # start/end do segmento: usa o das palavras quando o do segmento faltar
        s_ini = seg.get("start")
        s_fim = seg.get("end")
        if s_ini is None and palavras:
            s_ini = palavras[0]["start"]
        if s_fim is None and palavras:
            s_fim = palavras[-1]["end"]
        if s_ini is None or s_fim is None:
            continue
        segmentos.append({
            "start": float(s_ini),
            "end": float(s_fim),
            "text": seg.get("text", "").strip(),
            "words": palavras,
        })

    with open(saida, "w", encoding="utf-8") as f:
        json.dump(segmentos, f, ensure_ascii=False, indent=2)

    print(f"[WhisperX] OK: {len(segmentos)} segmentos salvos em {saida}", flush=True)


if __name__ == "__main__":
    main()
