"""Agentic DCS Lab: governed simulation and read-only shadow research."""

from .runtime import ControlRuntime, RunResult
from .shadow import ShadowEvaluator, ShadowResult

__all__ = ["ControlRuntime", "RunResult", "ShadowEvaluator", "ShadowResult"]
__version__ = "0.2.0"

