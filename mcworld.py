import sys
import os
import codecs
import shutil
import time
import json
import io
import zipfile

class mcworld(object):
	def __init__(self, leveldir, namespace):
		self.dir = leveldir
		self.zipbytes = io.BytesIO()
		self.zip = zipfile.ZipFile(self.zipbytes, 'w', zipfile.ZIP_DEFLATED, False)
		self.namespace = namespace
		
	def write_functions(self, functions):
		function_dir = 'data/{}/functions/'.format(self.namespace)
		
		for name in functions:
			filename = os.path.join(function_dir, "{0}.mcfunction".format(name))
			
			func = functions[name]
			text = func.get_utf8_text()
			self.zip.writestr(filename, text)
				
	def write_tags(self, clocks, block_tags):
		tag_dir = 'data/minecraft/tags/functions/'
		
		tick_tag_file = os.path.join(tag_dir, 'tick.json')
		self.zip.writestr(tick_tag_file, json.dumps({'values':['{0}:{1}'.format(self.namespace, name) for name in clocks]}, indent=4))
		
		
		load_tag_file = os.path.join(tag_dir, 'load.json')
		self.zip.writestr(load_tag_file, json.dumps({'values':['{0}:reset'.format(self.namespace)]}, indent=4))
			
		if len(block_tags) > 0:
			block_tag_dir = 'data/{}/tags/blocks/'.format(self.namespace)
			
			for tag in block_tags:
				blocks = block_tags[tag]
				
				tag_filename = os.path.join(block_tag_dir, '{0}.json'.format(tag))
				self.zip.writestr(tag_filename, json.dumps({'values':['minecraft:{0}'.format(block) for block in blocks]}, indent=4))
		
	def write_mcmeta(self, desc):
		mcmeta_file = 'pack.mcmeta'
		
		self.zip.writestr(mcmeta_file, json.dumps({'pack':{'pack_format':1, 'description':desc}}, indent=4))
	
	def write_zip(self):
		self.zip.close()
	
		zip_filename = os.path.join(self.dir, 'datapacks/{}.zip'.format(self.namespace))
		with open(zip_filename, 'wb') as file:
			file.write(self.zipbytes.getvalue())