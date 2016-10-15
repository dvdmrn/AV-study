# import scipy
# import scipy.io.wavfile
# import numpy

# convert_16_bit = float(2**15)
# sr,data = scipy.io.wavfile.read('sampletone.wav')

# sr1,data1 = scipy.io.wavfile.read('sampletone1.wav')
# # x = np.linspace(0, 2000, 0.01)
# # samples = samples / (convert_16_bit + 1.0)
# # y = samples
# # print samples
# # plt.plot(x, y)
# # plt.show()
# print data.size
# print data1.size
# print sr.size
# print sr1.size

#--------------------------------------------------------------------------------//
# import pygame
# from scikits.audiolab import wavread

# i = 0
# filename = "sampletone2.wav"

# data, sample_frequency,encoding = wavread(filename)


# print("sampe frequency: ",sample_frequency)
# print("samples: ",i)
# pygame.mixer.init(frequency=22050, size=8, channels=2, buffer=512)
# sound = pygame.mixer.Sound(filename)
# sound.play()


# for e in data:
# 	i+=1
# 	print("yo ",e*10)
#--------------------------------------------------------------------------------//

# import pyaudio
# import wave
# import sys

# CHUNK = 1024

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

# wf = wave.open(sys.argv[1], 'rb')

# p = pyaudio.PyAudio()

# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)

# data = wf.readframes(CHUNK)

# while data != '':
#     stream.write(data)
#     data = wf.readframes(CHUNK)

# stream.stop_stream()
# stream.close()

# p.terminate()

#--------------------------------------------------------------------------------//

import pygame
import numpy

pygame.mixer.init(frequency=44100, size=8, channels=2, buffer=512)


filename = "sampletone.wav"
sound = pygame.mixer.Sound(filename)

buf = pygame.sndarray.array(sound)

for i in buf:
	print i


pygame.sndarray.make_sound(buf)

print "done"