"""Minimal Anthropic-compatible Messages client (stdlib) with disk cache. Credentials come from env only."""
from __future__ import annotations

import hashlib
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path


class LLMUnavailable(RuntimeError):
    pass


def _ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    for var in ("PMDC_CA_BUNDLE", "SSL_CERT_FILE", "NODE_EXTRA_CA_CERTS"):  # corporate proxy CA bundles
        p = os.environ.get(var)
        if p and os.path.exists(p):
            ctx.load_verify_locations(p)
    return ctx


class LLM:
    def __init__(self, model: str | None = None, cache_dir: str | Path | None = None, cache_only: bool = False):
        self.model = model or os.environ.get("PMDC_MODEL", "claude-sonnet-5-5")
        self.base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
        self.token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
        self.key = os.environ.get("ANTHROPIC_API_KEY")
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.cache_only = cache_only
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def available(self) -> bool:
        return bool(self.token or self.key)

    def complete(self, system: str, user: str, max_tokens: int = 2000, salt: str = "") -> dict:
        """Returns {'text','input_tokens','output_tokens','latency_s','cached'}. `salt` separates repeat runs in the cache."""
        h = hashlib.sha256(json.dumps([self.model, system, user, salt], sort_keys=True).encode()).hexdigest()[:24]
        path = self.cache_dir / f"{h}.json" if self.cache_dir else None
        if path and path.exists():
            d = json.loads(path.read_text())
            d["cached"] = True
            return d
        if self.cache_only:
            raise LLMUnavailable(f"cache miss for {h} and --cache-only is set")
        if not self.available():
            raise LLMUnavailable("Set ANTHROPIC_AUTH_TOKEN or ANTHROPIC_API_KEY (and optionally ANTHROPIC_BASE_URL).")
        headers = {"content-type": "application/json", "anthropic-version": "2023-06-01"}
        if self.token:
            headers["authorization"] = "Bearer " + self.token
        if self.key:
            headers["x-api-key"] = self.key
        body = json.dumps({"model": self.model, "max_tokens": max_tokens, "system": system,
                           "messages": [{"role": "user", "content": user}]}).encode()
        last = None
        for attempt in range(4):
            t0 = time.time()
            try:
                req = urllib.request.Request(self.base + "/v1/messages", data=body, headers=headers)
                with urllib.request.urlopen(req, timeout=120, context=_ctx()) as r:
                    resp = json.loads(r.read())
                text = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
                usage = resp.get("usage", {})
                d = {"text": text, "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0),
                     "latency_s": round(time.time() - t0, 2), "cached": False, "model": self.model}
                if path:
                    path.write_text(json.dumps(d))
                return d
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code not in (408, 429, 500, 502, 503, 529):
                    raise LLMUnavailable(last) from e
            except (urllib.error.URLError, TimeoutError) as e:
                last = str(e)
            time.sleep(2 ** attempt)
        raise LLMUnavailable(f"LLM call failed after retries: {last}")
