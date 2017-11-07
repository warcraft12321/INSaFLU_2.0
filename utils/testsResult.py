'''
Created on Oct 28, 2017

@author: mmp
'''
from django.test import TestCase
from .result import Output, SoftwareDesc, DecodeResult, Result

class Test(TestCase):

	def test_result(self):
		result = Result()
		result.set_error("xpto")
		result.add_output(Output("name", 'path'))
		result.add_software(SoftwareDesc("name_s", '11212', 'ads'))
		
		sz_return = result.to_json()
		self.assertTrue(sz_return.find('"version": "11212"') != 0)
		self.assertTrue(sz_return.find('"name": "name_s"') != 0)
		
		decodeResult = DecodeResult()
		result_2 = decodeResult.decode_result(sz_return)
		self.assertEqual(result_2.result, result.result)
		self.assertEqual(len(result_2.outputs.list_output), len(result.outputs.list_output))
		self.assertEqual(result_2.outputs.list_output[0].file_name, result.outputs.list_output[0].file_name)
		self.assertEqual(len(result_2.softwares.list_software), len(result.softwares.list_software))
		self.assertEqual(result_2.softwares.list_software[0].name, result.softwares.list_software[0].name)
		
	def test_result_software(self):
		result = Result()
		result.set_error("xpto")
		result.add_output(Output("name", 'path'))
		result.outputs.list_output[0].set_software(SoftwareDesc("name44_s", '4444', 'sdfd'))
		result.add_software(SoftwareDesc("name_s", '11212', "sdd"))
		
		sz_return = result.to_json()
		self.assertTrue(sz_return.find('"version": "11212"') != 0)
		self.assertTrue(sz_return.find('"name": "name_s"') != 0)
		
		decodeResult = DecodeResult()
		result_2 = decodeResult.decode_result(sz_return)
		self.assertEqual(result_2.result, result.result)
		self.assertEqual(len(result_2.outputs.list_output), len(result.outputs.list_output))
		self.assertEqual(result_2.outputs.list_output[0].file_name, result.outputs.list_output[0].file_name)
		self.assertEqual(result_2.outputs.list_output[0].software.name, result.outputs.list_output[0].software.name)
		self.assertEqual(result_2.outputs.list_output[0].software.parameters, result.outputs.list_output[0].software.parameters)
		self.assertEqual(len(result_2.softwares.list_software), len(result.softwares.list_software))
		self.assertEqual(result_2.softwares.list_software[0].name, result.softwares.list_software[0].name)
