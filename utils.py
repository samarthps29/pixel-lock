import re
import json
from typing import List
# pattern that matches anything that is not a-z, A-Z, 0-9 or a whitespace
patternOnePass = r'[^a-zA-Z0-9\s]'
# pattern that matches more than one whitespace
patternSecondPass = r'\s+'


def filter(input: str) -> str:
    onepass = re.sub(patternOnePass, "", str(input).strip().lower())
    secondpass = re.sub(patternSecondPass, " ", onepass)
    return secondpass


def convert(input: List[str]) -> List[int]:
    data = []
    for char in input:
        val = ord(char) - 97 + 1
        if val < 0:
            val = 0
        data.append(val)
    return data


def render(data: List[str]) -> str:
    text = ""
    zero_cnt = 0
    for val in data:
        if (val == 0):
            zero_cnt += 1
            if (zero_cnt >= 2):
                break
            text += " "
        else:
            zero_cnt = 0
            text += chr(val + 97 - 1)
    return text


def readConfigFile(filepath: str):
    file = open(filepath, 'r', encoding='utf-8')
    json_data = json.load(file)
    return json_data
