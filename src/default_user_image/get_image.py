import json

import requests

URL = "https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg"

response = requests.get(URL)

if response.status_code == 200:
    with open("user-image.jpg", "wb") as f:
        f.write(response.content)
        print("image downloaded successfully!")

else:
    print(f"ERROR: {response.status_code}")
    print(response.text)
