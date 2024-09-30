import os
import xml.etree.ElementTree as ET
import pypandoc

#need to pull and count all the docs under Manuscript --> within .scrivx

def count_words_in_rtf(file_path):
    # Convert RTF content to plain text
    try:
        text = pypandoc.convert_file(file_path, 'plain')
        word_count = len(text.split())
        return word_count
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def parse_scrivx_file(scrivx_path):
    # Parse the .scrivx file to find included documents
    tree = ET.parse(scrivx_path)
    root = tree.getroot()

    included_docs = set()

    # Iterate over all the documents and check if they are in the manuscript
    for binder_item in root.iter('BinderItem'):
        if 'Type' in binder_item.attrib and binder_item.attrib['Type'] == 'Draft':
            # Document is part of the manuscript
            for child in binder_item.iter('BinderItem'):
                doc_id = child.attrib.get('ID')
                if doc_id:
                    included_docs.add(doc_id)

    return included_docs

def get_total_word_count(root_folder, scrivx_path):
    total_word_count = 0

    # Parse the .scrivx file to find included documents
    included_docs = parse_scrivx_file(scrivx_path)

    # Walk through the folder and all subfolders
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == "content.rtf":
                # Get the document ID from the folder name
                doc_id = os.path.basename(foldername)
                
                # Check if this document ID is part of the included manuscript
                if doc_id in included_docs:
                    file_path = os.path.join(foldername, filename)
                    word_count = count_words_in_rtf(file_path)
                    print(f"{file_path} contains {word_count} words.")
                    total_word_count += word_count

    return total_word_count

# Define paths
root_folder = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Files/Data"
scrivx_path = "/Users/balloon/Bel e Kyre/Bel e Kyre.scriv/Bel e Kyre.scrivx"

# Calculate total word count
total_words = get_total_word_count(root_folder, scrivx_path)
print(f"Total word count for included manuscript documents: {total_words}")
