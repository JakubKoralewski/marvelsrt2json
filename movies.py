movies = []


class Movie:
	name = None
	years = None
	
	def condition(self):
		return lambda f: self.name.lower() in f
	
	def generate_condition(self, splitter):
		"""
		Returns a function that splits the movie name by given splitter
		and if all parts of the movie title are in filename then that
		function will match that filename.
		:param splitter: a dash, a space
		:return:
		"""
		return lambda f: all([x.lower() in f.lower() for x in self.name.split(splitter)])
	
	def __init_subclass__(cls, movies, *a, **kw):
		super().__init_subclass__(**kw)
		# print('init subclass', cls, a, kw)
		if cls.name is None:
			raise TypeError("Movie has to have a name!")
		elif movies is None:
			raise TypeError("Movies list not given in cls declaration")
		elif not isinstance(cls.name, str):
			raise TypeError("Movie name must be a string")
		elif cls.years:
			if not isinstance(cls.years, list):
				raise TypeError("Movie's years must be a list")
			for year in cls.years:
				if not isinstance(year, str):
					is_correct_int = False
					if isinstance(year, int):
						if not year > 1000 and year < 3000:
							raise TypeError("Event though year is int it is not a year")
						else:
							is_correct_int = True
					if not is_correct_int:
						raise TypeError("Movie's years must be strs or ints")
		
		if '-' in cls.name:
			cls.condition = cls.generate_condition(cls, '-')
		elif ' ' in cls.name:
			cls.condition = cls.generate_condition(cls, ' ')
		movies.append(cls)


class AntMan(Movie, movies=movies):
	name = 'Ant-Man'
	years = ['2015', '2018']


class Avengers(Movie, movies=movies):
	name = 'Avengers'
	years = ['2012', '2015', '2018', '2019']


class BlackPanther(Movie, movies=movies):
	name = 'Black Panther'


class CaptainAmerica(Movie, movies=movies):
	name = 'Captain America'
	years = ['2011', '2014', '2016']


class CaptainMarvel(Movie, movies=movies):
	name = 'Captain Marvel'


class DoctorStrange(Movie, movies=movies):
	name = 'Doctor Strange'


class GuardiansOfTheGalaxy(Movie, movies=movies):
	name = 'Guardians of The Galaxy'
	years = ['2014', '2017']


class IronMan(Movie, movies=movies):
	name = 'Iron Man'
	years = ['2008', '2010', '2013']


class SpiderMan(Movie, movies=movies):
	name = 'Spider-Man'
	years = ['2017', '2019']


class IncredibleHulk(Movie, movies=movies):
	name = 'The Incredible Hulk'


class Thor(Movie, movies=movies):
	name = 'Thor'
	years = ['2011', '2013', '2017']


class MovieMatcher:
	def __call__(self, filename, movies):
		for movie in movies:
			if movie.condition(filename):
				if movie.years is None:
					return movie.name
				for i, year in enumerate(movie.years):
					if year in filename:
						return f'{match_roman(i + 1)} {movie.name}'
		import re
		if not re.search(r'\d\d\d\d', filename):
			raise TypeError(f"Given name does not have year!\nname: {filename}")


def match_roman(num):
	conv = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
			[100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
			[10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'],
			[1, 'I']]
	roman = ''
	i = 0
	while num > 0:
		while conv[i][0] > num:
			i += 1  # increments i to largest value greater than current num
		roman += conv[i][1]  # adds the roman numeral equivalent to string
		num -= conv[i][0]  # decrements your num
	return roman


# def filename_matcher(filename: str) -> str:
# 	f = filename.lower()
# 	if all([x in f for x in ['ant', 'man']]):
# 		if '2015' in f:
# 			return 'I Ant-Man'
# 		if '2018' in f:
# 			return 'II Ant-Man'
# 		raise LookupError("wrong ant man")
# 	elif 'avengers' in f:
# 		if '2012' in f:
# 			return 'I Avengers'
# 		if '2015' in f:
# 			return 'II Avengers'
# 		if '2018' in f:
# 			return 'III Avengers'
# 		if '2019' in f:
# 			return 'IV Avengers'
# 	elif all([x in f for x in ['black', 'panther']]):
# 		return 'Black Panther'
# 	elif all([x in f for x in ['captain', 'marvel']]):
# 		return 'Captain Marvel'
# 	elif all([x in f for x in ['doctor', 'strange']]):
# 		return 'Doctor Strange'
# 	elif all([x in f for x in ['captain', 'america']]):
# 		return 'Captain America'
