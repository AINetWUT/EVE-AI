import os
from time import gmtime, strftime
from pocketsphinx import LiveSpeech

#dictionary
'''
turn on 
turn off
recognize face
is there
human 
on the screen
go youtube
how are you
computer
'''

class AcousticModel:
    def __init__(self, model_path, model_hmm_path):
        self.model_path = model_path
        self.model_hmm_path = model_hmm_path

        self.SAMPLING_RATE = 16000
        self.BUFFER_SIZE = 2048

        config = LiveSpeech(
                verbose=False,
                sampling_rate=16000,
                buffer_size=2048,
                no_search=False,
                full_utt=False,
                hmm=os.path.join(model_hmm_path, 'en-us'),
                lm=os.path.join(model_path, '6856.lm'),
                dic=os.path.join(model_path, '6856.dic')
        )
        self.SPEECH = config
        self.words = []

    def run(self):
        print("Mice is listening...\n")
        for phrase in self.SPEECH:
            cur_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            split = [word for word in str(phrase).split()]
            record = (cur_time, split)
            self.words.append(record)
            print("\nYou said:" + str(phrase))
            print("All words in session: " + str(self.words))


def main():
    model_hmm_path = "/home/pawel/sphinxCMU/pocketsphinx/model/en-us"
    model_path = "/home/pawel/Desktop/acoustic model/"
    model = AcousticModel(model_path, model_hmm_path)
    model.run()

    
if __name__ == "__main__":
    main()
