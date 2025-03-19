import os
import json
from typing import List


def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_json(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_jsonl(file_path: str) -> List[dict]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]


def list_dir(dir_path: str) -> List[str]:
    return os.listdir(dir_path)
