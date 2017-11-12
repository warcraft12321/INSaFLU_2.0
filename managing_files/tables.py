import django_tables2 as tables
from django_tables2.utils import A
from managing_files.models import Reference, Sample
from django.utils.safestring import mark_safe
from django.conf import settings
from managing_files.manage_database import ManageDatabase
from utils.meta_key_and_values import MetaKeyAndValue
from utils.result import DecodeResultAverageAndNumberReads
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
import os

class ReferenceTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
#   account_number = tables.LinkColumn('customer-detail', args=[A('pk')])
	reference_fasta_name = tables.LinkColumn('reference_fasta_name', args=[tables.A('pk')], verbose_name='Fasta file')
	reference_genbank_name = tables.LinkColumn('reference_genbank_name', args=[tables.A('pk')], verbose_name='GenBank file')
	
	class Meta:
		model = Reference
		fields = ('name', 'scentific_name', 'reference_fasta_name', 'reference_genbank_name',
				  'creation_date', 'is_obsolete', 'number_of_locus')
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no References to show..."
		
	def render_reference_fasta_name(self, **kwargs):
		record = kwargs.pop("record")
		href = os.path.join(getattr(settings, "MEDIA_URL", None), record.reference_fasta.name)		
		return mark_safe('<a href="' + href + '">' + record.reference_fasta_name + '</a>')
	
	def render_reference_genbank_name(self, **kwargs):
		record = kwargs.pop("record")
		href = os.path.join(getattr(settings, "MEDIA_URL", None), record.reference_genbank.name)		
		return mark_safe('<a href="' + href + '">' + record.reference_genbank_name + '</a>')
	

class SampleTable(tables.Table):
#   Renders a normal value as an internal hyperlink to another page.
#   account_number = tables.LinkColumn('customer-detail', args=[A('pk')])
	number_quality_sequences = tables.Column('#Quality Seq.', empty_values=())
#	extra_info = tables.LinkColumn('sample-description', args=[tables.A('pk')], orderable=False, verbose_name='Extra Information', empty_values=())
	extra_info = tables.LinkColumn('Extra Information', empty_values=())
	type_and_subtype = tables.Column('Type and SubType', empty_values=())
	fastq_files = tables.Column('#Fastq Files', empty_values=())
	
	class Meta:
		model = Sample
		fields = ('name', 'creation_date', 'fastq_files', 'type_and_subtype', 'number_quality_sequences', 'extra_info')
		attrs = {"class": "table-striped table-bordered"}
		empty_text = "There are no Samples to show..."
	
	def render_fastq_files(self, record):
		"""
		number of fastqFiles, to show if there is 
		"""
		if (record.has_files):
			if (record.file_name_2 is None or len(record.file_name_2) == 0): return "1"
			return "2"
		return "0"
	
	def render_type_and_subtype(self, record):
		"""
		get type and sub type
		"""
		return record.get_type_sub_type()
	
	def render_number_quality_sequences(self, record):
		"""
		number of quality sequences and average
		"""
		manageDatabase = ManageDatabase()
		list_meta = manageDatabase.get_metakey(record, MetaKeyAndValue.META_KEY_Number_And_Average_Reads, None)
		if (list_meta.count() > 0 and list_meta[0].value == MetaKeyAndValue.META_VALUE_Success):
			decodeResultAverageAndNumberReads = DecodeResultAverageAndNumberReads()
			result_average = decodeResultAverageAndNumberReads.decode_result(list_meta[0].description)
			if (result_average.number_file_2 is None): return _('%s/%s' % (result_average.number_file_1, result_average.average_file_1 ))
			return _('%s/%s-%s/%s' % (result_average.number_file_1,\
					result_average.average_file_1, result_average.number_file_2,\
					result_average.average_file_2) )
		elif (list_meta.count() > 0 and list_meta[0].value.equals(MetaKeyAndValue.META_VALUE_Error)):
			return _("Error")
		return _('Not yet')

	def render_extra_info(self, record):
		"""
		icon with link to extra info
		"""
		manageDatabase = ManageDatabase()
		list_meta = manageDatabase.get_metakey(record, MetaKeyAndValue.META_KEY_Fastq_Trimmomatic, None)
		if (list_meta.count() > 0 and list_meta[0].value == MetaKeyAndValue.META_VALUE_Success):
			return mark_safe('<a href=' + reverse('sample-description', args=[record.pk]) + '><span ><i class="fa fa-plus-square"></i></span> More Info</a>')
		elif (list_meta.count() > 0 and list_meta[0].value == MetaKeyAndValue.META_VALUE_Error): return _("Error")
		return _('Not yet')
	
	

	
