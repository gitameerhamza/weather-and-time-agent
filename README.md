# Weather Time Agent

A simple Python agent built using Google's Agent Development Kit (ADK) that provides weather and timezone information for specific cities.

## Overview

This project implements a simple agent that can answer user questions about:
- Current weather conditions in supported cities (using OpenWeatherMap API)
- Current local time in supported cities (using TimeZoneDB API)

The agent is powered by Google's Gemini 1.5 Flash model and responds to natural language queries about weather and time.

## Features

- Get real-time weather information for any city using OpenWeatherMap API
- Get current local time for any city using TimeZoneDB API
- Natural language interface via Gemini 1.5
- Command-line interface (CLI) with interactive mode

## Supported Cities

For weather and timezone information:
- Any city supported by the OpenWeatherMap and TimeZoneDB APIs

## Project Structure

```
multi_tool_agent/
│── __init__.py
│── agent.py     # Main implementation of the agent and tools
│── cli.py       # Command-line interface implementation
│── tools.py     # Tool registry and utilities
│── .env         # Environment variables for API keys and configuration
```

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install google-generativeai zoneinfo requests google-adk
   ```
3. Configure API keys in the `.env` file:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_google_api_key_here
   WEATHER_API_KEY=your_openweathermap_api_key_here
   TIMEZONE_API_KEY=your_timezonedb_api_key_here
   ```
4. Get the required API keys:
   - **Google API Key**: Sign up for Google AI Studio to get access to Gemini models
   - **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - **TimeZoneDB API Key**: Sign up at [TimeZoneDB](https://timezonedb.com/api)

## Usage

### Python API

Import and use the agent in your Python code:

```python
from multi_tool_agent.agent import root_agent

# Use the agent to answer questions
response = root_agent.respond("What's the weather in New York?")
print(response)

response = root_agent.respond("What time is it in Lahore?")
print(response)
```

### Command Line Interface

The agent can also be used from the command line:

```bash
# Get weather information
python -m multi_tool_agent.cli "What's the weather in London?"

# Use interactive mode
python -m multi_tool_agent.cli

# List available tools
python -m multi_tool_agent.cli --list-tools

# Choose output format
python -m multi_tool_agent.cli --output json "What time is it in Berlin?"
```

CLI options:
- `--config`, `-c`: Path to configuration file
- `--log-level`, `-l`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--tool`, `-t`: Specify a specific tool to use
- `--list-tools`: List all available tools
- `--output`, `-o`: Output format (text or json)

## Implementation Details

The agent uses two main functions:

1. `get_weather(city)`: Returns real-time weather information for any city by making API calls to OpenWeatherMap
2. `get_current_time(city)`: Returns the current time in any city by using TimeZoneDB API

Both functions return a dictionary with either:
- Success status and a formatted report
- Error status and an error message when there's an issue (API key missing, city not found, etc.)

The project also includes a command-line interface that provides interactive access to the agent's capabilities.

## License

No license

## Contact

Email: ameerhamza.codes@gmail.com