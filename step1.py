def process(location, place_type, queries):
    import json
    import os
    from phasellm.agents import WebSearchAgent
    from itertools import chain
    from apikeys import openai_key, google_api_key, search_id

    openai_key = openai_key
    google_api_key = google_api_key
    search_id = search_id

    # Instantiate the PhaseLLM WebSearchAgent
    w = WebSearchAgent(api_key=google_api_key)

    # Split the queries text into a list of queries
    queries_list = queries.strip().split("\n")

    # Append location to each query aka the Veronica feature!
    queries_list_with_location = [f"{query} + \"{location}\"" for query in queries_list]

    # Loop through each query with location and get the results
    results = []
    for query_with_location in queries_list_with_location:
        print(query_with_location)
        results_new = w.search_google(query=query_with_location, custom_search_engine_id=search_id, num=10)
        results = list(chain(results, results_new))

    # We save each title, URL, description, and content of the URL into a JSON file
    results_dict = {"results": []}
    for result in results:
        r = {
            "title": result.title,
            "url": result.url,
            "desc": result.description,
            "content": result.content,
        }
        results_dict["results"].append(r)

    # Get the current working directory
    cwd = os.getcwd()

    # Combine the current working directory with the filename
    filename = os.path.join(cwd, "search.json")

    # Create the file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, 'w'):
            pass

    # Now write the file using the absolute path
    with open(filename, "w") as writer:
        writer.write(json.dumps(results_dict))

    titles_crawled = [result['title'] for result in results_dict['results']]

    num_sites_crawled = len(results_dict['results'])
    print(f"Number of sites found and crawled: {num_sites_crawled}")

    results_message = f"Step 1 worked. Number of sites found and crawled: {num_sites_crawled}"
    
    return results_message, titles_crawled
