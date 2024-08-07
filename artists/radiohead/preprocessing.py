import json
import re
import os
import pandas as pd
import numpy as np

for file in os.listdir("/home/jasmine/PROJECTS/lyriguessr/artists/radiohead"):
    if file.endswith(".json"):
        print(file)
# json_file = open('all_waterparks_lyrics.json')
# data = json.load(json_file)