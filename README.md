# Weather Time Agent

A simple Python agent built using Google's Agent Development Kit (ADK) that provides weather and timezone information for specific cities.

## Overview

This project implements a simple agent that can answer user questions about:
- Current weather conditions in supported cities (using OpenWeatherMap API)
- Current local time in supported cities

The agent is powered by Google's Gemini 1.5 Flash model and responds to natural language queries about weather and time.

## Features

- Get real-time weather information for any city using OpenWeatherMap API
- Get current local time for supported cities
- Natural language interface via Gemini 1.5

## Supported Cities

For weather information:
- Any city supported by the OpenWeatherMap API

For timezone information:
- New York
- Lahore

## Project Structure

```
multi_tool_agent/
│── __init__.py
│── agent.py     # Main implementation of the agent and tools
│── .env         # Environment variables for API keys and configuration
```

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install google-generativeai zoneinfo requests
   ```
3. Configure API keys in the `.env` file:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_google_api_key_here
   WEATHER_API_KEY=your_openweathermap_api_key_here
   ```
4. Get an OpenWeatherMap API key:
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Navigate to "API keys" tab and copy your key
   - Add it to your `.env` file as shown above

## Usage

Import and use the agent in your Python code:

```python
from multi_tool_agent.agent import root_agent

# Use the agent to answer questions
response = root_agent.respond("What's the weather in New York?")
print(response)

response = root_agent.respond("What time is it in Lahore?")
print(response)
```

## Implementation Details

The agent uses two main functions:

1. `get_weather(city)`: Returns real-time weather information for any city by making API calls to OpenWeatherMap
2. `get_current_time(city)`: Returns the current time in a supported city's timezone

Both functions return a dictionary with either:
- Success status and a formatted report
- Error status and an error message when there's an issue (API key missing, city not found, etc.)

## Adding More Cities for Timezone Support

To add support for additional cities' timezones:

1. Update the `get_current_time()` function with the appropriate timezone identifier for the new city

Note: Weather information is now available for any city supported by the OpenWeatherMap API.

## License

[Specify your license information here]

## Contact

[Your contact information]