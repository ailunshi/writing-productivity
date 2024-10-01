import os
import xml.etree.ElementTree as ET
import pypandoc
import re

def count_words_in_rtf(file_path):
    # Convert RTF content to plain text
    try:
        text = pypandoc.convert_file(file_path, 'plain')

        #Splits on space. Splits on em dash after a word UNLESS
        #1) it is followed by quotes
        #2) it is at the end of a sentence
        word_count = len(re.split(r'\s+|(?<=\w)\u2014(?![“”\'\".]|$)', text))

        return word_count
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def parse_scrivx_file(scrivx_path):
    # Parse the .scrivx file to find included documents
    tree = ET.parse(scrivx_path)
    root = tree.getroot()

    included_docs = set()

    # Iterate over all the documents, find Manuscript portion, pull all associated files
    for binder_item in root.iter('BinderItem'):
        section = binder_item[0]
        if section.text == "Manuscript":
            for child in binder_item.iter('BinderItem'):
                doc_id = child.attrib.get('UUID')
                if doc_id:
                    included_docs.add(doc_id)
            break
        else:
            continue

    return included_docs

def get_total_word_count(root_folder, scrivx_path):
    total_word_count = 0

    # Parse the .scrivx file to find included documents
    included_docs = parse_scrivx_file(scrivx_path)

    # Walk through the folder and all subfolders
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file == "content.rtf":
                # Get the document ID from the folder name
                doc_id = os.path.basename(root)
                
                # Check if this document ID is part of the included manuscript
                if doc_id in included_docs:
                    file_path = os.path.join(root, file)
                    word_count = count_words_in_rtf(file_path)
                    #print(f"{file_path} contains {word_count} words.")
                    total_word_count += word_count

    return total_word_count

# Define paths
root_folder = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
scrivx_path = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"

# Calculate total word count
total_words = get_total_word_count(root_folder, scrivx_path)
print(f"Total word count for included manuscript documents: {total_words}")
