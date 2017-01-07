from sense_hat import SenseHat
from threading import Timer

sense = SenseHat();
sense.low_light = True
sense.rotation = 180



def tempLoop():

	sense.show_message("POOPDICK", scroll_speed=0.2, text_colour=[139,0,0], back_colour=[0,0,0])
	Timer(8.0, tempLoop).start()

tempLoop()