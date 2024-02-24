function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    // Set the voice directly
    utterance.voiceURI = 'Google US English'; // Voice URI for Google US English
    utterance.lang = 'en-US'; // Language
    utterance.name = 'Google US English'; // Name
    speechSynthesis.speak(utterance);
}

const capturedEntriesElement = document.getElementById('capturedEntries');

                
// Function to handle key press events
function handleKeyPress(event) {
    // Get the key that was pressed
    const keyPressed = event.key;
    console.log("Key -> "+keyPressed)
    
    // If the ESC key is pressed, clear the captured entries
    if (keyPressed === '0') {
        speak("Do you want to send Email? Press ENTER to confirm.")
    }
    else if(keyPressed == 'Enter'){
        speak("What is the Subject?");
        startListening("sub");
    }
    else if(keyPressed == '1'){
        stopListening();
    }
    }

    // Add event listener for keydown event
    document.addEventListener('keydown', handleKeyPress);


// Speech to Text Code

function startListening(inp) {
    alert("Lisiting..")
    recognition = new webkitSpeechRecognition(); // Chrome requires 'webkit' prefix
    recognition.lang = 'en-US'; // Language for recognition
    recognition.onstart = function() {
    
    };
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        if(inp == 'sub'){
            document.getElementById('sub').value = transcript;
            startListening(inp)
        }
        else if(inp == 'msg'){
            document.getElementById('msg').value = transcript;
            startListening(inp) 
        }
    };
    recognition.onerror = function(event) {
        output.textContent = 'Error occurred: ' + event.error;
        stopListening(inp);
    };
    recognition.onend = function() {
    };
    recognition.start();
}

function stopListening(inp) {
    if (recognition) {
        recognition.stop();
        console.log("sub "+inp)
        if(inp == 'sub'){
            // speak("Ok what is the Message?");
            startListening("msg");
        }
        else if(inp == 'msg'){
            speak("Ok great sending email");
            document.getElementById('frm').submit()
        }
    }
}