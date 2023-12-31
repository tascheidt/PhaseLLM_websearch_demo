"""
Welcome to a PhaseLLM demo app where we build a spreadsheet of restaurant recommendations for you!

There are three parts to this process, separated into three separate files:
1. step1.py -- uses PhaseLLM's WebSearchAgent to get a list of URLs to crawl and crawls those URLs
2. step2.py -- use an LLM to extract and aggregate restaurant information
3. step3.py -- saves the outputs into an Excel file

This file is step3.py

Questions? Please reach out: w --at-- phaseai --dot-- com

"""

def process(location, place_type, filename_with_extension, sheet_name):
    
    import json
    import pandas as pd

    # Adding the .xlsx extension to the filename
    filename_with_extension = filename_with_extension
    sheet_name = sheet_name

    # Load processed JSON file.
    parsed = {}
    with open("parsed.json", "r") as reader:
        parsed = json.loads(reader.read())

    # Convert the JSON into a Pandas DataFrame and save it to an Excel file
    df = pd.DataFrame.from_records(list(parsed.values()))
    df.to_excel(filename_with_extension, sheet_name=sheet_name)
    
    # Including the filename in the results
    results3 = "Step 3 worked, results written to Filename: " + filename_with_extension + " on the sheet named: " + sheet_name
    return results3

