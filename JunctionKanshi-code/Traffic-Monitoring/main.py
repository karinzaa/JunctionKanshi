# Importing Libraries
import cv2
import dlib
import time
import math
import numpy as np

# Classifier File
carCascade = cv2.CascadeClassifier("CasCade/vech.xml")

# Video file capture
video = cv2.VideoCapture("https://streaming1.highwaytraffic.go.th/Phase3/PER_3_009_IN.stream/chunklist_w1042704716.m3u8") #This is public link you can put this link in VLC to watch this steam.

# Constant Declaration
WIDTH = 1280
HEIGHT = 720

# Load the logo, possibly resize and position
logo = cv2.imread("static/JunctionKanshiLogo.png", cv2.IMREAD_UNCHANGED)  # Logo must is PNG with transparency
logo = cv2.resize(logo, (50, 75))  # Resize as needed
position = 'bottom-right' #Location as needed

# Read the mask image
mask = cv2.imread("static/mask.png")
mask = cv2.resize(mask, (WIDTH, HEIGHT))

# Line position for counting cars
line_start, line_end = (70,900  // 2), (800,600  // 2)
line_color, line_thickness = (255, 255, 0), 30

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
    ppm = 8.8
    d_meters = d_pixels / ppm
    fps = 29.97
    speed = d_meters * fps * 3.6
    return speed

def isCrossingLine(point, line_start, line_end):
    line_vec = np.array(line_end) - np.array(line_start)
    point_vec = np.array(point) - np.array(line_start)
    dot = np.dot(line_vec, point_vec)
    len_sq = line_vec[0] ** 2 + line_vec[1] ** 2
    return dot > 0 and dot < len_sq

# Tracking multiple objects
def trackMultipleObjects():
    rectangleColor = (0, 255, 255)
    frameCounter = 0
    currentCarID = 0
    fps = 0

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 1000

    # out = cv2.VideoWriter('outTraffic.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (WIDTH, HEIGHT))

    while True:
        start_time = time.time()
        rc, image = video.read()
        if type(image) == type(None):
            break

        image = cv2.resize(image, (WIDTH, HEIGHT))
        # Apply the mask to the resized frame
        processed_img = cv2.bitwise_and(image, mask)
        resultImage = image.copy()
        # Overlay the logo on the resultImage
        resultImage = overlay_logo(resultImage, logo, position, margin=10)

        cv2.line(resultImage, line_start, line_end, line_color, line_thickness)


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

                    currentCarID += 1

        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()
            center_point = (x + w // 2, y + h // 2)

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())

            if carID not in carNumbers and isCrossingLine(center_point, line_start, line_end):
                carNumbers[carID] = True  # Mark this car as counted
                print(f"Car detected")  # Print the updated car count in the command line

            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

            carLocation2[carID] = [t_x, t_y, t_w, t_h]

        end_time = time.time()

        if not (end_time == start_time):
            fps = 1.0 / (end_time - start_time)

        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]

                carLocation1[i] = [x2, y2, w2, h2]

                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (speed[i] is None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x1, y2, w2, h2])
                        print(f"Car detected")
                    if speed[i] is not None and y1 >= 180:
                        cv2.putText(resultImage, str(int(speed[i])) + " km/h", (int(x1 + w1 / 2), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 2)
                        print(int(speed[i]), end=' ')
        cv2.imshow('JunctionKanshi Traffic Monitoring', resultImage)
        # out.write(resultImage)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    video.release()
    # out.release()

if __name__ == '__main__':
    trackMultipleObjects()