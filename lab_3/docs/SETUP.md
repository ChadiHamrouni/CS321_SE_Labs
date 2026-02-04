# Lab 3 Setup

## Prerequisites

### 1. Install Ollama
Download and install from: **https://ollama.com**

### 2. Pull a Model
```bash
ollama pull llama3.2
```

### 3. Install Python Dependencies
```bash
cd lab_3/code
pip install -r requirements.txt
```

## Verify Setup

Test that everything works:
```bash
python exercise_1_temperature.py
```

If you see outputs, you're ready! ✅

## Troubleshooting

**"Module not found: ollama"**
```bash
pip install ollama
```

**"Connection refused"**
- Make sure Ollama is running
- Windows: Check system tray
- Or run: `ollama serve`

**Model not found**
```bash
ollama pull llama3.2
```

**Model too slow**
Use a smaller model:
```bash
ollama pull llama3.2:1b
# or
ollama pull phi3.5
```

Then change `model='llama3.2'` in the code to your model name.

---

**That's it! You're ready to start the exercises.** 🚀
