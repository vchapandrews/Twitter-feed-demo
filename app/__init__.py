import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request

def create_app():

    # Create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET'],
    )

    # Homepage
    @app.route('/', methods=['GET', 'POST'])
    def home():

        tweets = None

        if request.method == 'POST':

            search_query = request.form['search-query']

            from twitter_api import collect_tweets, parse_response

            response = collect_tweets(search_query + ' -is:retweet')

            print('RESPONSE:', response)

            if response:
                tweets = parse_response(response)
            else:
                tweets = None

        return render_template('home.html', tweets=tweets)

    return app
