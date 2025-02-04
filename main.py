from custom_credentials import OUPUT_DIR, TEMPLATE_PATH, SERVICE_ACCOUNT_FILE, SCOPES, SPREADSHEET_ID, RANGE_NAME
from custom_credentials import SENDER_EMAIL, SENDER_PASSWORD, SUBJECT, EMAIL_BODY, FONT_PATH

import os
import json
import time
import textwrap
import mimetypes
import base64

from PIL import Image ,ImageDraw ,ImageFont
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build  # Required for Google Sheets API



""" ~~~~ GETs the Sheet data into our program ~~~~ """


def get_sheet_data():
    # Authenticate using the service account file
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE ,scopes=SCOPES)

    # Build the Sheets API service
    service = build('sheets', 'v4' ,credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID ,range=RANGE_NAME).execute()
    values = result.get('values' ,[])

    # Convert data to JSON
    if not values:
        print("No data found.")
        return None

    # Assuming the first row contains headers
    headers = values[0]
    rows = values[1:]
    data = [dict(zip(headers ,row)) for row in rows]

    # Save the JSON to a file or return it
    with open('sheet_data.json','w') as f:
        json.dump(data,f ,indent=4)

    return data


""" ~~~~~~~ Generates the welcome image with intern details using the welcome template ~~~~~~~~~~ """


def generate_welcome_image(record, template_path, output_dir ,font_path ,font_size=40):
    """
    Generates a personalized welcome image for a given intern record.

    Args:
        record (dict): A dictionary with keys like Name, Email Address, Joining Date, Mentor Name, etc.
        template_path (str): Path to the template image.
        output_dir (str): Directory where the generated image will be saved.
        font_path (str): Path to the font file.
        font_size (int): Font size for the text.
    """

    os.makedirs(output_dir ,exist_ok=True)

    # Load template
    template = Image.open(template_path)
    img = template.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path ,font_size)

    # Construct the welcome message
    name = record["Name"]
    # email = record["Email Address"]
    joining_date = record["Joining Date"]
    mentor_name = record["Mentor Name"]
    department = record.get("Department" ,"N/A")
    duration = record.get("Internship Duration (Months)" ,"N/A")

    # Add text to the image
    welcome_text = f"Welcome, {name}!\n"
    details = f"\n\nJoining Date: {joining_date}\n\n\nMentor: {mentor_name}\n\n\nDepartment: {department}\n\n\nDuration: {duration} months"

    # Center the welcome message
    img_width ,img_height = img.size
    welcome_width ,welcome_height = draw.textbbox((0 ,0) ,welcome_text ,font=font)[2:]
    details_width ,_ = draw.textbbox((0 ,0) ,details ,font=font)[2:]

    x_welcome = (img_width - welcome_width) // 2
    y_welcome = img_height // 2 - 100
    x_details = (img_width - details_width) // 2
    y_details = y_welcome + 60

    # Draw text
    draw.text((x_welcome ,y_welcome) ,welcome_text ,font=font ,fill="black")
    draw.text((x_details ,y_details) ,details ,font=font ,fill="black")

    # Save the image
    output_path = os.path.join(output_dir ,f"welcome_{name.replace(' ' ,'_').lower()}.png")
    img.save(output_path)
    return output_path


""" ~~~~~~~~~~ Sends the welcome email to the respective intern  ~~~~~~~~~~~~~ """


# Scopes for Gmail API


def send_welcome_email(sender_email, sender_password, intern_email, subject, intern_name, attachment_path):
    """
    Sends an email with an inline welcome image to the intern.
    """
    try:
        # Set up the email
        msg = MIMEMultipart("related")
        msg['From'] = sender_email
        msg['To'] = intern_email
        msg['Subject'] = subject

        # Email body with inline image reference using CID
        body = EMAIL_BODY.format(intern_name)

        msg.attach(MIMEText(body, "html"))

        # Attach image as a separate MIME part
        with open(attachment_path, "rb") as img_file:
            mime_type, _ = mimetypes.guess_type(attachment_path)
            mime_type = mime_type or "image/png"  # Default to PNG if unknown

            image_part = MIMEBase("image", mime_type.split("/")[1])
            image_part.set_payload(img_file.read())

        encoders.encode_base64(image_part)
        image_part.add_header("Content-Disposition", "inline", filename="welcome_image.png")
        image_part.add_header("Content-ID", "<image1>")
        image_part.add_header("X-Attachment-Id", "image1")

        msg.attach(image_part)

        # Connect to the mail server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Login
            server.sendmail(sender_email, intern_email, msg.as_string())  # Send email

        print(f"Email sent successfully to {intern_email}!")

    except Exception as e:
        print(f"Failed to send email to {intern_email}. Error: {e}")


"""~~~~~~~~~~~~~~~ MONITOR RECORDS ~~~~~~~~~~~~~~~"""
def monitor_and_send_email(previous_data):
    """ Monitor for new rows in the Google Sheet and send email when a new intern is added """
    new_data = get_sheet_data()
    # Check if there is a new row (compare last row of previous data with new data)
    if new_data and len(new_data) > len(previous_data):  # New row has been added
        # Get the new intern (last row is assumed to be new)
        new_intern = new_data[-1]
        required_fields = ["Name" ,"Email Address" ,"Joining Date" ,"Mentor Name", "Department", "Internship Duration (Months)"]

        # Check if all required fields are filled
        if all(field in new_intern and new_intern[field] for field in required_fields):
            template_path = TEMPLATE_PATH
            output_dir = OUPUT_DIR
            font_path = FONT_PATH
            attachment_path = generate_welcome_image(new_intern ,template_path ,output_dir ,font_path)

            # Send welcome email
            send_welcome_email(SENDER_EMAIL ,SENDER_PASSWORD ,new_intern["Email Address"] ,SUBJECT ,new_intern["Name"] ,
                               attachment_path)
            return new_data  # Update the previous_data
        else:
            # Not all required fields are filled, skip processing
            print("New intern row detected, but not all details are filled.")
            return previous_data  # No email sent as details are missing

    print("No new row added")
    previous_data = new_data
    return previous_data  # No new rows found

def run():
    """ Main function to start the monitoring process """
    previous_data = get_sheet_data()

    # Continuously monitor for new rows
    while True:
        previous_data = monitor_and_send_email(previous_data)
        time.sleep(30)  # Check 1/2 minute for new rows



if __name__ == "__main__":
    run()