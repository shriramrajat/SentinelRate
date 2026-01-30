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

    def allow_request(self, identifier: str, cost: int = 1) -> bool:
        now = self._get_current_time()
        
        # 1. Get or Create Bucket
        if identifier not in self._buckets:
            self._buckets[identifier] = BucketState(
                tokens=float(self.capacity),
                last_updated=now
            )
        
        bucket = self._buckets[identifier]

        # 2. Refill (The Magic)
        # Calculate time passed since last check
        time_passed = now - bucket.last_updated
        # Calculate new tokens to add
        new_tokens = time_passed * self.refill_rate
        
        # Update state
        bucket.tokens = min(self.capacity, bucket.tokens + new_tokens)
        bucket.last_updated = now

        # 3. Consume
        if bucket.tokens >= cost:
            bucket.tokens -= cost
            return True  # ALLOW
        else:
            return False # BLOCK