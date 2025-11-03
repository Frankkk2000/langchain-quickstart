# LangChain Quickstart

Simple and easy way to start learning LangChain

## Pre requisites

### Python 3.13.0

- Python 3.13.0 

Installing [`pyenv`](https://github.com/pyenv/pyenv) is optional but recommended for managing Python versions.

```bash
pyenv install 3.13.0
pyenv local 3.13.0
```

### Install Ollama
Follow the instructions at [https://ollama.com/download/](https://ollama.com/download/) to install Ollama on your system.

### Install and run a local model
```bash
ollama serve
ollama pull llama3.2
```

## Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate
```

## Install Python dependencies

```bash
pip install langchain==1.0.3 langchain-ollama==1.0.0
```

or install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Run the example

```bash
python main.py
```

You should an output similar to:

```
Fog-get about it, it's always raining in San Francisco!
```

