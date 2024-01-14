from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from common import JsonReader
from sentiment import MastodonPostman, MessageCleaner, SentimentAnalyser, Displayer

views = Blueprint('views', __name__)
secrets_file_path = "./keys/secrets.json"
keys_reader = JsonReader(secrets_file_path)
keys = keys_reader.read_json()
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        hashtag = request.form.get('hashtag')
        if len(hashtag) < 3:
            flash('hashtag is too short!', category='error')
        else:
            postman = MastodonPostman(keys['client_id'], keys['client_secret'], keys['access_token'], keys['api_base_url'])
            messages = postman.return_messages(hashtag)
            print(messages)
            message_cleaner = MessageCleaner()
            messages_cleaned = message_cleaner.return_messages(messages)
            analyser = SentimentAnalyser(messages_cleaned)
            sentiment = analyser.analyze_sentiment_transformer("text")
            print(sentiment)
            displayer = Displayer(sentiment)
            plot_html = displayer.display_pie()


    return render_template('home.html', user=current_user, plot_html=plot_html)

