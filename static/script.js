document.addEventListener("DOMContentLoaded", function () {
    // Elements from the DOM
    const toggleButton = document.getElementById("toggle-btn");
    const exitButton = document.getElementById("exit-btn");
    const liveTranscription = document.getElementById("live-transcription");
    const finalTranscription = document.getElementById("final-transcription");
    const grammarErrors = document.getElementById("grammar-errors");
    const accuracyScore = document.getElementById("accuracy-score");
    const recDot = document.getElementById("rec-dot");

    let eventSource; // Variable for EventSource instance
    let isListening = false; // To track whether the system is listening
    let hasReceivedSpeech = false; // To track if any speech was received
    let typingTimeout; // For controlling the typing animation delay

    // Helper function to send requests to the server
    function sendRequest(endpoint) {
        return fetch(endpoint).then(res => {
            if (!res.ok) throw new Error("Request failed");
            return res.json();
        });
    }

    // Function to toggle the listening state
    function toggleListening() {
        if (!isListening) {
            // Start listening
            isListening = true;
            hasReceivedSpeech = false; // Reset speech received flag
            toggleButton.textContent = "Stop";
            toggleButton.classList.remove("bg-green-500", "hover:bg-green-600");
            toggleButton.classList.add("bg-red-500", "hover:bg-red-600");
            recDot.classList.remove("hidden");

            // Clear old grammar and accuracy data
            grammarErrors.innerHTML = `<tr><td colspan='3' class="fade-text">Waiting for the speech to end...</td></tr>`;
            accuracyScore.innerHTML = `<span class="fade-text">Waiting for the speech to end...</span>`;
            document.getElementById("accuracy-feedback").innerHTML = "";

            liveTranscription.innerHTML = `<span class="fade-text">Listening...</span>`;
            finalTranscription.innerHTML = `<span class="fade-text">Waiting for the speech to end...</span>`;

            sendRequest("/start"); // Notify the server to start the recording
            initializeEventSource(); // Start listening for transcription data
        } else {
            // Stop listening
            isListening = false;
            toggleButton.textContent = "Start";
            toggleButton.classList.remove("bg-red-500", "hover:bg-red-600");
            toggleButton.classList.add("bg-green-500", "hover:bg-green-600");
            recDot.classList.add("hidden");

            liveTranscription.textContent = "Current transcription has ended. Press start to start a new Transcription.";
            grammarErrors.innerHTML = `<tr><td colspan='3' class="fade-text">Analyzing...</td></tr>`;
            accuracyScore.innerHTML = `<span class="fade-text">Analyzing...</span>`;
            sendRequest("/stop"); // Notify the server to stop the recording
        }
    }

    // Function to initialize the EventSource for live transcription data
    function initializeEventSource() {
        if (eventSource) eventSource.close(); // Close previous EventSource if any
        eventSource = new EventSource("/transcription"); // Create new EventSource

        // Handle incoming messages from the server
        eventSource.onmessage = function (event) {
            const message = event.data;

            if (message.startsWith("LIVE::")) {
                const text = message.replace("LIVE::", "").trim();
                hasReceivedSpeech = true;
                typeText(liveTranscription, text || "Listening...");
            } else if (message.startsWith("FULL_TRANSCRIPTION::")) {
                const text = message.replace("FULL_TRANSCRIPTION::", "").trim();
                finalTranscription.textContent = text || "No speech detected";
            } else if (message.startsWith("GRAMMAR_ERRORS::")) {
                const errors = JSON.parse(message.replace("GRAMMAR_ERRORS::", ""));
                updateGrammarErrorsTable(errors); // Update the grammar errors table
            } else if (message.startsWith("ACCURACY::")) {
                const scoreStr = message.replace("ACCURACY::", "").trim();
                const feedback = document.getElementById("accuracy-feedback");

                // Handle the accuracy feedback display
                if (!hasReceivedSpeech) {
                    accuracyScore.textContent = "No speech detected";
                    accuracyScore.className = "text-3xl font-bold text-gray-400";
                    feedback.textContent = "";
                } else {
                    accuracyScore.textContent = scoreStr;
                    const scoreNum = parseFloat(scoreStr.replace("%", ""));

                    // Set class and feedback based on the score
                    accuracyScore.className = "text-3xl font-bold";
                    feedback.className = "text-lg mt-2";

                    if (scoreNum >= 75) {
                        accuracyScore.classList.add("text-green-500");
                        feedback.classList.add("text-green-400");
                        feedback.textContent = "✅ Great job! Your accuracy is excellent.";
                    } else if (scoreNum >= 50) {
                        accuracyScore.classList.add("text-yellow-400");
                        feedback.classList.add("text-yellow-300");
                        feedback.textContent = "⚠️ Not bad, but there’s room for improvement.";
                    } else {
                        accuracyScore.classList.add("text-red-500");
                        feedback.classList.add("text-red-400");
                        feedback.textContent = "❌ Needs improvement. Keep practicing!";
                    }
                }

                if (eventSource) eventSource.close(); // Close the EventSource connection after receiving all necessary data
            }
        };

        eventSource.onerror = function (event) {
            console.error("EventSource error:", event);
        };
    }

    // Function to type the text with animation (simulating typing effect)
    function typeText(element, text, callback) {
        if (typingTimeout) clearTimeout(typingTimeout);

        element.textContent = "";
        let index = 0;

        function typeNextChar() {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                typingTimeout = setTimeout(typeNextChar, 25); // Speed of typing (ms per character)
            } else if (callback) {
                callback(); // Call the callback once typing is complete
            }
        }

        typeNextChar();
    }

    // Function to update the grammar errors table with the received errors
    function updateGrammarErrorsTable(errors) {
        grammarErrors.innerHTML = "";
        if (!Array.isArray(errors) || errors.length === 0) {
            if (!hasReceivedSpeech) {
                grammarErrors.innerHTML = "<tr><td colspan='3'>No speech is available to undergo Grammar error identification</td></tr>";
            } else {
                grammarErrors.innerHTML = "<tr><td colspan='3'>🎉 Congratulations! No grammar errors found.</td></tr>";
            }
            return;
        }

        errors.forEach(error => {
            const row = document.createElement("tr");
            row.className = "border-b border-gray-700";
            row.innerHTML = ` 
                <td class="p-3 text-left border border-gray-600">${error.sentence || "N/A"}</td>
                <td class="p-3 border border-gray-600">${error.message || error.error || "N/A"}</td>
                <td class="p-3 border border-gray-600">${Array.isArray(error.suggestions) ? error.suggestions.join(", ") : "N/A"}</td>
            `;
            grammarErrors.appendChild(row);
        });
    }

    // Event listener for the toggle button to start/stop transcription
    toggleButton.addEventListener("click", toggleListening);

    // Event listener for the exit button to close the application
    exitButton.addEventListener("click", () => {
        if (confirm("Are you sure you want to exit?")) {
            sendRequest("/exit").then(() => {
                if (eventSource) eventSource.close();
                alert("Server has shut down. Please close this tab manually.");
            });
        }
    });
});
