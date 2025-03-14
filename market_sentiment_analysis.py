"""
This file runs sentiment analysis on Reddit data for a given list of subreddits
and a specific stock symbol. It uses the general_reddit_analysis and
specific_stock_analysis functions from the reddit_analysis module to perform
the analysis.

- It uses the concurrent.futures module to run the analysis functions in parallel.
- This reduces the time for 2 10 post reddit analysis from 50 seconds to 30 seconds as they dont run one after the other.
- each new subreddit analysis for 10 post will take a max of 30 seconds no matter how many subreddits are added.

- it also uses yaspin for spinner to show the progress of the analysis.
- The spinner will show when the analysis is running and will stop when the analysis is completed.
"""

from sentiment_analysis import general_reddit_analysis, specific_stock_analysis
from market_analysis import merge_stock_data
import concurrent.futures


def general_stock_and_social_analysis(subreddit: str, limit: int, comment_limit: int, post_type: str, stock_period: str) -> dict:
    """
    Perform general Reddit analysis for a subreddit and a financial analysis from those results.

    Parameters:
        subreddit (str): The name of the subreddit to analyze.
        limit (int): The maximum number of posts to retrieve.

    Returns:
        dict: A dictionary containing the analysis results for the subreddit.
    """
    general_analysis = general_reddit_analysis(subreddit, limit, comment_limit, post_type)
    financial_data = merge_stock_data(general_analysis, stock_period)

    return {subreddit: financial_data}


def specific_stock_and_social_analysis(subreddit: str, stocks: list, limit: int, comment_limit: int, post_type: str, stock_period: str) -> dict:
    """
    Perform specific stock analysis for a subreddit and a financial analysis from those results.

    Parameters:
        subreddit (str): The name of the subreddit to analyze.
        stock (str): The stock symbol to analyze. must be in the format TSLA for Tesla, AAPL for Apple, etc.
        limit (int): The maximum number of posts to retrieve.

    Returns:
        dict: A dictionary containing the analysis results for the subreddit.
    """
    specific_analysis = specific_stock_analysis(subreddit, stocks, limit, comment_limit, post_type)

    financial_data = merge_stock_data(specific_analysis, stock_period)

    return {subreddit: financial_data}


def run_general_analysis(subreddits: list, limit: int = 10, comment_limit: int = 10, post_type: str = "hot", stock_period: str = "1mo") -> list[dict]:
    """
    Perform sentiment analysis on a list of subreddits for all stocks.

    Parameters:
        subreddits (list): A list of subreddit names to analyze.
        limit (int): The maximum number of posts to retrieve for each subreddit. Defaults to 10.

    Returns:
        list[dict]: A list containing a dictionary for each subreddit, with the analysis results for that subreddit.
    """
    results = []  # Store the results of each subreddit analysis

    # Run sentiment analysis in parallel on each subreddit
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("📈 Sentiment Analysis in progress...")
        futures = []
        futures.extend(
            executor.submit(
                general_stock_and_social_analysis,
                subreddit,
                limit,
                comment_limit,
                post_type,
                stock_period,
            )
            for subreddit in subreddits
        )
        results.extend(future.result() for future in futures)
        print("✅ Sentiment Analysis completed!")
    return results


def run_specific_stock_analysis(
    subreddits: list, stocks: list, limit: int = 10, comment_limit: int = 10, post_type: str = "hot", stock_period: str = "1mo"
) -> list[dict]:
    """
    Perform sentiment analysis on a list of subreddits for a specific stock.

    Parameters:
        subreddits (list): A list of subreddit names to analyze.
        stock (str): The stock symbol to analyze. must be in the format TSLA for Tesla, AAPL for Apple, etc.
        limit (int): The maximum number of posts to retrieve for each subreddit. Defaults to 10.

    Returns:
        list[dict]: A list containing a dictionary for each subreddit, with the analysis results in that subreddit for a specific stock.
    """
    results = []  # Store the results of each subreddit analysis

    # Run sentiment analysis in parallel on each subreddit
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("📈 Sentiment Analysis in progress...")
        futures = []
        futures.extend(
            executor.submit(
                specific_stock_and_social_analysis,
                subreddit,
                stocks,
                limit,
                comment_limit,
                post_type,
                stock_period,
            )
            for subreddit in subreddits
        )
        results.extend(future.result() for future in futures)
        print("✅ Sentiment Analysis completed!")

    return results
