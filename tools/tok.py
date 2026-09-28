"""Tokenizer loaders. Run tools/setup_tokenizers.sh first."""
import hashlib
import os
import shutil
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK_DIR = ROOT / "build" / "tokenizers"
O200K_URL = "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken"


@lru_cache(maxsize=None)
def o200k():
    """tiktoken's own o200k_base, fed the rebuilt file through its cache.

    tiktoken checks the file against its pinned sha256, so this is the exact
    official encoding or it raises."""
    cache = TOK_DIR / "tiktoken-cache"
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / hashlib.sha1(O200K_URL.encode()).hexdigest()
    if not target.exists():
        shutil.copy(TOK_DIR / "o200k_base.tiktoken", target)
    os.environ["TIKTOKEN_CACHE_DIR"] = str(cache)
    import tiktoken

    return tiktoken.get_encoding("o200k_base")


@lru_cache(maxsize=None)
def qwen3():
    from tokenizers import Tokenizer

    return Tokenizer.from_file(str(TOK_DIR / "qwen3-tokenizer.json"))


def count_o200k(text: str) -> int:
    return len(o200k().encode(text, disallowed_special=()))


def count_qwen3(text: str) -> int:
    return len(qwen3().encode(text, add_special_tokens=False).ids)
