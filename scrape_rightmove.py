import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page(url):
    response = requests.get(url)
    return response.text

def parse_listing(listing):
    spans = listing.find_all('span')
    span_count = len(spans)
    return {
        'span_count': span_count,
        'listing_html': str(listing)
    }

def scrape_rightmove(url):
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, 'html.parser')
    listings = soup.find_all('div', class_='propertyCard')

    data = []
    for listing in listings:
        data.append(parse_listing(listing))
    
    return data

# URL for the property listings (example URL)
url = 'https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E8764&index=0'

data = scrape_rightmove(url)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('rightmove_listings.csv', index=False)
print(df.head())