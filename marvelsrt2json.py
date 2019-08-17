import pysrt
from pathlib import Path
import os
import json
import re
from movies import MovieMatcher, movies
import argparse

parser = argparse.ArgumentParser(
	description="Given the subtitle folder with .SRT SubRip UTF-8 files in it," \
				"generates a folder with the format readable by the mcuverse project" \
				"in the folder given by you"
)

parser.add_argument(
	'--input',
	'-i',
	help='path of the source folder relative to script',
	nargs='?',
	type=str,
	default='subtitles'
)

parser.add_argument(
	'--output',
	'-o',
	help='path of the output folder relative to script',
	nargs='?',
	type=str,
	default='processed'
)
default_check_garbage = ['tłumaczenie:', 'dopasowanie:', 'korekta:', 'napisy24', 'hatak', 'http']

parser.add_argument(
	'--garbage',
	'-g',
	help='relative path to file with garbage to remove'
		 'separated by new lines',
	nargs='?',
	default=None
)
args = parser.parse_args()
check_garbage = []
HERE = Path(os.path.split(__file__)[0])
if args.garbage is None:
	check_garbage = default_check_garbage
else:
	with open(Path(HERE / args.garbage), 'r') as f:
		for line in f:
			check_garbage.append(line.strip())

subtitles_path = Path(HERE / args.input)
processed_path = Path(HERE / args.output)
for path in [subtitles_path, processed_path]:
	if not os.path.isdir(path):
		os.mkdir(path)

movie_matcher = MovieMatcher()

delete_formatting = re.compile(r'<.*>|\(.*\)|-\s?|{.*}')
files_to_scan = os.listdir(subtitles_path)
len_files_to_scan = len(files_to_scan)
print(f'Opening {len_files_to_scan} file(s) from "{subtitles_path.name}" and saving to "{processed_path.name}"')
for i, file in enumerate(files_to_scan):
	opened_path = Path(subtitles_path / file)
	subs = pysrt.open(opened_path, encoding='UTF-8')
	print(f'Opening {opened_path.name} {i+1}/{len_files_to_scan}')
	subtitles_list = []
	index = -1
	for sub in subs:
		text = sub.text_without_tags
		text = re.sub(delete_formatting, '', text)
		found_garbage = False
		for garbage in check_garbage:
			if garbage in text:
				found_garbage = True
				break
		if found_garbage or not text or text == "":
			continue
		
		index += 1
		sub = {
			"index": index,
			"sub": [sub.strip() for sub in text.split('\n')],
			"time": f'{sub.start.minutes + sub.start.hours * 60}:{sub.start.seconds}'
		}
		subtitles_list.append(sub)
	movie_title = movie_matcher(file, movies)
	print(f'Matched {movie_title}')
	new_filename = movie_title + '.json'
	
	with open(Path(processed_path / new_filename), 'w+', encoding='UTF-8') as f:
		json.dump(subtitles_list, f, ensure_ascii=False)
		
	print()
