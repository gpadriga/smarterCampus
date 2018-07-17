import numpy
import pyaudio
import analyse

# Initialize PyAudio
pyaud = pyaudio.PyAudio()

# Open input stream, 16-bit mono at 44100 Hz
# Device 2 is USB mic
stream = pyaud.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input_device_index=2,
    frames_per_buffer=1024,
    input=True)

while True:
    # Read raw microphone data
    rawsamps = stream.read(2048, exception_on_overflow=False)
    # Convert raw data to NumPy array
    samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
    # Show the volume and pitch
    print ("Sound in dB: " + str(analyse.loudness(samps)))
