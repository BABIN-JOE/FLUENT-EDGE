# app.py

# Import necessary functions for checking libraries and model paths
from fluent_edge_core.startup_checker import check_library, check_model_path

# Check libraries required for the project
check_library("flask")  # Verifies if Flask is installed
check_library("flask_cors")  # Verifies if Flask CORS is installed
check_library("sounddevice")  # Verifies if SoundDevice library is installed
check_library("language_tool_python")  # Verifies if LanguageTool for grammar checking is installed

# Check the path for the Vosk model, used for speech recognition
check_model_path("model/Indian English/vosk-model-en-in-0.5", "Vosk Model")

# Import other necessary modules
import os
import sys
import json
import threading
import time
import webbrowser
from flask import Flask, Response, render_template, jsonify, request  # Flask-related imports for the web app
from flask_cors import CORS  # Flask-CORS for enabling Cross-Origin Resource Sharing (CORS)
from fluent_edge_core.audio_handler import start_recording, stop_recording  # Audio handling functions
from fluent_edge_core.speech_recognizer import transcribe_audio  # Function for transcribing audio
from fluent_edge_core.grammar_checker import check_grammar  # Function for checking grammar
from fluent_edge_core.accuracy_checker import calculate_accuracy  # Function for calculating accuracy

# Initialize Flask app
app = Flask(__name__)  # Create a Flask app instance
CORS(app)  # Enable CORS for the app to allow cross-origin requests

# Global variables
full_transcription = []  # Stores the entire transcription
stop_recording_flag = threading.Event()  # Event to signal stopping the recording
transcription_thread = None  # Thread for transcribing audio in the background
stream = None  # Audio stream for recording
transcription_lock = threading.Lock()  # Lock to manage access to transcription data

# Serve the main HTML page
@app.route('/')
def index():
    if not os.path.exists("templates/index.html"):  # Check if the index.html file exists
        print("❌ ERROR: 'index.html' not found.", flush=True)  # Print error if not found
        return "ERROR: 'index.html' not found.", 404  # Return error response
    return render_template("index.html")  # Render the HTML page

# Start Listening API (initiates audio recording)
@app.route('/start', methods=['GET'])
def start_listening():
    global transcription_thread, stream
    if transcription_thread and transcription_thread.is_alive():  # Check if recording is already in progress
        print("⚠️ Already recording!", flush=True)  # Inform user that recording is already happening
        return jsonify({"status": "Already running"}), 400  # Return error response
    
    with transcription_lock:  # Acquire lock to safely access transcription data
        full_transcription.clear()  # Clear the existing transcription

    stop_recording_flag.clear()  # Reset the stop recording flag
    stream = start_recording()  # Start recording audio
    if not stream:  # Check if the recording failed
        print("❌ Failed to start recording!", flush=True)
        return jsonify({"status": "Recording failed"}), 500  # Return error response if recording failed

    # Start a new thread for transcribing audio
    transcription_thread = threading.Thread(
        target=lambda: transcribe_audio(full_transcription, stop_recording_flag),
        daemon=True  # Set thread as a daemon to terminate when the main program ends
    )
    transcription_thread.start()  # Start the transcription thread
    print("✅ Recording started.", flush=True)
    return jsonify({"status": "Recording started"}), 200  # Return success response

# Stop Listening API (stops audio recording)
@app.route('/stop', methods=['GET'])
def stop_listening():
    global stream
    stop_recording_flag.set()  # Set the flag to stop recording
    if stream:  # If recording is ongoing, stop it
        stop_recording(stream)  # Call the function to stop recording
        print("🛑 Recording stopped.", flush=True)
    return jsonify({"status": "Stopping recording"}), 200  # Return response indicating stopping recording

# Streaming Transcription to Frontend
@app.route('/transcription')
def transcription_generator():
    def generate():
        previous_length = 0  # Track the length of transcription to send new data
        while not stop_recording_flag.is_set():  # While the stop flag is not set, keep sending transcription data
            with transcription_lock:  # Acquire lock to safely access transcription data
                if len(full_transcription) > previous_length:  # Check if new data is available
                    new_text = full_transcription[previous_length:]  # Get new transcription data
                    previous_length = len(full_transcription)  # Update previous length
                    yield f"data: LIVE::{' '.join(new_text)}\n\n"  # Stream live transcription data
            time.sleep(0.5)  # Wait before checking for new transcription data again

        # Send the final transcription when the recording stops
        with transcription_lock:
            final_text = " ".join(full_transcription).strip()  # Final transcription as a single string
        yield f"data: FULL_TRANSCRIPTION::{final_text}\n\n"
        print(f"\n📜 Final Transcription: {final_text}", flush=True)

        # Perform grammar check on the final transcription
        try:
            corrections = check_grammar(final_text) or []  # Get grammar errors or an empty list
            print(f"📝 Grammar Errors: {json.dumps(corrections, indent=2)}", flush=True)
            yield f"data: GRAMMAR_ERRORS::{json.dumps(corrections)}\n\n"  # Stream grammar errors to frontend

            # Highlight grammar errors in the transcription
            highlighted_text = final_text
            for item in corrections:
                error = item.get("error")  # Get the error string
                if error and error in highlighted_text:  # If the error exists in the transcription
                    highlighted_text = highlighted_text.replace(
                        error, f"<span class='text-red-500 underline'>{error}</span>"  # Highlight the error in red
                    )
            yield f"data: HIGHLIGHTED_TRANSCRIPTION::{highlighted_text}\n\n"  # Stream the highlighted transcription

        except Exception as e:
            print(f"❌ Error during grammar check: {e}", flush=True)
            yield f"data: GRAMMAR_ERRORS::[]\n\n"  # Send empty grammar errors if there's an exception
            yield f"data: HIGHLIGHTED_TRANSCRIPTION::{final_text}\n\n"  # Send final text without highlighting

        # Calculate accuracy of the transcription based on grammar corrections
        try:
            accuracy = calculate_accuracy(final_text, corrections) or 100  # Default to 100% if no errors
            print(f"🎯 Accuracy: {accuracy}%", flush=True)
            yield f"data: ACCURACY::{accuracy}%\n\n"  # Stream accuracy data to frontend
        except Exception as e:
            print(f"❌ Error calculating accuracy: {e}", flush=True)
            yield f"data: ACCURACY::100%\n\n"  # Send 100% accuracy if there's an exception

    return Response(generate(), mimetype="text/event-stream")  # Return the generator as an EventSource stream

# Exit API (graceful shutdown of the server)
@app.route('/exit', methods=['GET'])
def exit_program():
    print("🛑 Shutting down server...", flush=True)
    shutdown_server()  # Call function to shut down the server
    return jsonify({"status": "Server shut down"}), 200  # Return server shutdown response

# Graceful shutdown of the server
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')  # Get shutdown function
    if func is None:  # If not running with Werkzeug server
        print("⚠️ Not running with Werkzeug server.", flush=True)
        os._exit(0)  # Forcefully exit the program
    else:
        func()  # Call the shutdown function to stop the server

# Main entry point
if __name__ == "__main__":
    print("🚀 Starting Fluent Edge at http://127.0.0.1:5000/", flush=True)
    try:
        webbrowser.open("http://127.0.0.1:5000/")  # Automatically open the web app in the browser
        app.run(debug=True, use_reloader=False, port=5000)  # Start the Flask app
    except Exception as e:
        print(f"❌ ERROR: {e}", flush=True)
        sys.exit(1)  # Exit the program if an error occurs during startup
