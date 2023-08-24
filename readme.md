# Student ID Card Generator

This script automates the process of generating student ID cards from provided data. Users can either supply a URL containing the relevant student data or input the data manually.

## Features

- Automated Data extraction from a given URL.
- Manual data input option for student details.
- Generation of individual student ID cards.
- Ability to generate individual cards from existing sheets
- Compilation of individual cards into sheets for easy printing.
- Some custom filtering options
- Output in both PNG and PDF formats.

## Usage

1. **URL Input**: When prompted, choose the URL input option and provide a URL containing the student data.
2. **Manual Input**: Choose the manual input option and follow the prompts. You'll be asked for the Teacher's name, Student's name, and School ID. The script will then generate an ID card with the provided details.

## Output

- The generated ID cards can be found in the `Cards` folder. They will also be compiled into sheets, available in both PNG and PDF formats.
- As well the gathered .csv files will be in the 'Data' folder

## Notes

- When extracting data from a URL, the script assumes a specific structure and element layout in the web page. If the structure changes, the script may need adjustments.
- The provided logo (Which should be 600x100), fonts `arial.tff`, and other assets should be in the same directory as the script or correctly referenced within the script.
- Make sure the "Data" directory exists in the same location as the script to store the extracted data and generated cards.
- In the root add a `login.txt`, the first line will be your `username`, second will be your `password`
- Also in the root there should be a folder called `cardinfo`, inside that will be `org_info.txt`,  first line will be the orginization name, second is street address, third is city and state, fourth is zip, fifth is phone number

## Requirements

- Python 3.x
- Required Python libraries listed in `requirements.txt`.

## Setup & Run

1. Install the required Python libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
2. Run the script.
    ```bash
    python download_libraries.py
    ```

## Contributions

Feel free to contribute to this project by opening issues or submitting pull requests for improvements and bug fixes.
