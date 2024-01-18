#This file use AI to determine how to transform one csv to another one, it save the result in a json


import json
import os
import pandas as pd
import questionary
from openai import OpenAI

prompt_system = """
For a python program that transform the content of the first csv file to the format (column names) of the second csv file using a list of pandas custom transformation
return a json map of expression that for each column name in the second csv provide the panda expression of the transformation to be use in the panda eval function.
for instance if the first csv has colums 'A','B','C' and the second has columns 'D','E','F','G' and from the analysis of the data you infer that 'D' must contains 'B', 'E' must be left empty, 'F' is 'B' +'C' and G is 'C' then returns
```json
{ 
  "D":"`B`",
  "E":"",
  "F":"`B`+`C`",
  "G":"`C`"
}
```
Always add single  in backticks (`) to the columns name in the panda expression as they may contain spaces.
Analyze the content of the file to infer the transformations, not only the column names.
Use also the hint provided.

"""

client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))


# Fonction pour envoyer une requête à l'API ChatGPT
def chatgpt_request(hint, csv_file1, csv_file2):
    print(f"Sending request to ChatGPT for hint: {hint}")

    # read the first 20 lines of csv_file1
    df1 = pd.read_csv(csv_file1, nrows=20)
    #print(f"csv1:\n{df1.to_string()}")
    # read the first 20 lines of csv_file2
    df2 = pd.read_csv(csv_file2, nrows=20)
    #print(f"csv2:\n{df2.to_string()}")

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": f"csv1:\n{df1.to_string()}"},
                {"role": "user", "content": f"csv2:\n{df2.to_string()}"},
                {"role": "user", "content": hint}
            ],
            max_tokens=4000,
            n=1,
            temperature=0)
        return response
    except Exception as e:
        print(f"Erreur lors de la requête à l'API : {e}")
        return None



def get_files_and_dirs(path):
    """ Helper function to list directories and files in the given path """
    items = ['../'] + [item + ('/' if os.path.isdir(os.path.join(path, item)) else '') for item in os.listdir(path)]
    return sorted(items, key=lambda x: (not x.endswith('/'), x))

def choose_file(start_path='.', label="Choose a file or directory:"):
    """ Allow the user to navigate directories and choose a file, with cursor initially on start_path if it's a file """
    if os.path.isfile(start_path):
        current_path = os.path.dirname(start_path)
        initial_choice = os.path.basename(start_path)
    else:
        current_path = os.path.abspath(start_path)
        initial_choice = None

    while True:
        choices = get_files_and_dirs(current_path)
        choice = questionary.select(label, choices=choices, default=initial_choice).ask()
        if choice.endswith('/'):
            if choice == '../':
                current_path = os.path.dirname(current_path)
            else:
                current_path = os.path.join(current_path, choice[:-1])
            initial_choice = None  # Reset initial choice after navigating directories
        else:
            return os.path.join(current_path, choice), current_path


def generate_transformation_filename(input_filename):
    """ Generate the default transformation filename based on the input filename """
    base, ext = os.path.splitext(input_filename)
    return f"{base}_transform.json"

def main():
    
    cookie_file = "convert_cookie.json"
    saved_output_file = "."
    target_format_file = "."
    default_input_file = "."
    default_hint = ""
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            try:
                cookie_data = json.load(f)
                print(cookie_data)
                default_hint = cookie_data.get('hint', '')
                default_input_file = cookie_data.get('input_file', '.')
                target_format_file = cookie_data.get("target_format_file","")
                saved_output_file = cookie_data.get('transfo_file', '')
            except json.JSONDecodeError:
                print("Error reading cookie file, using default values.")

    file1, path1 = choose_file(label="Choose the csv file to convert:",start_path=default_input_file)
    if(target_format_file==""):
        target_format_file = path1
    file2, _ = choose_file(start_path=target_format_file,label="Choose the target csv file format (choose the file itself):")

    default_output_file = generate_transformation_filename(file1)
    output_file = questionary.text("Enter the name of the output transformation :", default=default_output_file).ask()
    # check if there is a file called "convert_cookie.txt" if yes read its content in a default_hit variable
   
    
    hint = questionary.text("Enter a hint to help understand the transformation:",default=default_hint).ask()
    
    if hint != default_hint or output_file != saved_output_file:
        with open(cookie_file, 'w') as f:
            json.dump({'hint': hint, 'input_file':file1,'target_format_file':file2,'transfo_file': output_file}, f)

    if not file1 or not file2 or not output_file:
        return

    chatgpt_response = chatgpt_request(hint, file1, file2)
    #print(chatgpt_response)
    if not chatgpt_response:
        return
    # Write the response to the output file
    with open(output_file, 'w') as f:
        f.write(chatgpt_response.choices[0].message.content)

if __name__ == "__main__":
    main()