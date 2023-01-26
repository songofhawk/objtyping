import sys
from typing import List

from ruamel.yaml import YAML

from objtyping import objtyping


class X:
    x: int
    y: str


class A:
    q: str
    a: str
    b: int
    c: List[X]


if __name__ == '__main__':
    print("\r\n-----yaml-------")
    yaml = YAML()
    yaml_obj = yaml.load('''
    q: 9
    a: Mark
    b: 3
    c:
        - x: 15
          y: male
        - x: 9
          y: female
          z: 13    
    ''')
    typed_obj = objtyping.from_primitive(yaml_obj, A)
    d_l_obj = objtyping.to_primitive(typed_obj)
    yaml.dump(d_l_obj, sys.stdout)

    sys.exit()
