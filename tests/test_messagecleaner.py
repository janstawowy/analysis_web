import pytest
from sentiment import MessageCleaner  # Replace 'your_module' with the actual module containing MessageCleaner

def test_return_messages():
    # Create an instance of MessageCleaner
    cleaner = MessageCleaner()

    # Test case 1: Empty list of posts
    posts = []
    result_dataframe = cleaner.return_messages(posts)
    assert result_dataframe.empty  # Check if the resulting DataFrame is empty

    # Test case 2: Non-English posts
    posts = ["<p>Este es espanol post 1</p>", "<p>Este es espanol post 2</p>"]
    result_dataframe = cleaner.return_messages(posts)
    assert result_dataframe.empty  # Check if the resulting DataFrame is empty

    # Test case 3: English posts
    posts = ["<p>English post 1</p>", "<p>English post 2</p>"]
    result_dataframe = cleaner.return_messages(posts)
    assert not result_dataframe.empty  # Check if the resulting DataFrame is not empty
    assert "raw_text" in result_dataframe.columns  # Check if the raw_text column is present
    assert "text" in result_dataframe.columns  # Check if the text column is present
