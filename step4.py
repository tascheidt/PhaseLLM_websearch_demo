#Step 4 - cleans and augments the data with Google Maps information

import pandas as pd
import googlemaps
from apikeys import maps_api_key
import os

# Your Google Maps API key
API_KEY = maps_api_key

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

def process(location, filename_with_extension, sheet_name):

    cwd = os.getcwd()
    file_path = os.path.join(cwd, filename_with_extension)

    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    rows_to_drop = []

    # Iterate through the DataFrame and search for the restaurant information
    for index, row in df.iterrows():
        restaurant_name = row['Name']
        query = f"{restaurant_name} + {location}"
        place_result = gmaps.places(query=query)

        # Check if the search was successful
        if place_result['status'] == 'OK' and place_result['results']:
            result = place_result['results'][0]
            print(f"Search results for {restaurant_name}:")
            
            # Extract and print details
            name = result['name']
            address = result['formatted_address']
            place_id = result['place_id']
            url = gmaps.place(place_id=result['place_id'])['result']['url']
            status = result.get('business_status', 'UNKNOWN')  # Default to 'UNKNOWN' if not present
            #status = result['business_status']
            latitude = result['geometry']['location']['lat']
            longitude = result['geometry']['location']['lng']
            place_type = ', '.join(result['types'])

            #print the Google Map results to the screen if desired
            """
            print(f"Name: {name}")
            print(f"Address: {address}")
            print(f"Place ID: {place_id}")
            print(f"URL: {url}")
            print(f"Status: {status}")
            print(f"Place Type: {place_type}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            print("---")
            """

            # Write the data back to the DataFrame
            df.at[index, 'Address'] = address
            df.at[index, 'URL'] = url
            df.at[index, 'Place ID'] = result['place_id']
            df.at[index, 'Place Type'] = place_type
            df.at[index, 'Status'] = status
            df.at[index, 'Latitude'] = latitude
            df.at[index, 'Longitude'] = longitude
        else:
            rows_to_drop.append(index)
            print(f"No results found for {restaurant_name}.")

    # Drop rows with no results or businesses that are CLOSED_PERMANENTLY
    df.drop(rows_to_drop, inplace=True)
    df = df[df['Status'] != "CLOSED_PERMANENTLY"]

    # Drop duplicate entries based on Place ID
    duplicate_rows = df[df.duplicated(subset='Place ID', keep='first')].index.tolist()
    for r in duplicate_rows:
        print(f"Duplicate Place ID found for row {r}. This row will be deleted.")

    df.drop_duplicates(subset='Place ID', keep='first', inplace=True)

    # Save the updated DataFrame back to the Excel file
    df.to_excel(file_path, sheet_name=sheet_name, index=False)

    print("Process completed. Excel file has been updated.")
    results4 = "Step 4 worked, results written to Filename: " + file_path
    return results4