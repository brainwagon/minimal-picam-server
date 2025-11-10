from flask import Flask, Response
from picamera2 import Picamera2
from libcamera import Transform, controls
import io

# minimal-picam-server.py
# 
# I was experimenting with a Raspberry Pi 5 and a better camera, and realized that I still 
# had an original Pi Zero (with just 512M of RAM) and an early Raspberry Pi Camera.  I thought
# it might be fun to create a very minimal application that could stream images via 
# a web server.   This isn't quite as simple as it could be: it uses Flask and the picamera2 
# library has a pretty large footprint, but I thought it might be useful.
#

app = Flask(__name__)
camera = Picamera2()

# Configure the camera for still captures
transform = Transform(hflip=False, vflip=False, rotation=180)
camera.configure(camera.create_still_configuration(main={"size":(640,480)}, transform=transform))
camera.start()

@app.route('/')
def index():
    html = """
    <html>
    <head>
        <title>PiCamera2 Image Server</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding: 2em; }
            img { max-width: 100%; height: auto; border: 1px solid #ccc; }
            .endpoints { margin-top: 2em; }
            .endpoints a { display: block; margin: 0.5em; }
        </style>
    </head>
    <body>
        <h1>PiCamera2 Image Server</h1>
        <p>This server provides a live feed from a Raspberry Pi camera.</p>
        
        <h2>Live Snapshot</h2>
        <p>The image below is a single frame captured from the camera. Refresh the page to get a new one.</p>
        <img src="/snapshot" alt="Live Snapshot from PiCamera">
        
        <div class="endpoints">
            <h2>Available Endpoints</h2>
            <p>You can also access the raw streams directly:</p>
            <a href="/snapshot">/snapshot</a> - A single JPEG image.<br>
            <a href="/stream">/stream</a> - A Motion JPEG (mjpeg) stream.
        </div>
    </body>
    </html>
    """
    return html

@app.route('/snapshot')
def serve_image():
    stream = io.BytesIO()
    frame = camera.capture_file(stream, format='jpeg')
    stream.seek(0)
    return Response(stream.read(), mimetype='image/jpeg')

import time

@app.route('/stream')
def stream():
    def generate():
        while True:
            stream = io.BytesIO()
            camera.capture_file(stream, format='jpeg')
            stream.seek(0)
            frame = stream.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
