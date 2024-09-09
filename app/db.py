import os
import json

def add_record(record):
    with open('db.txt', 'a+') as f:
        f.write(record + '\n')

def get_records():
    records = ''
    with open('db.txt', 'r') as f:
        records = f.read()

    return records