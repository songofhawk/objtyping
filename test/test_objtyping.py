import json
import sys
from ruamel.yaml import YAML
from typing import List
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
    print("\r\n-----json-------")
    json_obj = json.loads('{"q":9, "a":"Mark", "b":3, "c":[{"x":15, "y":"male"},{"x":9, "y":"female", "z":13}]}')
    typed_obj = objtyping.from_dict_list(json_obj, A)
    d_l_obj = objtyping.to_dict_list(typed_obj)
    print(json.dumps(d_l_obj))

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
    typed_obj = objtyping.from_dict_list(yaml_obj, A)
    d_l_obj = objtyping.to_dict_list(typed_obj)
    yaml.dump(d_l_obj, sys.stdout)

    sys.exit()
