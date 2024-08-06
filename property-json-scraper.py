import requests
from bs4 import BeautifulSoup
import json
import csv

def fetch_properties(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', string=lambda text: text and 'jsonModel' in text)
    
    if script_tag:
        try:
            json_text = script_tag.string.split('=', 1)[1].strip(' ;')
            json_data = json.loads(json_text)
            return json_data['properties']
        except Exception as e:
            print(f"Error processing JSON data: {e}")
            return []
    else:
        print("No script tag with 'jsonModel' found.")
        return []

def extract_property_details(property):
    main_image_base_url = "https://media.rightmove.co.uk/"
    first_image = next((img['url'] for img in property.get('propertyImages', {}).get('images', []) if 'url' in img), '')
    price_data = property.get('price', {})
    display_price = price_data.get('displayPrices', [{}])[0].get('displayPrice', '') if 'displayPrices' in price_data else ''
    display_price_qualifier = price_data.get('displayPrices', [{}])[0].get('displayPriceQualifier', '') if 'displayPrices' in price_data else ''
    
    return {
        "slug": property.get('id', ''),
        "title": property.get('displayAddress', ''),
        "bedrooms": property.get('bedrooms', ''),
        "bathrooms": property.get('bathrooms', ''),
        "numberOfImages": property.get('numberOfImages', ''),
        "numberOfFloorplans": property.get('numberOfFloorplans', ''),
        "numberOfVirtualTours": property.get('numberOfVirtualTours', ''),
        "summary": property.get('summary', ''),
        "displayAddress": property.get('displayAddress', ''),
        "countryCode": property.get('countryCode', ''),
        "location": property.get('location', {}),
        "propertyImages": main_image_base_url + first_image,
        "propertySubType": property.get('propertySubType', ''),
        "listingUpdateReason": property.get('listingUpdate', {}).get('listingUpdateReason', ''),
        "listingUpdateDate": property.get('listingUpdate', {}).get('listingUpdateDate', ''),
        "premiumListing": property.get('premiumListing', False),
        "featuredProperty": property.get('featuredProperty', False),
        "displayPrice": display_price,
        "displayPriceQualifier": display_price_qualifier,
        "propertyType": property.get('propertyTypeFullDescription', ''),
        "customerSegment": property.get('customer', {}).get('customerSegment', ''),
        "availableFrom": property.get('availableFrom', ''),
        "letAgreed": property.get('letAgreed', False),
        "branchId": property.get('customer', {}).get('branchId', ''),
        "propertyUrl": f"https://www.rightmove.co.uk{property.get('propertyUrl', '')}",
        "shortDescription": property.get('shortDescription', ''),
        "longDescription": property.get('summary', ''),  # Assuming longDescription is the same as summary
        "commercial": property.get('commercial', False),
        "residential": property.get('residential', False),
        "newHome": property.get('newHome', False),
        "auction": property.get('auction', False),
    }

def main():
    base_url = "https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E8764"
    index = 0
    all_properties = []

    while True:
        url = f"{base_url}&index={index}"
        properties = fetch_properties(url)
        if not properties:
            break
        all_properties.extend(properties)
        index += 24  # Assuming each page lists 24 properties

    if not all_properties:
        print("No properties found.")
        return

    extracted_properties = [extract_property_details(prop) for prop in all_properties]

    keys = extracted_properties[0].keys()
    with open('property-json-output.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(extracted_properties)

if __name__ == "__main__":
    main()