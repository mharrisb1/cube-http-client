from typing import Any, Type

from pydantic import BaseModel

__all__ = ["model_build_recursive"]


def model_build_recursive(m: Type[BaseModel], **kwargs: Any) -> None:
    if hasattr(m, "model_rebuild"):
        return getattr(m, "model_rebuild")(**kwargs)
    else:
        return getattr(m, "update_forward_refs")(**kwargs)
