import datetime
import os
import requests
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    # Get API key from environment variable
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "Weather API key not found in environment variables.",
        }
    
    # Using OpenWeatherMap API
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Using metric units
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Extract relevant information
        temp_c = data["main"]["temp"]
        temp_f = (temp_c * 9/5) + 32
        weather_desc = data["weather"][0]["description"]
        
        return {
            "status": "success",
            "report": (
                f"The weather in {city} is {weather_desc} with a temperature of {temp_c:.1f} degrees"
                f" Celsius ({temp_f:.1f} degrees Fahrenheit)."
            ),
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error fetching weather for '{city}': {str(e)}",
        }
    except (KeyError, IndexError) as e:
        return {
            "status": "error",
            "error_message": f"Error parsing weather data for '{city}': {str(e)}",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    # Get API key from environment variable
    api_key = os.environ.get("TIMEZONE_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "Timezone API key not found in environment variables.",
        }
        
    # Using TimeZoneDB API
    base_url = "https://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        "key": api_key,
        "format": "json",
        "by": "position",
        "fields": "zoneName,formatted",
    }
    
    try:
        # First get coordinates for the city using OpenWeatherMap API as a geocoder
        weather_api_key = os.environ.get("WEATHER_API_KEY")
        if not weather_api_key:
            return {
                "status": "error",
                "error_message": "Weather API key not found in environment variables (needed for geocoding).",
            }
            
        geocode_url = "https://api.openweathermap.org/geo/1.0/direct"
        geocode_params = {
            "q": city,
            "limit": 1,
            "appid": weather_api_key
        }
        
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        
        geocode_data = geocode_response.json()
        if not geocode_data:
            return {
                "status": "error",
                "error_message": f"Could not find location data for '{city}'.",
            }
            
        # Extract coordinates
        lat = geocode_data[0]["lat"]
        lon = geocode_data[0]["lon"]
        
        # Add coordinates to timezone API params
        params["lat"] = lat
        params["lng"] = lon
        
        # Get timezone data
        timezone_response = requests.get(base_url, params=params)
        timezone_response.raise_for_status()
        
        timezone_data = timezone_response.json()
        
        if timezone_data["status"] != "OK":
            return {
                "status": "error",
                "error_message": f"Error fetching timezone data: {timezone_data.get('message', 'Unknown error')}",
            }
            
        # Use the formatted time from the API
        formatted_time = timezone_data["formatted"]
        zone_name = timezone_data["zoneName"]
        
        report = f"The current time in {city} is {formatted_time} ({zone_name})"
        return {"status": "success", "report": report}
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error fetching time data for '{city}': {str(e)}",
        }
    except (KeyError, IndexError) as e:
        return {
            "status": "error",
            "error_message": f"Error parsing time data for '{city}': {str(e)}",
        }


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-1.5-flash-8b",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
