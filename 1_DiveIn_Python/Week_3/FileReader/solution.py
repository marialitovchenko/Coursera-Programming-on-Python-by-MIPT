"""
Write python module solution.py containing class FileReader. The constructor
should accept 1 parameter: file to the path. There should be methods read,
which would return a string with the line from the file.

Python модуль должен быть написан таким образом, чтобы импорт класса FileReader из него не вызвал ошибок.

При написании реализации метода read, вам нужно учитывать случай, когда при инициализации был передан путь к несуществующему файлу. Требуется обработать возникающее при этом исключение FileNotFoundError и вернуть из метода read пустую строку.
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
