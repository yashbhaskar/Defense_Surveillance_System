# Defense_Surveillance_System
An AI-powered military surveillance system using YOLOv8 for real-time weapon and intruder detection. Features include instant alerts, Google Cloud logging, and face recognition for authorized personnel. Designed for 24/7 monitoring in high-security zones, enhancing threat detection and response.

---

## Key Features

1. **Real-Time Weapon Detection**:
   - Detects weapons such as:
     - Automatic Rifle
     - Bazooka
     - Grenade
     - Grenade Launcher
     - Handgun
     - SMG
     - Shotgun
     - Sniper
     - Sword

2. **Intruder and Commander Recognition**:
   - Detects and differentiates intruders from authorized personnel, such as commanders, for specific monitoring and logging.

3. **Instant Alerts**:
   - Sends notifications via WhatsApp using Twilio API.
   - Plays audio warnings for immediate response.
   - Logs events to Google Sheets for real-time tracking.

4. **Cloud Integration**:
   - Captures detection images with timestamps and live location links.
   - Uploads data to Google Drive for secure storage.

5. **Redetection Handling**:
   - Avoids redundant logs for recurring detections.

6. **24/7 Surveillance**:
   - Utilizes a webcam for continuous monitoring.

---

## Technologies Used

- **Python** for system development.
- **YOLOv8 (Ultralytics)** for object detection.
- **Google Drive API** for file storage.
- **Google Sheets API** for event logging.
- **Twilio API** for WhatsApp notifications.
- **OpenCV** for video processing.

---

## YOLOv8 model architecture

![Detailed-illustration-of-YOLOv8-model-architecture-The-Backbone-Neck-and-Head-are-the](https://github.com/user-attachments/assets/4e32ef46-b855-47f6-8633-029b8ca9d29e)


---

## Included Visualizations

### 1. Confusion Matrix
![confusion_matrix](https://github.com/user-attachments/assets/f2f92190-7a5d-4869-a636-5bc0f1223027)
The confusion matrix evaluates the detection performance across all trained classes. It highlights:
   - The detection accuracy for each class (e.g., "Automatic Rifle", "Intruder").
   - Misclassifications, if any, for further tuning.

### 2. F1-Confidence Curve
![F1_curve](https://github.com/user-attachments/assets/93cad5e6-2ab3-493d-a6f2-586f3e27d5dc)
This plot shows the relationship between confidence thresholds and F1 scores for all classes. It helps in understanding:
   - The optimal confidence threshold for reliable predictions.
   - The variability in precision and recall for different classes.

### 3. Real-Time Commander Detection
![Screenshot 2024-12-04 220342](https://github.com/user-attachments/assets/acd09eb2-591b-4c3b-b79c-1386b5286ac2)
This image showcases the system's real-time detection interface. It identifies a commander with a bounding box, displays the class name and confidence score, and highlights the efficiency of the YOLOv8 model.

### 4. Weapon Detection Interface
![Screenshot 2024-12-04 220243](https://github.com/user-attachments/assets/fd38b615-4315-4e43-ab12-20b90929561c)
 - Real-time video feed interface that detects multiple weapons simultaneously.
   - Features:
     - Bounding boxes around detected objects.
     - Labeled weapon types with confidence scores.
   - Example: Detection of "Sniper" and "Automatic Rifle" with high accuracy.

### 5. Intruder Detection Interface
![Screenshot 2024-12-04 215110](https://github.com/user-attachments/assets/0353aab0-76e6-4b85-a580-711534fb1f8c)
   - Real-time video feed highlighting the detection of an intruder.
   - Features:
     - Bounding box around the intruder.
     - Labeled tag "Intruder" with the corresponding confidence score.
     - Immediate response actions:
       - Audio alert playback.
       - WhatsApp notifications sent to designated recipients.

### 6. Google Sheets Logging
![Screenshot 2024-12-06 125646](https://github.com/user-attachments/assets/13009676-4138-4cd8-b551-9000123ae9db)
   - The Google Sheet logs every detection event with the following details:
     - **Detected Name**: Specifies the detected object, e.g., "Commander" , "Intruder".
     - **Date and Time**: Timestamp of the detection event.
     - **Captured Image**: A snapshot of the detected object or person.
     - **Live Location Link**: A clickable link to track the detection site in real time.



---

## How It Works

1. **Detection**:
   - The system processes real-time video feed using OpenCV.
   - YOLOv8 detects objects (weapons, intruders, commanders) and generates bounding boxes with confidence scores.

2. **Alert System**:
   - If a threat (weapon or intruder) is detected:
     - An audio warning is played.
     - A WhatsApp alert with an image and location is sent to predefined contacts.
![Screenshot 2024-12-06 151613](https://github.com/user-attachments/assets/327070fb-d3f4-475b-b179-e09185348780)

3. **Logging**:
   - Events are logged into Google Sheets with:
     - Timestamp
     - Detection class
     - Confidence score
     - Image link

4. **Continuous Monitoring**:
   - Prevents redundant logs for the same event and ensures updated tracking.

---

## Setup and Deployment

1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/yashbhaskar/Defense_Surveillance_System.git
   cd Defense_Surveillance_System
   pip install -r requirements.txt
