class styles(object):

	css_cards = {
		
		'card': """
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			line-height: 1.42857143;
			margin: 0.2rem;
			min-width: 28rem;
			max-width: 28rem;
			min-height: 15rem;
			max-height: 15rem;
			padding: 1.3rem;
			border-radius: 19px;
  			background-color: #e0e0e0;
			box-shadow: inset 5px 5px 10px #bebebe, inset -5px -5px 10px #ffffff;""",

		'repo-logo': """
			width: 5.5rem;""",

		'description': """
			text-align: justify;
			overflow: hidden;
			text-overflow: ellipsis;
			display: -webkit-box;
			-webkit-line-clamp: 6;
			line-clamp: 6; 
			-webkit-box-orient: vertical;""",

		'recently-updated': """
			width: 1.4rem;
			height: 1.4rem;
			border-radius: 50%;
			margin-left: auto;
			margin-right: 0.1rem;
			background-color: #3e3e3e;""",

		'repo-icon':"""
			height: 1.1rem;
			margin-left: 0.2rem;
			margin-right: 0.2rem;""",

		'card-row': """    
			display: flex;
			flex-direction: row;
			justify-content: space-between;""",

		'card-col1': """
			width: 72%;""",

		'flex-horizontal': """
			display: flex;
			align-items: center;
			flex-direction: row;""",

		'float-right': """
			justify-content: flex-end;""",

		'grey-color-svg': """
			filter: brightness(0) saturate(100%) invert(26%) sepia(0%) saturate(9%) hue-rotate(190deg) brightness(93%) contrast(100%);"""
		
	}

	css_global = """
			margin: 0;
			box-sizing: border-box;
			color: #3e3e3e;
			font-family: 'Helvetica Neue', Helvetica;
	"""

	def __init__(self, embedded):
		self.embedded =  embedded

	def get_rules(self):

		rules = ''
		
		# CSS rules will be inside the html tags
		if self.embedded and False:
			return rules
		
		for css_class in self.css_cards.keys():
			r = ' '.join(self.css_cards[css_class].split()) # Minify css rules
			rules += f".{css_class}{{{r}}}\n"

		return rules

	def get_global_css(self):

		if not self.embedded:
			return ''
		
		return self.css_global.replace("\n", "").replace("\t", "")

	def get(self, class_selector, custom_css = None):

		styles = ''

		# Return normal css class names        
		if not self.embedded or True:

			if isinstance(class_selector, list):
				styles += f'''class="{' '.join(class_selector)}"'''
			else:
				styles += f'''class="{class_selector}"'''

			if custom_css:
				styles += f' style="{custom_css}"'
			
			return styles
		
		# Embed all the styles in html
		styles += 'style=" '
		styles += self.css_global

		if isinstance(class_selector, list):
			styles += ' '.join([ self.css_cards[c] for c in class_selector ])
		else:
			styles += self.css_cards[class_selector]
		
		if custom_css:
			styles += custom_css
		

		styles += '"'

		return styles.replace("\n", "").replace("\t", "")



	