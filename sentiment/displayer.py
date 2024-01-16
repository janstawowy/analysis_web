import pandas as pd
import plotly.express as px

class Displayer:


    def __init__(self,dataframe):
        self.dataframe = dataframe

    def display_pie(self):
        # Create an interactive pie chart with text labels
        result = self.dataframe.groupby('sentiment_results_adjusted')['text'].apply(lambda x: '<br>'.join(x)).reset_index().rename(columns={'text': 'concat_text'})
        self.dataframe = self.dataframe.merge(result, on='sentiment_results_adjusted', how='left')
        fig = px.pie(self.dataframe, names='sentiment_results_adjusted',title='Sentiment analysis',
                     hover_name='sentiment_results_adjusted', hover_data={"concat_text": True})

        # Set how text labels are displayed on the chart
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Show the interactive chart
        return fig.to_html(full_html=False)