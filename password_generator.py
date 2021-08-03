import random
import string
import pyperclip

class PasswordGenerator:
	def __init__(self):
		super(PasswordGenerator, self).__init__()

		self.abc = string.ascii_lowercase
		self.ABC = string.ascii_uppercase
		self.digits = string.digits
		self.punctuation = string.punctuation
		self.whitespace = string.whitespace		

	def generate_password(self, first=True, length = 15, chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace": False}):
		password = ""

		length = self.divide(length) if first else [length, length]

		for e, i in enumerate(random.sample(range(-99999, 99999), length[0])):
			password = self.add_char(password, chars=chars)

		password = self.mess_string( password + self.generate_password(first=False, length=length[1], chars=chars) if first else password )

		self.check_password(password)

		return password

	def add_char(self, password: str, chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace": False}):
		indx = len(password) - 1 

		char = self.random_char(chars=chars)

		password += char

		return password

	def divide(self, number, by=2):

		int_division = number // by
		if int_division * 2 != number:

			return [int_division, int_division +1]

		return [int_division] * 2

	def check_password(self, password):
		checks = [self.is_upper, self.is_lower, self.is_digit, self.is_punctuation, self.is_whitespace]

		for e, char in enumerate(password):
			for check in checks:
				pass

	def is_upper(self, char):
		return char.isupper() 

	def is_lower(self, char):
		return char.islower()

	def is_digit(self, char):
		return char in self.digits 

	def is_punctuation(self, char):
		return char in self.punctuation

	def is_whitespace(self, char):
		return char in self.whitespace 

	def random_char(self, chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace": False}):
		allList = []

		for k, v in chars.items():
			if k == "lowercase" and v:
				allList.append(self.abc)
			elif k == "uppercase" and v:
				allList.append(self.ABC)
			elif k == "digits" and v:
				allList.append(self.digits)
			elif k == "punctuation" and v:
				allList.append(self.punctuation)
			elif k == "whitespace" and v:
				allList.append(self.whitespace)


		nrandom = random.randint(0, len(allList)-1)
		lenList = len(allList[nrandom])
		return allList[ nrandom ][ random.randint(-99999, 99999) %  lenList] 

	def mess_string(self, myStr: str):
		myList = [i for i in myStr]

		result = random.sample(myList, len(myList))

		return "".join(result)

def generate_password(chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace": False}, length=15):
	passwordGenerator = PasswordGenerator()
	password = passwordGenerator.generate_password(chars=chars, length=15)

	return password


def main():

	passwordGenerator = PasswordGenerator()
	password = passwordGenerator.generate_password(chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": False, "whitespace": False}, length=15)
	# pyperclip.copy(result)

	print(password, len(password))

if __name__ == "__main__":
	main()

