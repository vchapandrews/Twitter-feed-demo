class Author(object):

    def __init__(self, **kwargs):

        self.id = kwargs['id']
        self.username = kwargs['username']
        self.display_name = kwargs['display_name']
        self.profile_image = kwargs['profile_image']

    def __repr__(self):
        return self.id


class Tweet(object):

    def __init__(self, **kwargs):

        from datetime import datetime

        # Tweet ID
        self.id = kwargs['id']
        
        # Tweet content
        self.text = kwargs['text']
        
        # Publish time
        self.created_at = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.000Z')
        
        # Defining metrics
        self.retweet_count = kwargs['retweet_count']
        self.reply_count = kwargs['reply_count']
        self.like_count = kwargs['like_count']
        self.quote_count = kwargs['quote_count']

        # Attaching author object
        self.author = Author(
            id = kwargs['author_id'],
            username = kwargs['author_username'],
            display_name = kwargs['author_display_name'],
            profile_image = kwargs['author_profile_image']
        )

    def __repr__(self):
        return self.id


def get_credentials():

    # Setting up credentials

    from dotenv import load_dotenv
    load_dotenv()

    from searchtweets import load_credentials

    search_args = load_credentials()

    return search_args



def collect_tweets(search_query, results_per_call = 100):

    # Creating a search query

    from searchtweets import gen_request_parameters, collect_results

    query = gen_request_parameters(
        search_query,
        results_per_call=results_per_call,
        tweet_fields='created_at,public_metrics',
        expansions='author_id',
        user_fields='name,id,username,profile_image_url',
        granularity=None
    )

    response = collect_results(
        query,
        max_tweets=results_per_call,
        result_stream_args=get_credentials()
    )

    return response


def parse_response(response):

    tweets = response[0]['data']
    users = response[0]['includes']['users']
    meta = response[0]['meta']

    tweet_list = []

    for tweet in tweets:

        for user in users:

            if tweet['author_id'] == user['id']:

                tweet_to_add = Tweet(
                    id = tweet['id'],
                    text = tweet['text'],
                    created_at = tweet['created_at'],
                    retweet_count = tweet['public_metrics']['retweet_count'],
                    reply_count = tweet['public_metrics']['reply_count'],
                    like_count = tweet['public_metrics']['like_count'],
                    quote_count = tweet['public_metrics']['quote_count'],
                    author_id = tweet['author_id'],
                    author_display_name = user['name'],
                    author_username = user['username'],
                    author_profile_image = user['profile_image_url']
                )

                tweet_list.append(tweet_to_add)

                break # Breaks the inner loop once a match has been found to avoid unneccessary iterations

    return tweet_list
