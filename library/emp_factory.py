class Employer:
    __next_id = 1000 # private

    def __init__(self):
        self.id = Employer.__next_id
        Employer.__next_id += 1

    # @classmethod
    # def get_next_id(cls):
    #     return cls.__next_id

    @classmethod
    def create_employee(cls, name, role):
        """creates right type of employee based on Role"""

        if role.lower() == "manager":
            return Manager(name)
        
        elif role.lower() == "intern":
            return Intern(name)
        
        elif role.lower() == "qa engineer":
            return QaEngineer(name)
        
        else:
            return Employee(name, role)
        
class Employee(Employer):
    def __init__(self, name, role="Employee"):
        super().__init__()
        self.name = name
        self.role = role

    def employee_details(self):
        return {
            "ID"    : self.id,
            "Name" : self.name,
            "Role"  : self.role
        }
    
    
    def work(self):
        return f"{self.name} is working"
    
class Manager(Employee):
    def __init__(self, name):
        super().__init__(name, "Manager")
        self.team = []

    def add(self):
        self.team.append(Employee.name)

    def work(self):
        return f"{self.name} is managing team"
    
    def employee_details(self):
        details = super().employee_details()
        details["Team"] = self.team
        return details
    
class Intern(Employee):
    def __init__(self, name):
        super().__init__(name, "Intern")
        self.duration = "6 months"

    def work(self):
        return f"{self.name} is learning something"
    
    def employee_details(self):
        details = super().employee_details()
        details["Duration"] = self.duration
        return details
    
class QaEngineer(Employee):
    def __init__(self, name):
        super().__init__(name, "QA Engineer")
        self.tools = ["python", "pytest", "selenium"]

    def work(self):
        return f"{self.name} is testing the application"
    
    def employee_details(self):
        details = super().employee_details()
        details["Known Tools"] = self.tools
        return details
    
emp1 = Employer.create_employee("John", "QA Engineer")
emp2 = Employer.create_employee("Dave", "Manager")
emp3 = Employer.create_employee("Bob",  "Intern")
emp4 = Employer.create_employee("Jane", "Developer")

print(emp1.employee_details())
print("─" * 30)
print(emp2.employee_details())
print("─" * 30)
print(emp3.employee_details())
print("─" * 30)
print(emp4.employee_details())
print("─" * 30)

# Polymorphism — same method, different behavior!
all_employees = [emp1, emp2, emp3, emp4]
for emp in all_employees:
    print(emp.work())

