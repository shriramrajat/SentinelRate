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
    def allow_request(self, identifier: str, cost: int = 1):
        now = self._get_current_time()
        
        if identifier not in self._buckets:
            self._buckets[identifier] = BucketState(
                tokens=float(self.capacity),
                last_updated=now
            )
        
        bucket = self._buckets[identifier]

        # Refill
        time_passed = now - bucket.last_updated
        new_tokens = time_passed * self.refill_rate
        bucket.tokens = min(self.capacity, bucket.tokens + new_tokens)
        bucket.last_updated = now

        # Decision & Calculation
        if bucket.tokens >= cost:
            bucket.tokens -= cost
            # Allowed, Remaining, Retry After (0 because allowed)
            return (True, int(bucket.tokens), 0.0)
        else:
            # Calculate time needed to get enough tokens
            tokens_needed = cost - bucket.tokens
            wait_time = tokens_needed / self.refill_rate
            return (False, int(bucket.tokens), wait_time)