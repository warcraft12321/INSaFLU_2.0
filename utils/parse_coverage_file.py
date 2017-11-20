'''
Created on Nov 16, 2017

@author: mmp
'''
import os, gzip
from utils.utils import Utils
from utils.result import Coverage

from Bio import SeqIO

class ParseFile(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		self.data_file = None
		self.reference_dict = {}
		self.vect_reference = None
			
	def is_gzip(self, file_name): return True if (file_name.rfind(".gz") == len(file_name) - 3) else False
	
	def parse_file(self, file_name):
		"""
		"""
		self.data_file = DataFile(file_name)
		if (self.is_gzip(file_name)): handle = gzip.open(file_name, mode='rt')
		else: handle = open(file_name)
		for line in handle:
			sz_temp = line.strip().lower()
			if (len(sz_temp) == 0 or sz_temp[0] == '#'): continue
			self.data_file.add_data(line)
		handle.close()
		return self.data_file
	
		
	def read_reference_fasta(self, reference_file):
		"""
		test if the reference_file and ge the handle
		"""
		if (not os.path.exists(reference_file)): raise Exception("Can't locate the reference file: '" + reference_file + "'")

		### set temp file name
		temp_file_name = reference_file
		
		## create temp file
		b_temp_file = False
		if self.utils.is_gzip(reference_file):
			b_temp_file = True
			temp_file_name = self.utils.__get_temp_file__(reference_file, 10, self.utils.get_type_file(reference_file))
			cmd = "gzip -cd " + reference_file + " > " + temp_file_name
			sz_out = os.system(cmd)
			
		for rec in SeqIO.parse(temp_file_name, 'fasta'):
			self.reference_dict[rec.id] = len(str(rec.seq))
			self.vect_reference.append(rec.id)
		
		###
		if (b_temp_file): os.remove(temp_file_name)
		

class DataFile(object):
	'''
	classdocs
	'''
	util = Utils();

	def __init__(self, file_name):
		'''
		Constructor
		'''
		self.file_name = file_name
		self.vect_chromosomes = []
		self.dict_data = {}
		self.dict_data_coverage = {}
		self.previous_position = -1
		
	def get_vect_chromosomes(self): return self.vect_chromosomes
	def get_dict_data(self): return self.dict_data
	
	def add_data(self, line):
		if (len(line) == 0 or line[0] == '#'): return
		vect_data = line.split()
		if (len(vect_data) != 3): raise Exception("File: " + self.file_name + "\nThis line must have three values '" + line + "'")
		if (not self.util.is_integer(vect_data[1])): raise Exception("File: " + self.file_name + "\nLine: '" + line + "'\nThe locus need to be integer")
		if (not self.util.is_integer(vect_data[2])): raise Exception("File: " + self.file_name + "\nLine: '" + line + "'\nThe coverage need to be integer")
		if (vect_data[0] in self.dict_data): 
			if (int(vect_data[1]) <= (self.previous_position)): raise Exception("File: " + self.file_name + "\nLine: '" + line + "'\nThe locus need to be greater than the predecessor in the file")
			self.dict_data[vect_data[0]].append([vect_data[1], vect_data[2]])
			self.previous_position = int(vect_data[1])
		else:
			self.vect_chromosomes.append(vect_data[0])
			self.dict_data[vect_data[0]] = [[vect_data[1], vect_data[2]]]
			self.previous_position = int(vect_data[1])
			
		
	def get_coverage(self, sz_chromosome, length_chromosome):
		if (sz_chromosome not in self.dict_data): return 0
		if (sz_chromosome in self.dict_data_coverage): return self.dict_data_coverage[sz_chromosome]
		if (length_chromosome == 0): return 0
		if (len(self.dict_data[sz_chromosome]) > length_chromosome): 
			raise Exception("Chromosome '%s' has different sizes. Coverage: %d; Reference: %d" % (sz_chromosome, len(self.dict_data[sz_chromosome]), length_chromosome))
		sum_total = 0
		for data_ in self.dict_data[sz_chromosome]: sum_total += int(data_[1])
		self.dict_data_coverage[sz_chromosome] = sum_total / float(length_chromosome)
		return self.dict_data_coverage[sz_chromosome]
	
	def get_ratio_more_than(self, sz_chromosome, length_chromosome, value):
		if (sz_chromosome not in self.dict_data): return 0
		if (length_chromosome == 0): return 0
		if (len(self.dict_data[sz_chromosome]) > length_chromosome): 
			raise Exception("Chromosome '%s' has different sizes. Coverage: %d; Reference: %d" % (sz_chromosome, len(self.dict_data[sz_chromosome]), length_chromosome))
		sum_total = 0
		for data_ in self.dict_data[sz_chromosome]: sum_total += (1 if (int(data_[1]) > value) else 0)
		return sum_total / float(length_chromosome)
	
	def get_file_name(self):
		sz_return = os.path.basename(self.file_name)
		if (sz_return.rfind(".gz") == len(sz_return) - 3): sz_return = sz_return[:-3]
		if (sz_return.rfind(".") != -1): sz_return = sz_return[:-1 * (len(sz_return) - sz_return.rfind("."))]
		return sz_return

class GetCoverage(object):
	"""
	get coverage from deep.gz file
	need deep.gz file and reference
	"""
	utils = Utils()

	def __init__(self):
		self.reference_dict = {}
		self.vect_reference = []
		pass


	def get_dict_reference(self): return self.reference_dict
	def get_vect_reference(self): return self.vect_reference
	
	def get_coverage(self, deep_file, reference):
		self.reference_dict = {}
		self.vect_reference = []

		parse_file = ParseFile()
		data_file = parse_file.parse_file(deep_file)
		self.read_reference_fasta(reference)

		coverage = Coverage()
		for chromosome in self.vect_reference:
			if (chromosome not in self.reference_dict): raise Exception("Can't locate the chromosome '" + chromosome + "' in reference file")
			coverage.add_coverage(chromosome, Coverage.COVERAGE_ALL, "%.1f" % (data_file.get_coverage(chromosome, self.reference_dict[chromosome])))
			coverage.add_coverage(chromosome, Coverage.COVERAGE_MORE_0, "%.1f" % (data_file.get_ratio_more_than(chromosome, self.reference_dict[chromosome], 0) * 100))
			coverage.add_coverage(chromosome, Coverage.COVERAGE_MORE_9, "%.1f" % (data_file.get_ratio_more_than(chromosome, self.reference_dict[chromosome], 9) * 100))
		return coverage


	def read_reference_fasta(self, reference_file):
		"""
		test if the reference_file and ge the handle
		"""
		if (not os.path.exists(reference_file)): raise Exception("Can't locate the reference file: '" + reference_file + "'")

		### set temp file name
		temp_file_name = reference_file
		
		## create temp file
		b_temp_file = False
		if self.utils.is_gzip(reference_file):
			b_temp_file = True
			temp_file_name = self.utils.get_temp_file(os.path.basename(reference_file), self.utils.get_type_file(reference_file))
			cmd = "gzip -cd " + reference_file + " > " + temp_file_name
			sz_out = os.system(cmd)
			
		for rec in SeqIO.parse(temp_file_name, 'fasta'):
			self.reference_dict[rec.id] = len(str(rec.seq))
			self.vect_reference.append(rec.id)
		
		###
		if (b_temp_file): os.remove(temp_file_name)