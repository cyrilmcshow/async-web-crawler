import aiofiles
from os import path


def read_lines_from_file(path):
    with open(path, 'r') as file:
        return file.read().splitlines()


async def save_file(dir_path, file_name, content):
    file_path = '/'.join([dir_path, file_name])
    async with aiofiles.open(file_path, 'wb') as file:
        await file.write(content)
    return path.abspath(file_path)
