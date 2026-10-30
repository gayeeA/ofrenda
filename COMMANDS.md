# Ofrenda commands (Windows PowerShell)

Open PowerShell and move into the project folder:

```powershell
Set-Location 'C:\Users\HP\Downloads\ofrenda'
```

## Set up once

A project-local virtual environment keeps Python packages inside this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `requirements.txt` package enables optional audio transcription. The core commands use Python's standard library.

## Local models

Ollama is already installed on this computer, and `gemma3:4b` is available as the chat model. The embedding model `nomic-embed-text` is downloaded too. Set these for the current PowerShell window before using `remember` or `ask`:

```powershell
$env:OFRENDA_MODEL = 'gemma3:4b'
$env:OFRENDA_EMBED_MODEL = 'nomic-embed-text'
ollama list
```

If a model is missing on another computer, download it with:

```powershell
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

## Use it

Run the CLI through the project Python so activation is not required:

```powershell
$py = '.\.venv\Scripts\python.exe'
& $py -m ofrenda --help

& $py -m ofrenda add 'Abuela Rosa' --born 1931 --died 2019 `
  --foods 'tamales,champurrado' --songs 'Cielito Lindo' --items 'blue rebozo'

& $py -m ofrenda story abuela-rosa --text 'Every December she sang while stirring the masa.' --teller 'Mamá'
& $py -m ofrenda story abuela-rosa --text-file '.\story.txt' --teller 'Tía'
& $py -m ofrenda people
& $py -m ofrenda remember abuela-rosa
& $py -m ofrenda ask abuela-rosa 'What did she cook at Christmas?'
& $py -m ofrenda build --title 'Ofrenda de la familia' --out '.\ofrenda.html'
```

Audio transcription (optional):

```powershell
$env:HF_HOME = Join-Path (Get-Location) '.cache\huggingface'
$env:OFRENDA_WHISPER = 'small'
& $py -m ofrenda story abuela-rosa --audio '.\grandma-kitchen.m4a' --teller 'Mamá' --language es
```

The first audio transcription downloads the Whisper `small` model into `.cache\huggingface` in this project; later runs can work offline. To use a smaller model, set `$env:OFRENDA_WHISPER = 'tiny'` before the first audio command.

## Data and output

By default, stories and profiles are written to `.\ofrenda_data` under the current folder, and the built page is `ofrenda.html`. Keep a backup of `ofrenda_data`; it contains the family stories and profile details. Set a different data folder for the current PowerShell window with:

```powershell
$env:OFRENDA_HOME = 'D:\OfrendaData'
```

Ollama prompts stay on this computer at `localhost`. The generated HTML is a standalone file.

## Check the setup

Run these from the project folder to confirm the Python environment, dependency, CLI, Ollama models, and downloaded Whisper model:

```powershell
Set-Location 'C:\Users\HP\Downloads\ofrenda'
$py = '.\.venv\Scripts\python.exe'
$env:HF_HOME = Join-Path (Get-Location) '.cache\huggingface'

Test-Path $py
& $py --version
& $py -m pip show faster-whisper
& $py -m pip check
& $py -m ofrenda --help

Get-Command ollama | Select-Object Source
ollama --version
ollama list

Get-ChildItem '.cache\huggingface\hub\models--Systran--faster-whisper-small' -Recurse -Filter 'model.bin' |
  Select-Object FullName, @{Name='SizeMB'; Expression={[math]::Round($_.Length / 1MB, 1)}}
```

Expected results: `Test-Path` returns `True`; pip shows `faster-whisper` 1.2.1 and `pip check` reports no broken requirements; `ofrenda --help` lists commands; `ollama list` includes `gemma3:4b` and `nomic-embed-text`; and the Whisper check finds `model.bin` at about 461 MB.

## What was set up

- `.venv` was created inside this project; `requirements.txt` installed `faster-whisper` and its Python dependencies there.
- Ollama was already installed. The existing `gemma3:4b` chat model was reused; `nomic-embed-text` (274 MB) was downloaded for story search.
- Whisper `small` (about 464 MB) was downloaded into this project’s `.cache\huggingface` folder for audio transcription.
- `COMMANDS.md` contains the usage examples, and `.gitignore` excludes the virtual environment, model cache, story data, and generated HTML.
- No people, stories, or HTML memorial were created. No project tests were run.
