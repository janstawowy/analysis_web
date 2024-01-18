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




    def display_timeline(self):
        self.dataframe['date'] = pd.to_datetime(self.dataframe['date'])
        self.dataframe['date'] = self.dataframe['date'].dt.strftime('%d/%m/%Y')

        grouped_df = self.dataframe.groupby(['date', 'sentiment_results_adjusted']).size().reset_index(name='count')

        # Pivot the DataFrame to have a separate column for each sentiment category
        grouped_df_pivot = grouped_df.pivot(index='date', columns='sentiment_results_adjusted', values='count').fillna(
            0).reset_index()

        custom_colors = {
            'Negative': 'orange',
            'Neutral': 'gray',
            'Positive': 'lightgreen',
            'Strongly Negative': 'red',
            'Strongly Positive': 'green'
        }

        fig = px.line(grouped_df_pivot, x='date', y=grouped_df_pivot.columns[1:],
                      title='Sentiment Analysis Timeline by Day',
                      labels={'date': 'Date', 'value': 'Count', 'variable': 'Sentiment'},
                      color_discrete_map=custom_colors)

        return fig.to_html(full_html=False)

