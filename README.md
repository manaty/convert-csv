# convert-csv
AI tool to convert your input [csv](https://www.ietf.org/rfc/rfc4180.txt) to the same format as an output csv 

## Pain point
You created a program that handle some specific csv file but your users keep using csv files that do not comply with your format  

## Solution 
With python installed and an [openAI key](./private/keys.json) run the setup script
```
. setup_environment.sh
```  

Run the script that will infer the transformation between your client file and your desired file format.

```
python infer_transfo.py
```
![image](https://github.com/manaty/convert-csv/assets/16659140/19ad30c0-0da8-4547-b979-c2da10312321)

this creates a json file with the list of expression to transform your file.

EDIT THIS FILE AND CHECK ITS CONTENT, this is mandatory to make sure no malicious code is executed by the transformation step.  
![image](https://github.com/manaty/convert-csv/assets/16659140/87a8bc2e-3230-4bd8-bad7-14a6be1bf4b0)

in that example the IA decided to change the price from USD to EUR, lets just copy it

![image](https://github.com/manaty/convert-csv/assets/16659140/3078a875-f52d-4fe6-b20a-fe0368604f45)


Run the transformation by selecting the input file (it could be different than input file used in the previous step) and the transformation file.
```
python transform_csv.py
```
![image](https://github.com/manaty/convert-csv/assets/16659140/a9963da0-78c2-4deb-b510-5d917607e1a5)

![image](https://github.com/manaty/convert-csv/assets/16659140/102a0270-1e0e-4fa4-b912-d1eea2efa524)

![image](https://github.com/manaty/convert-csv/assets/16659140/53f7b894-26d7-4297-8a46-38da12a93e8e)

## Note about the CLI commands

When doing some test it is annoying to always navigate to the same folders to select the files, the program save the last choices in some "CLI cookie" file `convert_cookies.json` in the directory where you run the program.
