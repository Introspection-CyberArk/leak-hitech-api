from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        try:
            query = parse_qs(urlparse(self.path).query)

            number = query.get("number", [""])[0]

            if not number:
                self.wfile.write(json.dumps({
                    "status": False,
                    "message": "Missing number parameter"
                }).encode())
                return

            api_url = (
                "https://ukraine-xinfo-onrender-leak.42web.io/"
                f"leak-api.php?key=TusharT&type=leakk&term={number}"
            )

            response = requests.get(api_url, timeout=30)

            # if API returns non-json
            try:
                data = response.json()
            except:
                data = {
                    "status": False,
                    "response": response.text
                }

            self.wfile.write(json.dumps(data).encode())

        except Exception as e:
            self.wfile.write(json.dumps({
                "status": False,
                "error": str(e)
            }).encode())
