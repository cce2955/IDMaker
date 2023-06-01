import os
import shutil
import textwrap
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        """
        Overrides the header method of the FPDF class.
        This method is called before the first page is created.
        """
        pass

    def footer(self):
        """
        Overrides the footer method of the FPDF class.
        This method is called after the last page is created.
        """
        pass

def generate_card(user_name, id_number):
    """
    Generates a card image with the given user name and ID number.

    Args:
        user_name (str): The name of the user.
        id_number (str): The ID number associated with the user.

    Returns:
        Image: The generated card image.
    """
    # Card dimensions in pixels
    card_width = int(8 * 300)  
    card_height = int(4 * 300)
    column_width = card_width // 2

    # Padding sizes
    padding = int(card_width * 0.05)

    # Increase card height to accommodate additional content
    card_height += int(card_height * 0.1)

    # Create a blank white card
    card = Image.new('RGB', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    # Load and resize the logo image to fit in the left column
    logo = Image.open('./logo.jpg')
    logo_aspect = logo.size[1] / logo.size[0]
    logo_width = column_width - 2 * padding
    logo_height = int(logo_aspect * logo_width)
    logo = logo.resize((logo_width, logo_height))
    logo_x = padding
    logo_y = padding
    card.paste(logo, (logo_x, logo_y))

    # Set the font for the username
    font_path = './EBGaramond-Regular.ttf'
    font_size = 200
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the maximum width and height of the username
    max_username_width = logo_width
    max_username_height = logo_height - (padding * 2)  

    # Wrap the username to fit within the available width
    username_lines = textwrap.wrap(user_name, width=int(max_username_width / font.getbbox(' ')[2]))

    # Calculate the height of the wrapped username
    username_height = len(username_lines) * font.getbbox(' ')[3]

    # Calculate the starting position to center the username vertically within the logo column
    username_x = logo_x + (logo_width - max_username_width) // 2
    username_y = logo_y + (logo_height - username_height) // 2 + int(logo_height * 0.7)

    # Draw the wrapped username on the card
    for line in username_lines:
        line_width, line_height = draw.textsize(line, font=font)
        line_x = username_x + (max_username_width - line_width) // 2
        draw.text((line_x, username_y), line, font=font, fill='black')
        username_y += line_height

    # Calculate the position for the barcode below the logo and username
    barcode_width = logo_width - 2 * padding
    barcode_aspect = 1  # Adjust as needed
    barcode_height = int(barcode_width * barcode_aspect)
    barcode_x = logo_x + padding
    barcode_y = username_y + padding

    # Generate the barcode image and draw it on the card
    barcode_id = barcode.get('code128', str(id_number), writer=ImageWriter())
    barcode_image = barcode_id.render()
    barcode_image = barcode_image.resize((barcode_width, barcode_height))
    card.paste(barcode_image, (barcode_x, barcode_y))

    # Draw the organization name and return info in the right column
    right_column_x = column_width
    right_column_y = padding * 3
    organization_name = "Your Organization"
    organization_font_size = 80
    organization_font = ImageFont.truetype(font_path, organization_font_size)
    draw.text((right_column_x, right_column_y), organization_name, font=organization_font, fill='black')

    return_info = "Return ID to:\nYour Organization\nAddress\nCity, State, ZIP"
    return_info_font_size = 80
    return_info_font = ImageFont.truetype(font_path, return_info_font_size)
    return_info_y = right_column_y + organization_font.getsize(organization_name)[1] + padding
    draw.multiline_text((right_column_x, return_info_y), return_info, font=return_info_font, fill='black')

    return card


if __name__ == "__main__":
    # Delete the 'cards' and 'pdf' folders if they exist and create them again
    if os.path.exists('cards'):
        shutil.rmtree('cards')
    os.makedirs('cards')

    if os.path.exists('pdf'):
        shutil.rmtree('pdf')
    os.makedirs('pdf')

    # Input user names and id numbers
    user_names = []
    id_numbers = []
    print("Enter user names and id numbers. Enter 'END' when you're done.")
    counter = 1
    while True:
        user_name = input("Enter user name [{}]: ".format(counter))
        if user_name == 'END':
            break
        id_number = input("Enter id number [{}]: ".format(counter))
        if id_number == 'END':
            break
        user_names.append(user_name)
        id_numbers.append(id_number)
        counter += 1

    # Generate cards for each user
    cards = []
    for user_name, id_number in zip(user_names, id_numbers):
        card = generate_card(user_name, id_number)
        if card:
            cards.append(card)
            card.save('cards/temp_card_{}.png'.format(counter))

    # Paper dimensions in pixels (Letter size: 8.5x11 inches at 300 DPI)
    paper_width = int(8.5 * 300)
    paper_height = int(11 * 300)

    # Margins and spacing between cards
    left_margin = int(paper_width * 0.07)
    top_margin = int(paper_height * 0.07)
    horizontal_spacing = int(paper_width * 0.02)
    vertical_spacing = int(paper_height * 0.02)

    # Calculate the number of rows and columns
    rows = 6
    columns = 2

    # Calculate the width and height of each card
    card_width = int((paper_width - left_margin * 2 - horizontal_spacing * (columns - 1)) / columns)
    card_height = int((paper_height - top_margin * 2 - vertical_spacing * (rows - 1)) / rows)

    sheet_number = 0
    for i in range(0, len(cards), rows * columns):
        # Create a blank white paper sheet
        paper = Image.new('RGB', (paper_width, paper_height), 'white')
        for j in range(i, min(i + rows * columns, len(cards))):
            card = cards[j]
            row = (j - i) // columns
            col = (j - i) % columns
            x = left_margin + col * (card_width + horizontal_spacing)
            y = top_margin + row * (card_height + vertical_spacing)
            resized_card = card.resize((card_width, card_height))
            paper.paste(resized_card, (x, y))

        # Save the paper sheet with cards to a PNG file in the 'cards' folder
        paper.save('cards/cards_sheet_{}.png'.format(sheet_number))
        sheet_number += 1

    # Generate PDF from the individual card images
    pdf = PDF()
    for i in range(sheet_number):
        pdf.add_page()
        pdf.image('cards/cards_sheet_{}.png'.format(i), 0, 0, pdf.w, pdf.h)
    pdf.output('pdf/cards.pdf', 'F')
