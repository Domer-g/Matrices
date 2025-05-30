from typing import Any, Tuple
# https://www.pythonmorsels.com/every-dunder-method/#context-managers

class Matrix:
    def __init__(self, *creation_args: 'int | list[list[Any]] | Matrix') -> None:
        self.rows: int
        self.columns: int
        
        self.__data: list[list[Any]]

        if(isinstance(creation_args[0], int) and isinstance(creation_args[1], int)):
            self.rows = creation_args[0]
            self.columns = creation_args[1]

            self.__data = [ [0 for j in range(self.columns)]  for i in range(self.rows) ]
            return
        
        if(isinstance(creation_args[0], Matrix)):
            creation_args = (creation_args[0].__data,)

        if(isinstance(creation_args[0], list)):
            self.rows = len(creation_args[0])
            self.columns = len(creation_args[0][0])

            for row in creation_args[0]:
                if(len(row) != self.columns): raise ValueError("Given rows are not of the same lenght")

            self.__data = [ [creation_args[0][i][j] for j in range(self.columns)]  for i in range(self.rows) ]
            return
        
        raise ValueError("None arguments given match __init__; Matrix not created")
        
    