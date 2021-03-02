import ui
import numpy as np
from PIL import Image
from io import BytesIO


class Joystick(ui.View):
	class joystickImage(ui.View):
		def __init__(self, **kwargs):
			kwargs.setdefault("tint_color", "black")
			super().__init__(**kwargs)

		def draw(self):
			if self.tint_color != (0, 0, 0, 1):
				pil = Image.open("iow:pinpoint_256")
				arr = np.asarray(pil)
				arr = np.where(arr == [255, 255, 255, 255],
											 [int(i * 255.) for i in self.tint_color],
											 [255, 255, 255, 0])
				img = Image.fromarray(arr.astype("uint8"))
				img = self.pil2ui(img)
			else:
				img = ui.Image("iow:pinpoint_256")
			img.draw(-.08 * self.superview.width,
							 -.08 * self.superview.width,
							 1.16 * self.superview.width,
							 1.16 * self.superview.width)

		@staticmethod
		def pil2ui(imgIn):
			with BytesIO() as bIO:
				imgIn.save(bIO, "PNG")
				imgOut = ui.Image.from_data(bIO.getvalue())
			del bIO
			return imgOut

	def __init__(self, **kwargs):
		self.action = None
		self.stick = Joystick.joystickImage(name="stick",
																				frame=(0, 0, self.width, self.height))
		if "texture_color" in kwargs.keys():
			self.stick.tint_color = kwargs.pop("texture_color")

		kwargs.setdefault("background_color", "white")
		kwargs.setdefault("tint_color", "grey")
		kwargs.setdefault("frame", (50, 50, 100, 100))
		super().__init__(**kwargs)

		if self.width != self.height:
			raise ValueError("Joystick frame must be square...")

		self.radius = self.width / 2
		self.corner_radius = self.radius
		self.stick.corner_radius = self.corner_radius
		self.stick.touch_enabled = False
		self.stick.flex = "WH"
		self.originalPosition = self.stick.center
		self.objc_instance.setClipsToBounds_(False)
		self.add_subview(self.stick)

	def touch_moved(self, touch):
		touch = touch.location
		touchVec = touch - [self.radius] * 2
		vecMagn = abs(touchVec)
		if vecMagn < self.radius and self.bounds.contains_point(touch):
			self.stick.center = touch
		else:
			self.stick.center = touchVec / vecMagn * self.radius + [self.radius] * 2
		if self.action:
			self.action(touchVec)

	def touch_ended(self, touch):
		self.stick.center = self.originalPosition

	@property
	def tint_color(self):
		return self._tint_color

	@tint_color.setter
	def tint_color(self, value):
		self._tint_color = value
		self.stick.bg_color = value
		return

	def layout(self):
		if self.width != self.height:
			raise ValueError("Joystick frame must be square...")
		self.radius = self.width / 2
		self.corner_radius = self.radius
		self.stick.corner_radius = self.corner_radius
		self.originalPosition = self.stick.center
		self.stick.frame = (0, 0, self.width, self.height)


if __name__ == "__main__":
	x, y = ui.get_screen_size()

	j = Joystick(name="joystick",
							 tint_color="grey",
							 texture_color="blue",
							 frame=(x / 2 - 75, y / 2 - 150, 50, 50))
	root = ui.View(frame=(0, 0, x, y),
							   bg_color="white")

	def closeRoot(sender):
		root.close()
		return

	btn = ui.Button(name="button",
									frame=(50, 50, 25, 25),
									image=ui.Image("iob:close_32"),
									tint_color = "red",
									action = closeRoot)
	label = ui.Label(name="label",
									 frame=(x - 175, 50, 200, 20),
									 text = "x, y")

	def moveButton(touchVec):
		magn = abs(touchVec)
		if magn > 80:
			scale = 80 / magn
			touchVec.x *= scale
			touchVec.y *= scale
		btn.center += touchVec / 10
		label.text = f"{btn.center.x:.4f}"
		label.text += f",{btn.center.x:.4f}"

	j.action = moveButton

	root.add_subview(j)
	root.add_subview(btn)
	root.add_subview(label)
	root.present("popover", hide_title_bar=True)

