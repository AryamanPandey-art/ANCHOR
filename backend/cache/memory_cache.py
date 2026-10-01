import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from anchor_ai.engine import IntelligenceEngine
from student_kit.schema import ContextDeeplinkResponse
from student_kit.verification import ActionVerifier


class MemoryCache:
    """In-memory static data cache, singleton engine holder, and context-safe response cache."""

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

        # Context-safe response cache storage
        self._exact_response_cache: Dict[str, ContextDeeplinkResponse] = {}
        self._semantic_response_cache: Dict[str, ContextDeeplinkResponse] = {}
        self._cache_stats: Dict[str, int] = {
            "cold_requests": 0,
            "repeat_hits": 0,
            "paraphrase_hits": 0,
            "misses": 0,
        }

        self.is_loaded = False

    @classmethod
    def get_instance(cls) -> "MemoryCache":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def compute_siis_hash(title: str, content: str) -> str:
        """Compute deterministic SHA256 digest over normalized SIIS title and content."""
        raw = f"{str(title or '').strip().lower()}:::{str(content or '').strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def compute_exact_key(siis_hash: str, query: str) -> str:
        """Compute exact query cache key strictly bound to SIIS context."""
        norm_q = " ".join(str(query or "").strip().lower().split())
        return f"{siis_hash}:exact:{norm_q}"

    @staticmethod
    def compute_semantic_key(siis_hash: str, direction: str) -> str:
        """Compute semantic paraphrase cache key strictly bound to SIIS context and direction."""
        norm_dir = str(direction or "null").strip().lower()
        return f"{siis_hash}:dir:{norm_dir}"

    def get_cached_response(
        self,
        exact_key: str,
        semantic_key: Optional[str] = None
    ) -> Tuple[Optional[ContextDeeplinkResponse], Optional[str]]:
        """Look up response in exact cache first, then semantic/paraphrase cache."""
        if exact_key in self._exact_response_cache:
            self._cache_stats["repeat_hits"] += 1
            return self._exact_response_cache[exact_key], "EXACT_HIT"
        if semantic_key and semantic_key in self._semantic_response_cache:
            self._cache_stats["paraphrase_hits"] += 1
            return self._semantic_response_cache[semantic_key], "PARAPHRASE_HIT"
        self._cache_stats["misses"] += 1
        return None, None

    def store_cached_response(
        self,
        exact_key: str,
        semantic_key: Optional[str],
        response: ContextDeeplinkResponse
    ) -> None:
        """Store verified response in exact and semantic context-safe caches."""
        self._exact_response_cache[exact_key] = response
        if semantic_key:
            self._semantic_response_cache[semantic_key] = response

    def clear_response_cache(self) -> None:
        """Reset dynamic response caches and tracking counters."""
        self._exact_response_cache.clear()
        self._semantic_response_cache.clear()
        self._cache_stats = {
            "cold_requests": 0,
            "repeat_hits": 0,
            "paraphrase_hits": 0,
            "misses": 0,
        }

    @property
    def cache_stats(self) -> Dict[str, int]:
        """Return shallow copy of cache hit/miss statistics."""
        return dict(self._cache_stats)

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

