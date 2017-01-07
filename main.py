from sense_hat import SenseHat
from threading import Timer

class CPUTemp:
    def __init__(self, tempfilename = "/sys/class/thermal/thermal_zone0/temp"):
        self.tempfilename = tempfilename

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.tempfile = open(self.tempfilename, "r")

    def read(self):
        self.tempfile.seek(0)
        return self.tempfile.read().rstrip()

    def get_temperature(self):
        return self.get_temperature_in_c()

    def get_temperature_in_c(self):
        tempraw = self.read()
        return float(tempraw[:-3] + "." + tempraw[-3:])

    def get_temperature_in_f(self):
        return self.convert_c_to_f(self.get_temperature_in_c())

    def convert_c_to_f(self, c):
        return c * 9.0 / 5.0 + 32.0

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.tempfile.close()


sense = SenseHat();
sense.low_light = True
sense.rotation = 180

loop = 1

def toFarenheit(c):
	return  9.0/5.0 * c + 32

def tempLoop():
	t = sense.get_temperature()
	p = sense.get_temperature_from_pressure()
	h = sense.get_temperature_from_humidity()
	with CPUTemp() as cpu_temp:
		c = cpu_temp.get_temperature()
	temp_calc = ((t+p+h)/3) - (c/5)
	sense.show_message(str(round((toFarenheit(temp_calc)), 1)), scroll_speed=0.2, text_colour=[139,0,0], back_colour=[0,0,0])
	Timer(15.0, tempLoop).start()

tempLoop()