# Career Coach backend

## Terminal Qwen demo

The midway check-in demo connects the Python backend to a locally running Ollama
service, asks Qwen to greet the user and request a resume file path, then exits.
It does not read or upload a resume and does not wait for a reply.

1. Install and start [Ollama](https://ollama.com/).
2. Download the project's Qwen model:

   ```sh
   ollama pull qwen3.5:4b
   ```

3. From this directory, run:

   ```sh
   uv run python main.py
   ```

The demo defaults to `qwen3.5:4b`, matching the installed model shown in the
project setup. The default Ollama address is `http://127.0.0.1:11434`. Set
`OLLAMA_URL` if Ollama is hosted elsewhere, or set `CAREER_COACH_MODEL` to use
another installed Qwen model. If the service is unavailable or the model is
missing, the demo prints a setup error and exits.

## FastAPI

The API remains available separately:

```sh
uv run uvicorn main:app --reload
```

It exposes `/` and `/health`.
