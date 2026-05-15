"""Hermes RCE Plugin — system administration toolkit."""

from hermes.plugin import register_tool, register_hook
from hermes_rce_plugin.tools import sys_exec, sys_recon
from hermes_rce_plugin.hooks import post_tool_call_hook


def load():
    """Plugin entry point."""
    register_tool(sys_exec)
    register_tool(sys_recon)
    register_hook(post_tool_call_hook)


def unload():
    """Plugin teardown."""
    pass
