import time
from dataclasses import dataclass
from typing import Dict

@dataclass
class BucketState:
    tokens: float
    last_updated: float

class TokenBucketLimiter:
    def __init__(self):
        """
        Initializes the TokenBucketLimiter with an empty state.
        Limits are now passed dynamically per request.
        """
        # The "Database" (In-Memory for now)
        self._buckets: Dict[str, BucketState] = {}
        # Optimization: Clean up stale entries periodically
        self._ops_count: int = 0
        self._cleanup_interval: int = 1000  # Check every 1000 requests

    def _get_current_time(self) -> float:
        return time.monotonic()

    def _cleanup_stale_buckets(self, current_time: float, ttl: int = 300):
        """
        Remove buckets not updated in 'ttl' seconds (default 5 mins).
        """
        # Identifying stale keys
        expired_keys = [
            k for k, v in self._buckets.items()
            if (current_time - v.last_updated) > ttl
        ]
        # Deleting them
        for k in expired_keys:
            del self._buckets[k]

    # Pass limits dynamically
    def allow_request(self, identifier: str, capacity: int, refill_rate: float, cost: int = 1):
        now = self._get_current_time()
        
        # 🧹 LAZY CLEANUP CHECK
        self._ops_count += 1
        if self._ops_count >= self._cleanup_interval:
            self._cleanup_stale_buckets(now)
            self._ops_count = 0  # Reset counter

        if identifier not in self._buckets:
            self._buckets[identifier] = BucketState(
                tokens=float(capacity), # Start full based on THEIR limit
                last_updated=now
            )
        
        bucket = self._buckets[identifier]
        # Refill
        time_passed = now - bucket.last_updated
        new_tokens = time_passed * refill_rate
        
        # Clamp to CURRENT capacity (e.g. if user upgraded plan)
        bucket.tokens = min(float(capacity), bucket.tokens + new_tokens)
        bucket.last_updated = now
        # ... (rest is same: consume and return tuple) ...
        # (Copy the decision logic from yesterday here)
        if bucket.tokens >= cost:
             bucket.tokens -= cost
             return (True, int(bucket.tokens), 0.0)
        else:
             tokens_needed = cost - bucket.tokens
             wait_time = tokens_needed / refill_rate
             return (False, int(bucket.tokens), wait_time)