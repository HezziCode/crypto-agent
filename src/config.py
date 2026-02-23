from agents import AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunConfig 
from dotenv import load_dotenv
import os
import requests


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client

)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)


@function_tool
def crypto_prices(crypto: str):
    """
    Fetches the current price of a given cryptocurrency using CoinGecko's API.

    Parameters:
        crypto (str): The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').

    Returns:
        dict: A dictionary containing the current price in USD.

    Raises:
        Exception: If the API request fails or the response is invalid.
    """
   
    try:
        # CoinGecko free API - no API key required
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': crypto.lower(),
            'vs_currencies': 'usd'
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if crypto.lower() in data:
            price = data[crypto.lower()]['usd']
            return {
                'crypto': crypto,
                'price_usd': price,
                'status': 'success'
            }
        else:
            return {
                'crypto': crypto,
                'error': f'Cryptocurrency "{crypto}" not found',
                'status': 'error'
            }

    except requests.exceptions.RequestException as e:
        return {
            'crypto': crypto,
            'error': f'API request failed: {str(e)}',
            'status': 'error'
        }
    except Exception as e:
        return {
            'crypto': crypto,
            'error': f'Unexpected error: {str(e)}',
            'status': 'error'
        }


@function_tool
def market_sentiment():
    """
    Analyzes market sentiment using 24h global market cap change from CoinGecko.

    Returns:
        dict: A dictionary indicating if the market is bullish or bearish.
    """
    try:
        response = requests.get("https://api.coingecko.com/api/v3/global")
        response.raise_for_status()
        data = response.json()

        change = data["data"]["market_cap_change_percentage_24h_usd"]
        sentiment = "bullish 📈" if change > 0 else "bearish 📉"

        return {
            'sentiment': sentiment,
            'market_cap_change_24h': round(change, 2),
            'status': 'success'
        }

    except requests.exceptions.RequestException as e:
        return {
            'error': f'API request failed: {str(e)}',
            'status': 'error'
        }
    except Exception as e:
        return {
            'error': f'Unexpected error: {str(e)}',
            'status': 'error'
        }



@function_tool
def trending_coins():
    """
    Fetches currently trending cryptocurrencies from CoinGecko.

    Returns:
        dict: A dictionary containing a list of trending coin names.
    """
    try:
        response = requests.get("https://api.coingecko.com/api/v3/search/trending")
        response.raise_for_status()
        data = response.json()
        coins = [coin["item"]["name"] for coin in data["coins"]]
        return {
            'trending': coins,
            'status': 'success'
        }
    except requests.exceptions.RequestException as e:
        return {
            'error': f'API request failed: {str(e)}',
            'status': 'error'
        }
    except Exception as e:
        return {
            'error': f'Unexpected error: {str(e)}',
            'status': 'error'
        }