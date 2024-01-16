from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from common import JsonReader
from sentiment import MastodonPostman, MessageCleaner, SentimentAnalyser, Displayer
from . import db
from .models import Post


views = Blueprint('views', __name__)
secrets_file_path = "./keys/secrets.json"
keys_reader = JsonReader(secrets_file_path)
keys = keys_reader.read_json()
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    plot_html = None
    if request.method == 'POST':
        hashtag = request.form.get('hashtag')
        if len(hashtag) < 3:
            flash('hashtag is too short!', category='error')
        else:
            #get posts by hashtag
            postman = MastodonPostman(keys['client_id'], keys['client_secret'], keys['access_token'], keys['api_base_url'])
            messages = postman.return_messages(hashtag)
            print(messages)
            #clean messages
            message_cleaner = MessageCleaner()
            messages_cleaned = message_cleaner.return_messages(messages)
            print(messages_cleaned)
            #analyse sentiment
            analyser = SentimentAnalyser(messages_cleaned)
            sentiment = analyser.analyze_sentiment_transformer("text")
            print(sentiment)
            #prepare piechart to display
            displayer = Displayer(sentiment)
            plot_html = displayer.display_pie()
            #write to db for other users
            for index, row in sentiment.iterrows():
                raw_text = row['raw_text']
                text = row['text']
                sentiment_transformer = row['sentiment_transformer']
                transformer_score = row['transformer_score']
                sentiment_results_adjusted = row['sentiment_results_adjusted']
                print(row)
            """
            new_user = Post(hashtag=hashtag, raw_text=raw_text,
                            first_name=name)
            db.session.add(new_user)
            db.session.commit()"""


    return render_template('home.html', user=current_user, plot_html=plot_html)

