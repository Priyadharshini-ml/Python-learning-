
import os
import requests


API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> None:
    """Fetch and display current weather for a city."""

    if not API_KEY:
        print("Please configure your weather API key.")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(
            BASE_URL, params=params, timeout=10
        )
        response.raise_for_status()
        data = response.json()

        print(f"\nWeather Report: {data['name']}")
        print(f"Condition: {data['weather'][0]['description']}")
        print(f"Temperature: {data['main']['temp']} °C")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Wind Speed: {data['wind']['speed']} m/s")

    except requests.exceptions.HTTPError:
        print("Weather request failed. Check the city or API key.")
    except requests.exceptions.RequestException:
        print("Network error. Please try again.")
    except (KeyError, IndexError, TypeError):
        print("Unexpected weather data received.")


def main() -> None:
    city = input("Enter city name: ").strip()

    if city:
        get_weather(city)
    else:
        print("City name cannot be empty.")


if __name__ == "__main__":
    main()
