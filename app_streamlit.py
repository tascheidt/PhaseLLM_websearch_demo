import step1
import step2
import step3
import step4
import streamlit as st
import pandas as pd
import base64
from io import BytesIO


def run_step1(location, place_type, queries):
    result1 = step1.process(location, place_type, queries)
    return result1

#create a function to run step2
def run_step2(message_prompt):
    result2 = step2.process(message_prompt)
    return result2

#create a function to run step3
def run_step3(location, place_type, filename_with_extension, sheet_name):
    result3 = step3.process(location, place_type, filename_with_extension, sheet_name)
    return result3

#create a funtion to run step4
def run_step4(location, filename_with_extension, sheet_name):
    result4 = step4.process(location, filename_with_extension, sheet_name)
    return result4


st.title("Supercool PhaseLLM Demo 😎")
st.divider()

st.title("Preferences form for your tour location and type of tour")

with st.form('Inputs'):
    location = st.text_input("Location", "Tokyo, Japan")
    place_type = st.text_input("Place type", "Restaurants")
    queries = st.text_area("Search queries, you don't need to include the location in your queries", "best japanese restaurants in ginza part of tokyo\n"
                                    "ginza restaurants that only locals know\n"
                                    "tokyo ginza restaurants that are holes in the wall but AMAZING\n"
                                    "best tokyo ginza restaurants you can't miss", height=200)
    message_prompt_text = """You are a culinary researcher putting together a food tour. This food tour needs to include the best restaurants from a broader list that has been provided to you. You are going to follow these steps in generating your list:
1. You will be given content to review.
2. Please review the content and simply make a list of all the restaurants mentioned.
3. Each element in the list should ONLY include the (a) restaurant name, and (b) a 5-10 word description of the food they serve.
Please provide the output in the following format for each restaurant:
NAME: <restaurant name>
DESCRIPTION: <5-10 words describing the food>
<exactly one line break between each restaurant>"""

    message_prompt = st.text_area("Message Prompt for ChatGPT", value=message_prompt_text, height=300)
    filename = place_type + "-in-" + location
    #filename = st.text_input("Filename", "restaurants-in-ginza")
    filename_with_extension = filename + ".xlsx"
    sheet_name = location + "-" + place_type
    sheet_name = sheet_name[:30]

    submit = st.form_submit_button('Submit')

    if submit:
        result1_message, titles_crawled = run_step1(location, place_type, queries)
        st.title("Results from step 1")
        st.write(result1_message)
        st.write("Crawled sites:")
        for title in titles_crawled:
            st.write(title)

        result2 = run_step2(message_prompt)  # Add appropriate arguments if needed
        st.title("Results from step 2")
        st.write(result2)

        result3 = run_step3(location,place_type, filename_with_extension, sheet_name)  # Add appropriate arguments if needed
        st.title("Results from step 3")
        st.write(result3)

        result4 = run_step4(location, filename_with_extension, sheet_name)  # Add appropriate arguments if needed
        st.title("Results from step 4")
        st.write(result4)

        # display results
        st.divider()
        st.title("Here are your results. Enjoy!")

        # Read Excel file from user input
        df = pd.read_excel(filename_with_extension, sheet_name=sheet_name)

        def get_table_download_link(df, filename_with_extension=filename_with_extension):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name=sheet_name)
            excel_data = output.getvalue()
            b64 = base64.b64encode(excel_data).decode()
            return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename_with_extension}">Download Excel file</a>'

        # Display results
        st.dataframe(df)

        st.markdown(get_table_download_link(df), unsafe_allow_html=True)


