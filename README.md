# Whisper on device

Open-source, on-device voice dictation for macOS. Press Cmd+Control to record, speak naturally, and have text appear in any app.

## Features

- **System-wide**: Works in any app (Slack, Gmail, Cursor, etc.)
- **Fast**: ~0.5-1s on Apple Silicon (MLX), ~2-3s on Intel
- **Private**: Everything runs on-device, no cloud
- **Free**: Uses open-source models
- **Simple**: Hold Cmd+Control to record
- **Smart Cleanup**: Optional LLM post-processing via Ollama (removes filler words, fixes grammar)

## Installation

### 1. Install Dependencies

```bash
# Install PortAudio (required for PyAudio)
brew install portaudio

# Install Python packages
pip3 install -r requirements.txt
```

### 2. Grant Permissions

On first run, macOS will request:
- **Microphone Access**: Allow
- **Accessibility Access**: System Settings → Privacy & Security → Accessibility → Add Python
- **Input Monitoring**: System Settings → Privacy & Security → Input Monitoring → Add Python

## Usage

### Start the app:

```bash
python3 main.py
```

A status icon will appear in your menu bar:
- **○** — Idle (ready to record)
- **●** — Recording in progress
- **◐** — Processing transcription

### Use it:

1. Click into any text field
2. Hold **Cmd+Control** together
3. Speak naturally
4. Release the keys
5. Text appears!

### Quit:

Click the menu bar icon → Quit

## How It Works

```
Hold Cmd+Control → Record → Release → Whisper → [Ollama Cleanup] → Text Injection
```

- **MLX Whisper**: Apple Silicon optimized (2-3x faster) - auto-detected
- **Faster Whisper**: Fallback for Intel Macs
- **Ollama**: Optional LLM cleanup (auto-detected)
- **PyAudio**: Microphone capture
- **pynput**: Keyboard automation
- **rumps**: Menu bar UI

### Performance

| Mac Type | Backend | Latency |
|----------|---------|---------|
| Apple Silicon (M1/M2/M3/M4) | MLX Whisper | ~0.5-1s |
| Intel Mac | Faster Whisper | ~2-3s |

The backend is automatically selected based on your hardware.

## LLM Cleanup (Optional)

Whisper on device can use Ollama to clean up transcriptions — removing filler words (um, uh, like), fixing grammar, and adding punctuation.

**Note:** This feature is disabled by default. To enable it, edit `main.py` and change `enabled=False` to `enabled=True`.

### Setup

```bash
# Install Ollama
brew install ollama

# Pull a fast, small model
ollama pull llama3.2:1b

# Start Ollama (runs in background)
ollama serve
```

### How it works

- LLM cleanup is **disabled by default** (raw transcription is used)
- To enable: set `enabled=True` in `main.py`
- If enabled and Ollama is running, cleanup is automatic
- If Ollama is not running, raw transcription is used (still works!)

### Example

| Before (raw) | After (cleaned) |
|--------------|-----------------|
| "So um I was thinking that uh we should like maybe go to the store" | "I was thinking that we should go to the store." |

## Configuration

Edit `transcriber.py` to change model size:
- `tiny`: Fastest, least accurate
- `base`: Good balance (default)
- `small`: More accurate, slower
- `medium`: Very accurate, much slower
- `large`: Most accurate, slowest

## Troubleshooting

**"No audio recorded"**
- Check microphone permissions
- Ensure microphone is working

**"Permission denied"**
- Grant Accessibility and Input Monitoring permissions in System Settings

**Slow transcription**
- On Apple Silicon: Ensure MLX Whisper is installed (`pip install mlx-whisper`)
- Use `tiny` model instead of `base`
- Check CPU usage

**Text not appearing**
- Ensure Accessibility permissions are granted
- Try clicking in the text field again

## Credits

Built with:
- [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) - Apple Silicon optimized
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper) - Intel fallback
- [Ollama](https://ollama.ai) - Local LLM for text cleanup
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- [pynput](https://github.com/moses-palmer/pynput)
- [rumps](https://github.com/jaredks/rumps)
