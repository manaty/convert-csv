#This file transform one csv to another one, using a list of transformation


import json
import os
import pandas as pd
import questionary


def apply_transformation(input_csv_path, transformation_json_path, output_csv_path):
    # Load the transformation rules from the JSON file
    with open(transformation_json_path, 'r') as file:
        transformations = json.load(file)

    # Load the input CSV file
    input_df = pd.read_csv(input_csv_path)

    # Initialize an empty DataFrame for the transformed data
    transformed_df = pd.DataFrame()

    # Apply transformations
    for column, transformation in transformations.items():
        if transformation:
            try:
                # Dynamically evaluate the transformation
                transformed_df[column] = input_df.eval(transformation)
            except Exception as e:
                print(f"Error applying transformation for column {column}: {e}")
        else:
            # Handle empty transformations (create an empty column or drop)
            transformed_df[column] = pd.NA

    # Save the transformed DataFrame to a new CSV file
    transformed_df.to_csv(output_csv_path, index=False)
    print(f"Transformed CSV saved to {output_csv_path}")

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

    #print(f"current path:{current_path}")
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


def generate_output_filename(input_filename):
    """ Generate the default output filename based on the input filename """
    base, ext = os.path.splitext(input_filename)
    return f"{base}_out{ext}"

def main():
    # check if there is a file called "convert_cookie.txt" if yes read its content in a default_hit variable
    cookie_file = "convert_cookie.json"
    transfo_file = ""
    default_input_file = "."
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            try:
                cookie_data = json.load(f)
                #print(cookie_data)
                default_input_file = cookie_data.get('input_file', '.')
                transfo_file = cookie_data.get('transfo_file', '')
            except json.JSONDecodeError:
                print("Error reading cookie file, using default values.")
    file1, _ = choose_file(label="Choose the csv file to convert:",start_path=default_input_file)
    file2, _ = choose_file(start_path=transfo_file,label="Choose the json transformation file:")
    default_output_file = generate_output_filename(file1)
    output_file = questionary.text("Enter the name of the output file :", default=default_output_file).ask()
    
    if not file1 or not file2 or not output_file:
        return

    apply_transformation(file1,file2,output_file)
    
if __name__ == "__main__":
    main()