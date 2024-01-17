from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from common import JsonReader
from sentiment import MastodonPostman, MessageCleaner, SentimentAnalyser, Displayer
from . import db
from .models import Post
import pandas as pd


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
        if hashtag.startswith("#"):
            hashtag = hashtag.replace("#","")
        if len(hashtag) < 3:
            flash('hashtag is too short!', category='error')
        else:
            #get posts by hashtag
            postman = MastodonPostman(keys['client_id'], keys['client_secret'], keys['access_token'], keys['api_base_url'])
            messages = postman.return_messages(hashtag)
            #print(messages)
            #clean messages
            message_cleaner = MessageCleaner()
            messages_cleaned = message_cleaner.return_messages(messages)
            #print(messages_cleaned)
            #analyse sentiment
            analyser = SentimentAnalyser(messages_cleaned)
            sentiment = analyser.analyze_sentiment_transformer("text")
            #print(sentiment)
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
                post = Post.query.filter_by(text=text).first()
                if(post):
                    print("already got this one")
                    continue
                else:

                    new_post = Post(hashtag=hashtag, raw_text=raw_text,text=text,sentiment_transformer=sentiment_transformer,transformer_score=transformer_score,sentiment_results_adjusted=sentiment_results_adjusted)
                    db.session.add(new_post)
                    db.session.commit()

    return render_template('home.html', user=current_user, plot_html=plot_html)


@views.route('/timeline', methods=['GET','POST'])
@login_required
def timeline():
    #initialize plot html as none so if we have no data nothing is displayed
    plot_html = None
    #form handling
    if request.method == 'POST':
        hashtag = request.form.get('hashtag')
        if hashtag.startswith("#"):
            hashtag = hashtag.replace("#", "")
        if len(hashtag) < 3:
            flash('hashtag is too short!', category='error')
        else:
            posts = Post.query.filter_by(hashtag=hashtag).all()
            # Decompose each Post object to a dictionary
            post_dicts = [post.__dict__ for post in posts]

            # Exclude unnecessary keys from the dictionaries
            for post_dict in post_dicts:
                post_dict.pop('_sa_instance_state', None)

            # Create a Pandas DataFrame from the list of dictionaries
            df = pd.DataFrame(post_dicts)
            displayer = Displayer(df)
            plot_html = displayer.display_timeline()





    return render_template('timeline.html', user=current_user, plot_html=plot_html)