# Importing Libraries
import cv2
import dlib
import time
import math
import numpy as np
import queue
import threading
import json
from comm_task.mqtt_client import MQTTClient
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

banner = r"""
     _                  _   _             _  __               _     _ 
    | |_   _ _ __   ___| |_(_) ___  _ __ | |/ /__ _ _ __  ___| |__ (_)
 _  | | | | | '_ \ / __| __| |/ _ \| '_ \| ' // _` | '_ \/ __| '_ \| |
| |_| | |_| | | | | (__| |_| | (_) | | | | . \ (_| | | | \__ \ | | | |
 \___/ \__,_|_| |_|\___|\__|_|\___/|_| |_|_|\_\__,_|_| |_|___/_| |_|_|
                                                    Traffic Monitoring 
"""
print(banner)
print(f"Systems startup at: {dt_string}")
print("Traffic Monitoring client is running. Press Ctrl+C to stop.")


# Define MQTT broker configuration
broker_address = "broker.hivemq.com"
broker_port = 1883
topic = "taist/aiot/junctionkanshi/camera1/detection"

# Create an instance of the MQTTClient class
mqtt_client = MQTTClient(broker_address, broker_port, topic)

def publish_data(carCount, speeds):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = json.dumps({
        "vehicleCount": carCount,
        "speed": speeds,
        "datetime": dt_string
    })
    try:
        mqtt_client.connect()  # Make sure the client is connected
        mqtt_client.run(topic, data)  # Assuming the MQTTClient has a publish method
        mqtt_client.disconnect()  # Optionally disconnect after sending
    except Exception as e:
        print(f"Failed to publish data: {str(e)}")

# Classifier File
carCascade = cv2.CascadeClassifier("CasCade/vech.xml")

# Constant Declaration
WIDTH = 1280
HEIGHT = 720

# Video capture
video_url = "https://streaming1.highwaytraffic.go.th/Phase3/PER_3_009_IN.stream/chunklist_w1042704716.m3u8"

# Load the logo, possibly resize and position
logo = cv2.imread("static/JunctionKanshiLogoLandscape.png", cv2.IMREAD_UNCHANGED)  # Logo must is PNG with transparency
logo = cv2.resize(logo, (195, 50))  # Resize as needed
position = 'bottom-right' # Location as neededq

# Read the mask image
mask = cv2.imread("static/mask.png")
mask = cv2.resize(mask, (WIDTH, HEIGHT))

# Line position for counting cars
line_start, line_end = (60, 900 // 2), (750, 600 // 2)
line_color, line_thickness = (255, 255, 0), 50

# Buffer for video frames
frame_buffer = queue.Queue(maxsize=29.97)

def fetch_frames(video_capture):
    while True:
        ret, frame = video_capture.read()
    
        if not ret:
            print("Failed to fetch frame.")
            break
        if not frame_buffer.full():
            frame_buffer.put(frame)
        else:
            time.sleep(0.4)  # Wait if the buffer is full

# Initialize video capture with threading
video_capture = cv2.VideoCapture(video_url)
thread = threading.Thread(target=fetch_frames, args=(video_capture,))
thread.daemon = True
thread.start()

def overlay_logo(frame, logo, position, margin=10):
    frame_h, frame_w, _ = frame.shape
    logo_h, logo_w, _ = logo.shape

    if position == 'top-right':
        x, y = frame_w - logo_w - margin, margin
    elif position == 'top-left':
        x, y = margin, margin
    elif position == 'bottom-right':
        x, y = frame_w - logo_w - margin, frame_h - logo_h - margin
    elif position == 'bottom-left':
        x, y = margin, frame_h - logo_h - margin

    # If the logo has transparency (4 channels), we need to blend it accordingly.
    if logo.shape[2] == 4:
        overlay = logo[..., :3]  # RGB channels
        mask = logo[..., 3:]  # Alpha channel
        background = frame[y:y+logo_h, x:x+logo_w]
        foreground = cv2.bitwise_and(overlay, overlay, mask=mask)
        background = cv2.bitwise_and(background, background, mask=cv2.bitwise_not(mask))
        frame[y:y+logo_h, x:x+logo_w] = cv2.add(background, foreground)
    else:
        frame[y:y+logo_h, x:x+logo_w] = logo

    return frame

# Estimate speed function
def estimateSpeed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    ppm = 9.8
    # ppm = 8.8
    d_meters = d_pixels / ppm
    # fps = 24.97
    fps = 29.97
    speed = d_meters * fps * 2.85
    # speed = d_meters * fps * 3.6
    return speed

def isCrossingLine(point, line_start, line_end):
    line_vec = np.array(line_end) - np.array(line_start)
    point_vec = np.array(point) - np.array(line_start)
    dot = np.dot(line_vec, point_vec)
    len_sq = np.dot(line_vec, line_vec)
    is_crossing = (dot > 0) and (dot < len_sq)
    return is_crossing

# Tracking multiple objects
def trackMultipleObjects():
    rectangleColor = (0, 255, 255)
    frameCounter = 0
    currentCarID = 0
    carCountPerMinute = 0
    startTime = time.time()

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = {}

    while True:
        # Initialize resultImage at the start of the loop to avoid UnboundLocalError
        resultImage = None  # This will be replaced with actual frame processing below

        if not frame_buffer.empty():
            start_time = time.time()  # Record the start time before processing the frame

            image = frame_buffer.get()
            if image is None:  # Check if the frame is valid
                continue  # Skip this iteration if the frame is not valid

            image = cv2.resize(image, (WIDTH, HEIGHT))
            processed_img = cv2.bitwise_and(image, mask)
            resultImage = image.copy()
            resultImage = overlay_logo(resultImage, logo, position, margin=10)
            cv2.line(resultImage, line_start, line_end, line_color, line_thickness)
            
            for carID in carTracker.keys():
                trackedPosition = carTracker[carID].get_position()
                center_point = (int(trackedPosition.left() + trackedPosition.width() / 2), 
                                int(trackedPosition.top() + trackedPosition.height() / 2))

                """
                if carID not in carNumbers and isCrossingLine(center_point, line_start, line_end):
                    carNumbers[carID] = True
                    carCountPerMinute += 1
                    # print(f"Car detected total in this minute: {carCountPerMinute}")

        
        # Minute timer for car count
        if time.time() - startTime >= 60:
            print(f"Cars per minute: {carCountPerMinute}")
            carCountPerMinute = 0
            startTime = time.time()
        """

        frameCounter += 1
        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(processed_img)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)

        if not (frameCounter % 10):
            gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))
            # print(f"Detected {len(cars)} cars in this frame.")

            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                matchCarID = None

                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarID = carID

                if matchCarID is None:
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(processed_img, dlib.rectangle(x, y, x + w, y + h))
                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]
                    # print(f"New car tracked: ID {currentCarID} at position {x}, {y}, {w}, {h}")
                    currentCarID += 1

        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()
            center_point = (x + w // 2, y + h // 2)

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())

            center_point = (t_x + t_w // 2, t_y + t_h // 2)
            if carID not in carNumbers and isCrossingLine(center_point, line_start, line_end):
                carNumbers[carID] = True  # Mark this car as counted
                carCountPerMinute += 1
                # print(f"Car detected total in this minute: {carCountPerMinute}")
                # print(f"Car ID {carID} detected crossing. Total this minute: {carCountPerMinute}")

            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

            carLocation2[carID] = [t_x, t_y, t_w, t_h]

            end_time = time.time()
            frame_time = end_time - start_time
            if frame_time > 0:
                fps = 1.0 / frame_time
                # Optionally display FPS on the frame
            else:
                # If the buffer is empty, wait a bit for it to fill
                time.sleep(0.1)

        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]

                carLocation1[i] = [x2, y2, w2, h2]

                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (i not in speed or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])
                        # print(f"Car detected with speed: {int(speed[i])} km/h")
                    if i in speed and y1 >= 180:
                        cv2.putText(resultImage, f"{int(speed[i])} km/h", (int(x1 + w1 / 2), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 2)
        if resultImage is not None:
            cv2.putText(resultImage, "Press 'Q' in ENG key to stop system.", (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.90, (0, 0, 0), 10,)
            cv2.putText(resultImage, "Press 'Q' in ENG key to stop system.", (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.90, (255, 255, 255), 2,)
            cv2.imshow('JunctionKanshi: Traffic Monitoring', resultImage)
        # out.write(resultImage)

        # Minute timer for car count
        current_time = time.time()
        if current_time - startTime >= 60:
            threading.Thread(target=publish_data, args=(carCountPerMinute, speed)).start()
            print(f"Cars per minute: {carCountPerMinute}")
            carCountPerMinute = 0
            startTime = current_time


        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    video_capture.release()
    # out.release()

if __name__ == '__main__':
    trackMultipleObjects()