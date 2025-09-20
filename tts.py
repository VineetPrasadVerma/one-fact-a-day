from gtts import gTTS
import sys

# text = sys.argv[1]
text = "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old — and still perfectly edible! It’s one of the few foods that can last forever. Follow for more daily facts! "
tts = gTTS(text)
tts.save("output/audio.mp3")
