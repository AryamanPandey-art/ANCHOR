"""Internal backend data structures."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VerifiedActionInternal(BaseModel):
    action_name: str
    description: str
    steps: List[str]
    category: str = "manual"
    confidence: float = 1.0
    actionable_deeplink: Optional[str] = None
    validation_deeplink: Optional[str] = None
    validation_key: Optional[str] = None
    catalog_id: Optional[str] = None
    verification_reason: str = "Verified"
