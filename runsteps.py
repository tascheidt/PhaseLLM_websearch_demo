import step1
import step2
import step3
import step4

# earch run_step function, add an input prompt for each parameter


def run_step1():
    location = input("Location: ")
    place_type = input("Place type: ")
    queries = input("Search queries, you don't need to include the location in your queries: ")
    result1 = step1.process(location, place_type, queries)
    return result1

#create a function to run step2
def run_step2():
    message_prompt = input("Message Prompt for ChatGPT: ")
    result2 = step2.process(message_prompt)
    return result2

#create a function to run step3
def run_step3():
    location = input("Location: ")
    place_type = input("Place type: ")
    filename_with_extension = input("Filename: ")
    sheet_name = input("Sheet name: ")
    result3 = step3.process(location, place_type, filename_with_extension, sheet_name)
    return result3

#create a funtion to run step4
def run_step4():
    location = input("Location: ")
    filename_with_extension = input("Filename: ")
    sheet_name = input("Sheet name: ")
    result4 = step4.process(location, filename_with_extension, sheet_name)
    return result4

if __name__ == "__main__":
    import sys

    step_to_run = sys.argv[1] if len(sys.argv) > 1 else "all"

    if step_to_run == "all" or step_to_run == "1":
        print(run_step1())
    if step_to_run == "all" or step_to_run == "2":
        print(run_step2())
    if step_to_run == "all" or step_to_run == "3":
        print(run_step3())
    if step_to_run == "all" or step_to_run == "4":
        print(run_step4())
