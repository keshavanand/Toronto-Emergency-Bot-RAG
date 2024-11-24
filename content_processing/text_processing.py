
from content_processing.processPdf import get_chunks
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize
from functools import reduce
from nltk.corpus import stopwords
import nltk

print("\n............................Downloading NLTK Data............................\n")
# Download all NLTK data (useful if you are missing required datasets like stopwords or tokenizers)
nltk.download('all')

def process_text(chunks: dict) -> dict:
    """
    Processes the text chunks to remove stopwords and apply stemming.

    Args:
        chunks (dict): A dictionary where keys are section titles and values are text content.

    Returns:
        dict: The updated dictionary with processed text for each key.
    """
    # Load the list of stopwords for English
    stop_words = set(stopwords.words('english'))

    # Initialize the Porter Stemmer for word stemming
    ps = PorterStemmer()

    print("\n............................Applying Processing............................\n")
    
    # Iterate over each key-value pair in the chunks dictionary
    for key in chunks:
        # Combine all lines of the text for the current key into a single sentence
        sentence = " ".join(str(chunks[key]).splitlines())
        
        # Tokenize the sentence into words
        words = word_tokenize(sentence, language="english")
        
        # Remove stopwords from the tokenized words
        wordsFiltered = [w for w in words if w not in stop_words]

        # Stem each word and reconstruct the sentence using reduce
        stemmed_sentence = reduce(lambda x, y: x + " " + ps.stem(y), wordsFiltered, "")
        
        # Update the dictionary with the processed sentence
        chunks[key] = stemmed_sentence
        
    print("\n............................Done processing chunks............................\n")
    # Return the processed chunks
    return chunks

