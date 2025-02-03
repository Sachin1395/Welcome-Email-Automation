# Intern Welcome Automation

This project automates the process of sending personalized welcome emails to interns using Google Sheets, Python, and SMTP.

## Features
- Fetches new intern data from a Google Sheet.
- Generates a personalized welcome image using a template.
- Sends an email with the welcome image attached.
- Runs continuously to monitor new entries in the Google Sheet.

## Prerequisites
- A Google Service Account with access to Google Sheets.
- SMTP email credentials (preferably an app password).
- Python 3.x installed on your system.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sachin1395/Welcome-Email-Automation.git
cd Intern_Welcome_Automation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Google Service Account
- Generate a Google Service Account JSON file with Sheets API access.
- Place the JSON file in the project directory.
- Update the `SERVICE_ACCOUNT_FILE` variable in `main.py` with the file path.

### 4. Configure SMTP Email Settings
- Use an app password for secure authentication.
- Update `SENDER_EMAIL` and `SENDER_PASSWORD` in `main.py`.

### 5. Run the Script
```bash
python main.py
```

## Project Structure
```
📂 Intern_Welcome_Automation
│-- 📂 intern_welcome_images/   # Folder to store generated welcome images
│-- 📜 main.py                   # Python script
│-- 📜 requirements.txt           # Dependencies
│-- 📜 README.md                  # Project documentation
│-- 📜 .gitignore                  # Ignore sensitive files
│-- 📜 service_account.json       # Google service account file (DO NOT UPLOAD THIS)
│-- 📜 welcome_template.png       # Template image for the welcome card
│-- 📜 SFMono-Light.otf           # Font file for text rendering
```

## Author
Developed by QuietkidAniket, arushiranjan, Sachin1395

