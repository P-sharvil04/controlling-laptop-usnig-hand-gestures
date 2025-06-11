from flask import Flask, render_template
import subprocess
import os
import signal

app = Flask(__name__)

# Store the process ID of the running Arduino script
arduino_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run_arduino")
def run_arduino():
    global arduino_process
    
    try:
        # Check if Arduino process is already running
        if arduino_process and arduino_process.poll() is None:
            return "python script is already running."

        # Start the Arduino script and store the process ID
        arduino_process = subprocess.Popen(["python", "arduino.py"])
        return "python script started successfully."
    except Exception as e:
        return f"Error starting python script: {str(e)}"

@app.route("/stop_arduino")
def stop_arduino():
    global arduino_process
    
    try:
        # Check if Arduino process is running
        if arduino_process and arduino_process.poll() is None:
            # Terminate the Arduino process
            arduino_process.terminate()
            arduino_process.wait()  # Wait for the process to finish
            return "python script stopped successfully."
        else:
            return "No running python script to stop."
    except Exception as e:
        return f"Error stopping python script: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
