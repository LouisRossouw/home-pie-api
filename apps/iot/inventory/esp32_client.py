import requests

# TODO; Explore an mqtt broker; mosquitto - https://mosquitto.org/ .. Do i need this? No idea.


def esp32_post(url, payload=None, timeout=2):
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("ESP32 API error:", e)
        return {"error": str(e)}
