import os
import re

def clean_text(text):
    """
    Cleans the input text by removing newline characters and reducing all instances of multiple
    spaces to a single space.

    Parameters:
    - text (str): The input text to be cleaned.

    Returns:
    - str: The cleaned text with newline characters removed and multiple spaces reduced to a single space.
    """
    # Use regex to replace one or more whitespace characters (including spaces, tabs, and newlines)
    # with a single space, and then strip leading and trailing whitespace from the result.
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text

class UnstructuredDataLoader:
    """
    A class for loading unstructured data from files within a specified directory structure.

    This loader is specifically designed to work within a predefined folder hierarchy, where
    the base directory ('unstructured_data') contains subdirectories corresponding to different
    categories of unstructured data (e.g., 'art', 'history'). Each subdirectory may contain multiple
    text files, from which data can be loaded individually or in bulk.
    """

    def __init__(self):
        """
        Initializes the data loader by setting up the base path to the 'unstructured_data' folder.

        The base path is constructed relative to the location of this script, allowing for flexible
        use across different environments without needing to hard-code the absolute path.
        """
        # Correctly determine the script's directory for consistent relative path resolution.
        self.base_path = os.path.join(os.path.dirname(__file__), "LPS")

    def read_file(self, path):
        """
        Reads and returns the content of a file located at a given path.

        Parameters:
        - path (str): The full path to the file to be read.

        Returns:
        - str: The content of the file.
        """
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def get_data(self, folder_name, file_name=None):
        """
        Fetches and returns the data from files located within a specified subfolder of the 'unstructured_data' directory.

        If a specific file name is provided, only the content of that file is returned. If no file name is provided,
        the function returns the contents of all files within the specified subfolder.

        Parameters:
        - folder_name (str): The name of the subfolder within 'unstructured_data' from which to load files.
        - file_name (str, optional): The name of a specific file to load from the subfolder. If None, all files
          in the subfolder are loaded. Defaults to None.

        Returns:
        - list of dict: A list of dictionaries, each containing the file name ('file_name') and its content ('data').
          If a specific file is not found, an appropriate message is printed.
        """
        folder_path = os.path.join(self.base_path, folder_name)
        data = []

        if file_name:
            # Construct the full path to the specified file and load its content if it exists.
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                data.append({'file_name': file_name, 'data': self.read_file(file_path)})
            else:
                print(f"File {file_name} not found in {folder_name}.")
        else:
            # Load the content of all files in the specified subfolder.
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    data.append({'file_name': filename, 'data': self.read_file(file_path)})

        return data

# Example uses
# loader = UnstructuredDataLoader()
# # Example: Get data from a specific file
# data = loader.get_data(folder_name='Cultural_Festival_of_Lucknow')
# print(data)


# loader = UnstructuredDataLoader()
# # Example: Get data from a specific file
# data = loader.get_data(folder_name='Cultural_Festival_of_Lucknow', file_name= 'General_combined_data.txt')
# print(data)


def limit_to_approx_words(sentence, limit=200, backtrack_limit=100):
    """
    Truncates a sentence to a specified limit of words, attempting to end with a full stop, question mark,
    or exclamation point within a backtrack limit if possible.

    Parameters:
    - sentence (str): The sentence to truncate.
    - limit (int, optional): The maximum number of words desired in the truncated sentence. Defaults to 200.
    - backtrack_limit (int, optional): The maximum number of words to backtrack through to find a suitable
      ending punctuation. Defaults to 100.

    Returns:
    - str: The truncated sentence, ideally ending with a complete sentence.
    """
    words = sentence.split()
    if len(words) <= limit:
        return sentence

    # Join words up to the limit, then strip to remove any leading or trailing whitespace.
    limited_text = " ".join(words[:limit]).strip()
    # Attempt to find a sentence-ending punctuation within the backtrack limit.
    for i in range(limit - 1, max(0, limit - backtrack_limit), -1):
        if words[i][-1] in ".!?":
            # Return the text up to and including the punctuation.
            return " ".join(words[:i + 1])

    # If no suitable punctuation is found, return the text up to the word limit.
    return limited_text


def split_into_segments(sentence, limit=200, backtrack_limit=100):
    """
    Splits a long sentence into multiple smaller segments based on specified limits, ensuring
    segments end with complete sentences where possible.

    Parameters:
    - sentence (str): The long sentence to split.
    - limit (int): The approximate limit for the number of words in each segment.
    - backtrack_limit (int): The maximum number of words to backtrack in an effort to end a segment with complete sentences.

    Returns:
    - list: A list of sentence segments.
    """
    segments = []
    # Clean the sentence to remove excessive whitespace and newline characters.
    remaining_sentence = clean_text(sentence)

    while remaining_sentence:
        # Generate a segment that respects the limit and attempts to end with complete sentences.
        segment = limit_to_approx_words(remaining_sentence, limit, backtrack_limit)
        segments.append(segment)
        # Update the remaining sentence by removing the processed segment and leading spaces.
        remaining_sentence = remaining_sentence[len(segment):].lstrip()

        # If there's no remaining sentence to process, exit the loop.
        if not remaining_sentence:
            break
    return segments


