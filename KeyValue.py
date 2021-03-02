import ui
import validator

def _color_error(attr):
	raise Exception(f"'{attr}' expects expects a valid color string, RGB tuple, or RGBA tuple")


def _font_error(attr):
	raise Exception(f"'{attr}' expects a 2 tuple like: (font_family_str, float_or_int)")


def _int_or_float_error(attr, tup=False):
	raise Exception(f"'{attr}' expects a positive int or float" + ('2 tuple' if tup else ''))


class KeyValue (ui.View):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault("bg_color", "white")
		self.underline_color = "black"
		self.underline_width = 1
		self.underline_padding = (5, 5)
		
		self.key_label = ui.Label(name="key",
												 			text="Key",
												 			flex='')
		self.key_label.size_to_fit()
		self.key_label.x = 5
		
		self.value_label = ui.Label(name="value",
													 			text="Value",
													 			alignment=ui.ALIGN_RIGHT,
													 			flex='')
		self.value_label.size_to_fit()
		self.value_label.x = self.width - self.value_label.width - 5
		
		ui.View.__init__(self, *args, **kwargs)
		self.add_subview(self.key_label)
		self.add_subview(self.value_label)
		self.layout()
		
		self.key_padding = 5
		self.value_padding = 5
		for k, v in kwargs.items():
			setattr(self, k, v)

	@property
	def key_text(self):
		return self.key_label.text
	
	@key_text.setter
	def key_text(self, value):
		if type(value) is str:
			self.key_label.text = value
		else:
			raise TypeError("'key_text' expects a string")
			
	@property
	def key_font(self):
		return self.key_label.font
	
	@key_font.setter
	def key_font(self, value):
		if validator.validate_font(value):
			self.key_label.font = value
		else:
			_font_error("key_font")
			
	@property
	def key_color(self):
		return self.key_label.text_color
	
	@key_color.setter
	def key_color(self, value):
		if validator.validate_color(value):
			self.key_label.text_color = value
		else:
			_color_error("key_color")
	
	@property
	def key_padding(self):
		return self.key_label.x
	
	@key_padding.setter
	def key_padding(self, value):
		if isinstance(value, (int, float)) and value >= 0:
			self.key_label.x = value
		else:
			_int_or_float_error('key_padding')
	
	@property
	def value_text(self):
		return self.value_label.text

	@value_text.setter
	def value_text(self, value):
		if type(value) is str:
			self.value_label.text = value
		else:
			raise TypeError("'value_text' expects a string")
	
	@property
	def value_font(self):
		return self.value_label.font
	
	@value_font.setter
	def value_font(self, value):
		if validator.validate_font(value):
			self.value_label.font = value
		else:
			_font_error("key_font")
	
	@property
	def value_color(self):
		return self.value_label.text_color
			
	@value_color.setter
	def value_color(self, value):
		if validator.validate_color(value):
			self.value_label.text_color = value
		else:
			_color_error("value_color")
	
	@property
	def value_padding(self):
		return self.width - (self.value_label.x + self.value_label.width)
	
	@value_padding.setter
	def value_padding(self, value):
		if isinstance(value, (int, float)) and value >= 0:
			self.value_label.x = self.width - self.value_label.width - value
		else:
			_int_or_float_error("value_padding")
	
	@property
	def underline_color(self):
		return self._underline_color
	
	@underline_color.setter
	def underline_color(self, value):
		if validator.validate_color(value):
			self._underline_color = value
			self.set_needs_display()
		else:
			_color_error("underline_color")
		
	@property
	def underline_width(self):
		return self._underline_width
	
	@underline_width.setter
	def underline_width(self, value):
		if isinstance(value, (int, float)) and value >= 0:
			self._underline_width = value
			self.set_needs_display()
		else:
			_int_or_float_error("underline_width")
		
	@property
	def underline_padding(self):
		return self._underline_padding
	
	@underline_padding.setter
	def underline_padding(self, value):
		if type(value) is tuple and len(value) == 2:
			x, y = value
			if isinstance(x, (int, float)) and isinstance(y, (int, float)) and x >= 0 and y >= 0:
				self._underline_padding = value
			else:
				_int_or_float_error("underline_padding", True)
		else:
			_int_or_float_error("underline_padding", True)
 
	def draw(self):
		underline = ui.Path()
		x1, x2 = self.underline_padding
		y = self.key_label.height
		underline.move_to(x1, y - 2)
		underline.line_to(self.width - x2, y - 2)
		ui.set_color(self.underline_color)
		underline.line_width = self.underline_width
		underline.stroke()

	def layout(self):
		self.key_label.size_to_fit()
		self.value_label.size_to_fit()
		self.key_label.x = self.key_padding
		self.value_label.x = self.width - self.value_label.width - self.value_padding
			

if __name__ == "__main__":
	import time
	root = ui.View()
	v = KeyValue(key_text='hi',
							 value_text='there',
							 frame=(50,50,150,30))					 
	root.add_subview(v)
	root.present('sheet')
	hex_wheel = "000000"
	while root.on_screen:
		num = int(hex_wheel, 16)
		v.value_text = hex_wheel
		v.value_font = (validator.FONT_FAMILIES[num % len(validator.FONT_FAMILIES)], 17)
		v.value_color = '#' + hex_wheel
		v.value_padding = num % 10
		v.layout()
		hex_wheel = hex(num + 1)[2:].zfill(6)
		time.sleep(0.1)
		
