"""Catalog and internal data models."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ValidationEntry(BaseModel):
    deeplink: Optional[str] = None
    key: Optional[str] = None


class CatalogEntry(BaseModel):
    id: str
    deeplink: str
    description: str
    message: str
    originalType: Optional[str] = None
    control_type: Optional[str] = None
    qna_description: Optional[str] = None
    validation: Optional[ValidationEntry] = None


class DeeplinkCatalog(BaseModel):
    count: int = 0
    deeplinks: List[CatalogEntry] = Field(default_factory=list)
