from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

@app.route("/search/<number>")
def search(number):

    url = (
        "https://ukraine-xinfo-onrender-leak.42web.io/"
        f"leak-api.php?key=TusharT&type=leakk&term={number}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers
    )

    return response.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
