from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

IMAGE_DIR = Path.home() / "aquaclean/new_data/labeled/images"

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

server = ThreadingHTTPServer(
    ("127.0.0.1", 8000),
    lambda *args, **kwargs:
        CORSHandler(*args, directory=str(IMAGE_DIR), **kwargs)
)

print(f"Serving images from: {IMAGE_DIR}")
print("Open images at: http://127.0.0.1:8000/frame_101.jpg")
print("Press Ctrl+C to stop.")

server.serve_forever()
