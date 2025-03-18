from ultralytics import YOLO
import json
from collections import Counter
import os
from tqdm import tqdm
import sqlite3

def count_name_values(data_str):
    data = json.loads(data_str)
    name_counts = Counter(item["name"] for item in data)
    return name_counts

# Create or connect to SQLite database
conn = sqlite3.connect('object_counts.db')
c = conn.cursor()

# Create table with predefined columns
c.execute(
'''
CREATE TABLE IF NOT EXISTS counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT,
    datetime timestamp,
    person INTEGER,
    bicycle INTEGER,
    car INTEGER,
    motorcycle INTEGER,
    airplane INTEGER,
    bus INTEGER,
    train INTEGER,
    truck INTEGER,
    boat INTEGER,
    "traffic light" INTEGER,
    "fire hydrant" INTEGER,
    "stop sign" INTEGER,
    "parking meter" INTEGER,
    bench INTEGER,
    bird INTEGER,
    cat INTEGER,
    dog INTEGER,
    horse INTEGER,
    sheep INTEGER,
    cow INTEGER,
    elephant INTEGER,
    bear INTEGER,
    zebra INTEGER,
    giraffe INTEGER,
    backpack INTEGER,
    umbrella INTEGER,
    handbag INTEGER,
    tie INTEGER,
    suitcase INTEGER,
    frisbee INTEGER,
    skis INTEGER,
    snowboard INTEGER,
    "sports ball" INTEGER,
    kite INTEGER,
    "baseball bat" INTEGER,
    "baseball glove" INTEGER,
    skateboard INTEGER,
    surfboard INTEGER,
    "tennis racket" INTEGER,
    bottle INTEGER,
    "wine glass" INTEGER,
    cup INTEGER,
    fork INTEGER,
    knife INTEGER,
    spoon INTEGER,
    bowl INTEGER,
    banana INTEGER,
    apple INTEGER,
    sandwich INTEGER,
    orange INTEGER,
    broccoli INTEGER,
    carrot INTEGER,
    "hot dog" INTEGER,
    pizza INTEGER,
    donut INTEGER,
    cake INTEGER,
    chair INTEGER,
    couch INTEGER,
    "potted plant" INTEGER,
    bed INTEGER,
    "dining table" INTEGER,
    toilet INTEGER,
    tv INTEGER,
    laptop INTEGER,
    mouse INTEGER,
    remote INTEGER,
    keyboard INTEGER,
    "cell phone" INTEGER,
    microwave INTEGER,
    oven INTEGER,
    toaster INTEGER,
    sink INTEGER,
    refrigerator INTEGER,
    book INTEGER,
    clock INTEGER,
    vase INTEGER,
    scissors INTEGER,
    "teddy bear" INTEGER,
    "hair drier" INTEGER,
    toothbrush INTEGER
)
''')

# Load a model
model = YOLO("yolo12x.pt")

# Define a function to detect objects in an image and return a dictionary of name counts
def detect_objects(image_name):
    # Run batched inference on a list of images
    results = model([image_name], imgsz=1024, conf=0.4, verbose=False)  # return a list of Results objects
    # Process results list
    for result in results:
        result_json = result.to_json()
        name_counts = count_name_values(result_json)
        # Insert image name into SQLite database
        c.execute('INSERT INTO counts (image_name) VALUES (?)',(image_name,))
        count_id = c.lastrowid
        # Insert name counts into SQLite database
        for name, count in name_counts.items():
            c.execute(f'UPDATE counts SET "{name}" = ? WHERE id = ?', (count, count_id))
        conn.commit()
    return name_counts

images_dir = "/Users/yang_li/yolo11"
# read jpg list from images_dir
jpg_list = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
for jpg in tqdm(jpg_list, desc="Processing images"):
    detect_objects(jpg)

# Close the database connection
conn.close()
