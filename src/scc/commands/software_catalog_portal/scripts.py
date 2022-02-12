from scc import base_dir
import json

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
        
        with open(f"{base_dir}/assets/scripts/filtering.js") as flt:
            self.filtering = ''.join(flt.readlines())

    def set_card_data(self,card_data):
        self.card_data = "let cards = "+json.dumps(card_data, indent=4, sort_keys=True).replace('</script>','<\\/script>')+";\n"






	