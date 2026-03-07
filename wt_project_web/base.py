"""Re-export base classes from wt-project-base.

All base classes and dataclasses are defined in wt-project-base.
This module re-exports them for backward compatibility.
"""

from wt_project_base.base import (
    OrchestrationDirective,
    ProjectType,
    ProjectTypeInfo,
    TemplateInfo,
    VerificationRule,
)

__all__ = [
    "OrchestrationDirective",
    "ProjectType",
    "ProjectTypeInfo",
    "TemplateInfo",
    "VerificationRule",
]
