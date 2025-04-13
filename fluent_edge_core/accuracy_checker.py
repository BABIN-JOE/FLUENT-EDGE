def calculate_accuracy(text, corrections):
    """
    Calculates the accuracy of the transcribed speech based on the number of detected grammar errors.

    :param text: The full transcribed text.
    :param corrections: A list of detected grammar errors.
    :return: Accuracy percentage (float).
    """
    
    if not text.strip():
        return 0  # No text means 0% accuracy

    if not isinstance(corrections, list):
        return 0  # Invalid corrections format, return 0% accuracy

    total_words = len(text.split())  # Count the total number of words in the transcription
    error_count = len(corrections)  # Count the number of grammar errors

    # Calculate accuracy by subtracting the percentage of errors from 100% and ensure it's not negative
    accuracy = max(0, 100 - (error_count / total_words * 100))
    return round(accuracy, 2)  # Return the accuracy as a rounded percentage
