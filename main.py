import os
import json
import time
import textwrap

from PIL import Image ,ImageDraw ,ImageFont
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build  # Required for Google Sheets API




SERVICE_ACCOUNT_FILE="add your service account file"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID="1HBfvTrs2gK-hiW5ylc-4O-Wu_CW1GOSPezih_mQO_2Q"
RANGE_NAME = "Sheet1!A1:Z100"

# Email Details (Sender)
SENDER_EMAIL = "your email"
SENDER_PASSWORD = "your app password"  # Use app password
SUBJECT = "Welcome to the Team!"


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

def send_welcome_email(sender_email ,sender_password ,intern_email ,subject ,intern_name ,attachment_path):
    """
    Sends an email with an attached image to the intern.

    Args:
        sender_email (str): The sender's email address.
        sender_password (str): The sender's email password or app-specific password.
        intern_email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body of the email.
        attachment_path (str): Path to the attachment (welcome image).
    """
    try:

        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = intern_email
        msg['Subject'] = subject

        # Add body to the email
        body = textwrap.dedent(f"""\
                Hi {intern_name},

                Welcome to the team! We are excited to have you onboard. 
                Please find your welcome image attached.

                Best Regards,  
                SpectoV
                """)
        msg.attach(MIMEText(body ,'plain'))

        # Attach the welcome image
        with open(attachment_path ,'rb') as attachment:
            part = MIMEBase('application' ,'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition' ,
            f'attachment; filename={os.path.basename(attachment_path)}'
        )
        msg.attach(part)

        # Connect to the mail server
        with smtplib.SMTP('smtp.gmail.com' ,587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email ,sender_password)  # Login
            server.sendmail(sender_email ,intern_email ,msg.as_string())  # Send email

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
            template_path = "welcome_template (1).png"
            output_dir = "intern_welcome_images/"
            font_path = "SFMono-Light.otf"
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
        time.sleep(60)  # Check every minute for new rows



if _name_ == "_main_":
    run()
