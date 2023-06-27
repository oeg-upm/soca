from ... import base_dir

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
	
@singleton
class styles(object):

	def __init__(self):
		with open(f"{base_dir}/assets/soca-card.css") as f_rules:
			self.rules = ''.join(f_rules.readlines())






	