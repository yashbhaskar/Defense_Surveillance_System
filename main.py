import cv2
from ultralytics import YOLO
from datetime import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import time
from twilio.rest import Client
import playsound

# Load the trained YOLOv8 model
model = YOLO("D:\\Software Projects\\Weapons Detection\\runs\\detect\\train2\\weights\\best.pt")

# Initialize webcam (0 for default webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Define the object detection classes
classes = ["Automatic Rifle", "Bazooka", "Commander Yash Bhaskar", "Grenade", "Grenade Launcher",
           "Handgun", "Intruder", "SMG", "Shotgun", "Sniper", "Sword"]

# Google API Setup - Load credentials from your credentials.json file
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = "D:\\Software Projects\\Motion_Alert_Indication\\Project\\yolo-person-detection-d51656861a1a.json"

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Drive API setup
drive_service = build('drive', 'v3', credentials=creds)

# Google Sheets API setup
sheets_service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = ''  # Replace with your Google Sheet ID
SHEET_NAME = ''  # The sheet name where you log the data

# Function to upload image to Google Drive and return public link
def upload_image_to_drive(image_path):
    file_metadata = {
        'name': os.path.basename(image_path),
        'parents': ['']  # Replace with Drive folder ID Ensure folder ID has permissions
    }
    media = MediaFileUpload(image_path, mimetype='image/jpeg')

    try:
        file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        file_id = file.get('id')

        # Make the file publicly accessible
        drive_service.permissions().create(
            fileId=file_id, body={'role': 'reader', 'type': 'anyone'}
        ).execute()

        return f"https://drive.google.com/uc?id={file_id}"
    except Exception as e:
        print(f"Error uploading image to Drive: {e}")
        return None

live_location_link = "https://maps."    # Replace this with your real-time location link

# Function to log data in Google Sheets
def log_to_google_sheets(detected_name, date, time_only, image_url, live_location_link):
    try:
        # Create the Google Sheets-compatible image formula
        image_formula = f'=IMAGE("{image_url}",1)'
        
        # Values to log (ensure date and time are passed as strings)
        values = [[detected_name, date, time_only, image_formula, live_location_link]]  # Add live_location_link as 5th column
        
        # Append values to Google Sheets
        response = sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",  # Columns: Detected Name, Date, Time, Detected Face, Live Location
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()

        print(f"Logged {detected_name} detection to Google Sheets successfully.")
        
        # Trigger an alert if the Intruder is detected
        if detected_name == "Intruder":
            alert_intruder()

    except Exception as e:
        print(f"Error logging to Google Sheets: {e}")

# Function to send alert when Intruder is detected
def alert_intruder():
    try:
        # Twilio credentials
        account_sid = ''
        auth_token = ''
        client = Client(account_sid, auth_token)

        # Send WhatsApp message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Human Intruder Detected Near LOC !!. Indian Army, Report',
            to='whatsapp:+91 '
        )
        print(f"WhatsApp message sent: {message.sid}")

        # Play alert audio
        playsound.playsound("D:\\Software Projects\\Weapons Detection\\Alert_Audio.wav")
        print("Alert audio played.")
    except Exception as e:
        print(f"Error during alert: {e}")

# Keep track of the last detection time for objects
last_detected_time = {}
re_detection_interval = 30  # Time interval for re-detection (in seconds)

# Track if specific objects are detected and logged
logged_objects = {"Commander Yash Bhaskar": False, "Intruder": False}

# Object detection loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break

    # Perform detection
    results = model(frame)

    # Annotate the frame with bounding boxes and labels
    annotated_frame = results[0].plot()  # This automatically draws the bounding boxes and labels

    # Process detected objects
    for result in results[0].boxes:
        class_id = int(result.cls)
        confidence = result.conf

        if confidence > 0.5 and class_id < len(classes):  # Ensure valid detection
            detected_object = classes[class_id]

            # Check if this object was detected recently
            current_time = time.time()  # Current time in seconds since epoch
            if detected_object in last_detected_time:
                time_since_last_detection = current_time - last_detected_time[detected_object]
                if time_since_last_detection < re_detection_interval:
                    # If the object was detected within the re-detection interval, skip logging
                    continue

            # Check if the object is either "Commander Yash Bhaskar" or "Intruder"
            if detected_object in ["Commander Yash Bhaskar", "Intruder"]:
                timestamp = datetime.now()
                date = timestamp.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
                time_only = timestamp.strftime("%H:%M:%S")  # Format as HH:MM:SS

                # Save detected frame with bounding boxes and labels
                image_path = f"D:\\Software Projects\\Weapons Detection\\Detected Images\\{detected_object}_{date}_{time_only.replace(':', '-')}.jpg"
                cv2.imwrite(image_path, annotated_frame)

                # Upload image to Google Drive and get the URL
                image_url = upload_image_to_drive(image_path)

                # Log detection to Google Sheets
                log_to_google_sheets(detected_object, date, time_only, image_url, live_location_link)
                print(f"{detected_object} detected and logged.")

                # Update the last detection time
                last_detected_time[detected_object] = current_time

                # Mark that the object has been logged
                logged_objects[detected_object] = True

            # If the object was not detected previously and is now gone, reset its status
            if detected_object in logged_objects and not logged_objects[detected_object]:
                logged_objects[detected_object] = False

    # Display the annotated frame
    cv2.imshow("Weapon Detection - Real-Time", annotated_frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
