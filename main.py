from sense_hat import SenseHat
from threading import Timer

sense = SenseHat();
sense.low_light = True
sense.rotation = 180

loop = 1

def tempLoop():
	t = ap.get_temperature()
	p = ap.get_temperature_from_pressure()
	h = ap.get_temperature_from_humidity()
	with CPUTemp() as cpu_temp:
		c = cpu_temp.get_temperature()
	temp_calc = ((t+p+h)/3) - (c/5)
	sense.show_message(str(round((temp_calc + 32), 2)), scroll_speed=0.2, text_colour=[139,0,0], back_colour=[0,0,0])
	Timer(15.0, tempLoop).start()

tempLoop()
