import os
from pocketsphinx.pocketsphinx import *
from pocketsphinx import get_data_path, get_model_path
from sphinxbase.sphinxbase import *
import pyaudio
import wave


class AcousticModel(object):

    def __init__(self):

        model_path = get_model_path()
        data_path = get_data_path()
        config = Decoder.default_config()

        config.set_string('-hmm', os.path.join(model_path, 'en-us'))
        config.set_string('-lm', os.path.join(model_path, 'en-us.lm.bin'))
        config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))

        self.decoder = Decoder(config)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "tmp.wav"

    def write_to_wave(self, frames):
        wave_file = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wave_file.setnchannels(self.CHANNELS)
        wave_file.setsampwidth(pyaudio.get_sample_size(self.FORMAT))
        wave_file.setframerate(self.RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        return str(wave_file)

    def decode_phrase(self, wav_file):
        words = []
        file_path = 'C:/Users/pawel/PycharmProjects/EVE-AI/'
        buf = bytearray(1024)
        with open(os.path.join(file_path, 'tmp.wav'), 'rb') as f:
            self.decoder.start_utt()
            while f.readinto(buf):
                self.decoder.process_raw(buf, False, False)
            self.decoder.end_utt()
        print('Best hypothesis segments:', [seg.word for seg in self.decoder.seg()])
        [words.append(seg.word) for seg in self.decoder.seg()]
        return words
    ''''
    def show_speech(self, words):
        for word in words:
            print(word)
    '''
    def run(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        print("Mic is recording...")
        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        words = self.decode_phrase(self.write_to_wave(frames))
        #self.show_speech(words)


model = AcousticModel()
model.run()

