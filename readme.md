
# Student ID Card Generator

This script automates the process of generating student ID cards from provided data. Users can either supply a URL containing the relevant student data or input the data manually.

## Features

- Data extraction from a given URL.
- Manual data input option for student details.
- Generation of individual student ID cards.
- Compilation of individual cards into sheets for easy printing.
- Output in both PNG and PDF formats.

## Usage

1. **URL Input**: When prompted, choose the URL input option and provide a URL containing the student data.
2. **Manual Input**: Choose the manual input option and follow the prompts. You'll be asked for the Teacher's name, Student's name, and School ID. The script will then generate an ID card with the provided details.

## Output

The generated ID cards can be found in the `Cards` folder. They will also be compiled into sheets, available in both PNG and PDF formats.

## Requirements

- Python 3.x
- Required Python libraries: `pandas`, `PIL`

## Setup & Run

1. Install the required Python libraries.
    ```bash
    pip install pandas Pillow
    ```
2. Run the script.
    ```bash
    python download_libraries.py
    ```

## Contributions

Feel free to contribute to this project by opening issues or submitting pull requests for improvements and bug fixes.

