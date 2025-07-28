from typing import List

@staticmethod
def get_criterions(self) -> List:
    return list(self.conditions) + list(self.exceptions) + list(self.restrictions)