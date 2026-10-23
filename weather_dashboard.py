
import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    if not API_KEY:
        print("Error: Configure OPENWEATHER_API_KEY first.")
        return

    if not city.strip():
        print("Error: City cannot be empty.")
        return

    try:
        response = requests.get(
            BASE_URL,
            params={
                "q": city.strip(),
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        if response.status_code == 404:
            print("Error: City not found.")
            return

        if response.status_code in (401, 403):
            print("Error: API key is invalid or not authorized.")
            return

        response.raise_for_status()
        data = response.json()

        print(f"\nWeather Report: {data['name']}")
        print(f"Condition: {data['weather'][0]['description']}")
        print(f"Temperature: {data['main']['temp']} °C")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Wind speed: {data['wind']['speed']} m/s")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Try again.")
    except requests.exceptions.RequestException as error:
        print(f"Network or API error: {error}")
    except (KeyError, IndexError, TypeError, ValueError):
        print("Error: Unexpected response from the weather service.")


def main():
    city = input("Enter city name: ").strip()
    get_weather(city)


if __name__ == "__main__":
    main()
