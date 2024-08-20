from client.microphone import * 
from client.worker import Worker
import requests
import numpy as np

SERVER_URL = "http://www.funsound.cn:5002"


class AudioStream(Worker):
    def __init__(self,
                 mphone:Microphone=None):
        super().__init__()
        self.mphone = mphone

    def run(self):
        self.waveform = []
        chunk_size = 1024
        mphone.init_stream()
        while not self._stop_event.is_set():
            data = mphone.stream.read(chunk_size)
            data = np.frombuffer(data,dtype='int16')
            self.waveform.extend(data)
        mphone.deinit_stream()





if __name__ == "__main__":

    device = init_device()
    mphone = Microphone(device=device)
    

    while 1:
        audio_stream = AudioStream(mphone=mphone)

        input("按下任意键开始录音")
        audio_stream.start()

        input("按下任意键结束录音")
        audio_stream.stop()
        audio_stream.join()

        save_wavfile('tmp.wav',np.array(audio_stream.waveform))

        # with open('tmp.wav', 'rb') as audio_file:
        #     files = {'file': audio_file}
        #     response = requests.post(f"{SERVER_URL}/kws", files=files)

        # if response.status_code == 200:
        #     print(response.json())
        # else:
        #     print(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")
        print("---\n")
