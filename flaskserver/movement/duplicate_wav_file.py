import wave
import os

def read_wav_file_to_copy(name):
    filename = r'/home/pi/sensory/SEnsory/oop/inner'
    filename += f"/{name}"
    wave_read = wave.open(filename, 'rb')
    return wave_read


def wav_file_to_write(name):
    filename = r"/home/pi/sensory/SEnsory/oop/inner"
    name = name.split(".")[0] 
    filename += f"/{name}_copy"+".wav"
    wav_obj = wave.open(filename, 'wb')
    return wav_obj


def copy_file(wav_read, wav_write):
    wav_write.setnchannels(wav_read.getnchannels())
    wav_write.setsampwidth(wav_read.getsampwidth())
    wav_write.setframerate(wav_read.getframerate())
    
    frames = []
    for i in range(wav_read.getnframes()):
        frames.append(wav_read.readframes(i))

    wav_write.writeframes(b''.join(frames))
    wav_write.close()
    


def duplicateIt():
    onlyfiles = os.listdir(r"/home/pi/sensory/SEnsory/oop/inner")
    
    wav_read = read_wav_file_to_copy(onlyfiles[0])
    wav_write = wav_file_to_write(onlyfiles[0])
    copy_file(wav_read, wav_write)