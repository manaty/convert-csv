# convert-csv
AI tool to convert your input csv to the same format as an output csv 

## Pain point
You created a program that handle some specific csv file but your users keep using csv files that do not comply with your format  

## Solution 
With python installed and an openAI key set in your env variables (set it in the ./private/keys.json ) run the setup script
```
. setup_environment.sh
```  

Run the script that will infer the transformation between your client file and your desired file format.

```
python3 infer_transfo.py
```

this creates a json file with the list of expression to transform your file.

EDIT THIS FILE AND CHECK ITS CONTENT, this is mandatory to make sure no malicious code is executed by the transformation step.  

Run the transformation by selecting the input file (it could be different than input file used in the previous step) and the transformation file.
```
python3 transform_csv.py
```

## Note about the CLI commands

When doing some test it is annoying to always navigate to the same folders to select the files, the program save the last choices in some "CLI cookie" file `convert_cookies.json` in the directory where you run the program.