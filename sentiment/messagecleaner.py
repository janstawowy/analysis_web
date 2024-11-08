from bs4 import BeautifulSoup
from langdetect import detect_langs
import pandas as pd
class MessageCleaner:
    """
    A class for cleaning and processing messages extracted from HTML content.

    Attributes:
    - posts (list): A list to store the original messages.
    - posts_dataframe (pd.DataFrame): A DataFrame to store cleaned and processed messages.
    """
    def __init__(self):
        self.posts = []
        self.posts_dataframe = pd.DataFrame()


    def return_messages(self,posts):
        """
        Processes and cleans messages extracted from HTML content.

        Parameters:
        - posts (list): A list of messages extracted from HTML content.

        Returns:
        - pd.DataFrame: A DataFrame containing cleaned and processed messages.
        """

        self.posts = posts
        data = []
        for post in self.posts:

            # Instantiate a BS object to clean html code
            soup = BeautifulSoup(post, 'html.parser')
            # Remove anchor tags
            for a_tag in soup.find_all('a'):
                a_tag.decompose()

            # Get text and remove extra spaces
            text_content = soup.get_text()
            text_without_spaces = " ".join(text_content.split()).strip()

            if(len(text_without_spaces)>0):
                print(text_without_spaces)
                try:
                    # Detect language of the text and if it's not English continue to next row
                    languages = detect_langs(text_without_spaces)
                    language = str(languages[0])[0:2]
                    print("processing "+text_without_spaces)
                    if (language != "en"):
                        continue
                    # If text is in english append raw text and processed text to dataframe
                    data.append({"raw_text":post,"text":text_without_spaces})
                except:
                    continue
        self.posts_dataframe = pd.DataFrame(data)
        return self.posts_dataframe







