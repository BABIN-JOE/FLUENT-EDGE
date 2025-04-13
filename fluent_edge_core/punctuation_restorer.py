import re

class PunctuationRestorer:
    def __init__(self):
        """
        Initializes the PunctuationRestorer class, defining common sentence starters,
        question words, and non-ending words that help in restoring punctuation.
        """
        # Define common sentence starters
        self.sentence_starters = [
            "i", "we", "you", "they", "he", "she", "it", "this", "that", "these", "those", 
            "the", "a", "an", "my", "your", "his", "her", "their", "our", "when", "where",
            "why", "how", "what", "who", "which", "if", "because", "since", "while", "although",
            "however", "therefore", "thus", "hence", "so", "but", "and", "or", "nor", "yet"
        ]
        
        self.question_words = ["what", "when", "where", "which", "who", "whom", "whose", "why", "how"]
        
        # Words that usually don't end sentences
        self.non_ending_words = ["the", "a", "an", "of", "in", "on", "at", "to", "for", "with", "by", "as", "and", "or", "but"]
        
        # Log initialization
        print("✅ Punctuation restorer initialized.", flush=True)

    def restore_punctuation(self, text):
        """
        Restores punctuation to a text based on linguistic rules and patterns.

        :param text: The input text that requires punctuation restoration.
        :return: The text with restored punctuation (e.g., periods, commas, question marks).
        """
        if not text:
            return ""  # If the text is empty, return an empty string
        
        # Clean up excess spaces and strip leading/trailing whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split text into individual words for processing
        words = text.split()
        sentences = []
        current_sentence = []
        
        # Process each word in the text
        for i, word in enumerate(words):
            current_sentence.append(word)
            
            # Skip if we're at the last word or the next word is only 1-2 letters
            if i == len(words) - 1 or len(words[i+1]) <= 2:
                continue
            
            next_word = words[i+1].lower()
            
            # Flag to determine if a sentence should end here
            end_sentence = False
            
            # Check if the current word ends with a question mark
            if word.endswith("?"):
                end_sentence = True
            # Check for question sentence patterns
            elif i >= 2 and words[i-2].lower() in self.question_words and len(current_sentence) > 3:
                end_sentence = True
                current_sentence[-1] = current_sentence[-1] + "?"  # Add a question mark to the sentence
            # Check for statement sentence patterns
            elif (next_word in self.sentence_starters and 
                  word.lower() not in self.non_ending_words and
                  len(current_sentence) >= 4):
                end_sentence = True
                # Don't add period if the word already has punctuation
                if not word[-1] in ".!?":
                    current_sentence[-1] = current_sentence[-1] + "."  # Add a period to end the sentence
            
            # Add commas for natural pauses between conjunctions
            elif (i < len(words) - 2 and 
                  next_word in ["and", "but", "or", "nor", "yet", "so"] and
                  len(current_sentence) > 3):
                if not word[-1] in ",.!?":
                    current_sentence[-1] = current_sentence[-1] + ","  # Add a comma for a pause
            
            # Finalize the sentence
            if end_sentence:
                sentences.append(" ".join(current_sentence))  # Add the current sentence to the list
                current_sentence = []  # Start a new sentence
        
        # If there are any words left in the current sentence, finalize it
        if current_sentence:
            last_text = " ".join(current_sentence)
            if not last_text[-1] in ".!?":
                last_text += "."  # Add a period to the last sentence if needed
            sentences.append(last_text)
        
        # Capitalize the first letter of each sentence
        sentences = [s[0].upper() + s[1:] if s else "" for s in sentences]
        
        # Join all sentences into a single text with proper punctuation
        result = " ".join(sentences)
        
        return result

    def process_streaming_text(self, text):
        """
        Processes streaming text by capitalizing the first letter and adding basic punctuation.

        :param text: The incoming text stream that needs minimal processing.
        :return: The capitalized text with basic punctuation.
        """
        text = text.strip()  # Remove leading and trailing spaces
        if not text:
            return ""  # Return empty string if there's no text
        
        # Capitalize the first letter of the text
        text = text[0].upper() + text[1:]
        
        return text
