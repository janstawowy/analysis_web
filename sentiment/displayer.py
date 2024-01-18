import pandas as pd
import plotly.express as px

class Displayer:
    """
    A class for displaying sentiment analysis results using interactive visualizations.

    Attributes:
    - dataframe (pd.DataFrame): The DataFrame containing sentiment analysis data.
    - custom_colors (dict): A dictionary mapping sentiment categories to custom colors.

    Methods:
    - display_pie: Display a pie chart representing sentiment analysis results.
    - display_timeline: Display a timeline chart representing sentiment analysis results over time.
    """

    def __init__(self,dataframe):
        self.dataframe = dataframe

    custom_colors = {
        'Negative': 'orange',
        'Neutral': 'gray',
        'Positive': 'lightgreen',
        'Strongly Negative': 'red',
        'Strongly Positive': 'green'
    }

    def display_pie(self):
        """
        Display a pie chart representing sentiment analysis results.

        Returns:
        - str: HTML representation of the Plotly pie chart.
        """

        # Create an interactive pie chart with text labels
        result = self.dataframe.groupby('sentiment_results_adjusted')['text'].apply(
            lambda x: '<br>'.join(x)).reset_index().rename(columns={'text': 'concat_text'})
        self.dataframe = self.dataframe.merge(result, on='sentiment_results_adjusted', how='left')

        # Prepare the figure
        fig = px.pie(self.dataframe,names='sentiment_results_adjusted',title='Sentiment analysis',
                     hover_name='sentiment_results_adjusted', hover_data="concat_text",color='sentiment_results_adjusted',color_discrete_map=Displayer.custom_colors)

        # Set how text labels are displayed on the chart
        fig.update_traces(textposition='inside', textinfo='percent+label')

        # Show the interactive chart
        return fig.to_html(full_html=False)


    def display_timeline(self):
        """
        Display a timeline chart representing sentiment analysis results over time.

        Returns:
        - str: HTML representation of the Plotly line chart.
        """

        # Adjust Datetime format
        self.dataframe['date'] = pd.to_datetime(self.dataframe['date'])
        self.dataframe['date'] = self.dataframe['date'].dt.strftime('%d/%m/%Y')

        #Group the results by date and count occurrences of each sentiment
        grouped_df = self.dataframe.groupby(['date', 'sentiment_results_adjusted']).size().reset_index(name='count')

        # Pivot the DataFrame to have a separate column for each sentiment category
        grouped_df_pivot = grouped_df.pivot(index='date', columns='sentiment_results_adjusted', values='count').fillna(
            0).reset_index()

        # Prepare the figure
        fig = px.line(grouped_df_pivot, x='date', y=grouped_df_pivot.columns[1:],
                      title='Sentiment Analysis Timeline by Day',
                      labels={'date': 'Date', 'value': 'Count', 'variable': 'Sentiment'},
                      color_discrete_map=Displayer.custom_colors)

        return fig.to_html(full_html=False)

