from typing import Tuple, Dict, Any

import requests

unit_of_measurement = 'C'


def get_coordinates(city: str) -> Tuple[float, float] | Tuple[None, None]:
    params = {"city": city, "format": "json"}
    response = requests.get("https://nominatim.openstreetmap.org/search", params=params)
    data = response.json()
    data_element = [element for element in data if element['type'] == 'city' or element['type'] == 'town']
    if data_element:
        lat = data_element[0]['lat']
        lon = data_element[0]['lon']
        return lat, lon
    else:
        return None, None


def get_weather(lat: float, lon: float, days: int = 1) -> Dict[str, Any]:
    params = {"latitude": lat, "longitude": lon, "current": "temperature_2m", "hourly": "temperature_2m",
              "forecast_days": days}
    if unit_of_measurement == 'F':
        params["temperature_unit"] = "fahrenheit"
    response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
    data = response.json()
    return data


def current_weather(city: str) -> None:
    lat, lon = get_coordinates(city)
    if lat and lon:
        weather_data = get_weather(lat, lon)
        print(f'Current temp is {weather_data['current']['temperature_2m']}{unit_of_measurement}')
    else:
        print('Invalid city name.')


def forecast_weather(city: str, days: int) -> None:
    lat, lon = get_coordinates(city)
    if lat and lon:
        weather_data = get_weather(lat, lon, days)
        forecast_data = weather_data['hourly']
        for i in range(days):
            date = forecast_data['time'][i * 24]
            for j in range(4):
                time_1 = forecast_data['time'][i * 24 + j * 6].split('T')[1]
                time_2 = forecast_data['time'][i * 24 + (j + 1) * 6 - 1].split('T')[1]
                temp = forecast_data['temperature_2m'][i * 24 + j * 6:i * 24 + (j + 1) * 6]
                print(
                    f'{date.split('T')[0]} {time_1}-{time_2} min: {min(temp)}{unit_of_measurement}\tmax: {max(temp)}{unit_of_measurement}')
    else:
        print('Invalid city name.')


def set_unit(unit: str) -> None:
    global unit_of_measurement
    if unit.lower() in ['c', 'celsius']:
        unit_of_measurement = 'C'
    elif unit.lower() in ['f', 'fahrenheit']:
        unit_of_measurement = 'F'
    else:
        print('Invalid unit of measurement. Available units are c, f, celsius, fahrenheit')


def get_unit() -> None:
    if unit_of_measurement == 'C':
        print('celsius')
    else:
        print('fahrenheit')


def main() -> None:
    while True:
        command = input('>>> ')
        words = command.split()
        match words[0]:
            case 'current' if len(words) >= 2:
                city = ' '.join(words[1:])
                current_weather(city)
            case 'forecast' if len(words) >= 3 and words[-1].isdigit():
                city = ' '.join(words[1:-1])
                days = int(words[-1])
                forecast_weather(city, days)
            case 'setunit' if len(words) == 2:
                unit = words[1]
                set_unit(unit)
            case 'getunit' if len(words) == 1:
                get_unit()
            case 'exit' if len(words) == 1:
                break
            case _:
                print(
                    'Unknown command. Available commands:\n\tcurrent %city%\n\tforecast %city% %days%\n\tsetunit %unit%\n\tgetunit\n\texit')


if __name__ == "__main__":
    main()
