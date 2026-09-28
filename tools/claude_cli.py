"""Headless Claude Code subagent calls (`claude -p`), configured to be as close
to a bare API call as the CLI allows: empty system prompt, no tools, no
settings/MCP/skills, no thinking, no prompt caching. Prompt goes via stdin
(argv is capped at 128 KB per argument)."""
import json
import os
import subprocess
import time

MODEL_ALIASES = {"haiku": "haiku", "sonnet": "sonnet", "opus": "opus"}
BASE_ARGS = [
    "claude", "-p",
    "--system-prompt", "",
    "--tools", "",
    "--setting-sources", "",
    "--strict-mcp-config",
    "--disable-slash-commands",
    "--no-session-persistence",
    "--output-format", "json",
    "--effort", "low",
]
# The parent session exports CLAUDE_EFFORT=high; pin the lowest effort for every model
# (Opus 5.5 still uses adaptive thinking that the CLI cannot switch off; see DEVIATIONS D5).
ENV = dict(os.environ, MAX_THINKING_TOKENS="0", DISABLE_PROMPT_CACHING="1", CLAUDE_EFFORT="low")


def call(model: str, prompt: str, retries: int = 3, timeout: int = 600) -> dict:
    """Returns a dict with result text, usage, served model id(s), cost, error."""
    last_err = None
    for attempt in range(retries + 1):
        t0 = time.time()
        try:
            proc = subprocess.run(
                BASE_ARGS + ["--model", MODEL_ALIASES[model]],
                input=prompt, capture_output=True, text=True, env=ENV, timeout=timeout,
                cwd="/tmp",
            )
            data = json.loads(proc.stdout)
            if data.get("is_error") or data.get("subtype") != "success":
                raise RuntimeError(f"cli error: {str(data)[:500]}")
            u = data["usage"]
            return {
                "ok": True,
                "text": data.get("result", ""),
                "input_total": u["input_tokens"] + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
                "input_tokens": u["input_tokens"],
                "cache_creation": u.get("cache_creation_input_tokens", 0),
                "cache_read": u.get("cache_read_input_tokens", 0),
                "output_tokens": u["output_tokens"],
                "thinking_tokens": (u.get("output_tokens_details") or {}).get("thinking_tokens"),
                "served_models": sorted(data.get("modelUsage", {}).keys()),
                "cost_usd": data.get("total_cost_usd", 0.0),
                "duration_ms": data.get("duration_ms"),
                "attempts": attempt + 1,
                "wall_s": round(time.time() - t0, 2),
            }
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e}"[:800]
            time.sleep(2 ** attempt * 3)
    return {"ok": False, "error": last_err, "attempts": retries + 1}
