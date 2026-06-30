import logging
from library.emp_factory import Employer, Manager, QaEngineer, Intern, Employee

logger = logging.getLogger(__name__)


class TestEmployeeFactory:
    
    def test_factory_creates_correct_type(self):
        logger.info("Starting factory type creation test")
        manager = Employer.create_employee("Bob", "manager")
        qa = Employer.create_employee("Jane", "QA Engineer")
        intern = Employer.create_employee("Alice", "intern")
        dev = Employer.create_employee("John", "developer")

        assert isinstance(manager, Manager)
        logger.info("Successfully created and verified Manager object")
        assert isinstance(qa, QaEngineer)
        logger.info("Successfully created and verified QA Engineer object")
        assert isinstance(intern, Intern)
        logger.info("Successfully created and verified Intern object")
        assert isinstance(dev, Employee)
        assert type(dev) is Employee
        logger.info("Successfully verified fallback to default Employee object")

    def test_employee_ids_are_unique_and_incrementing(self):
        logger.info("Starting unique ID increment test")
        emp1 = Employer.create_employee("Emp1", "test")
        logger.info(f"Created first employee with ID: {emp1.id}")
    
        emp2 = Employer.create_employee("Emp2", "test")
        logger.info(f"Created second employee with ID: {emp2.id}")

        assert emp1.id < emp2.id
        assert emp2.id == emp1.id + 1
        logger.info(f"Successfully verified the employee ID's are unique and incrementing sequentially")

    def test_polymorphism_work_method(self):
        logger.info(f"starting polymorphsim work() method test")
        qa = Employer.create_employee("Jane", "qa engineer")
        intern = Employer.create_employee("Alice", "intern")
        manager = Employer.create_employee("Bob", "manager")

        assert qa.work() == "Jane is testing the application"
        logger.info(f"QA Engineer work(): '{qa.work()}'")
        assert intern.work() == "Alice is learning something"
        logger.info(f"Intern work(): '{intern.work()}'")
        assert manager.work() == "Bob is managing team"
        logger.info(f"Manager work(): '{manager.work()}'")

    def test_employee_details_format(self):
        logger.info("Starting employee details dictionary format test")
        qa = Employer.create_employee("Jane", "qa engineer")
        details = qa.employee_details()
        logger.info(f"QA Engineer Employee Details : {details}, {type(details)}")

        assert isinstance(details, dict)

        assert details.get("Name").lower() == "jane"
        assert details.get("Role").lower() == "qa engineer"
        logger.info("Validated Base Employee Details (Name, Role)")
        
        assert "pytest" in details["Known Tools"]
        assert "python" in details["Known Tools"]
        logger.info("Validated inherited subclass details (Tools list)")

