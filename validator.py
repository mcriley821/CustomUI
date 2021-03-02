import objc_util as objc


UIFont = objc.ObjCClass('UIFont')
FONT_FAMILIES = [i.cString().decode() for i in UIFont.familyNames()]
FONT_FAMILIES.extend(['<System>', '<System-Bold>'])

UIColor = objc.ObjCClass('UIColor')


def validate_font(value):
	if type(value) is tuple and len(value) == 2:
		x, y = value
		if isinstance(y, (int, float)) and type(x) is str:
			if x in FONT_FAMILIES and y > 0:
				return True
	return False


def validate_color(value):
	if type(value) is str:
		if len(value) == 7 or len(value) == 9 and value[0] == '#':
			if all(i in '0123456789abcdef' for i in value[1:]):
				return True
		elif UIColor.colorWithName_(value):
			return True
	elif type(value) is tuple:
		if 3 <= len(value) <= 4  and all(isinstance(i, (int, float)) for i in value):
			if all(0 <= i <= 1 for i in value):
				return True
	elif type(value) == type(None):
		return True
	return False


if __name__ == '__main__':
	print('Validating fonts')
	print(validate_font(4))
	print(validate_font((4,)))
	print(validate_font(('test', 'test')))
	print(validate_font(('temp', 4)))
	print(validate_font(('temp', 4.0)))
	print(validate_font(('<System>', 12)))
	print(validate_font(('Arial Rounded MT Bold', '4')))
	print('\nValidating colors')
	print(validate_color(5))
	print(validate_color('test'))
	print(validate_color((3, 4)))
	print(validate_color((3, 4, 5)))
	print(validate_color((1, 1, 0, 0)))
	print(validate_color(''))
	print(validate_color(None))
	print(validate_color('blue'))
	print(validate_color('#shei2729'))
	print(validate_color('#95ffb4'))
	print(validate_color('#95ffb4ff'))
	print(validate_color('#ahahsb'))
	print(validate_color('#abababa'))
