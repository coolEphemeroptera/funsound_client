from recorder import * 
import requests
import numpy as np

SERVER_URL = "http://www.funsound.cn:5002"

if __name__ == "__main__":

    device = init_device()
    

    while 1:
        recorder = Recorder(device=device)
        input("按下任意键开始录音")
        recorder.start()

        input("按下任意键结束录音")
        recorder.stop()
        recorder.join()

        save_wavfile('tmp.wav',np.array(recorder.waveform))

        with open('tmp.wav', 'rb') as audio_file:
            files = {'file': audio_file}
            response = requests.post(f"{SERVER_URL}/kws", files=files)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")
        print("---\n")
