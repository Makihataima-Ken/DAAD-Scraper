import time
import random

def delay_random(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))
