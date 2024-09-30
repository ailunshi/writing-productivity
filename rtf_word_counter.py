import os
import pypandoc

def count_words_in_rtf(file_path):
    # Convert RTF content to plain text
    try:
        text = pypandoc.convert_file(file_path, 'plain')
        # Split the text by spaces to count the words
        word_count = len(text.split())
        return word_count
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def get_total_word_count(root_folder):
    total_word_count = 0

    # Walk through the folder and all subfolders
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # Look for content.rtf files
            if file == "content.rtf":
                file_path = os.path.join(root, file)
                word_count = count_words_in_rtf(file_path)
                print(f"{file_path} contains {word_count} words.")
                total_word_count += word_count

    return total_word_count

# Define the root folder you want to start from
root_folder = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"

# Calculate total word count
total_words = get_total_word_count(root_folder)
print(f"Total word count across all content.rtf files: {total_words}")