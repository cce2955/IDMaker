import os
import sys
import time
import pandas as pd
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_student_data(url):
    # Create a new instance of the Firefox web driver.
    driver = webdriver.Firefox()

    try:
        # Navigate to the provided URL.
        driver.get(url)

        # Use explicit wait to wait for the presence of the 'class-students' div.
        wait = WebDriverWait(driver, 30)
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

def main():
    # Check if a URL argument is provided
    if len(sys.argv) < 2:
        print("Error: URL not provided.")
        sys.exit(1)

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

if __name__ == "__main__":
    main()
