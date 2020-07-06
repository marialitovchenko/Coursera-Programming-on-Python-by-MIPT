"""
Write class File with re-implemented magic methods:

- for the creation of instance of the class a full path to the file is given
- if file doesn't exist, an empty file should be created
- a string representation of the class should be a full path to the file

- reading from the file (method read), which should return file content
- writing into the file (method write). A new file content is an argument of
  the function
- addition of the objects type File, and the result should be the other object
  of class File. A new file and File object should be created and it should
  contain strings from both files. A new file should be created in the
  directory got by function tempfile.gettempdir. Use os.path.join to get full
  path
"""
import os
import tempfile


class File:
    def __new__(cls, file_path):
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as f:
                f.write('')
        instance = super().__new__(cls)
        return instance

    def __init__(self, file_path):
        self.file_path = file_path

    def __str__(self):
        return self.file_path

    def __add__(self, other):
        with open(self.file_path) as f:
            file_one_content = f.read()
        with open(other.file_path) as f:
            file_two_content = f.read()
        combined_content = file_one_content + file_two_content

        result = File(tempfile.mkstemp()[1])
        result.write(combined_content)
        return result

    def __getitem__(self, index):
        with open(self.file_path) as f:
            file_content = f.readlines()
        return file_content[index]

    def read(self):
        with open(self.file_path) as f:
            file_content = f.read()
        return file_content

    def write(self, one_string):
        with open(self.file_path, 'w') as f:
            f.write(one_string)