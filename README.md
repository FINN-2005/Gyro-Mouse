# Gyro-Mouse

Control your PC’s mouse cursor using your Android phone’s gyroscope.

# Description

This project turns an Android phone into a motion-based mouse by streaming gyroscope data to your PC over WebSocket.
A Python script receives the sensor data, converts it to a normalized velocity vector, and moves the mouse cursor accordingly.

The system uses two threads:
- one for receiving gyroscope readings
- one for updating the mouse position

This is an experimental prototype intended for simple motion control and testing, not a polished final product.

# Installation
- clone this repo
- install dependencies
  ```bash
  pip install websocket-client pynput pyautogui
  ```

# Usage
- Get your PC’s local IP address (e.g., 192.168.x.x).
- Update line 10 in `server.py`:
  ```python
  IP = '_enter_ip_here_'
  ```
- Run the Python script:
- python server.py
- Open Sensor Server on your Android phone:
  - Select the Gyroscope sensor
  - Enter the WebSocket address:
    ```ws://<PC_IP>:8080/sensor/connect?type=android.sensor.gyroscope```
  - Start streaming
- Tilt/rotate your phone to move the PC mouse cursor.
- Press Ctrl + C to stop the program safely.
