from FlightRadar24.api import FlightRadar24API
from datetime import datetime
from zoneinfo import ZoneInfo
import telepot

import sys

tz = ZoneInfo("Europe/Rome")

def read_bot_token():
    with open("bot_token.txt", 'r') as file:
        return file.readline().strip()

def read_chat_id():
    with open("users.txt", 'r') as file:
        chat_ids = [line.strip() for line in file]
    return chat_ids

def telegram_notification(msg):
    bot_token = read_bot_token()
    print(bot_token)
    bot = telepot.Bot(bot_token)
    chat_ids = read_chat_id()
    for chat_id in chat_ids:
        bot.sendMessage(chat_id, msg)

def get_flights_between_airports(departure_airport, arrival_airport):
    api = FlightRadar24API()
    departure_details = api.get_airport_details(departure_airport)
    tag = departure_details['airport']['pluginData']['schedule']['departures']['data']
    
    for flight in tag:
        flight_number = flight['flight']['identification']['number']['default']
        destination_iata = flight['flight']['airport']['destination']['code']['iata']
        destination_name = flight['flight']['airport']['destination']['name']
        departure_timestamp = flight['flight']['time']['scheduled']['departure']
        arrival_timestamp = flight['flight']['time']['scheduled']['arrival']

        if destination_iata == arrival_airport:
            departure_time = datetime.fromtimestamp(departure_timestamp, tz=tz)
            arrival_time = datetime.fromtimestamp(arrival_timestamp, tz=tz)
            
            departure_date_time = departure_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            arrival_date_time = arrival_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            msg = (f"‼️Flight {flight_number} from {departure_airport} to {destination_iata} ({destination_name})\n"
                f" - Departure: {departure_date_time}\n"
                f" - Arrival: {arrival_date_time}\n")
            telegram_notification(msg)      

def main():
    departure_airport = sys.argv[1] #'CGN'
    arrival_airport = sys.argv[2] #'TLS'
    get_flights_between_airports(departure_airport, arrival_airport)

if __name__ == "__main__":
    main()
