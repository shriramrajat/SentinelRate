import time
import pytest
from app.limiter.token_bucket import TokenBucketLimiter

def test_initial_allow():
    # Setup: No args in init anymore
    limiter = TokenBucketLimiter()
    
    # Action: First request (capacity=10, limit=1.0)
    # Result is now a tuple (allowed, remaining, retry_after)
    is_allowed, _, _ = limiter.allow_request("user_1", capacity=10, refill_rate=1.0)
    
    # Assert: Should be allowed
    assert is_allowed is True

def test_hard_limit_blocking():
    # Setup
    limiter = TokenBucketLimiter()
    
    # check [0] for is_allowed boolean
    assert limiter.allow_request("user_2", 2, 1.0)[0] is True # 1 left
    assert limiter.allow_request("user_2", 2, 1.0)[0] is True # 0 left
    
    # This should fail immediately
    assert limiter.allow_request("user_2", 2, 1.0)[0] is False # Blocked

def test_refill_over_time():
    # Setup
    limiter = TokenBucketLimiter()
    
    # Consume the token (capacity 1, refill 10/sec)
    assert limiter.allow_request("user_3", 1, 10.0)[0] is True
    assert limiter.allow_request("user_3", 1, 10.0)[0] is False
    
    # Wait for refill (0.15s should give us >1 token)
    time.sleep(0.15)
    
    # Should work again
    assert limiter.allow_request("user_3", 1, 10.0)[0] is True