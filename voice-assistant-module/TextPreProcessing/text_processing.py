import string
from spellchecker import SpellChecker  # Install with: pip install pyspellchecker

# Define your custom list of stopwords
stop_words = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
    "you", "your", "yours", "yourself", "yourselves", "he", "him", 
    "his", "himself", "she", "her", "hers", "herself", "it", "its", 
    "itself", "they", "them", "their", "theirs", "themselves", "what", 
    "which", "who", "whom", "this", "that", "these", "those", "am", 
    "is", "are", "was", "were", "be", "been", "being", "have", "has", 
    "had", "having", "do", "does", "did", "doing", "a", "an", "the", 
    "and", "but", "if", "or", "because", "as", "until", "while", 
    "of", "at", "by", "for", "with", "about", "against", "between", 
    "into", "through", "during", "before", "after", "above", "below", 
    "to", "from", "out", "over","under", "again", "further", "then", "once", "here", "there", 
    "when", "where", "why", "how", "all", "any", "both", "each", 
    "few", "more", "most", "other", "some", "such", "no", "nor", 
    "not", "only", "own", "same", "so", "than", "too", "very", 
    "s", "t", "can", "will", "just", "don", "should", "now","the","please"
}

# Initialize the spell checker
spell = SpellChecker()

def text_preprocessor(text: str):
    # Step 1: Remove punctuation and convert to lowercase
    translator = str.maketrans('', '', string.punctuation)
    text = text.lower()
    text = text.translate(translator)

    # Step 2: Split text into words
    words = text.split()

    # Step 3: Correct misspelled words
    corrected_words = []
    for word in words:
        # Correct the word if it's misspelled
        corrected_word = spell.correction(word)
        # Handle cases where correction returns None
        if corrected_word is None:
            corrected_word = word  # Use the original word if no correction is found
        corrected_words.append(corrected_word)

    # Step 4: Remove stopwords
    filtered_words = [word for word in corrected_words if word.lower() not in stop_words]

    # Step 5: Join the words back into a single string
    preprocessed_text = " ".join(filtered_words)
    return preprocessed_text


if __name__ == "__main__":
    text = ' please Turn off the light of liing Room light.'
    print(text_preprocessor(text=text))

    text = 'adjust the living room heater at 23°'
    print(text_preprocessor(text=text))