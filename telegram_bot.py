import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Directly use the provided bot token
TOKEN = '7276267864:AAFFpamtVlpoIgQSD7m-m0oYNoJAyKjDNTE'

# Updated URL for fetching leaderboard data
LEADERBOARD_URL = 'https://europe-west2-g3casino.cloudfunctions.net/user/affiliate/referral-leaderboard'

# Function to fetch data from the API
def fetch_data():
    try:
        response = requests.get(LEADERBOARD_URL)
        response.raise_for_status()  # Raise an HTTPError if the response was unsuccessful
        return response.json()  # Parse the response as JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

# Command handler for /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Welcome to the Affiliate Player Leaderboard Bot!\n'
        'Commands available:\n'
        '/daily - Top players for today\n'
        '/weekly - Top players for the last 7 days\n'
        '/monthly - Top players for the last 30 days'
    )

# Function to get the top 10 wagers from data for the given period
def get_top_wagers(data, period):
    # Define keys to use based on the period
    period_key_map = {
        'daily': 'wager_today',
        'weekly': 'wager_week',
        'monthly': 'wager_month'
    }
    
    key = period_key_map.get(period)
    if not key:
        return "Invalid period requested."
    
    if 'players' not in data:
        return "Invalid data format."

    # Sort players based on the period's wager key
    top_players = sorted(data['players'], key=lambda x: x.get(key, 0), reverse=True)[:10]
    response = f"Top 10 players for {period.capitalize()}:\n"
    for idx, player in enumerate(top_players, 1):
        response += f"{idx}. Username: {player['name']} - Wager: {player[key]}\n"
    
    return response

# Handler functions for each command
def daily(update: Update, context: CallbackContext):
    data = fetch_data()
    if data:
        response = get_top_wagers(data, 'daily')
        update.message.reply_text(response)
    else:
        update.message.reply_text("Error loading data. Please try again later.")

def weekly(update: Update, context: CallbackContext):
    data = fetch_data()
    if data:
        response = get_top_wagers(data, 'weekly')
        update.message.reply_text(response)
    else:
        update.message.reply_text("Error loading data. Please try again later.")

def monthly(update: Update, context: CallbackContext):
    data = fetch_data()
    if data:
        response = get_top_wagers(data, 'monthly')
        update.message.reply_text(response)
    else:
        update.message.reply_text("Error loading data. Please try again later.")

def main():
    if not TOKEN:
        print("Error: Bot token not found.")
        return

    # Set up the Updater and Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('daily', daily))
    dispatcher.add_handler(CommandHandler('weekly', weekly))
    dispatcher.add_handler(CommandHandler('monthly', monthly))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    