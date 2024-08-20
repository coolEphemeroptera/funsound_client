from client.utils import *

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self._stop_event = threading.Event()
        
    def stop(self):
        self._stop_event.set()
    
    def run(self) -> None:
        self.waveform = []
        chunk_size = 1024
        while not self._stop_event.is_set():
            pass 
