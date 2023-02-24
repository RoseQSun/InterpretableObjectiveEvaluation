from pathlib import Path
from music21 import *
import tqdm

abc_fps = Path('./abc_all').glob('*/*.abc')

for fp in tqdm.tqdm(abc_fps):
    try:
        abcScore = converter.parse(fp)
    except (ValueError,KeyError):
        print(fp)
        continue

