from summary.summary_container import *
from typing import List


class AbstractStorage:

    def __init__(self, file_path: List[str]):
        self._filename = os.path.join(os.getcwd(), *file_path)
        print(self._filename)

    def save(self, container: SummaryContainer):
        raise NotImplementedError()