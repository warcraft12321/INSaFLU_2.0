from django.db import models

# Create your models here.
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import GeoManager
from django.contrib.auth.models import User
from utils.constants import Constants, TypePath
from fluwebvirus.formatChecker import ContentTypeRestrictedFileField
from manage_virus.models import IdentifyVirus
from django.conf import settings
import os

def reference_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/<filename>
	return 'uploads/generic_data/user_{0}/{1}'.format(instance.owner.id, filename)


def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/<filename>
	return 'uploads/generic_data/user_{0}/{1}'.format(instance.owner.id, filename)

class SeasonReference(models.Model):
	"""
	Each sample needs a dataset 
	"""
	name = models.CharField(max_length=100, blank=True, null=True)
	owner = models.ForeignKey(User, related_name='season_reference', blank=True, null=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['name', ]
		
class Reference(models.Model):
	name = models.CharField(max_length=200, default='New reference')
	isolate_name = models.CharField(max_length=200, default='', verbose_name='Isolate Name')
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded Date')
	
	## Size 100K
	reference_fasta = ContentTypeRestrictedFileField(upload_to=reference_directory_path, content_types=['application/octet-stream', 'application/gzip'], max_upload_size=100000, blank=True, null=True)
	reference_fasta_name = models.CharField(max_length=200, default='', verbose_name='Fasta file')
	hash_reference_fasta = models.CharField(max_length=50, blank=True, null=True)

	## Size 200K
	reference_genbank = ContentTypeRestrictedFileField(upload_to=reference_directory_path, content_types=['application/octet-stream', 'application/gzip'], max_upload_size=200000, blank=True, null=True)
	reference_genbank_name = models.CharField(max_length=200, default='', verbose_name='Genbank file')
	hash_reference_genbank = models.CharField(max_length=50, blank=True, null=True)

	owner = models.ForeignKey(User, related_name='reference', blank=True, null=True, on_delete=models.CASCADE)
	is_obsolete = models.BooleanField(default=False, verbose_name='Obsolete')
	number_of_locus = models.IntegerField(default=0, verbose_name='#Sequences')
	
	season = models.ManyToManyField(SeasonReference)		## can have the season
	description = models.CharField(max_length=500, default='', blank=True, null=True, verbose_name='Description')

	def __str__(self):
		return self.file_name

	class Meta:
		verbose_name = 'Reference'
		verbose_name_plural = 'References'
		ordering = ['-creation_date', ]
		indexes = [
			models.Index(fields=['name'], name='name_idx'),
		]



class MetaKey(models.Model):
	"""
	Has meta tags to put values, for example, quality in the files, or samples
	"""
	name = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['name', ]


class TagName(models.Model):
	"""
	Has the tags to ticked the samples
	"""
	name = models.CharField(max_length=100, blank=True, null=True)
	owner = models.ForeignKey(User, related_name='tag_name', blank=True, null=True, on_delete=models.CASCADE)
	is_meta_data = models.BooleanField(default=False)	## if this tag belongs to meta data or not.
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['name', ]


class DataSet(models.Model):
	"""
	Each sample needs a dataset 
	"""
	name = models.CharField(max_length=100, blank=True, null=True)
	owner = models.ForeignKey(User, related_name='data_set', blank=True, null=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['name', ]
		
class VacineStatus(models.Model):
	"""
	Each sample needs a dataset 
	"""
	name = models.CharField(max_length=100, blank=True, null=True)
	owner = models.ForeignKey(User, related_name='vacine_status', blank=True, null=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['name', ]
	
class Sample(models.Model):
	"""
	Sample, each sample has one or two files...
	"""
	OUT_FILE_ABRICATE = "abricate.txt"
	
	## to remove in future
	objects = models.Manager()
	
	name = models.CharField(max_length=200, blank=True, null=True)  ## This Id should match the prefix of the reads files (i.e. prefix_R1_001.fastq.gz /  
																	##    prefix_R2_001.fastq.gz),
	date_of_onset = models.DateField('date of onset', blank=True, null=True)
	date_of_collection = models.DateField('date of collection', blank=True, null=True)
	date_of_receipt_lab = models.DateField('date of receipt lab', blank=True, null=True)
	week = models.IntegerField(blank=True, null=True)
	day = models.IntegerField(blank=True, null=True)	## from "Date of onset” or “Date of collection” 
	month = models.IntegerField(blank=True, null=True)
	year = models.IntegerField(blank=True, null=True)
	vaccine_status = models.ForeignKey(VacineStatus, related_name='sample', blank=True, null=True, on_delete=models.CASCADE)
	creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded Date')
	is_rejected = models.BooleanField(default=False)
	is_obsolete = models.BooleanField(default=False)
	owner = models.ForeignKey(User, related_name='sample', blank=True, null=True, on_delete=models.CASCADE)
	tag_names = models.ManyToManyField(TagName)
	data_set = models.ForeignKey(DataSet, related_name='sample', blank=True, null=True, on_delete=models.CASCADE)
	geo_local = PointField(null=True, blank=True, srid=4326);  ## 4326 which means latitude and longitude
	geo_manager = GeoManager()
	identify_virus = models.ManyToManyField(IdentifyVirus)

	### files
	is_valid_1 = models.BooleanField(default=False)
	file_name_1 = models.CharField(max_length=300, blank=True, null=True)
	path_name_1 = ContentTypeRestrictedFileField(upload_to=user_directory_path, blank=True, null=True, content_types=['application/octet-stream', 'application/gzip'], max_upload_size=30971520)
	is_valid_2 = models.BooleanField(default=False)
	file_name_2 = models.CharField(max_length=300, blank=True, null=True)
	path_name_2 = ContentTypeRestrictedFileField(upload_to=user_directory_path, blank=True, null=True, content_types=['application/octet-stream', 'application/gzip'], max_upload_size=30971520)

	## has files, the user can upload the files after
	has_files = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-creation_date', ]

	def get_file_names(self):
		sz_return = "" if self.file_name_1 == None else self.file_name_1
		sz_return += "/" if len(sz_return) > 0 and self.file_name_2 is not None else ""
		sz_return += "" if self.file_name_2 == None else self.file_name_2
		return sz_return

	def exist_file_2(self):
		if (self.path_name_2 is None or self.path_name_2.name is None): return False
		return True

	def get_abricate_output(self, type_path):
		"""
		type_path = [MEDIA_ROOT, MEDIA_URL]
		Return the file name of the abricate output base on fastq File input
		path it's a FileField instance, or a string
		"""
		return os.path.join(self.__get_path__(type_path, True), self.OUT_FILE_ABRICATE)
	
	def get_trimmomatic_file(self, type_path, b_first_file):
		"""
		get the trimmomatic files, it's going to be use for all processing
		type_path = [MEDIA_ROOT, MEDIA_URL]
		"""
		if (not b_first_file and not self.exist_file_2()): return None
		return os.path.join(self.__get_path__(type_path, b_first_file), self.name + ("_1P.fastq.gz" if b_first_file else "_2P.fastq.gz"))
	
	def get_fastq(self, type_path, b_first_file):
		"""
		return fastq output first step
		"""
		if (not b_first_file and not self.exist_file_2()): return None
		return os.path.join(self.__get_path__(type_path, b_first_file), self.file_name_1 if b_first_file else self.file_name_2)

	def get_fastq_output(self, type_path, b_first_file):
		"""
		return fastq output first step
		"""
		if (not b_first_file and not self.exist_file_2()): return None
		return os.path.join(self.__get_path__(type_path, b_first_file), self.file_name_1.replace(".fastq.gz", "_fastqc.html") if b_first_file else self.file_name_2.replace(".fastq.gz", "_fastqc.html"))

	
	def get_fastq_trimmomatic(self, type_path, b_first_file):
		"""
		return fastq output first step
		"""
		if (not b_first_file and not self.exist_file_2()): return None
		return os.path.join(self.__get_path__(type_path, b_first_file), self.name + ("_1P_fastqc.html" if b_first_file else "_2P_fastqc.html"))

	def __get_path__(self, type_path, b_first_file):
		"""
		get a path, from MEDIA_URL or MEDIA_ROOT
		"""
		if (b_first_file):
			path_to_find = os.path.dirname(self.path_name_1.name)
			if (type_path == TypePath.MEDIA_ROOT): 
				if not path_to_find.startswith('/'): path_to_find = os.path.join(getattr(settings, "MEDIA_ROOT", None), path_to_find)
			else:
				path_to_find = os.path.join(getattr(settings, "MEDIA_URL", None), path_to_find)
		else:
			path_to_find = os.path.dirname(self.path_name_2.name)
			if (type_path == TypePath.MEDIA_ROOT): 
				if not path_to_find.startswith('/'): path_to_find = os.path.join(getattr(settings, "MEDIA_ROOT", None), path_to_find)
			else:
				path_to_find = os.path.join(getattr(settings, "MEDIA_URL", None), path_to_find)
		return path_to_find



class MetaKeySample(models.Model):
	"""
	Relation ManyToMany in 
	"""
	meta_tag = models.ForeignKey(MetaKey, related_name='meta_key_sample', on_delete=models.CASCADE)
	sample = models.ForeignKey(Sample, related_name='meta_key_sample', on_delete=models.CASCADE)
	owner = models.ForeignKey(User, related_name='meta_key_sample', on_delete=models.CASCADE)
	creation_date = models.DateTimeField('uploaded date', auto_now_add=True)
	value = models.CharField(default=Constants.META_KEY_VALUE_NOT_NEED, max_length=200)
	description = models.TextField(default="")
	
	class Meta:
		ordering = ['sample__id', '-creation_date']
	
	def __str__(self):
		return self.value
	
class UploadFiles(models.Model):
	"""
	this class has the files that the user can upload, has he want,
	then the system make the relations with the samples
	"""
	is_valid = models.BooleanField(default=False)
	file_name = models.CharField(max_length=300, blank=True, null=True)
	creation_date = models.DateTimeField('uploaded date', auto_now_add=True)
	owner = models.ForeignKey(User, related_name='upload_files', on_delete=models.CASCADE)
	path_name = ContentTypeRestrictedFileField(upload_to=user_directory_path, blank=True, null=True, content_types=['application/octet-stream'], max_upload_size=30971520)
	is_day_month_year_from_date_of_onset = models.BooleanField(default=False)
	is_day_month_year_from_date_of_collection = models.BooleanField(default=False)
	
	class Meta:
		ordering = ['creation_date']

	def __str__(self):
		return self.file_name
	
class Project(models.Model):
	"""
	Project for run a pipeline in the data,
	It's possible to run several times and add data to the project
	"""
	name = models.CharField(max_length=200, blank=True, null=True)
	owner = models.ForeignKey(User, related_name='project', blank=True, null=True, on_delete=models.CASCADE)
	samples = models.ManyToManyField(Sample, related_name='project')
	creation_date = models.DateTimeField('uploaded date', auto_now_add=True)
	is_finished = models.BooleanField(default=False)
	
	def __str__(self):
		return self.name
	
	class Meta:
		ordering = ['-creation_date', ]


class Version(models.Model):
	"""
	"""
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
	
	class Meta:
		ordering = ['name', ]
		

class Software(models.Model):
	"""
	Has all the softwares
	It can be used for all users 
	"""
	name = models.CharField(max_length=100, blank=True, null=True)
	path_to_run = models.CharField(max_length=300)
	version = models.ForeignKey(Version, related_name='software', on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['name', 'version__name']

