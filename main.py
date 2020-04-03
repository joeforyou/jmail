#!/usr/bin/env python3
import confuse, os
from mail import send_mail
from player import get_players
# Load config file.
config = confuse.Configuration('jmail', __name__)
config.set_file(os.path.dirname(os.path.abspath(__file__)) + '/' + 'config.yaml')

def main():
    # Iterate through games.
    for game in config['games']:
        print('Loading game: ' + game['name'].get())
        players = [player for player in get_players() if player['Game'] == game['name'].get()]
        # Send email.
        send_mail(
            config['account'],
            config['password'],
            players,
            config['form_url'],
            game['sheet']['url'],
            game['name'].get())

if __name__ == "__main__":
    main()

