#!/bin/bash

# Ensure the .kaggle directory exists
mkdir -p "$HOME/.kaggle"

# Check if the .kaggle directory is present
if [ -d "$HOME/.kaggle" ]; then
    echo ".kaggle exists! Now checking kaggle.json"

    # Check if kaggle.json exists
    if [ -f "$HOME/.kaggle/kaggle.json" ]; then
        echo "✅ kaggle.json exists! Proceeding to extract the token."
    else
        echo "❌ kaggle.json does not exist!"

        # Ask user for the path and copy kaggle.json
        read -p "Enter the path to kaggle.json: " json_path
        if [ -f "$json_path" ]; then
            cp "$json_path" "$HOME/.kaggle/"
            chmod 600 "$HOME/.kaggle/kaggle.json"
            echo "✅ kaggle.json copied successfully!"
        else
            echo "❌ Invalid path! Please try again."
            exit 1
        fi
    fi
else
    echo ".kaggle directory missing. Creating it now..."
    mkdir -p "$HOME/.kaggle"
fi

# checking if jq is present or not.

if command -v jq >/dev/null 2>&1; then
    echo "✅ jq is installed."
else
    echo "❌ jq is NOT installed. Installing now..."
    sudo apt update && sudo apt install jq -y
fi

# Extracting Kaggle API key ...

if [ -f "$HOME/.kaggle/kaggle.json" ]; then
    KAGGLE_KEY=$(jq -r '.key' "$HOME/.kaggle/kaggle.json")
    echo "✅ API Key Extracted: $KAGGLE_KEY"
else
    echo "❌ kaggle.json not found!"
    exit 1
fi

# Check if API key is valid or not

if [ -z "$KAGGLE_KEY" ]; then
    echo "❌ API key is empty or invalid. Please check kaggle.json!"
    exit 1
else
    echo "✅ API key is valid."
fi

# Input Dataset Name

read -p "Enter Kaggle dataset (e.g., 'username/dataset-name'): " DATASET

if [ -z "$DATASET" ]; then
    echo "❌ Dataset cannot be empty!"
    exit 1
fi

# Generating URL dynamically

DOWNLOAD_URL="https://www.kaggle.com/api/v1/datasets/download/$DATASET"
echo "Downloading from: $DOWNLOAD_URL"

# Downloading the dataset

# Extract filename from the download URL
FILENAME=$(basename "$DOWNLOAD_URL").zip

# Download the Kaggle dataset with dynamic filename
wget --header="Authorization: Bearer $KAGGLE_KEY" "$DOWNLOAD_URL" -O "$FILENAME"

if [ $? -eq 0 ]; then
    echo "✅ Download complete!"
else
    echo "❌ Download failed. Check dataset name and API key."
    exit 1
fi

# Extract the dataset if it's a .zip file
if [ -f "$FILENAME" ]; then
    echo "Extracting dataset..."
    unzip -o "$FILENAME" -d ./dataset
    echo "✅ Extraction complete!"
else
    echo "❌ Error: $FILENAME not found!"
    exit 1
fi
