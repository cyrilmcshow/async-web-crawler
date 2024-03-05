def read_lines_from_file(path):
    with open(path, 'r') as file:
        return file.read().splitlines()
