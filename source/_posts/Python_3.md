---
title: Python Note 3
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Python
tags: 
- Python
- Note
---
# Python Note 3

### Classes
> Use Pacal naming convertion,not like variables/function use lower cases and underscore connection.
> Basic usage:

```python
class Point:
	def draw(self):
		print("draw")

	def print(self):
		print("this is point")


point1 = Point()
point1.x = 5
point1.draw()
print(point1.x)
```

### Constructor

```python
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self):
		print("draw")

	def print(self):
		print("this is point")


point1 = Point(10, 5)
point1.draw()
print(point1.x)

#exercise
class Person:
	def __init__(self, name):
		self.name = name

	def talk(self):
		print(f"{self.name} is talking..")


while True:
	person_name = str(input("Please enter person: "))
	if person_name == "Quit":
		break
	elif person_name != "":
		new_person = Person(person_name)
		new_person.talk()
	else:
		print("You enter a empty!")

```

### inheritance
> use bracket to inherit parent class

```python
class Mammal:
	def walk(self):
		print("walk")


class Dog(Mammal):
	def bark(self):
		print("bark")


class Cat(Mammal):
	pass  # tell python to pass this line


dog1 = Dog()
dog1.walk()
dog1.bark()

```

### module
> each file refer a module

```python
import converters #to import converters.py
from converters import kg_to_lbs

#exercise
import  convertors
from convertors import weight_to_lbs

print(weight_to_lbs())
numbers = [5,1,8,2]
maximum = convertors.find_max(numbers)
print(max(numbers))
```

### package
> a set of modules: directory with "__init__.py" file

```python
from ecommerce.shopping import test
from ecommerce import shopping
test()
shopping.test()
```

### use python build-in module
> search [python module index](https://docs.python.org/3/py-modindex.html)
> PEP: python enhancement proposal

```python
import  random
members = ["Jack", "Rose", "Bob", "Avery", "Mosh"]
m = random.choice(members)
print(m)

#exercise
import random
class Dice: #will get PEP 8 warning
    def roll(self):
        r1 = random.randint(0, 5)
        r2 = random.randint(0, 5)
        return r1,r2  #Python will auto make it to Tuple



mydice = Dice()
print(mydice.roll())
```

```python
from pathlib import Path

path = Path("pydemo2/ecommerce")
for p in path.glob("*.py"):
    print(p)

```

### 使用type直接拿到类句柄

+ 以type取得的值为句柄创建一个新的对象
```python
result = type(self)(self.a)
```