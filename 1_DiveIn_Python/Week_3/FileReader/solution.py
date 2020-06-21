"""
Write python module solution.py containing class FileReader. The constructor
should accept 1 parameter: file to the path. There should be methods read,
which would return a string with the line from the file.

Import of this file like module shouldn't call errors.

Read method should handle FileNotFoundError
"""


class FileReader:
    """Class for reading from files"""

    def __init__(self, file_path):
        self._file_path = file_path

    def read(self):
        try:
            with open(self._file_path) as f:
                result = f.read()
        except FileNotFoundError:
            result = ''

        return result


if __name__ == "__main__":
    pass
