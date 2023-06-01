# ID Card Generator

The ID Card Generator is a Python script that generates ID cards with user names, ID numbers, barcodes, and organization information. It uses the `barcode` library to generate barcodes and the `Pillow` library to manipulate images and create ID card designs. The generated ID cards are saved as PNG images and can be combined into a PDF document for printing.

## Features

- Generates custom ID cards with user names, ID numbers, barcodes, and organization information.
- Supports customizing the ID card design, including logo placement, font selection, and organization information.
- Generates individual ID card images as well as organized sheets of multiple cards.
- Supports exporting the ID cards as a PDF document for easy printing.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/your-username/id-card-generator.git 
   ```
   
   
2. Install the required dependencies using pip:
   
   ```shell
   pip install -r requirements.txt    
    ```
  
## Usage
1. Place your organization's logo in the project folder and name it logo.jpg. This program assumes your logo has a resolution of 600 x 113

2. Run the script:

    ```shell
    python main.py
    ```
3. Follow the on-screen instructions to enter user names and ID numbers. Enter END to finish.

4. The generated ID cards will be saved in the cards folder as individual PNG images.

5. The ID cards will also be organized into sheets and saved as PNG images in the cards folder.

6. A PDF document containing all the ID cards can be found in the pdf folder.

Configuration
* You can customize the ID card design by modifying the constants in the generate_card function in main.py. Adjust the dimensions, padding, font sizes, and organization information to suit your needs.
* Use different fonts by placing the font file (.ttf) in the project folder and updating the font_path constant.
* Modify the paper dimensions, margins, and spacing in the main script to match your desired printing format.
## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgements
The barcode generation is powered by the barcode library.
The image manipulation is done using the Pillow library.
The PDF generation is handled by the FPDF library.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
