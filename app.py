from flask import Flask, render_template
from sense_hat import SenseHat, ACTION_PRESSED
from threading import Timer
sense = SenseHat();

current_temp = 0

###
# Web Server
###

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html');

@app.route('/current-temp')
def get_temp():
    return str(current_temp);

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0');

###
# Temperature Monitoring
###
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

        def __exit__(self, type, value, traceback):
            self.close()

        def close(self):
            self.tempfile.close()


# Display illumination toggle
sense.low_light = True
no_gamma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def gamma_off():
    sense.low_light = False
    sense.gamma = no_gamma

def pushed_up(event):
    if sense.low_light == False and event.action != ACTION_PRESSED:
        sense.low_light = True

def pushed_down(event):
    if sense.low_light == True and event.action != ACTION_PRESSED:
        gamma_off()

sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down

# Number display matrix
OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1]  # 9

# Displays a single digit (0-9)
def show_digit(val, xd, yd, r, g, b):
  offset = val * 15
  for p in range(offset, offset + 15):
    xt = p % 3
    yt = (p-offset) // 3
    sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

# Displays a two-digits positive number (0-99)
def show_number(val, r, g, b):
  abs_val = abs(val)
  tens = abs_val // 10
  units = abs_val % 10
  if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
  show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)

def toFarenheit(c):
    return  int(9.0/5.0 * c + 32)

def tempLoop():
    t = sense.get_temperature()
    p = sense.get_temperature_from_pressure()
    h = sense.get_temperature_from_humidity()
    with CPUTemp() as cpu_temp:
        c = cpu_temp.get_temperature()
    temp_calc = ((t+p+h)/3) - (c/5)
    sense.clear()
    f_temp = toFarenheit(temp_calc)
    show_number(int(f_temp), 255, 0 , 190)
    current_temp = f_temp
    Timer(15.0, tempLoop).start()

tempLoop()