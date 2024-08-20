from client.utils import *

# 获取麦克风设备列表
def list_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    devices = []
    for i in range(numdevices):
        if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
            devices.append(p.get_device_info_by_host_api_device_index(0, i))
    p.terminate()

    print("Available recording devices:")
    devices_dict = {}
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']}")
        devices_dict[device['name']] = i
    return devices, devices_dict

def init_device():
    devices, devices_dict = list_devices()
    device_id = int(input("请选择设备:"))
    print("选择设备：",devices[device_id])
    device = devices[device_id]  # Select the first available device, modify as needed
    return device

class Microphone():
    def __init__(self,
                 format=pyaudio.paInt16,
                channels=1,
                sample_rate=16000,
                frames_per_buffer=1024,
                device = None):
        
        self.device = device
        self.format = format
        self.channels = channels
        self.sample_rate = sample_rate
        self.frames_per_buffer = frames_per_buffer
        
    def demo(self):
        self.waveform = []
        chunk_size = 1024
        while 1:
            data = self.stream.read(chunk_size)
            data = np.frombuffer(data,dtype='int16')
            self.waveform.extend(data)
        self.deinit_stream()


    def init_stream(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.device['index'],
            frames_per_buffer=self.frames_per_buffer
        )
        print("Initialized the stream reader successfully.")

    def deinit_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("Deinitialized the stream reader successfully.")


if __name__ == "__main__":

    device = init_device()
    mphone = Microphone(device=device)
    waveform = []
    chunk_size = 1024

    mphone.init_stream()
    for _ in range(200):
        data = mphone.stream.read(chunk_size)
        data = np.frombuffer(data,dtype='int16')
        waveform.extend(data)
    mphone.deinit_stream()

    print(len(waveform))

