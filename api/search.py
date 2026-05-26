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

            url = f"https://ukraine-xinfo-onrender-leak.42web.io/leak-api.php?key=TusharT&type=leakk&term={number}"

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json,text/plain,*/*"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=60
            )

            text = response.text

            try:
                data = response.json()
            except:
                data = {
                    "status": True,
                    "raw_response": text
                }

            self.wfile.write(json.dumps(data).encode())

        except Exception as e:
            self.wfile.write(json.dumps({
                "status": False,
                "error": str(e)
            }).encode())
