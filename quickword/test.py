class Person(object): 
      
    # Constructor 
    def __init__(self, name): 
        self.name = name 
  
    # To get name 
    def getName(self): 
        return self.name 
  
    # To check if this person is employee 
    def isEmployee(self): 
        return False
  
  
# Inherited or Sub class (Note Person in bracket) 
class Employee(Person): 
  
    # Here we return true 
    def isEmployee(self): 
        return True


  
emp = Employee("Geek2") # An Object of Employee 
print(emp.getName(), emp.isEmployee()) 

print(emp.name)