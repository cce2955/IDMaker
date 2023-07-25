import os
import sys
import time
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def extract_student_data(url):
    # Create a new instance of the Firefox web driver.
    driver = webdriver.Firefox()

    try:
        # Navigate to the provided URL.
        driver.get(url)

        # Use explicit wait to wait for the presence of the 'class-students' div.
        wait = WebDriverWait(driver, 300)
        div_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "class-students")))
        print("The 'class-students' div exists on the webpage.")

        # Use explicit wait to wait for the presence of the 'class-teacher' divs.
        teacher_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "class-teacher")))
        print("Teacher Elements:")
        print(teacher_elements)

        # Extract teacher names from the 'class-teacher' divs.
        teacher_names = []
        for elem in teacher_elements:
            try:
                teacher_name_elem = elem.find_element(By.XPATH, ".//div[contains(@class, 'user-name')]")
                teacher_names.append(teacher_name_elem.text)
            except NoSuchElementException:
                print("Could not find 'user-name' div inside 'class-teacher' div.")

        print("Teacher Names:")
        print(teacher_names)

        try:
            # Use explicit wait to wait for the presence of the rows containing student data.
            student_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//spark-grid-row[contains(@class, 'ng-scope ng-isolate-scope')]")))
            print("Student Rows:")
            print(student_rows)

            # Extract data for each student.
            student_data = []
            for row in student_rows:
                try:
                    # Extract student name and school ID number.
                    student_name_elem = row.find_element(By.XPATH, ".//span[contains(@ng-bind-html, '$ctrl.Data.Name')]")
                    school_id_elem = row.find_element(By.XPATH, ".//span[contains(@ng-bind-html, '$ctrl.Data.SchoolIdNumber')]")
                    student_name = student_name_elem.text
                    school_id = school_id_elem.text

                    # Check for the existence of the model.
                    model_elements = row.find_elements(By.XPATH, ".//span[contains(@ng-bind, '$ctrl.SelectedAsset.Model.Name')]")
                    has_hp_chromebook = False
                    for model_elem in model_elements:
                        model_name = model_elem.text
                        if model_name == "HP Chromebook 11 G9 EE":
                            has_hp_chromebook = True

                    # Append the student data to the list.
                    student_data.append({"Teacher": teacher_names[0], "Student Name": student_name, "School ID": school_id, "Has HP Chromebook": has_hp_chromebook})

                except NoSuchElementException as e:
                    print("Invalid URL: The 'class-students' div does not exist on the webpage.")
                except Exception as e:
                    print("Error occurred:")
                    traceback.print_exc()

            print("Student Data:")
            print(student_data)

            # Create a DataFrame to store the student data.
            student_df = pd.DataFrame(student_data)

            # Get the teacher name (use the first teacher name if there are multiple teachers).
            teacher_name = teacher_names[0]

            # Save the student DataFrame to a CSV file named after the teacher.
            csv_path = os.path.join("Data", f"{teacher_name}.csv")
            student_df.to_csv(csv_path, index=False)

        except TimeoutException as e:
            print("TimeoutException: The rows containing student data did not load within the specified timeout.")
        except Exception as e:
            print("Error occurred:")
            traceback.print_exc()

    finally:
        # Close the web browser.
        driver.quit()

import shutil

def clear_cards_folder(output_folder):
    # Delete the entire "Cards" folder if it exists.
    if os.path.exists(output_folder):
        try:
            shutil.rmtree(output_folder)
            print(f"Deleted the '{output_folder}' folder.")
        except Exception as e:
            print(f"Error while deleting the '{output_folder}' folder: {e}")

    # Recreate the "Cards" folder.
    os.makedirs(output_folder)
    print(f"Recreated the '{output_folder}' folder.")


def create_id_cards(csv_path):
    # Load the CSV data into a DataFrame with utf-8 encoding.
    df = pd.read_csv(csv_path, encoding="utf-8")

    # Filter out students who don't have a Chromebook.
    df = df[df["Has HP Chromebook"] == False]

    # Load the logo image.
    logo_path = "logo.jpg"  # Replace with the path to your logo image.
    logo = Image.open(logo_path)

    # Set the card size and margins.
    card_width, card_height = 600, 400
    margin = 10

    # Create an output folder for the ID cards.
    output_folder = "Cards"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        # Clear the "Cards" folder before generating new ID cards.
        clear_cards_folder(output_folder)

    # Read organization details from a text file.
    with open("cardinfo/org_info.txt", "r") as file:
        lines = file.readlines()
        organization = lines[0].strip()
        address = lines[1].strip()
        state = lines[2].strip()
        zip_code = lines[3].strip()
        phone_number = lines[4].strip()
    
    # Create a new image for the sheet.
    sheet_width, sheet_height = 2550, 3300  # Size for a standard letter sheet.
    cards_per_sheet = 10
    card_index = 0
    sheet = Image.new("RGB", (sheet_width, sheet_height), color="white")

    # Loop through the filtered DataFrame and create ID cards for each student.
    for index, row in df.iterrows():
        student_name = row["Student Name"]
        student_id = str(row["School ID"])  # Convert student_id to string
        teacher_name = row["Teacher"]

        # Create a new blank image for the ID card.
        card = Image.new("RGB", (card_width, card_height), color="white")
        draw = ImageDraw.Draw(card)

        # Squish the logo to the left side of the card (60% of the left side).
        logo_width = int(card_width * 1.4)
        logo_height = int(logo_width * logo.size[1] / logo.size[0])
        logo_resized = logo.resize((logo_width, logo_height))
        #card.paste(logo_resized, (margin, margin))

        # Calculate the height of each section
        logo_height = int(card_height * 0.2)
        student_name_height = int(card_height * 0.2)
        barcode_height = int(card_height * 0.45)
        teacher_name_height = int(card_height * 0.2)

        # Resize the logo to the new height
        logo_width = int(logo_height * logo.size[0] / logo.size[1])
        logo_resized = logo.resize((logo_width, logo_height))
        card.paste(logo_resized, (margin, margin))

        # Add student name (slightly bigger font).
        font_student_name = ImageFont.truetype("arial.ttf", 30)  # Increase the font size.
        student_name_position = (int(card_width * 0.1), margin + logo_height + margin)  # Move student name to the right by 10%
        draw.text(student_name_position, student_name, fill="black", font=font_student_name)

        # Add student ID as a scannable barcode (type 128).
        barcode_value = student_id
        barcode_image = Code128(barcode_value, writer=ImageWriter())
        barcode_image_rendered = barcode_image.render(text=barcode_value)
        barcode_image_width, barcode_image_height = barcode_image_rendered.size

        # Resize the barcode image to the new height and increase the width by 20%
        new_width = int(barcode_image_width * (barcode_height / barcode_image_height) * 1.2)
        barcode_image_resized = barcode_image_rendered.resize((new_width, barcode_height))

        # Calculate the position for the barcode (move it to the left by 15% more)
        barcode_position = (int(card_width * 0.15), margin + logo_height + student_name_height + margin)
        card.paste(barcode_image_resized, barcode_position)

        # Add teacher name under the barcode.
        font_teacher_name = ImageFont.truetype("arial.ttf", 30)  # Adjust the font size as needed.
        bbox = font_teacher_name.getbbox(teacher_name)
        teacher_name_width = bbox[2] - bbox[0]
        teacher_name_height = bbox[3] - bbox[1]
        # Get the teacher's last name.
        teacher_name = row["Teacher"].split()[-1]


        # Calculate the position for the teacher name (move it to the left by 15% more)
        teacher_name_position = (int(card_width * 0.15), margin + logo_height + student_name_height + barcode_height + margin)
        draw.text(teacher_name_position, teacher_name, fill="black", font=font_teacher_name)

        # Add return information on the right side of the card.
        return_info_font = ImageFont.truetype("arial.ttf", 20)  # Adjust the font size as needed.
        return_info = f"Belongs to\n {organization},\n return to:\n {address},\n {state},\n {zip_code}.\n {phone_number}"
        draw.text((int(card_width * 0.6), int(card_height * 0.4)), return_info, fill="black", font=return_info_font)

        # Save the ID card as an image file.
        card_filename = f"{student_name}.png"
        card_path = os.path.join(output_folder, card_filename)
        card.save(card_path)

        # Paste the ID card onto the sheet.
        card_position = ((card_index % 2) * card_width, (card_index // 2) * card_height)
        sheet.paste(card, card_position)
        card_index += 1

        # If the sheet is full or if this is the last student, save the sheet.
        if card_index == cards_per_sheet or index == len(df) - 1:
            sheet_filename = f"Sheet_{index // cards_per_sheet + 1}"
            sheet_path_jpg = os.path.join(output_folder, f"{sheet_filename}.jpg")
            sheet_path_png = os.path.join(output_folder, f"{sheet_filename}.png")
            sheet_path_pdf = os.path.join(output_folder, f"{sheet_filename}.pdf")
            sheet.save(sheet_path_jpg)
            sheet.save(sheet_path_png)

            # Convert the sheet image to a PDF.
            c = canvas.Canvas(sheet_path_pdf, pagesize=letter)
            c.drawImage(sheet_path_jpg, 0, 0, *letter)
            c.showPage()
            c.save()

            # Create a new image for the next sheet.
            sheet = Image.new("RGB", (sheet_width, sheet_height), color="white")
            card_index = 0

            # Save the ID card as an image file.
            card_filename = f"{student_name}.png"
            card_path = os.path.join(output_folder, card_filename)
            card.save(card_path)

            # Compile the cards into sheets and output them in different formats.
            compile_cards_to_sheets(output_folder, ["JPEG", "PDF", "PNG"])


def compile_cards_to_sheets(output_folder, formats):
    # Get the list of card images.
    card_images = [f for f in os.listdir(output_folder) if f.endswith(".png")]

    # Set the number of cards per sheet and the size of each card.
    cards_per_sheet = 8
    card_width, card_height = 600, 400

    # Calculate the size of the sheet.
    sheet_width = card_width * 2
    sheet_height = card_height * 4

    # Create output folders for each format.
    for fmt in formats:
        fmt_folder = os.path.join(output_folder, fmt)
        if not os.path.exists(fmt_folder):
            os.makedirs(fmt_folder)

    # Loop through the card images and add them to sheets.
    for i in range(0, len(card_images), cards_per_sheet):
        # Create a new blank sheet.
        sheet = Image.new("RGB", (sheet_width, sheet_height), color="white")

        # Add the cards to the sheet.
        for j in range(cards_per_sheet):
            if i + j < len(card_images):
                # Open the card image.
                card_image = Image.open(os.path.join(output_folder, card_images[i + j]))

                # Calculate the position of the card on the sheet.
                pos_x = (j % 2) * card_width
                pos_y = (j // 2) * card_height

                # Paste the card image onto the sheet.
                sheet.paste(card_image, (pos_x, pos_y))

        # Save the sheet in each format.
        for fmt in formats:
            if fmt == "PDF":
                # Convert the sheet to PDF.
                pdf_path = os.path.join(output_folder, fmt, f"sheet_{i // cards_per_sheet + 1}.pdf")
                pdf = canvas.Canvas(pdf_path, pagesize=letter)
                pdf.drawInlineImage(sheet, 0, 0, width=sheet_width, height=sheet_height)
                pdf.save()
            else:
                # Save the sheet as an image.
                image_path = os.path.join(output_folder, fmt, f"sheet_{i // cards_per_sheet + 1}.{fmt.lower()}")
                sheet.save(image_path, fmt.upper())

def main():
    # Check if a URL argument is provided
    if len(sys.argv) < 2:
        print("Error: URL not provided.")
        sys.exit(1)
    """
    # Get the URL from the command-line argument
    url = sys.argv[1]

    # Call the function to extract teacher and student data and save the student data in a CSV file.
    extract_student_data(url)

    # Combine all CSV files in the "Data" folder into a single "total.csv" file.
    data_folder = "Data"
    total_csv_path = os.path.join(data_folder, "total.csv")
    if os.path.exists(total_csv_path):
        os.remove(total_csv_path)

    for file in os.listdir(data_folder):
        if file.endswith(".csv") and file != "total.csv":
            file_path = os.path.join(data_folder, file)
            df = pd.read_csv(file_path)
            df.to_csv(total_csv_path, mode='a', index=False, header=not os.path.exists(total_csv_path))

    # Provide the CSV path directly to the create_id_cards function.
    create_id_cards(total_csv_path)
    """
    # Provide the CSV path directly to the create_id_cards function.
    # #Comment out the above if you just want to test the card function
    csv_path = "Data/total.csv"
    create_id_cards(csv_path)
if __name__ == "__main__":
    main()