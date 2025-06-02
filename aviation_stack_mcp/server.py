import argparse
import requests

from aviation_stack_mcp.config import (
    DEFAULT_CONNECTION_TYPE,
    AVIATION_STACK_API_KEY,
)
from aviation_stack_mcp.utils import fetch_flights_data, logger
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("aviation_stack_mcp")


def create_mcp_server():
    """
    Create and configure the Model Context Protocol server.

    Returns:
        Configured MCP server instance
    """
    mcp = FastMCP("AviationStackMcpServer")

    # Register MCP-compliant tools
    register_tools(mcp)

    return mcp


def register_tools(mcp):
    """
    Register all tools with the MCP server following the Model Context Protocol specification.

    Each tool is decorated with @mcp.tool() to make it available via the MCP interface.

    Args:
        mcp: The MCP server instance
    """

    @mcp.tool()
    async def search_flights_tool(flight_number: str):
        """
        Search for flights using the IATA flight number on the AVIATION STACK API.

        This MCP tool allows AI models to search for flight information by specifying
        the flight number.

        Args:
            flight_number: IATA flight number (e.g., DL123 -> Delta Air Lines Flight 123)

        Returns:
            flight details
        """
        return await search_flight_by_number(flight_number)

    @mcp.tool()
    async def find_flight_duplicates_tools(flight_number: str):
        """
        Deduplicate a list of flight entries by consolidating code-shared flights into a single canonical entry.

        This MCP tool allows AI models to

        Args:
            origin: Departure airport code (e.g., ATL, JFK)

        Returns:
            A list of available flights with details
        """
        return await find_flight_duplicates(flight_number)


def search_flight_by_number(flight_number: str):
    """
    Search for flight information using the IATA flight number via the Aviationstack API.

    Parameters:
    -----------
    flight_number : str
        The IATA flight number to search for (e.g., "CX383").

    Returns:
    --------
    dict
        A dictionary containing flight data if the request is successful and results are found.
        If the API call fails or no data is found, a dictionary with an error message is returned.

    Example:
    --------
    >>> search_flight_by_number("CX383")
    {
        "data": [
            {
                "flight": {
                    "iata": "CX383",
                    ...
                },
                ...
            }
        ]
    }
    """
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATION_STACK_API_KEY,
        "flight_iata": flight_number,
        "limit": 5,  # Optional: limit the number of results
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": f"API request failed with status code {response.status_code}"}

    data = response.json()
    if "data" not in data or not data["data"]:
        return {"error": f"No flight found for flight number {flight_number}"}

    return data


def find_flight_duplicates(known_flight_number):
    """
    Given a list of flights and a known flight number (iata code), find all code-shared versions of that flight.

    This function is designed for travelers who know their flight number and want to find any duplicated
    or code-shared flights that correspond to the same physical flight (operated by different airlines).

    Parameters:
    -----------
    known_flight_number : str
        The flight number (IATA format, e.g., "CX383") that the traveler knows.

    Returns:
    --------
    list of dict
        A list of all matching flights (including code-shared versions) that refer to the same physical flight.

    Example:
    --------
    >>> find_codeshare_duplicates(api_response["data"], "CX383")
    [
        {"flight": {"iata": "CX383"}, "airline": {"name": "Cathay Pacific"}, ...},
        {"flight": {"iata": "LX4321"}, "airline": {"name": "Swiss"}, ...},
    ]
    """
    canonical_key = None
    matching_group = []

    flight_data = fetch_flights_data(flight_iata=known_flight_number)

    # Step 1: Find the canonical key based on known flight number
    for flight in flight_data:
        flight_iata = flight["flight"].get("iata")
        codeshared = flight["flight"].get("codeshared")
        codeshared_iata = codeshared.get("flight_iata") if codeshared else None

        if flight_iata == known_flight_number or codeshared_iata == known_flight_number:
            canonical_key = codeshared_iata if codeshared_iata else flight_iata
            break  # We can exit once we know the canonical key

    # Step 2: Group all flights under this canonical key
    if canonical_key:
        for flight in flight_data:
            flight_iata = flight["flight"].get("iata")
            codeshared = flight["flight"].get("codeshared")
            codeshared_iata = codeshared.get("flight_iata") if codeshared else None

            # Match by either the flight itself or a codeshare that points to the same canonical key
            if flight_iata == canonical_key or codeshared_iata == canonical_key:
                matching_group.append(flight)

    return matching_group


def main():
    """
    Main entry point for the Model Context Protocol Server.
    """
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Model Context Protocol Service")
    parser.add_argument(
        "--connection_type",
        type=str,
        default=DEFAULT_CONNECTION_TYPE,
        choices=["stdio"],
        help="Connection type (stdio)",
    )
    # args = parser.parse_args()

    transport_type = "stdio"
    # Initialize MCP server
    mcp = create_mcp_server()

    logger.info(
        f"🚀 Starting Aviation Stack MCP Service with {transport_type} connection"
    )

    # Start the server
    mcp.run(transport=transport_type)


if __name__ == "__main__":

    main()
