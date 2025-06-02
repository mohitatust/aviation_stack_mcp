# Aviation Stack MCP

This project implements the MCP tools that can be used by Claude and other MCP-compatible models.

## What is Model Context Protocol?

The Model Context Protocol (MCP) is a standard developed by Anthropic that enables AI models to use tools by defining a structured format for tool descriptions, calls, and responses. 

## Installation

```bash
# Install from PyPI
pip install aviation-stack-mcp

# Or install from the project directory (development mode)
pip install -e .
```

## Usage

Start the MCP server:

```bash
# Using the command-line entry point
aviation-stack-mcp --connection_type stdio

# Or run directly
python main.py --connection_type stdio
```

## Environment Variables
Register and fetch your API keys from the [aviation stack website](https://aviationstack.com/). 

Set the AVIATION_STACK_API_KEY key as an environment variable:
```bash
# On Unix/macOS
export AVIATION_STACK_API_KEY="your-api-key-here"

# On Windows (PowerShell)
$env:AVIATION_STACK_API_KEY="your-api-key-here"
```

## Features
- Flight search by IATA number
- Flight duplication finder


## License

This project is licensed under the MIT License - see the LICENSE file for details. 