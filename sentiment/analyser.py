
import pandas as pd
from transformers import pipeline

class SentimentAnalyser:

    """
    A class for performing sentiment analysis on a DataFrame using the Hugging Face Transformers library.

    Attributes:
    - dataframe (pd.DataFrame): The input DataFrame containing text data.
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe


    def analyze_sentiment_transformer(self, text_column):
        """
        Analyzes sentiment using the Hugging Face Transformers library and adds the results to the DataFrame.

        Parameters:
        - text_column (str): The name of the column in the DataFrame containing the text to analyze.

        Returns:
        - pd.DataFrame: The DataFrame with added sentiment analysis results.
            - new column sentiment_transformer: transformer label
            - new column transformer_score: numeric value of sentiment analysis
            - new column sentiment_results_adjusted: more granular label based on score adjusting negative or positive labels
              to reflect strong sentiment values
        """
        sentiment_results = []
        sentiment_score = []
        sentiment_results_adjusted =[]
        #classifier = pipeline("sentiment-analysis")

        classifier = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
        for text in self.dataframe[text_column]:
            analysis = classifier(text, padding=True, truncation=True)[0]
            label = analysis["label"]
            score = analysis["score"]
            sentiment_results.append(label)
            sentiment_score.append(score)
            if label == "NEG":
                if score > 0.6:
                    sentiment_results_adjusted.append("Strongly Negative")
                else:
                    sentiment_results_adjusted.append("Negative")
            elif label == "POS":
                if score > 0.6:
                    sentiment_results_adjusted.append("Strongly Positive")
                else:
                    sentiment_results_adjusted.append("Positive")
            else:
                sentiment_results_adjusted.append("Neutral")


        self.dataframe['sentiment_transformer'] = sentiment_results
        self.dataframe["transformer_score"] = sentiment_score
        self.dataframe["sentiment_results_adjusted"] = sentiment_results_adjusted
        return self.dataframe

# Example usage:
# dataframe = pd.read_csv("your_data.csv")
# sentiment_analyser = SentimentAnalyser(dataframe)
# dataframe_with_sentiment = sentiment_analyser.analyze_sentiment_transformer("text_column_name")



