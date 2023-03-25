## Author: ChatGPT

import itertools
import hashlib
import signal
import sys
import csv

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
CHUNK_SIZE = 5
PROGRESS_FILENAME = 'progress.txt'
OUTPUT_FILENAME = 'permutations.csv'

def signal_handler(signal, frame):
    print("Interrupción del usuario. Guardando progreso...")
    save_progress()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_permutations():
    print("Generando permutaciones...")
    with open(OUTPUT_FILENAME, 'w') as f:
        writer = csv.writer(f)
        for i in range(1, len(ALPHABET) + 1):
            for perm in itertools.product(ALPHABET, repeat=i):
                writer.writerow([''.join(perm)])
                if int(hashlib.sha1(''.join(perm).encode()).hexdigest(), 16) % CHUNK_SIZE == 0:
                    print(f"Progreso: {ALPHABET.index(perm[0])}-{ALPHABET.index(perm[-1])} ({''.join(perm)})")
                    save_progress(perm)

def save_progress(perm=None):
    with open(PROGRESS_FILENAME, 'w') as progress_file:
        if perm:
            progress_file.write(''.join(perm))
        else:
            progress_file.write('')

def resume_permutations():
    try:
        with open(PROGRESS_FILENAME, 'r') as progress_file:
            start_perm = progress_file.read()
            start_index = ''.join(start_perm).rfind(ALPHABET[0])
            start_index = start_index + 1 if start_index != -1 else 0
            start_perm = list(start_perm[start_index:])
            if start_perm:
                print(f"Resumiendo desde {ALPHABET.index(start_perm[0])}-{ALPHABET.index(start_perm[-1])} ({''.join(start_perm)})...")
                return start_perm
    except FileNotFoundError:
        pass
    return None

if __name__ == '__main__':
    start_perm = resume_permutations()
    if start_perm:
        for i, c in enumerate(start_perm):
            ALPHABET = ALPHABET[ALPHABET.index(c):]
            start_perm[i] = 0
        ALPHABET = ALPHABET[1:]
    else:
        start_perm = []

    generate_permutations()
    save_progress()
