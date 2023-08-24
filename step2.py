from phasellm.llms import OpenAIGPTWrapper, ChatBot, ChatPrompt
from apikeys import openai_key, google_api_key, search_id
import json
import os

def parse_lines(content, results):
    """
    We expect our chatbot to return a piece of text with the following format:

    NAME: <restaurant 1>
    DESCRIPTION: <description 1>

    NAME: <restaurant 2>
    DESCRIPTION: <description 2>

    ... and so on

    This function parses the output above into a set of dictionary objects and appends it back into the results object.
    """
    if results is None:
        results = {}

    lines = content.split("\n")
    for i in range(len(lines)):
        line = lines[i].strip()
        if line and line.startswith("NAME"):
            restaurant_name = line[6:].strip()
            if restaurant_name not in results:
                results[restaurant_name] = {
                    "Name": restaurant_name,
                    "Description": "",
                    "Count": 1,
                }
            else:
                results[restaurant_name]["Count"] += 1

            if i + 1 < len(lines):
                desc = lines[i + 1][13:].strip()
            else:
                # Handle the case where i + 1 is out of range
                desc = ""

            if desc:
                results[restaurant_name]["Description"] += f"- {desc}\n"

    return results

def process(messageprompt):

    # Message prompts
    message_prompt_1 = messageprompt
    message_prompt_2 = """Here is the information to review.
------------------------------------------
{title}

{content} 
"""

    # Set up the ChatBot flow with the prompts above
    cp = ChatPrompt([
        {"role": "system", "content": message_prompt_1},
        {"role": "user", "content": message_prompt_2},
    ])

    llm = OpenAIGPTWrapper(openai_key, model="gpt-3.5-turbo-16k")
    cb = ChatBot(llm)

    # Load results from step1.py
    results = []
    with open("search.json", "r") as reader:
        results_ = reader.read()
        results = json.loads(results_)["results"]

    # Parse the results from step1.py
    parsed = {}
    ctr_r = 1
    for r in results:
        # Helper print() statements to show where we're at
        print(ctr_r)
        ctr_r += 1
        print(r["title"])

        # Use the PhaseLLM ChatBot object to fill in our prompt
        cb.messages = cp.fill(content=r["content"], title=r["title"])

        # Send and process the content using the ChatBot approach above
        try:
            response = cb.resend()
        except:
            print("Error, likely due to length of content. Trying shorter content.")
            cb.messages = cp.fill(content=r["content"][0:10000], title=r["title"])
            response = cb.resend()

        parsed = parse_lines(response, parsed)

    # Save results to JSON
    # Get the current working directory
    cwd = os.getcwd()
    filename = os.path.join(cwd, "parsed.json")

    # Create the file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, 'w'):
            pass

    with open(filename, "w") as writer:
        writer.write(json.dumps(parsed))

    results2 = "Step 2 worked, results written to parsed.json"
    return results2


