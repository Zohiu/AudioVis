import numpy
import sounddevice
import pyaudio
import numpy as np
from scipy.fftpack import fft
import struct
import json


class Audio:
    pa = pyaudio.PyAudio()
    pa.get_default_host_api_info()

    with open("data.json", "r") as f:
        s = json.loads(f.read())

    CHUNK = s["Audio"]["CHUNK"]
    RATE = s["Audio"]["RATE"]
    CHANNELS = s["Audio"]["CHANNELS"]

    FORMAT = pyaudio.paInt16

    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK, input_device_index=12
    )

    all_stages = ["PEAK", "BASS", "MID", "HIGH"]

    OUTPUT = {"RAW": stream.read(CHUNK), "FREQ": [], "FLOOR": 0, "VOL": 0, "PEAK": False, "BASS": False, "MID": False, "HIGH": False}

    save = {"index": 0, "data": {"PEAK": [], "BASS": [], "MID": [], "HIGH": []}}

    @staticmethod
    def streamRead():
        raw = Audio.stream.read(Audio.CHUNK)
        data = struct.unpack(str(Audio.CHUNK * Audio.CHANNELS) + 'h', raw)
        fft_data = fft(data)
        fft_data = np.abs(fft_data[:Audio.CHUNK]) * 2 / (256 * Audio.CHUNK)

        n = Audio.CHUNK // 512
        bands = [sum(fft_data[i:(i + n)] * 2) for i in range(0, fft_data.size, n)]

        peak = ((np.average(np.abs(np.fromstring(raw, dtype=np.int16))) * 2) / 50000) * 255
        if peak > 255:
            peak = 255

        current_freq = {"PEAK": peak, "BASS": np.average(bands[:2]), "MID": np.average(bands[2:6]), "HIGH": np.average(bands[6])}

        if Audio.save["index"] >= 4:
            floor = np.average(Audio.save["data"]["PEAK"])
            Audio.OUTPUT["FLOOR"] = np.average(floor)
            Audio.OUTPUT["VOL"] = current_freq["PEAK"]
            Audio.OUTPUT["FREQ"] = bands[:10]

            for stage in Audio.all_stages:
                stage_floor = round(np.average(Audio.save["data"][stage]), 1)
                highest = round(max(Audio.save["data"][stage]), 1)
                now = round(current_freq[stage], 1)

                # print(stage, stage_floor, highest, now)
                if stage == "HIGH":
                    compare_to = 1
                elif stage == "MID":
                    compare_to = 1 / 2
                else:
                    compare_to = 1 / 3

                #if stage_floor + stage_floor * compare_to < highest or stage_floor + stage_floor * compare_to < now:

                if now > 5:
                    now += current_freq["PEAK"] / 6


                if stage_floor + stage_floor * compare_to < now :
                    Audio.OUTPUT[stage] = True
                else:
                    Audio.OUTPUT[stage] = False

            Audio.save["index"] = 0
            for i in ["PEAK", "BASS", "MID", "HIGH"]:
                Audio.save["data"][i] = []
        else:
            Audio.save["index"] += 1
            Audio.save["data"]["PEAK"].append(current_freq["PEAK"])
            Audio.save["data"]["BASS"].append(current_freq["BASS"])
            Audio.save["data"]["MID"].append(current_freq["MID"])
            Audio.save["data"]["HIGH"].append(current_freq["HIGH"])

    @staticmethod
    def stopStream():
        # close the stream gracefully
        Audio.stream.stop_stream()
        Audio.stream.close()
        Audio.p.terminate()

    @staticmethod
    def audioReadStarter():
        while True:
            Audio.streamRead()