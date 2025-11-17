import websocket
import json
import threading
import time
import pyautogui
from pynput.mouse import Controller



IP = '_enter_ip_here_'




class GyroMouseServer:
    def __init__(self, data, stop_event, ip="192.168.1.14", port=8080):
        self.data = data
        self.stop_event = stop_event
        self.ip = ip
        self.port = port
        self.last_time = time.time()

    def process_sensor_data(self, sensor_timestamp):
        current_time = sensor_timestamp / 1e9
        dt = current_time - self.last_time
        self.last_time = current_time
        return dt

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            values = data.get('values', [0, 0, 0])
            dt = self.process_sensor_data(data.get('timestamp', 0))
            
            dx = -values[2] * 640
            dy = -values[0] * 480
            self.data['velocity'] = self.normalize([dx, dy])
            self.data['velocity'][0] *= dt
            self.data['velocity'][1] *= dt
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_open(self, ws):
        self.last_time = time.time()

    def run(self):
        url = f"ws://{self.ip}:{self.port}/sensor/connect?type=android.sensor.gyroscope"
        ws = websocket.WebSocketApp(url, on_open=self.on_open, on_message=self.on_message)
        while not self.stop_event.is_set():
            ws.run_forever()

    @staticmethod
    def normalize(vel):
        x, y = vel
        mag = (x**2 + y**2) ** 0.5
        if mag == 0:
            return [0, 0]
        return [x / mag, y / mag]

def move_mouse(data, stop_event):
    mouse = Controller()
    while not stop_event.is_set():
        if 'velocity' in data:
            dx, dy = data['velocity']
            current_x, current_y = pyautogui.position()
            new_x = max(min(current_x + dx * 100, 1920 - 2), 1)
            new_y = max(min(current_y + dy * 100, 1080 - 2), 1)
            mouse.position = (new_x, new_y)
        time.sleep(0.01)

if __name__ == "__main__":
    data = {}
    stop_event = threading.Event()
    
    server = GyroMouseServer(data, stop_event, IP)
    sensor_thread = threading.Thread(target=server.run)
    mouse_thread = threading.Thread(target=move_mouse, args=(data, stop_event))
    
    sensor_thread.start()
    mouse_thread.start()
    
    try:
        sensor_thread.join()
        mouse_thread.join()
    except KeyboardInterrupt:
        print("Stopping threads...")
        stop_event.set()
