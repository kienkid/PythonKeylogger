from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

HOST = "192.168.1.28"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
DATA_FILE = os.path.join(BASE_DIR, "data.txt")


class SimpleHandler(BaseHTTPRequestHandler):

    # -------- GET request --------
    def do_GET(self):
        if self.path == "/":
            if os.path.exists(INDEX_FILE):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                with open(INDEX_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"index.html not found")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    # -------- POST request --------
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)

            # Validate format {"key": "value"}
            if isinstance(data, dict) and "key" in data:
                with open(DATA_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(data) + "\n")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "saved"}')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON format")

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")


def run():
    try:
        server = HTTPServer((HOST, PORT), SimpleHandler)
        print(f"Server running on http://{HOST}:{PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    run()