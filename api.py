import os
import lorem
import re
import numpy as np

from flask import Flask, jsonify, abort, send_from_directory
from datetime import datetime


# Root directory for stored text files
ROOT_FILE_DIR = 'static/text_files/'

# Create directory if it does not exist
if not os.path.exists(ROOT_FILE_DIR):
    os.makedirs(ROOT_FILE_DIR)


def create_app(config=None):
# Function to create Flask app

    api = Flask(__name__)

    api.config.update(dict(DEBUG=True))

    @api.route('/api/files/<path:path>', methods=['POST'])
    def create_file(path):
        # Create text file with random contents, in given path

        # Directories not allowed
        if path.endswith('/'):
            # Return 400 BAD REQUEST
            abort(400, 'Path must end with file not directory.')

        # Generate random text
        text = lorem.text()
        file_path = ROOT_FILE_DIR + path
        
        if os.path.isfile(file_path):
            abort(409, 'File already exists.')
        else:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as text_file:
                print(text, file=text_file)
            return f'File created at {file_path}.', 201


    @api.route('/api/files/<path:path>')
    def get_file_content(path):
        # Returns file contents
        file_path = ROOT_FILE_DIR + path
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                text = f.read()
            # create JSON with text body    
            data = {
                "content": text
            }
            return jsonify(data), 200
        else:
            abort(404, 'File not found.')


    @api.route('/api/files/<path:path>', methods=['PUT'])
    def replace_file_content(path):
        # Replace the contents of text file
        text = lorem.text()
        file_path = ROOT_FILE_DIR + path
        if not os.path.isfile(file_path):
            abort(404, 'File does not exist.')
        else:
            with open(file_path, 'w') as text_file:
                print(text, file=text_file)
            return f'File contents at {file_path} changed.', 200


    @api.route('/api/files/<path:path>', methods=['DELETE'])
    def delete_file(path):
        # Deletes resource at given path
        file_path = ROOT_FILE_DIR + path
        if os.path.isfile(file_path):
            os.remove(file_path)
            return f'File contents at {file_path} deleted.', 200
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
            return f'Directory at {file_path} deleted.', 200
        else:
            abort(404, 'File does not exist.')


    @api.route('/api/folder-stats/<path:path>')
    def get_folder_stats(path):
        # Gets stats for a directory
        folder_path = ROOT_FILE_DIR + path

        if os.path.isdir(folder_path):
            file_list = []
            total_size = 0
            # Walk through directories from given path
            for path, _, files in os.walk(folder_path):
                for name in files:
                    file_name = os.path.join(path, name)
                    # Appends filename to list
                    file_list.append(file_name)
                    # Add size (in bytes) to total_size
                    total_size += os.path.getsize(file_name)

            # Use list of file names to get number of chars per file and each word length
            chars_per_file, word_lengths = get_folder_text_nums(file_list)
            number_of_files = len(file_list)

            return generate_stats_json(number_of_files, chars_per_file, word_lengths, total_size), 200
        else:
            abort(404, 'Directory not found.')


    def get_folder_text_nums(file_list):
        # Returns two lists: 
        #   - number of characters in each file
        #   - lengths of each word in each file
        
        chars_per_file = []
        word_lengths = []

        for file in file_list:
            with open(file, 'r') as f:
                text = f.read()
                # Regex to strip non-alphanumerics characters
                alphanumeric_text = re.sub(r'\W+', '', text)
                chars_per_file.append(len(alphanumeric_text))

                for word in text.split():
                    word_lengths.append((len(word)))

        return chars_per_file, word_lengths


    def generate_stats_json(file_count, char_count, word_lengths, size):
        # Creates JSON containing statistics about a directory

        # Calculate average and standard deviation
        average_chars = np.average(char_count)
        char_std = np.std(char_count)
        average_word_len = np.average(word_lengths)
        word_len_std = np.std(word_lengths)

        # Create JSON containing stats info
        stats = {
            'number_of_files': file_count,
            'avg_alphanumeric_chars': average_chars,
            'avg_alphanumeric_chars_std': char_std,
            'avg_word_length': average_word_len,
            'avg_word_length_std': word_len_std,
            'total_bytes': size
        }

        return jsonify(stats)

    return api 


if __name__ == '__main__':
    api = create_app()
    api.run(host="0.0.0.0", debug=True)
