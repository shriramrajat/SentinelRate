import time
from dataclasses import dataclass
from typing import Dict

@dataclass
class BucketState:
    tokens: float
    last_updated: float

class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: Max tokens the bucket can hold (Burst size).
        refill_rate: Tokens added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        # The "Database" (In-Memory for now)
        self._buckets: Dict[str, BucketState] = {}

    def _get_current_time(self) -> float:
        return time.monotonic()

        # Update the type hint if you wish, or just use the logic
    
    # Pass limits dynamically
    def allow_request(self, identifier: str, capacity: int, refill_rate: float, cost: int = 1):
        now = self._get_current_time()
        
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