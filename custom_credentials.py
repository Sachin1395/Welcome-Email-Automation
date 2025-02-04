OUPUT_DIR = "intern_welcome_images/"
TEMPLATE_PATH = "welcome_template.png"
FONT_PATH = "SFMono-Light.otf"

# !PERSONAL!
SERVICE_ACCOUNT_FILE= "core-cascade-416415-aa7f0ebff386.json"


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID="1HBfvTrs2gK-hiW5ylc-4O-Wu_CW1GOSPezih_mQO_2Q"

# !COMMON!
RANGE_NAME = "Sheet1!A1:Z100"

# SENDER Email Details 
SENDER_EMAIL = "aniketkundu12072004@gmail.com"
SENDER_PASSWORD = "lrbq zusf waos duny"  # Use app password
SUBJECT = "Welcome to the Team!"
EMAIL_BODY = """
        <html>
            <body>
                <p>Hi {},</p>
                <p>Welcome to the team! We are excited to have you onboard.</p>
                <p>Please find your welcome image below:</p>
                <img src="cid:image1" style="width:600px;">
                <p>Best Regards,<br>SpectoV</p>
            </body>
        </html>
        """
