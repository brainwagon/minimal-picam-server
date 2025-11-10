# minimal-picam-server

A minimal HTTP server to capture and serve images from a Raspberry Pi camera.

Quickstart

- Clone: git clone https://github.com/brainwagon/minimal-picam-server.git
- Run: python3 server.py
- Default: listens on 0.0.0.0:8000

Endpoints

- GET /capture — capture and return a JPEG
- GET /images — list saved images
- GET /images/<name> — download a saved image

Notes

- Enable the Pi camera (raspi-config) and reboot if needed.
- For public access, run behind a reverse proxy and add authentication.

License: MIT
