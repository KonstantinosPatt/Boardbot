# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from secondary_functions import extract_top_games

import requests
import re
import pandas as pd

csvfile = 'C:/Users/kosti/Documents/NLP/913_Dialogue_Systems/boardbot/games_db_1000.csv'

games = pd.read_csv(csvfile)

games['type'] = games['type'].str.lower()
games['category 1'] = games['category 1'].str.lower()


class action_suggest_game(Action):

    def name(self) -> Text:
        return "action_suggest_game"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gametype = tracker.get_slot('gametype').lower()
        category = tracker.get_slot('category').lower()
        pref_time = int(tracker.get_slot('play_time'))
        num_players = int(tracker.get_slot('num_players'))

        print()
        print('gametype:   ', gametype)
        print('category:   ', category)
        print('play time:  ', pref_time)
        print('num players:', num_players)

        suggestion = games.loc[games['type'] == gametype]
        suggestion = suggestion.loc[suggestion['category 1'] == category]

        suggestion = suggestion.loc[suggestion['min players'] <= num_players]
        suggestion = suggestion.loc[suggestion['max players'] >= num_players]

        suggestion = suggestion.loc[suggestion['mean time'] <= int(pref_time + ((pref_time/6)))]
        suggestion = suggestion.loc[suggestion['mean time'] >= int(pref_time - ((pref_time/6)))]
        
        try:
            final_sug = suggestion.iloc[0]['title']
            print('suggestion: ', final_sug)

            dispatcher.utter_message(text=f"May I suggest {final_sug}?")
            dispatcher.utter_message(image=suggestion.iloc[0]['image'])
            dispatcher.utter_message(text=suggestion.iloc[0]['description'])
            dispatcher.utter_message(text="Here's a link to the game: " + suggestion.iloc[0]['link'])

        except:
            dispatcher.utter_message(text=f"I can't seem to find a {gametype} {category} game for {num_players} players that lasts {pref_time} minutes. Would you like to try something else?")

        return []

