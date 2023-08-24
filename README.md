# Sample project using to PhaseLLM Web Search Agents and LLMs

Sample project to use PhaseLLM Web Search Agent to create a list of places to go, LLM (OpenAI) to synthesize the results, and Google Maps API to augment the list. Users can input the location, type of places, queries, and LLM prompt via a simple frontend built with Streamlit. 

You need API access to OpenAI, Google's [Custom Search API] (https://developers.google.com/custom-search/v1/overview), and Google's Google Maps API (https://developers.google.com/maps/documentation/javascript/get-api-key)

To run the demo, simply type 'streamlit run app_streamlit.py' from your development environment

The demo will run python files for each step: 
- `step1.py` search the web and crawl the search results
- `step2.py` extract data about restaurants from the above
- `step3.py` converts the results into an Excel file
- 'step4.py' add Google Maps data and cleans up any duplicates, locations that are closed, or don't have a maps listing

Note that this requires [PhaseLLM](https://phasellm.com/) version 0.0.14 or later.
