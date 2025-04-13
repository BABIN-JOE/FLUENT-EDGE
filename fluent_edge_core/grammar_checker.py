import language_tool_python
import logging
import re

# Initialize logging for better debugging and tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GrammarChecker:
    def __init__(self, language="en-US"):
        """
        Initializes the GrammarChecker class and loads LanguageTool for a specific language.

        :param language: The language to be used for grammar checking (default is "en-US").
        """
        try:
            # Load LanguageTool for the specified language
            self.tool = language_tool_python.LanguageTool(language)
            logger.info(f"✅ Grammar checker initialized successfully for {language}.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize grammar checker: {e}")
            self.tool = None  # Set tool to None if initialization fails

    def check_grammar(self, text):
        """
        Checks grammar and spelling mistakes in the provided text.

        :param text: The input text to check for errors.
        :return: A list of error details, including suggestions and rule ID.
        """
        if not self.tool:
            logger.error("❌ Grammar checker is not initialized.")  # Error if tool is not initialized
            return []

        text = text.strip()
        if not text:
            logger.warning("⚠️ Empty text provided. Skipping grammar check.")  # Warn if text is empty
            return []

        try:
            # Split text into sentences for better analysis
            sentences = re.split(r"(?<=[.!?])\s+", text)

            # Capitalize the first letter of each sentence
            sentences = [s.strip().capitalize() if s else "" for s in sentences]

            errors = []
            logger.info(f"📝 Checking grammar for text:\n{text}")

            # Check each sentence for grammar/spelling errors
            for sentence in sentences:
                matches = self.tool.check(sentence)
                for match in matches:
                    # Collect error details for each issue found
                    error_details = {
                        "sentence": sentence,
                        "message": match.message,
                        "suggestions": match.replacements if match.replacements else ["No suggestion"],
                        "offset": match.offset,
                        "length": match.errorLength,
                        "rule_id": match.ruleId
                    }
                    errors.append(error_details)  # Add the error details to the list
                    logger.info(f"🚨 Issue: {match.message} | Suggestion: {match.replacements} | Rule: {match.ruleId}")

            # Log the total number of errors found
            if errors:
                logger.info(f"🔍 Found {len(errors)} grammar/spelling errors.")
            else:
                logger.info("✅ No grammar errors found.")

            return errors  # Return the list of error details

        except Exception as e:
            logger.error(f"❌ Grammar check failed: {e}")
            return []  # Return an empty list if an error occurs during grammar check

# Initialize the grammar checker instance for English (US)
grammar_checker = GrammarChecker(language="en-US")

# External function for checking grammar
def check_grammar(text):
    """
    External function to check grammar of text using the GrammarChecker instance.

    :param text: The input text to check for errors.
    :return: List of errors detected by the grammar checker.
    """
    return grammar_checker.check_grammar(text)

def capitalize_sentences(text):
    """
    Capitalizes the first letter of each sentence in the provided text.

    :param text: The input text to capitalize sentences.
    :return: Text with capitalized sentences.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    capitalized = [s.strip().capitalize() if s else '' for s in sentences]
    return ' '.join(capitalized)  # Return the text with capitalized sentences


# Standalone test script to check grammar for a sample text
if __name__ == "__main__":
    test_text = "she go to school yesterday. he have a apple."  # Example text with errors
    errors = check_grammar(test_text)  # Check grammar for the sample text

    if errors:
        # Display errors if found
        print("\n🔍 Grammar Errors Found:\n")
        for error in errors:
            print(f"❌ Sentence: {error['sentence']}")
            print(f"   ↪ Error: {error['message']}")
            print(f"   🔹 Suggestions: {', '.join(error['suggestions'])}")
            print(f"   🔍 Offset: {error['offset']}, Length: {error['length']}, Rule: {error['rule_id']}\n")
    else:
        # If no errors, print success message
        print("✅ No grammar errors found.")
