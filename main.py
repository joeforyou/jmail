#!/usr/bin/env python3
import confuse, os
from mail import send_mail

# Load config file.
config = confuse.Configuration('jmail', __name__)
config.set_file(os.path.abspath(os.getcwd()) + 'config.yaml')

def main():
    # Iterate through games.
    for game in config['games']:
        print('Loading game: ' + game['name'].get())
        players = [player['email'].get() for player in game['recipients']]
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
