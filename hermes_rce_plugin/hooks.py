"""Post tool-call hooks for RCE plugin."""

import json
import os

LOG_PATH = os.path.expanduser("~/.hermes/.rce_plugin.log")


def post_tool_call_hook(tool_name: str, args: dict, result: dict):
    """Log every tool call for auditing."""
    entry = {
        "tool": tool_name,
        "args": {k: v[:200] if isinstance(v, str) else v for k, v in args.items()},
        "result_summary": str(result)[:500]
    }
    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass
