from flask import Flask, render_template

execfile("/temp_monitor/temp_monitor.py")
monitor()

print __name__

app = Flask(__name__)

monitor()

@app.route('/')
def index():
    return render_template('index.html');

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0');
