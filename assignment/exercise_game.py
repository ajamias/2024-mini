"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import uresquests as requests
import json
import network
SSID = "BU Guest (unencrypted)"


           
            
    


N = 10.0
on_ms = 500
FIREBASE_URL = "https://minipro-c5169-default-rtdb.firebaseio.com/"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("loading")
        wlan.connect(SSID)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected to:", wlan.ifconfig())
           
connect_wifi()

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if t_good:
        min_time = min(t_good)
        max_time = max(t_good)
        avg_time = sum(t_good) / len(t_good)
        print(f"Average response time: {avg_time} ms")
        print(f"Minimum response time: {min_time} ms")
        print(f"Maximum response time: {max_time} ms")
    else:
        max_time = min_time = avg_time = None
        
    score = (len(t_good) / len(t)) if len(t) else 0.0
    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {
        "min_time": min_time,
        "max_time": max_time,
        "average_time": avg_time,
        "misses": misses,
        "total_flashes": len(t),
        "non_misses": len(t_good),
    }

    # %% make dynamic filename and write JSON

    now = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    
    filename = f"score-{now_str}.json"
    
    

    print("write", filename)

    write_json(filename, data)

    try:
           response = requests.post(FIREBASE_URL, json=data)
           print(f"Data uploaded. Status code: {response_code}")
    except Exception as e:
           print(f"unable to upload: {e}")


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    led = Pin("LED, Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t = []
    #indicate start game
    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()
        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
