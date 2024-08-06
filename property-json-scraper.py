import requests
from bs4 import BeautifulSoup
import json
import csv

def get_property_data(base_url):
    properties = []
    index = 0

    while True:
        url = f"{base_url}&index={index}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', string=lambda string: string and 'jsonModel' in string)
        
        if script_tag:
            json_text = script_tag.string.split('jsonModel = ')[1].rsplit(';', 1)[0]
            data = json.loads(json_text)
            if 'properties' not in data or not data['properties']:
                break
            properties.extend(data['properties'])
        else:
            break

        index += 24  # Increment index to get the next page

    return properties

def extract_property_details(property):
    return {
        "id": property.get("id"),
        "bedrooms": property.get("bedrooms"),
        "bathrooms": property.get("bathrooms"),
        "numberOfImages": property.get("numberOfImages"),
        "numberOfFloorplans": property.get("numberOfFloorplans"),
        "numberOfVirtualTours": property.get("numberOfVirtualTours"),
        "summary": property.get("summary"),
        "displayAddress": property.get("displayAddress"),
        "countryCode": property.get("countryCode"),
        "location": property.get("location"),
        "propertyImages": property.get("propertyImages"),
        "propertySubType": property.get("propertySubType"),
        "listingUpdateReason": property.get("listingUpdate", {}).get("listingUpdateReason"),
        "listingUpdateDate": property.get("listingUpdate", {}).get("listingUpdateDate"),
        "premiumListing": property.get("premiumListing"),
        "featuredProperty": property.get("featuredProperty"),
        "price": property.get("price"),
        "propertyType": property.get("propertyType"),
        "customerSegment": property.get("customerSegment"),
        "availableFrom": property.get("availableFrom"),
        "letAgreed": property.get("letAgreed"),
        "branchId": property.get("branchId"),
        "propertyUrl": property.get("propertyUrl"),
        "shortDescription": property.get("shortDescription"),
        "longDescription": property.get("longDescription"),
        "commercial": property.get("commercial"),
        "residential": property.get("residential"),
        "newHome": property.get("newHome"),
        "auction": property.get("auction"),
    }

def save_to_csv(properties, filename='property-json-output.csv'):
    keys = properties[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(properties)

def main():
    base_url = "https://www.rightmove.co.uk/property-for-sale/find.html?includeSSTC=true&locationIdentifier=BRANCH%5E8764"
    properties = get_property_data(base_url)
    extracted_properties = [extract_property_details(prop) for prop in properties]
    save_to_csv(extracted_properties)

if __name__ == "__main__":
    main()