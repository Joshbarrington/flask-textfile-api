"""
Unit test using pytest-flask see: https://pypi.org/project/pytest-flask/
Example usage at command line: $ py.test

Requires initial file structure in project directory:
- static/
    - text_files/
        - test_folder/
            - test_file (contents: 'test test')
        - test_file1 (contents 'test test test')
        - test_file2
        - test_file3

Passes all 5 test cases.
"""


import pytest


class TestApp:

    def test_create_file(self, client):
        res = client.post('/api/files/test_file')
        assert res.status_code == 201

    def test_get_file_content(self, client):
        res = client.get('/api/files/test_file1')
        assert res.status_code == 200
        assert res.json == {'content': 'test test test'}
    
    def test_replace_file_content(self, client):
        res = client.put('/api/files/test_file2')
        assert res.status_code == 200

    def test_delete_file(self, client):
        res = client.delete('/api/files/test_file3')
        assert res.status_code == 200
    
    def test_get_folder_stats(self, client):
        res = client.get('/api/folder-stats/test_folder')
        assert res.status_code == 200
        assert res.json == {
            'number_of_files': 1,
            'avg_alphanumeric_chars': 8,
            'avg_alphanumeric_chars_std': 0,
            'avg_word_length': 4,
            'avg_word_length_std': 0,
            'total_bytes': 9
            }