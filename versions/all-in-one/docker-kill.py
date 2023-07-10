import os
import time
import signal

IDLE_THRESHOLD = 30 * 60  # 30 minutes

def check_inactivity():
    last_activity = time.time()
    while True:
        current_time = time.time()
        if current_time - last_activity > IDLE_THRESHOLD:
            print("Idle time exceeded. Shutting down.")
            os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(60)

if __name__ == "__main__":
    check_inactivity()
