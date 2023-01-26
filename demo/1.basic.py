from typing import List

from objtyping import objtyping


class Person:
    name: str
    age: int


class Company:
    name: str
    revenue: float
    employees: List[Person]

    def __str__(self):  # 其实一般可能都是这样简单用一下的
        return "'{}' has {} employees: {}".format(self.name, len(self.employees), ' and '.join(map(lambda emp: emp.name, self.employees)))


if __name__ == '__main__':
    company1 = objtyping.from_primitive({
        'name': 'Apple',
        'revenue': 18.5,
        'employees': [{
            'name': 'Tom',
            'age': 20
        }, {
            'name': 'Jerry',
            'age': 31
        }]
    }, Company)

    print(company1)
