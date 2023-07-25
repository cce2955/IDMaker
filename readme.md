# Student ID Card Generator

This project is a Python script that generates student ID cards from a CSV file. The ID cards include a logo, the student's name, a scannable barcode of the student's ID, and the teacher's name. The cards also include return information on the right side. The cards are compiled onto sheets, with 10 cards per sheet.

## Setup

1. Clone this repository to your local machine.

2. Install the required Python packages using pip:

    ```
    pip install -r requirements.txt
    ```

3. Download the appropriate [WebDriver](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) for your browser and add it to your system's PATH.

4. Replace the `logo.jpg` file in the root directory with the logo you want to use on the ID cards. The logo should be formatted to 600x100 pixels.

5. Add a `org_info.txt` file in the `cardinfo` directory with the following format:

    ```
    Organization Name
    Address
    State
    Zip Code
    Phone Number
    ```

## Usage

1. Run the `main.py` script with the URL of the webpage containing the student data as a command-line argument:

    ```
    python main.py "http://example.com"
    ```

2. The script will extract the student data from the webpage and save it in a CSV file in the `Data` directory.

3. The script will then generate ID cards for each student and save them as PNG images in the `Cards` directory.

4. Finally, the script will compile the cards onto sheets and save the sheets as PDF, JPG, and PNG files in the `PDF`, `JPEG`, and `PNG` directories within the `Cards` directory.

## Note

This script is intended for educational purposes and should not be used for any illegal activities.
