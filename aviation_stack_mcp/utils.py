import os
import requests
import logging
from aviation_stack_mcp.config import AVIATION_STACK_API_KEY
from rich.logging import RichHandler


def setup_logging():
    """Configure and set up logging for the application."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="| %(levelname)-8s | %(name)s | %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True)],
        force=True,  # This is the fix that overrides uvicorn & third-party loggers
    )

    logger = logging.getLogger("aviation_stack_mcp_logger")
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logger


# Create the logger instance for import by other modules
logger = setup_logging()


def fetch_flights_data(limit=20, flight_iata=None, flight_date=None):
    """
    Fetch flight data from the Aviationstack API.

    This function retrieves flight information from the Aviationstack API.
    You can optionally filter by flight number (IATA code) and/or date.

    Parameters:
    -----------
    limit : int, optional
        Maximum number of results to return (default is 20).
    flight_iata : str, optional
        Specific flight number to search for (e.g., "CX383").
    flight_date : str, optional
        Date of the flight in 'YYYY-MM-DD' format (e.g., "2025-06-01").

    Returns:
    --------
    dict
        Parsed JSON response from the API. If the request fails, a dict with an "error" key is returned.

    Example:
    --------
    >>> fetch_flights_data(flight_iata="CX383", flight_date="2025-06-01")
    {
        "data": [...],
        "pagination": {...}
    }
    """
    url = "http://api.aviationstack.com/v1/flights"

    AVIATION_STACK_API_KEY = os.environ["AVIATION_STACK_API_KEY"]
    if not AVIATION_STACK_API_KEY:
        raise ValueError("AVIATION_STACK API KEY IS Missing")

    params = {"access_key": AVIATION_STACK_API_KEY, "limit": limit}

    if flight_iata:
        params["flight_iata"] = flight_iata
    if flight_date:
        params["flight_date"] = flight_date

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": f"API request failed with status code {response.status_code}"}

    return response.json()
