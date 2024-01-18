from mastodon import Mastodon

class MastodonPostman:
    """
    A class for interacting with the Mastodon API to retrieve posts with a specific hashtag.

    Attributes:
    - client_id (str): The client ID for Mastodon API authentication.
    - client_secret (str): The client secret for Mastodon API authentication.
    - access_token (str): The access token for authenticating requests to the Mastodon API.
    - api_base_url (str): The base URL of the Mastodon API (server you want to connect to).
    attributes below are created by class during object construction
    - mastodon (Mastodon): An instance of the Mastodon class for API interactions.
    - posts (list): A list to store retrieved posts.
    """
    def __init__(self, client_id, client_secret, access_token, api_base_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.api_base_url = api_base_url
        self.mastodon = Mastodon(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token,
            api_base_url=self.api_base_url
        )
        self.posts = []

    def return_messages(self, hashtag):
        """
            Fetches posts with a specific hashtag from the Mastodon API.

            Parameters:
            - hashtag (str): The hashtag for which to retrieve posts.

            Returns:
                list: A list of posts with the specified hashtag.
        """
        # Fetch posts with the hashtag
        hashtag_posts = self.mastodon.timeline_hashtag(hashtag)
        # Get content of each post
        self.posts = [post["content"] for post in hashtag_posts]
        return self.posts