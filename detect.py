from ultralytics import YOLO
import os
import sqlite3
from datetime import datetime
import time
import logging

logfile = "camera.log"
logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#logging info with timestamp
logging.info("Loading model") 
model = YOLO("yolo12n.pt")
conn = sqlite3.connect('data.db')
logging.info("Database connected")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TIMESTAMP,
                     people INTEGER,
                     dogs INTEGER,
                     cats INTEGER,
                     bikes INTEGER)''')
conn.commit()
conn.close()

def take_picture(filename):
    logging.info("Taking picture")
    # Potential command injection here, luckly no user input is used
    if os.system(f"libcamera-still -v 0 -o {filename} --nopreview --immediate --width 2028 --height 1520") != 0:
        print("Error: Failed to capture image")
        logging.error("Error: Failed to capture image")
def delete_picture(filename):
    os.system("rm " + filename) # Potential command injection here, luckly no user input is used
    logging.info("Picture deleted")
def detect_object(filename):
    # Run inference on the source
    logging.info("Detecting object")
    results = model(filename, verbose=False)  # list of Results objects
    person_count = 0
    dog_count = 0
    cat_count = 0
    bike_count = 0
    for result in results:
        names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
        for name in names:
            if name == 'person':
                person_count += 1
            elif name == 'dog':
                dog_count += 1
            elif name == 'cat':
                cat_count += 1
            elif name == 'bicycle':
                bike_count += 1
    # return in json format
    return {
        "people": person_count,
        "dogs": dog_count,
        "cats": cat_count,
        "bikes": bike_count
    }

def save_to_sqlite3(json):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info("Saving to database")
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (timestamp, people, dogs, cats, bikes) VALUES (?, ?, ?, ?, ?)",
                       (timestamp, json['people'], json['dogs'], json['cats'], json['bikes']))
        conn.commit()
    
if __name__ == '__main__':
    try:
        while True:
            # unix timestamp
            u_time = int(time.time())
            filename = "image_" + str(u_time) + ".jpg"
            take_picture(filename)
            json = detect_object(filename)
            save_to_sqlite3(json)
            if all(value == 0 for value in json.values()):
                delete_picture(filename)
            else:
                logging.info("Image retained as it contains objects")
            logging.info("Sleeping for 10 seconds")
            os.system("sleep 10")
    except KeyboardInterrupt:
        print("Stopping...")
        conn.close()