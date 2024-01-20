import pytest
import pandas as pd

from sentiment import SentimentAnalyser

SAMPLE_DATA = {
    'text_column': ['This is a positive sentence.','This is neutral sentence' ,'This is a negative sentence.']
}

def test_analyze_sentiment_transformer():
    # Create a DataFrame for testing
    sample_dataframe = pd.DataFrame(SAMPLE_DATA)

    # Create a SentimentAnalyser instance
    sentiment_analyser = SentimentAnalyser(sample_dataframe)

    # Analyze sentiment using the transformer
    result_dataframe = sentiment_analyser.analyze_sentiment_transformer("text_column")

    # Check if the expected columns are present in the result DataFrame
    assert 'sentiment_transformer' in result_dataframe.columns
    assert 'transformer_score' in result_dataframe.columns
    assert 'sentiment_results_adjusted' in result_dataframe.columns

    # Check if the sentiment_transformer column contains the expected values
    expected_sentiment_transformer = ['POS','NEU' ,'NEG']
    assert result_dataframe['sentiment_transformer'].tolist() == expected_sentiment_transformer

