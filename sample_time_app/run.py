from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

# Define the domain route
@app.route('/')
def hello_world():
    return 'Hello world!'

# Get the current time
@app.route('/time')
def get_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The current time is: {current_time}" 


app.run(host='0.0.0.0',
        port=8080,
        debug=True)



