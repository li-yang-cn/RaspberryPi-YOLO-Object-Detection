# YOLO-Object-Detection-Camera

## Project Description
A real-time object detection system using YOLO and a camera module, storing detected data in an SQLite database. 

Designed for Raspberry Pi with automated image capture and analysis.

## Requirements
- Raspberry Pi 4B
- Official HD Camera Module
- Python 3.7 or higher

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/li-yang-cn/YOLO-Object-Detection-Camera.git
   cd YOLO-Object-Detection-Camera
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure the camera:**

   `**INFO:** No need to enable camera on the new Raspbian OS.`

   Ensure the camera is properly connected to the Raspberry Pi and enabled. You can enable the camera using the `raspi-config` tool:
   ```sh
   sudo raspi-config
   ```
   Navigate to `Interfacing Options` -> `Camera` and enable it.

4. **Run the detection script:**
   ```sh
   python detect.py
   ```

## Usage
The `detect.py` script will start capturing images from the camera and perform real-time object detection using YOLO. Detected objects and their timestamps will be stored in an SQLite database.

## Directory Structure
```
YOLO-Object-Detection-Camera/
├── README.md
├── detect.py
├── requirements.txt
└── data.db
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

Make sure to replace `https://github.com/li-yang-cn/YOLO-Object-Detection-Camera.git` with the actual URL of your GitHub repository. This `README.md` provides clear instructions and a concise overview of your project.