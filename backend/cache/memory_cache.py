"""In-memory cache and singleton provider for static data and shared engines."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from anchor_ai.engine import IntelligenceEngine
from student_kit.verification import ActionVerifier


class MemoryCache:
    """In-memory static data cache and singleton engine holder."""

    _instance: Optional["MemoryCache"] = None

    def __init__(self, root_dir: Optional[Path] = None):
        if root_dir is None:
            root_dir = Path(__file__).parent.parent.parent / "student_kit"
        self.root_dir = Path(root_dir)

        self.deeplinks_path = self.root_dir / "deeplinks.json"
        self.siis_responses_path = self.root_dir / "siis_responses.json"

        self.deeplinks_raw: Dict[str, Any] = {}
        self.valid_deeplink_uris: Set[str] = set()
        self.allowed_placeholders: Set[str] = {"bixby://dummy_positive"}
        self.siis_responses_raw: Dict[str, Any] = {}

        self.engine: Optional[IntelligenceEngine] = None
        self.verifier: Optional[ActionVerifier] = None

        self.is_loaded = False

    @classmethod
    def get_instance(cls) -> "MemoryCache":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self) -> None:
        """Load static json files and initialize shared engines."""
        if self.is_loaded:
            return

        # 1. Load deeplinks.json
        if self.deeplinks_path.exists():
            with open(self.deeplinks_path, "r", encoding="utf-8") as f:
                self.deeplinks_raw = json.load(f)

            entries = self.deeplinks_raw.get("deeplinks", [])
            for entry in entries:
                act_uri = entry.get("deeplink")
                if act_uri:
                    self.valid_deeplink_uris.add(act_uri)
                val_dict = entry.get("validation") or {}
                val_uri = val_dict.get("deeplink")
                if val_uri:
                    self.valid_deeplink_uris.add(val_uri)

        # 2. Load siis_responses.json
        if self.siis_responses_path.exists():
            with open(self.siis_responses_path, "r", encoding="utf-8") as f:
                self.siis_responses_raw = json.load(f)

        # 3. Shared IntelligenceEngine instance (disable LLM by default or use standard)
        self.engine = IntelligenceEngine(enable_llm=False)

        # 4. Shared ActionVerifier instance
        self.verifier = ActionVerifier(catalog_path=str(self.deeplinks_path) if self.deeplinks_path.exists() else None)

        self.is_loaded = True

    def is_valid_deeplink(self, uri: str) -> bool:
        """Check if URI is a known catalog deeplink or allowed placeholder."""
        if not uri:
            return False
        return (uri in self.valid_deeplink_uris) or (uri in self.allowed_placeholders)


def get_cache() -> MemoryCache:
    """Dependency helper to get the initialized MemoryCache singleton."""
    cache = MemoryCache.get_instance()
    if not cache.is_loaded:
        cache.load()
    return cache
