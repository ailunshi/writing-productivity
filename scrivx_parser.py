import os
import xml.etree.ElementTree as ET
import pypandoc
import re
import argparse
import time
from multiprocessing import Pool

class ScrivxParser:
    def __init__(self, root_folder, scrivx_path):
        self.included_docs = set()
        self.file_paths = []
        self.root_folder = root_folder
        self.scrivx_path = scrivx_path

    def parse_scrivx_file(self):
        # Parse the .scrivx file to find included documents
        tree = ET.parse(self.scrivx_path)
        root = tree.getroot()

        # Iterate over all the documents, find Manuscript portion, pull all associated files
        for binder_item in root.iter('BinderItem'):
            section = binder_item[0]
            if section.text == "Manuscript":
                for child in binder_item.iter('BinderItem'):
                    doc_id = child.attrib.get('UUID')
                    if doc_id:
                        self.included_docs.add(doc_id)
                break
            else:
                continue

    def get_files(self):
        # Walk through the folder and all subfolders
        for root, dirs, files in os.walk(self.root_folder):
            for file in files:
                if file == "content.rtf":
                    # Get the document ID from the folder name
                    doc_id = os.path.basename(root)
                    
                    # Check if this document ID is part of the included manuscript
                    if doc_id in self.included_docs:
                        self.file_paths.append(os.path.join(root, file))

    def count_words(self, file_path):
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

    def run(self):
        # Parses the project file using parallelization

        if not self.file_paths:
            self.get_files()
        
        print("There are ", len(self.file_paths), " files in the project.")

        with Pool() as pool:            
            word_counts = pool.map(self.count_words, self.file_paths)

        total_word_count = sum(word_counts)
        print(total_word_count)
        return total_word_count