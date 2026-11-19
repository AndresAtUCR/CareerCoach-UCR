"""Career Coach API and terminal-only Qwen demo."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
QWEN_MODEL = os.getenv("CAREER_COACH_MODEL", "qwen3.5:4b")
RESUME_PROMPT = (
    "You are Qwen, the AI assistant for Career Coach. Greet the user briefly and ask them "
    "to provide the path to their resume file (PDF or DOCX) when they are ready. "
    "Do not ask anything else."
)

app = FastAPI(title="Career Coach API", description="API for Career Coach Application", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Hello World! Your FastAPI backend is running seamlessly."}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def ask_qwen_for_resume_prompt():
    """Generate the demo's opening resume request using the local Ollama service."""
    request = Request(
        f"{OLLAMA_URL.rstrip('/')}/api/generate",
        data=json.dumps(
            {"model": QWEN_MODEL, "prompt": RESUME_PROMPT, "stream": False}
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama returned HTTP {error.code}: {details}") from error
    except URLError as error:
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}. Start Ollama, then run this demo again."
        ) from error

    generated_text = result.get("response", "").strip()
    if not generated_text:
        raise RuntimeError("Ollama returned an empty response from Qwen.")
    return generated_text


def run_demo():
    """Print Qwen's opening prompt and stop before collecting a resume."""
    print(f"Starting Career Coach demo with {QWEN_MODEL}...", flush=True)
    try:
        print(f"\nQwen: {ask_qwen_for_resume_prompt()}")
    except (RuntimeError, TimeoutError) as error:
        print(f"\nDemo could not start: {error}", file=sys.stderr)
        print(
            f"Confirm Ollama is running and the model is installed (ollama pull {QWEN_MODEL}).",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    run_demo()
