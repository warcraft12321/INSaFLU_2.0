from django.apps import AppConfig
# 
from constants.constants import Constants, FileExtensions
from constants.constants_mixed_infection import ConstantsMixedInfection
from django.db import transaction
import os


class ManagingFilesConfig(AppConfig):
	name = 'managing_files'
	verbose_name = "Managing Files"
	
	def ready(self):
		
		## create a default user
		self.create_default_user()
			
		#### Now upload the 
		self.upload_default_files()
		
		#### set default fields
		self.default_database_fields()
		
		#### set default references
		self.upload_default_references()
		
		#### only used for test of max open files
#		self.test_open_files()
		
#		pass

	def create_default_user(self):
		"""
		create a default user to link the default references...
		"""
		from django.contrib.auth.models import User
		from managing_files.models import DataSet
		try:
			User.objects.get(username=Constants.DEFAULT_USER)
			### great, the default user exist 
		except User.DoesNotExist:
			
			### need to create it
			user = User()
			user.username = Constants.DEFAULT_USER
			user.password = Constants.DEFAULT_USER_PASS
			user.first_name = Constants.DEFAULT_USER
			user.is_active = False
			user.is_staff = False
			user.is_superuser = False
			user.save()
	
		### create generic dataset
		for user in User.objects.all():
			result = DataSet.objects.filter(owner__id=user.id)
			if (len(result) == 0):
				### need to create it
				dataSet = DataSet()
				dataSet.name = Constants.DATA_SET_GENERIC
				dataSet.owner = user
				dataSet.save()


	def upload_default_files(self):
		"""
		Upload default files
		"""
		## only runs once, wen start ans test if the file was uploaded with virus hypothesis
		from manage_virus.uploadFiles import UploadFiles
		from utils.software import Software
		uploadFiles = UploadFiles()
		## get version and pah
		b_test = False
		(version, path) = uploadFiles.get_file_to_upload(b_test)
		
		## uplaod
		uploadFile = uploadFiles.upload_file(version, path)

		# create the abricate database
		if (uploadFile != None):
			software= Software()
			if (not software.is_exist_database_abricate(uploadFile.abricate_name)):
				software.create_database_abricate(uploadFile.abricate_name, uploadFile.path)


	def default_database_fields(self):
		"""
		set default fields in database
		"""
		
		### MixedInfectionsTag
		from managing_files.models import MixedInfectionsTag
		constants_mixed_infection = ConstantsMixedInfection()
		for tag in constants_mixed_infection.vect_upload_to_database:
			try:
				mixed_infections_tag = MixedInfectionsTag.objects.get(name=tag)
			except MixedInfectionsTag.DoesNotExist as e:
				mixed_infections_tag = MixedInfectionsTag()
				mixed_infections_tag.name = tag
				mixed_infections_tag.save()
	
	
	@transaction.atomic
	def upload_default_references(self):
		"""
		upload default files for reference
		"""
		from manage_virus.uploadFiles import UploadFiles
		from django.contrib.auth.models import User
		
		uploadFiles = UploadFiles()
		self.create_default_user()
		b_test = False
		uploadFiles.upload_default_references(User.objects.get(username=Constants.DEFAULT_USER), b_test) 
		
	def test_open_files(self):
		
		from utils.utils import Utils
		from django_q.tasks import async
		utils = Utils()
		b_close = False
		n_count = 0
		max_files = 10000
		while n_count < max_files:
			async(utils.open_file, b_close)
			n_count += 1
			print('file: ' +  str(n_count) + '   close: ' + str(b_close))
		print('finished')
