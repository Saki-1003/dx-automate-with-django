from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol, exchange):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  }

  url = f"https://finance.yahoo.com/quote/{symbol}"

  try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      
      # Get current price
      price_element = soup.find("span", {"data-testid": "qsp-price"})
      current_price = price_element.text.strip()

      # Get price change and percentage change
      price_change_element = soup.find("span",{"data-testid": "qsp-price-change"})
      percentage_change_element = soup.find("span", {"data-testid": "qsp-price-change-percent"})
      price_changed = price_change_element.text.strip() 
      percentage_changed = percentage_change_element.text.strip()

      # Get previous close
      previous_close_element = soup.find("fin-streamer", {"data-field": "regularMarketPreviousClose"})     
      previous_close = previous_close_element.text.strip() 

      # Get 52 week high and low
      fiftyTwo_week_range_element = soup.find("fin-streamer", {"data-field": "fiftyTwoWeekRange"})
      week_range = fiftyTwo_week_range_element.text.strip() 
      week_high, week_low = week_range.split(' - ') 
      week_52_high = week_high.strip()
      week_52_low = week_low.strip() 

      # Get market cap
      market_cap_element = soup.find("fin-streamer", {"data-field": "marketCap"})
      market_cap = market_cap_element.text.strip() 

      # Get PE ratio
      pe_ratio_element = soup.find("fin-streamer", {"data-field": "trailingPE"})
      pe_ratio = pe_ratio_element.text.strip() 

      # Get dividend yield
      label_span = soup.find("span", {"title": "Forward Dividend & Yield"})
      if label_span:
        value_span = label_span.find_next("span", class_="value")
        dividend_yield = value_span.text.strip() 
      else:
        dividend_yield = "N/A"

      stock_response = {
        'current_price': current_price,
        'previous_close': previous_close,
        'price_changed': price_changed,
        'percentage_changed': percentage_changed,
        'week_52_high': week_52_high,
        'week_52_low': week_52_low,
        'market_cap': market_cap,
        'pe_ratio': pe_ratio,
        'dividend_yield': dividend_yield
      }

      return stock_response
  
  except Exception as e:
    print(f"Error scraping the data: {e}")
    return None