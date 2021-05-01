import multiprocessing
import time
from typing import Callable

import requests


def staying_alive(url: str, wait_seconds: float, quit_event: multiprocessing.Event):
    while not quit_event.is_set():
        print(f'Ha! Ha! Ha! Ha! Staying {url} alive')
        requests.get(url)
        time.sleep(wait_seconds)


def worker(process: Callable, quit_event: multiprocessing.Event):
    process()
    quit_event.set()
