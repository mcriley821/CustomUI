import ui
from objc_util import UIEdgeInsets, ObjCClass


NSIndexPath = ObjCClass('NSIndexPath')

"""ComboBox is a ui.View subclass that allows a
string to be chosen from a list of choices.
Needs the superview object for the dropbox.
Accepts all kwargs of ui.View, as well as:
	font						 ->		Font of all choice strings
	choices					 ->		List of choice strings
	selected_index	 ->		Initial choice index
	button_tint 		 ->		Color of the dropdown button tint
	display_count		 ->		Number of rows to display in the drop down"""
class ComboBox (ui.View):
	"""ComboBox initialization"""
	def __init__(self, _superview, *args, **kwargs):
		# ui.View kwargs
		kwargs.setdefault('bg_color', 'white')
		kwargs.setdefault('border_width', 1.0)
		kwargs.setdefault('border_color', '#e5e5e5')
		kwargs.setdefault('corner_radius', 3.5)
		kwargs.setdefault('name', 'ComboBox')
		
		# custom kwargs
		self.font 					 = kwargs.pop('font', ('<System>', 20))
		self.text_color 		 = kwargs.pop('text_color', "black")
		self.highlight_color = kwargs.pop('highlight_color', 'grey')
		self.button_tint 		 = kwargs.pop('button_tint', "grey")
		self.display_count	 = kwargs.pop('display_count', 5)
		self.selected_index  = kwargs.pop('selected_index', 0)	
		self.choices			   = kwargs.pop('choices', [""])		
		
		# init super 
		ui.View.__init__(self, *args, **kwargs)
		
		x, y, w, h = self.frame
		row_sizes = [ui.measure_string(i, font=self.font) for i in self.choices]
		w = max([w] + [i[0] for i in row_sizes])
		h = max([h] + [i[1] for i in row_sizes])
		# button for the dropbox
		self.drop_button = ui.Button(name='drop_button',
																 frame=(w - h - 3, 3, h, h - 6),
																 image=ui.Image('iow:arrow_down_b_24'),
																 tint_color=self.button_tint,
																 action=self.do_dropbox)
		# label for selected item
		self.selected_label = ui.Label(name='selected_label',
																	 alignment=ui.ALIGN_CENTER,
																	 text=self.choices[self.selected_index],
																	 frame=(3, 3, w - self.drop_button.width - 6, h),
																	 corner_radius=self.corner_radius)
		# dropbox
		lbl_w = self.selected_label.width
		ds = ComboBoxDataSource(self.choices,
														self.font,
														self.text_color,
														self.bg_color,
														self.index_changed,
														self.selected_index,
														self.highlight_color)
		self.dropbox = ui.TableView(name='dropbox',
																bg_color=self.bg_color,
																data_source=ds,
																delegate=ds,
																selected_row=(0, self.selected_index),
																seperator_color=self.border_color,
																allows_selection=True,
																row_height=30,
																frame=(x, y + h - 1, lbl_w, self.display_count * h),
																border_color=self.border_color,
																border_width=self.border_width,
																corner_radius=self.corner_radius,
																hidden=True)
		# complete the lines on the table
		self.dropbox.objc_instance.setSeparatorInset_(UIEdgeInsets(0))

		# clip to rounded corners 
		obj = self.objc_instance
		obj.setClipsToBounds_(True)

		# add subviews
		self.add_subview(self.selected_label)
		self.add_subview(self.drop_button)
		_superview.add_subview(self.dropbox)
	
	@property
	def font(self):
		return self._font
	
	@font.setter
	def font(self, value):
		if type(value) == tuple:
			self._font = value
			if hasattr(self, 'selected_label'):
				self.selected_label.font = value
			if hasattr(self, 'dropbox'):
				self._data_source.font = value
				self.layout()
	
	@property
	def text_color(self):
		return self._text_color
	
	@text_color.setter
	def text_color(self, value):
		value = ui.parse_color(value)
		self._text_color = value
		if hasattr(self, 'selected_label'):
			self.selected_label.text_color = value
		if hasattr(self, 'dropbox'):
			self.dropbox.data_source.text_color = value
			self.dropbox.data_source.reload_cells()
			self.dropbox.reload()
			self.dropbox.selected_row = self.selected_index
	
	@property
	def highlight_color(self):
		return self._highlight_color
	
	@highlight_color.setter
	def highlight_color(self, value):
		value = ui.parse_color(value)
		self._highlight_color = value
		if hasattr(self, 'dropbox'):
			self.dropbox.data_source.highlight_color = value
			self.dropbox.data_source.reload_cells()
			self.dropbox.reload()
			self.dropbox.selected_row = self.selected_index
	
	@property
	def selected_index(self):
		return self._selected_index		
	
	@selected_index.setter
	def selected_index(self, value):
		if type(value) is int:
			self._selected_index = value
			if hasattr(self, 'selected_label'):
				self.selected_label.text = self.choices[value]

	@property
	def selected_text(self):
		return self.selected_label.text
			
	@property
	def choices(self):
		return self._choices
	
	@choices.setter
	def choices(self, value):
		if type(value) is list and all(type(i) == str for i in value):
			self._choices = value
			if hasattr(self, 'dropbox'):
				ds = ComboBoxDataSource(value,
																self.font,
																self.text_color,
																self.bg_color,
																self.index_changed,
																self.selected_index,
																self.highlight_color)
				self.dropbox.data_source = ds
				self.dropbox.delegate = ds
				self.dropbox.reload()
				self.layout()
	
	@property
	def button_tint(self):
		return self._btn_tint
	
	@button_tint.setter
	def button_tint(self, value):
		value = ui.parse_color(value)
		if hasattr(self, 'drop_button'):
			self.drop_button.tint_color = value
		self._btn_tint = value
	
	@property
	def display_count(self):
		return self._display_count
	
	@display_count.setter
	def display_count(self, value):
		if type(value) is int:
			self._display_count = value
			if hasattr(self, 'dropbox'):
				self.layout()

	def layout(self):
		sizes = [ui.measure_string(i, font=self.font) for i in self.choices]
		_row_w = max(self.width, max(i[0] for i in sizes))
		_row_h = max(i[1] for i in sizes) + 3
		
		# self layout
		if _row_w != self.width:
			self.width = _row_w + _row_h + 9
		if _row_h > self.height:
			self.height = _row_h

		# selected label layout
		self.selected_label.width = self.width - self.height - 6
		self.selected_label.height = self.height - 6
		
		# drop button layout
		self.drop_button.x = self.width - self.height
		self.drop_button.width = self.height - 3
		self.drop_button.height = self.height - 6
		
		# dropbox layout
		_h = _row_h * min(self.display_count, len(self.choices))
		self.dropbox.row_height = _row_h
		self.dropbox.width = self.selected_label.width
		self.dropbox.x = self.x + 3
		self.dropbox.y = self.y + self.height
		self.dropbox.height = _h
		self.dropbox.reload()
		self.dropbox.selected_row = self.selected_index
	
	def touch_began(self, touch):
		if self._hit_test(touch):
			self.do_dropbox()
	
	def _hit_test(self, touch):
		v = touch.objc_instance.view()
		name = v.name()
		if name:
			name = name.cString().decode('utf8')
			if name == self.name or name == self.drop_button.name:
				return True
		return False
	
	def draw(self):
		# draw the splitter line
		p = ui.Path()
		p.move_to(self.selected_label.width + 4.5, 0)
		p.line_to(self.selected_label.width + 4.5, self.height)
		p.line_width = self.border_width
		ui.set_color(self.border_color)
		p.stroke()
	
	def do_dropbox(self, sender=None):
		self.dropbox.hidden = not self.dropbox.hidden
		self.drop_button.enabled = self.dropbox.hidden

	def index_changed(self, sender):
		new_index = sender.selected_row
		if new_index != -1:
			self.selected_index = new_index
			self.do_dropbox()
			

class ComboBoxDataSource (object):
	def __init__(self, data, font, text_color, bg_color, 
							 action, selected_index, highlight_color):
		if not type(data) is list and not all(type(i) == str for i in data):
			raise ValueError('Data must be list of strings')
		self.items = data
		self.font = font
		self.text_color = text_color
		self.bg_color = bg_color
		self.selected_row = selected_index
		self.action = action
		self.cells = []
		self.highlight_color = highlight_color
						
	def tableview_number_of_sections(self, tableview):
		return 1
	
	def tableview_number_of_rows(self, tableview, section):
		return len(self.items)
	
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.selectable = True
		cell.text_label.alignment = ui.ALIGN_CENTER
		cell.text_label.font = self.font
		cell.text_label.text_color = self.text_color
		cell.text_label.text = self.items[row]
		cell.background_color = self.bg_color
		highlight_view = ui.View(frame=cell.bounds, bg_color=self.highlight_color)
		cell.objc_instance.setSelectedBackgroundView_(highlight_view.objc_instance)
		self.cells.append(cell)
		return cell

	def tableview_can_delete(self, tableview, section, row):
		return False
	
	def tableview_can_move(self, tableview, section, row):
		return False
	
	def tableview_did_select(self, tableview, section, row):
		self.selected_row = row
		self.action(self)
	
	def reload_cells(self):
		for cell in self.cells:
			cell.text_label.font = self.font
			cell.text_label.text_color = self.text_color
			highlight_view = ui.View(frame=cell.bounds, bg_color=self.highlight_color)
		cell.objc_instance.setSelectedBackgroundView_(highlight_view.objc_instance)


if __name__ == "__main__":
	import string
	root = ui.View(bg_color="white")
	combo = ComboBox(root,
									 bg_color="#cdcdcd",
									 choices=list(string.ascii_letters),
									 corner_radius=5,
									 button_tint='#6f6f6f',
									 highlight_color='#616f0b',
									 selected_index=0,
									 frame=(50, 50, 275, 40))
	
	def change_items(sender):
		sender.title = combo.selected_text
		
	btn = ui.Button(bg_color='grey',
									action=change_items,
									frame=(50, 300, 50, 50))
	root.add_subview(combo)
	root.add_subview(btn)
	root.present('popover', hide_title_bar=True)
	

