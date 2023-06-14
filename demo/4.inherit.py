from objtyping import objtyping


class Person:
    name: str = 'No name'
    age: int = 0


class Employee(Person):
    title: str = 'developer'


if __name__ == '__main__':
    emp = Employee()

    emp_primitive = objtyping.to_primitive(emp)

    print(emp_primitive)
