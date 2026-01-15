import subprocess
import json

def call_llm(prompt: str) -> str:
    """
    Calls local Ollama LLaMA model.
    Returns raw text output.
    """
    process = subprocess.run(
        ["ollama", "run", "llama3.1:8b"],
        input=prompt,
        text=True,
        capture_output=True,
    )

    if process.returncode != 0:
        raise RuntimeError(process.stderr)

    return process.stdout.strip()