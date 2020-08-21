from dataclasses import dataclass

@dataclass
class Data:
	name: str = ""
	age: int = 0
	number: int = 0

	def getName(self):
		return self.name

	def getAge(self):
		return self.age

	def getNumber(self):
		return self.number

d = Data("JD", 1, 2)

print(d.getName())
print(d.getAge())
print(d.getNumber())