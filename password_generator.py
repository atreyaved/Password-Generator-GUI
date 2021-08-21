import string
import pyperclip
import secrets
import time 

class PasswordGenerator:
	def __init__(self):
		super(PasswordGenerator, self).__init__()

		self.abc = string.ascii_lowercase
		self.ABC = string.ascii_uppercase
		self.digits = string.digits
		self.punctuation = string.punctuation

		self.all_char = self.ABC + self.abc + self.digits + self.punctuation

	def generate_password(self, length = 15, chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": True}, repeated_char=False, consecutive_char=False):
		all_char = {
			"lowercase": self.abc, 
			"uppercase": self.ABC, 
			"digits": self.digits * 3 if not consecutive_char else self.digits * 2, 
			"punctuation": self.punctuation, 
		}

		selected_char_static = {}

		for k, v in chars.items():
			if k in all_char and v:
				selected_char_static[k] = all_char[k]
		
		selected_char = selected_char_static
		password = ""
		options = "".join(selected_char.values())
		removed = ""

		if not any(v for v in selected_char_static.values()):
			return "", "Please select at least one type of characters."

		for i in range(length):
			if not any(v for v in selected_char.values()): 
				if not repeated_char:
					return password, "Couldn't reach requested lenght because repeated characters is disabled."

				selected_char = selected_char_static
			
			if not options: options = "".join(selected_char.values())
		
			nchar = secrets.choice(options)

			password += nchar

			if not repeated_char:
				selected_char = {k:v.replace(nchar, "") for k, v in selected_char.items()}
			
			if not consecutive_char:
				options = "".join({key:val for key, val in selected_char.items() if key != self.char_type(nchar)}.values())

			if removed != "":
				options += selected_char[removed]

			removed = self.char_type(nchar)	

		return password, ""

	def ispunct(self, char):
		return char in self.punctuation

	def isequal(self, char1, char2):
		if char1.islower() and char2.islower():
			return True
		elif char1.isupper() and char2.isupper():
			return True
		elif char1.isdigit() and char2.isdigit():
			return True
		elif self.ispunct(char1) and self.ispunct(char2):
			return True
		else:
			return False

	def char_type(self, char):
		if char.isupper():
			return "uppercase"
		elif char.islower():
			return "lowercase"
		elif char.isdigit():
			return "digits"
		elif self.ispunct(char):
			return "punctuation"
		return False


def generate_password(chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": True}, length=15, repeated_char=False, consecutive_char=False):
	passwordGenerator = PasswordGenerator()
	password = passwordGenerator.generate_password(chars=chars, length=length, repeated_char=repeated_char, consecutive_char=consecutive_char)

	return password

def main():
	begin = time.time()
	loop = 10

	for i in range(loop):
		password = generate_password(chars={"lowercase": True, "uppercase": True, "digits": True, "punctuation": True}, length=15, repeated_char=False, consecutive_char=False)

		pyperclip.copy(password)

		print(f"\n{password} Length:{len(password)}\n")

	time_ = time.time() - begin

	print(f"Time: {time_}\nAverage: {time_/loop}")

if __name__ == "__main__":
	main()

