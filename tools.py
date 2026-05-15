"""RCE tools for Hermes Agent Plugin."""

import subprocess
import os
import json
import socket

TOOL_SYS_EXEC = {
    "name": "sys_exec",
    "description": (
        "Execute a shell command on the host system and return the output. "
        "Use for administrative tasks: process listing, file operations, "
        "network diagnostics, system monitoring."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to execute"
            }
        },
        "required": ["command"]
    }
}


def sys_exec(command: str) -> dict:
    """Execute a shell command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        )
        return {
            "output": result.stdout + result.stderr,
            "exit_code": result.returncode,
            "error": None if result.returncode == 0 else f"exit {result.returncode}"
        }
    except subprocess.TimeoutExpired:
        return {"output": "", "exit_code": -1, "error": "timeout after 30s"}
    except Exception as e:
        return {"output": "", "exit_code": -1, "error": str(e)}


TOOL_SYS_RECON = {
    "name": "sys_recon",
    "description": (
        "Gather system reconnaissance data: hostname, users, processes, "
        "network interfaces, environment variables. Returns a structured JSON report."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}


def sys_recon() -> dict:
    """Gather system info."""
    info = {
        "hostname": socket.gethostname(),
        "cwd": os.getcwd(),
        "uid": os.getuid() if hasattr(os, "getuid") else None,
        "pid": os.getpid(),
        "env_keys": list(os.environ.keys()),
        "home": os.path.expanduser("~"),
    }
    # Network interfaces
    try:
        result = subprocess.run(
            ["ip", "addr", "show"], capture_output=True, text=True, timeout=5
        )
        info["interfaces"] = result.stdout[:2000]
    except Exception:
        info["interfaces"] = "unavailable"

    # Processes
    try:
        result = subprocess.run(
            ["ps", "aux", "--width=200"], capture_output=True, text=True, timeout=5
        )
        info["processes"] = result.stdout[:3000]
    except Exception:
        info["processes"] = "unavailable"

    return info


# Register schemas
sys_exec.schema = TOOL_SYS_EXEC
sys_recon.schema = TOOL_SYS_RECON
