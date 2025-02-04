
# 🚀 **Intern Welcome Automation**

![Intern Welcome Banner](https://via.placeholder.com/1000x300?text=Intern+Welcome+Automation)  

## 📌 **Overview**
This project automates the intern onboarding process by:
✅ Monitoring a **Google Sheet** for new intern records  
✅ Generating **personalized welcome images**  
✅ Sending **customized emails** with embedded images  

## 📂 **Project Structure**
```
📦 Intern-Welcome-Automation/
├── 📜 main.py                 # Core script for monitoring and email automation
├── 📜 custom_credentials.py    # Configuration file (User-defined variables)
├── 📂 intern_welcome_images/   # Stores generated welcome images
├── 🖼️ welcome_template.png      # Default welcome image template
├── 📜 sheet_data.json          # Cached Google Sheet data
├── 📜 requirements.txt         # Dependencies
└── 📜 README.md                # Documentation
```
---

## 🛠 **Setup Guide**
### **1️⃣ Obtain Google Service Account Credentials**
🔹 To access Google Sheets, follow these steps:  
1. Go to [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a new project.  
3. Enable **Google Sheets API**.  
4. Navigate to **IAM & Admin > Service Accounts** and create a new service account.  
5. Assign the **Editor** role.  
6. Generate and **download the JSON key file**.  
7. Save this file in your project folder and set its path in `custom_credentials.py` as:  
   ```python
   SERVICE_ACCOUNT_FILE = "path/to/your/credentials.json"
   ```
8. **Grant access**: Share your Google Sheet with the service account email.

---

### **2️⃣ Obtain Gmail App Password**
🔹 To send emails using Gmail:  
1. Enable **2-Step Verification** for your Google account.  
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).  
3. Generate a password and **copy it**.  
4. Set this password in `custom_credentials.py`:  
   ```python
   SENDER_PASSWORD = "your-app-password"
   ```

---

### **3️⃣ Install Dependencies**
Run the following command:
```sh
pip install -r requirements.txt
```

---

### **4️⃣ Configure `custom_credentials.py`**
Set the following **mandatory variables** before running the script:
- 📂 `OUPUT_DIR` – Directory for storing images  
- 🖼️ `TEMPLATE_PATH` – Path to the welcome image template  
- 🔑 `SERVICE_ACCOUNT_FILE` – Google service account credentials  
- 📊 `SCOPES` – API access scopes for Google Sheets  
- 📋 `SPREADSHEET_ID` – The **Google Sheet ID** containing intern data  
- 📌 `RANGE_NAME` – The range of data to monitor  
- 📧 `SENDER_EMAIL` – Your email address for sending emails  
- 🔑 `SENDER_PASSWORD` – Your **app password** for authentication  
- 📜 `SUBJECT` – Subject of the welcome email  
- ✉️ `EMAIL_BODY` – HTML template for the email content  
- 🔠 `FONT_PATH` – Font file for text rendering  

---

### **5️⃣ Running the Script**
Run the script to **start monitoring the Google Sheet**:
```sh
python main.py
```
🚀 **How it works:**
1. ✅ Fetches intern data from Google Sheets  
2. 🔄 Monitors for new additions every **30 seconds**  
3. 🖼️ Generates a welcome image for new interns  
4. 📩 Sends an email with the generated image  

---

## ⚙️ **How It Works**
| Function | Description |
|----------|------------|
| 📝 `get_sheet_data()` | Fetches data from the Google Sheet and stores it as JSON. |
| 🖼️ `generate_welcome_image()` | Creates a personalized welcome image with intern details. |
| 📧 `send_welcome_email()` | Sends an email with the generated image. |
| 🔍 `monitor_and_send_email()` | Continuously checks for new interns and triggers email sending. |

---

## 🛑 **Troubleshooting**
🔹 **Email Not Sending?**  
- Ensure your **Gmail App Password** is set correctly.  
- Check your SMTP settings and network connection.  

🔹 **Google Sheets Data Not Fetching?**  
- Ensure your **service account email** has access to the Google Sheet.  
- Verify **SPREADSHEET_ID** and **RANGE_NAME** in `custom_credentials.py`.  

🔹 **Image Generation Issues?**  
- Make sure `welcome_template.png` exists.  
- Verify `FONT_PATH` is set correctly.  

---

## 🏆 **Conclusion**
This project **automates intern onboarding** by integrating Google Sheets, Gmail, and Python scripting. It **simplifies** the process by ensuring each intern receives a **personalized welcome email** with an image. 🎉  

🔹 **Customizable**: Modify the email template & welcome image to match your branding.  
🔹 **Scalable**: Works for **any number of interns** without manual intervention.  

---

### ⭐ **Like this project? Give it a star on GitHub!** ⭐  
💬 **Have questions?** Feel free to raise an issue or contribute!  

---