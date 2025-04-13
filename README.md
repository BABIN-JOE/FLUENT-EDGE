
# Fluent Edge

Fluent Edge is a Flask-based web application that records live audio, transcribes it using Vosk, restores punctuation, checks grammar using LanguageTool, and calculates accuracy. The transcription and analysis results are displayed in real-time on the frontend.

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Folder and File Descriptions](#folder-and-file-descriptions)

## Installation
To get started with Fluent Edge, follow these steps:

1. **Clone this repository to your local machine:**

    ```bash
    git clone <repository_url>
    cd FLUENT-EDGE
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

    ```bash
    venv\Scripts\activate
    ```

    - On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Download the required Vosk models for transcription:**

    You need to download the following Vosk models for transcription:

    - [Vosk Model (US English)](https://alphacephei.com/vosk/models)
    - [Vosk Model (Indian English)](https://alphacephei.com/vosk/models)

6. **Place these models in the following directories:**

    - Download and extract the models from the above links.
    - Place the extracted folders in the respective directories:
    
    ```
    model/US English/
    model/Indian English/
    ```

## Project Structure
Here is a breakdown of the directory structure:

```
FLUENT-EDGE/
│
├── __pycache__/                      # Compiled Python files (auto-generated)
│
├── fluent_edge_core/                 # Core logic of the application
│   ├── __init__.py                   # Initialization for the core module
│   ├── accuracy_checker.py           # Logic for calculating accuracy of transcription
│   ├── audio_handler.py              # Handles audio recording and processing
│   ├── grammar_checker.py            # Grammar checking functionality using LanguageTool
│   ├── punctuation_restorer.py       # Restores punctuation in transcribed text
│   ├── speech_recognizer.py          # Handles speech recognition using Vosk
│   └── startup_checker.py            # Verifies dependencies during startup
│
├── model/                            # Vosk speech recognition models
│   ├── Indian English/               # Downloaded model for Indian English
│   ├── US English/                   # Downloaded model for US English
│   └── model_description.txt         # Description of the models
│
├── static/                           # Static files for frontend (JS, CSS)
│   ├── script.js                     # JavaScript file for frontend behavior
│   └── style.css                     # Stylesheet for the frontend
│
├── templates/                        # HTML templates for the frontend
│   └── index.html                    # Main HTML template for the app
│
├── Testing/                          # Unit tests for the application
│   ├── accuracy_test.py              # Tests for the accuracy calculation
│   ├── app_test.py                   # Tests for the Flask app's functionality
│   ├── audio_test.py                 # Tests for audio handling (e.g., Vosk integration)
│   ├── error_logging_test.py         # Tests for logging errors and warnings
│   ├── grammar_test.py               # Tests for grammar checking
│   ├── integration_test.py           # Tests for the integration of components
│   ├── mic_test.py                   # Tests for microphone input handling
│   ├── punctuation_test.py           # Tests for punctuation restoration
│   └── vosk_test.py                  # Tests for the Vosk speech recognition models
│
├── venv/                             # Virtual environment
├── .gitattributes                    # Git configuration
├── .gitignore                        # Git ignore file
├── app.py                            # Main Flask app entry point
├── requirements.txt                  # List of project dependencies
└── README.md                         # Project documentation (this file)
```

## Dependencies
The project has the following dependencies:

- **Flask**: A web framework used for the frontend and backend integration.
- **language-tool-python**: A library for grammar checking using LanguageTool.
- **numpy**: A numerical computation library used in audio processing.
- **sounddevice**: A library used for audio recording.
- **vosk**: A speech recognition toolkit for transcribing audio.
- **pytest**: A testing framework to run unit tests.

These dependencies are listed in the `requirements.txt` file, and can be installed with:

```bash
pip install -r requirements.txt
```

## Usage
### Starting the Flask Application:
To start the Flask web server, run the following command:

```bash
python app.py
```

By default, the server will run on `http://127.0.0.1:5000/`.

### Recording Audio:
Once the app is running, click the "Start" button to begin recording audio. The app will transcribe the speech and display the results (including punctuation restoration and grammar check).

### Transcription and Analysis:
After speech is recorded, the transcription, grammar errors, and punctuation-restored text will be displayed in real-time.

### Accuracy Calculation:
The app calculates the accuracy of the transcription by comparing the detected grammar errors with the total number of words in the transcription.

## Running the Application
1. Navigate to the project directory:

    ```bash
    cd FLUENT-EDGE
    ```

2. Start the Flask application:

    ```bash
    python app.py
    ```

3. Open a web browser and go to `http://127.0.0.1:5000/` to interact with the app.

## Testing
To run unit tests for the application, use the `pytest` framework. This will run all the tests in the `Testing/` folder.

```bash
pytest
```

You can run specific tests as well, for example:

```bash
pytest Testing/accuracy_test.py
```

### Available Test Files:
- **accuracy_test.py**: Tests the accuracy calculation logic.
- **app_test.py**: Tests the Flask app's routes and functionality.
- **audio_test.py**: Tests the audio handling functionality (e.g., recording and Vosk integration).
- **error_logging_test.py**: Tests the logging functionality during errors.
- **grammar_test.py**: Tests the grammar checker functionality.
- **integration_test.py**: Tests the integration of all components.
- **mic_test.py**: Tests the microphone input handling.
- **punctuation_test.py**: Tests punctuation restoration.
- **vosk_test.py**: Tests Vosk speech recognition models.

## Folder and File Descriptions

### fluent_edge_core/
Contains the core logic of the application:
- **accuracy_checker.py**: Contains the logic for calculating transcription accuracy.
- **audio_handler.py**: Handles audio recording and processing.
- **grammar_checker.py**: Integrates with LanguageTool to check grammar.
- **punctuation_restorer.py**: Restores punctuation in transcribed text.
- **speech_recognizer.py**: Handles the Vosk speech recognition model.
- **startup_checker.py**: Checks if all necessary dependencies are available during startup.

### model/
Contains the Vosk models for different languages. Make sure to download and place the models in the correct directories.

### static/
Contains the JavaScript and CSS files used by the frontend.

### templates/
Contains the `index.html` file, which is the main template for the web interface.

### Testing/
Contains unit tests for different components of the project to ensure functionality.

### app.py
The entry point for the Flask web application. It runs the Flask server and integrates with the backend logic.

### requirements.txt
Contains the list of dependencies for the project. Install these dependencies by running `pip install -r requirements.txt`.

### .gitattributes
Git configuration file that specifies how Git handles certain files in the repository.

### .gitignore
Specifies which files and directories Git should ignore. Common entries include `__pycache__/` and `venv/`.
