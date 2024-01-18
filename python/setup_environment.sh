#!/bin/bash

# Create a Python virtual environment
echo "Creating Python virtual environment for $PROJECT_NAME..."
python3 -m venv "python-venv"

# Activate the virtual environment
echo "Activating the virtual environment..."
source "python-venv/bin/activate"

# Install required packages
pip install openai
pip install Pandas
pip install requests
pip install questionary


# Set environment variables from keys.json
echo "Setting up environment variables..."
KEYS_FILE="../private/keys.json"

if [ -f "$KEYS_FILE" ]; then
    while IFS=":" read -r key value
    do
        # Remove quotes and commas from JSON keys and values
        key=$(echo $key | tr -d '" ,' )
        value=$(echo $value | tr -d '" ,' )
        
        # Export the environment variable
        export "$key"="$value"
        echo "Set $key"
    done < <(grep ':' "$KEYS_FILE")
else
    echo "Error: $KEYS_FILE not found."
fi

echo "Environment setup complete."
