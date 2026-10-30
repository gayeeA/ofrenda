"""Local speech-to-text with faster-whisper (open-weight Whisper). Audio never leaves the machine."""
import os


def transcribe(path: str, language=None) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise SystemExit("Audio needs: pip install faster-whisper   (or pass --text / --text-file)")
    model = WhisperModel(os.environ.get("OFRENDA_WHISPER", "small"), compute_type="int8")
    segments, info = model.transcribe(path, language=language, vad_filter=True)
    text = " ".join(s.text.strip() for s in segments)
    print(f"  (transcribed {info.duration:.0f}s of audio, language: {info.language})")
    return text
