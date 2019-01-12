import math

class python_for_block(object):
	def __init__(self, line, id, code, sub):
		self.line = line
		self.id = id
		self.code = code
		self.sub = sub
		
	def compile(self, func):
		try:
			set = eval(self.code, globals(), func.get_python_env())
		except:
			raise ValueError('Could not evaluate "{0}" in "for" block at line {1}'.format(self.code, self.line))
		
		try:
			iter(set)
		except:
			raise ValueError('"{0}" in "for" block at line {1} is not an iterable set.'.format(self.code, self.line))

		for v in set:
			func.set_dollarid(self.id, v)
			try:
				func.compile_blocks(self.sub)
			except Exception as e:
				print(e.message)
				raise Exception('Unable to compile python for block contents at line {}'.format(self.line))