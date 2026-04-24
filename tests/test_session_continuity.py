import json
import os
import pytest

class SessionState:
    def __init__(self, session_id: str, context_snapshot: dict, metadata: dict = None):
        self.session_id = session_id
        self.last_active = 123456789 # Mock timestamp
        self.context_snapshot = context_snapshot
        self.metadata = metadata or {}

    def to_json(self):
        return json.dumps(self.__dict__)

def test_session_snapshot_privacy():
    # 1. Create session state
    state = SessionState(
        session_id="test-session-123",
        context_snapshot={"last_topic": "BMO Evolution", "entities": ["Prismo", "Cody"]},
        metadata={"env": "dev"}
    )
    
    # 2. Simulate recording an event
    state.context_snapshot["last_event"] = "User requested sync"
    
    # 3. Emit snapshot
    snapshot = state.to_json()
    
    # 4. Confirm no secrets/raw logs/local machine paths
    # Check for common secret patterns or local paths
    forbidden_patterns = ["/Users/", "/home/", "API_KEY", "TOKEN", "password", "SECRET"]
    for pattern in forbidden_patterns:
        assert pattern not in snapshot, f"Snapshot contains forbidden pattern: {pattern}"
    
    assert "test-session-123" in snapshot
    assert "BMO Evolution" in snapshot

if __name__ == "__main__":
    pytest.main([__file__])
