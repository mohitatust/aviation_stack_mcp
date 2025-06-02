import pytest
from aviation_stack_mcp.utils import fetch_flights_data


def test_fetch_flights_data_missing_key(monkeypatch):
    # Remove the environment variable temporarily
    monkeypatch.delenv("AVIATION_STACK_API_KEY", raising=False)

    # Should raise KeyError since the env variable is missing
    with pytest.raises(KeyError):
        fetch_flights_data()
