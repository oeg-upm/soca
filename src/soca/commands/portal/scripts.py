from ... import base_dir

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
	
@singleton
class scripts(object):
        
    js_dependencies = """
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>"""

    def __init__(self):
        with open(f"{base_dir}/assets/scripts/copy_card.js") as cc:
            self.copy_card = ''.join(cc.readlines())

        with open(f"{base_dir}/assets/scripts/tooltip.js") as tt:
            self.tooltip = ''.join(tt.readlines())

        with open(f"{base_dir}/assets/scripts/modals.js") as mm:
            self.modals = ''.join(mm.readlines())


    def function_copy_card(self):
        return mini(f"function add_copy_card(){{{self.copy_card}}};") 
    
    def function_tooltip(self):
        return mini(f"function add_tooltip(){{{self.tooltip}}};")
    
    def functions_modals(self):
        return mini(self.modals)

def mini(js):
    return '\n'+js.replace('    ','').replace('\n','')
