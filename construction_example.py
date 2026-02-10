#Use class level attributes
#number of wheels on a car, Pi constant, configuartion shared by all instances, version numbers

class Car:
    wheels = 4 #same for all cars as a default

'''
These attributes lives on the class , not the object

use constructor (_init_) for instance specific data. They are unique per object

examples: car color, max speed, current car, registration number'''

class Car:
    wheels = 4 

    def _init_(self, color, max_speed)
        self.color = color
        self.max_speed = max_speed
        self.current_speed = 0

'''
everytime time you create a new object, constructor (_init_) runs and gives that specific object its own attributes
why not put object-specific attribute in the root? because attributes in the root are shared unless overwritten

example:'''

class person:
    hobbies = [] #shared list

p1 = person ()
p2 = person ()

p1.hobbies.append("Football")
p1.hobbies.append("Reading")
p2.hobbies.append("Making music")
print(p2.hobbies) #they share the same list, thats not what we want

'''
if the list was inside _init_ , each would get its own list.
'''

class Student:
    def __init__(self):
        self.hobbies =[]

s1 = Student()
s2 = Student()

s1.hobbies.append("Ballet")
s2.hobbies.append("Gym")
