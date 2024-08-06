import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_properties(base_url):
    properties = []
    seen_links = set()
    index = 0  # Start with the first page

    while True:
        url = f"{base_url}&index={index}"
        print(f"Fetching page with index {index}: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find property listings
        listings = soup.find_all('div', class_='l-searchResult is-list')
        if not listings:
            break  # Exit the loop if no listings are found
        print(f"Found {len(listings)} listings on page with index {index}")

        for listing in listings:
            try:
                property_id = listing.get('id').replace('property-', '') if listing.get('id') else ''
                title = listing.find('h2', class_='propertyCard-title').text.strip()
                price = listing.find('div', class_='propertyCard-priceValue').text.strip()
                address = listing.find('address', class_='propertyCard-address').text.strip()
                details_link = listing.find('a', class_='propertyCard-link')['href']
                full_link = f"https://www.rightmove.co.uk{details_link}"

                image_tag = listing.find('div', class_='propertyCard-img').find('img')
                image_url = image_tag['src'] if image_tag else ''

                property_info = listing.find('div', class_='property-information')
                if property_info:
                    spans = property_info.find_all('span')
                    span_count = len(spans)
                    
                    property_type = spans[0].text.strip() if span_count > 0 else 'N/A'
                    bedroom_icon = 'Y' if span_count > 1 and 'bed-icon' in spans[1].get('class', []) else 'N'
                    no_of_bedrooms = spans[2].text.strip() if span_count > 2 else 'NULL'
                    bathroom_icon = 'Y' if span_count > 3 and 'bathroom-icon' in spans[3].get('class', []) else 'N'
                    no_of_bathrooms = spans[4].text.strip() if span_count > 4 else 'NULL'
                else:
                    property_type = 'N/A'
                    bedroom_icon = 'N'
                    no_of_bedrooms = 'NULL'
                    bathroom_icon = 'N'
                    no_of_bathrooms = 'NULL'

                if title and price and address and full_link and full_link not in seen_links:
                    properties.append({
                        'property_id': property_id,
                        'title': title,
                        'price': price,
                        'address': address,
                        'details_link': full_link,
                        'image_url': image_url,
                        'property_type': property_type,
                        'bedroom_icon': bedroom_icon,
                        'no_of_bedrooms': no_of_bedrooms,
                        'bathroom_icon': bathroom_icon,
                        'no_of_bathrooms': no_of_bathrooms
                    })
                    seen_links.add(full_link)
            except AttributeError as e:
                print(f"Error parsing listing: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        # Increment index to get the next page
        index += 24

    return properties

# Base URL of the estate agent's listings page
base_url = "https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E8764"

properties = get_properties(base_url)

# Save the properties to a CSV file
df = pd.DataFrame(properties)
df.to_csv('estate_agent_properties-new.csv', index=False)