from dataclasses import dataclass

@dataclass
class MetricsState:
    allowed_requests: int = 0
    blocked_requests: int = 0

class MetricsManager:
    _state = MetricsState()

    @classmethod
    def track_allowed(cls):
        cls._state.allowed_requests += 1

    @classmethod
    def track_blocked(cls):
        cls._state.blocked_requests += 1

    @classmethod
    def get_stats(cls):
        return {
            "allowed": cls._state.allowed_requests,
            "blocked": cls._state.blocked_requests,
            "total": cls._state.allowed_requests + cls._state.blocked_requests
        }
