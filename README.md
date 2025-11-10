# minimal-picam-server

A minimal HTTP server to stream video from a Raspberry Pi camera.

## Quickstart

- Clone this repository: `git clone https://github.com/brainwagon/minimal-picam-server.git`
- Navigate to the directory: `cd minimal-picam-server`
- Install dependencies: `pip install Flask picamera2`
- Run the server: `python3 minimal-picam-server.py`
- The server will be running on `http://0.0.0.0:8080`.

## Endpoints

- **GET /**: Returns a simple HTML page with links to the snapshot and stream.
- **GET /snapshot**: Captures and returns a single JPEG image from the camera.
- **GET /stream**: Returns a Motion JPEG (mjpeg) stream from the camera.

## Running as a service

To have the server run automatically on boot, you can install the provided `systemd` service file.

1.  **Edit the service file** to reflect the correct paths for your setup. The `minimal-picam-server.service` file assumes the user is `pi` and the code is in `/home/pi/minimal-picam-server`. You **must** change the `User`, `WorkingDirectory`, and `ExecStart` paths to match your specific user and the location where you cloned the repository. For example, if your user is `markv` and the code is in `/home/markv/minimal-picam-server`, you would edit the file to look like this:

    ```
    [Unit]
    Description=Minimal Picam Server
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /home/markv/minimal-picam-server/minimal-picam-server.py
    WorkingDirectory=/home/markv/minimal-picam-server
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    RestartSec=5
    User=markv
    Environment=PYTHONUNBUFFERED=1

    [Install]
    WantedBy=multi-user.target
    ```

2.  **Copy the service file** to the systemd directory:

    ```bash
    sudo cp minimal-picam-server.service /etc/systemd/system/
    ```

3.  **Enable the service** to start on boot:

    ```bash
    sudo systemctl enable minimal-picam-server.service
    ```

4.  **Start the service**:

    ```bash
    sudo systemctl start minimal-picam-server.service
    ```

5.  **Check the status** of the service:

    ```bash
    sudo systemctl status minimal-picam-server.service
    ```

## Notes

- Make sure the Pi camera is enabled in `raspi-config`.
- For public access, it is recommended to run this server behind a reverse proxy and add authentication.

## License

MIT
