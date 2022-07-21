import pyaudio
import numpy as np
from scipy.fftpack import fft
import struct
import json


class Audio:
    pa = pyaudio.PyAudio()

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

    device = input("Which device is your input? : ")

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK, input_device_index=int(device)
    )

    print("yeeees")

    all_stages = ["PEAK", "BASS", "MID", "HIGH"]

    OUTPUT = {"RAW": stream.read(CHUNK), "FREQ": [], "FLOOR": 0, "VOL": 0, "PEAK": False, "BASS": False, "MID": False, "HIGH": False}

    save = {"index": 0, "data": {"PEAK": [], "BASS": [], "MID": [], "HIGH": []}}

    @staticmethod
    def streamRead():
        raw = Audio.stream.read(Audio.CHUNK)
        data = struct.unpack(str(Audio.CHUNK * Audio.CHANNELS) + 'h', raw)
        fft_data = fft(data)
        fft_data = np.abs(fft_data[:Audio.CHUNK]) * 2 / (256 * Audio.CHUNK)

        n = Audio.CHUNK // 64
        bands = [sum(fft_data[i:(i + n)] * 2) for i in range(0, fft_data.size, n)]

        peak = ((np.average(np.abs(np.fromstring(raw, dtype=np.int16))) * 2) / 50000) * 255
        if peak > 255:
            peak = 255

        current_freq = {"PEAK": peak, "BASS": np.average(bands[:3]), "MID": np.average(bands[3:4]), "HIGH": np.average(bands[4:])}

        if Audio.save["index"] >= 10:
            floor = np.average(Audio.save["data"]["PEAK"])
            Audio.OUTPUT["FLOOR"] = np.average(floor)

            Audio.save["index"] = 0
            for i in Audio.all_stages:
                Audio.save["data"][i] = []
                Audio.OUTPUT[i] = False
        else:
            Audio.save["index"] += 1
            Audio.save["data"]["PEAK"].append(current_freq["PEAK"])
            Audio.save["data"]["BASS"].append(current_freq["BASS"])
            Audio.save["data"]["MID"].append(current_freq["MID"])
            Audio.save["data"]["HIGH"].append(current_freq["HIGH"])

            Audio.OUTPUT["VOL"] = int(current_freq["PEAK"])
            Audio.OUTPUT["FREQ"] = bands[:10]

            for stage in Audio.all_stages:
                stage_floor = Audio.OUTPUT["FLOOR"]
                highest = round(max(Audio.save["data"][stage]), 1)
                now = round(current_freq[stage], 1)

                # print(stage, stage_floor, highest, now)
                if stage == "HIGH":
                    compare_to = 0.25
                elif stage == "MID":
                    compare_to = 0.35
                elif stage == "BASS":
                    compare_to = 4
                else:
                    compare_to = 1 / 3

                #if stage_floor + stage_floor * compare_to < highest or stage_floor + stage_floor * compare_to < now:

                if now > 5:
                    now += current_freq["PEAK"] / 4

                if stage_floor + stage_floor * compare_to < now :
                    Audio.OUTPUT[stage] = True

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