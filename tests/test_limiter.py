import time
import pytest
from app.limiter.token_bucket import TokenBucketLimiter

def test_initial_allow():
    # Setup: 10 tokens max, refill 1 per second
    limiter = TokenBucketLimiter(capacity=10, refill_rate=1.0)
    
    # Action: First request
    result = limiter.allow_request("user_1")
    
    # Assert: Should be allowed
    assert result is True

def test_hard_limit_blocking():
    # Setup: Capacity of 2
    limiter = TokenBucketLimiter(capacity=2, refill_rate=1.0)
    
    assert limiter.allow_request("user_2") is True # 1 left
    assert limiter.allow_request("user_2") is True # 0 left
    
    # This should fail immediately
    assert limiter.allow_request("user_2") is False # Blocked

def test_refill_over_time():
    # Setup: Capacity of 1, very slow refill (1 per 100ms)
    limiter = TokenBucketLimiter(capacity=1, refill_rate=10.0)
    
    # Consume the token
    assert limiter.allow_request("user_3") is True
    assert limiter.allow_request("user_3") is False
    
    # Wait for refill (0.15s should give us >1 token)
    time.sleep(0.15)
    
    # Should work again
    assert limiter.allow_request("user_3") is True