from typing import Any, Iterator
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

    def __getitem__(self, index: tuple[int|slice, int|slice] | int | slice) -> 'Matrix':

        # return while only 'int' given
        if(isinstance(index, int)): return Matrix([[self.get_item(index)]])
        
        # return while only 'slice' given
        if(isinstance(index, slice)):
            start = index.start
            stop = index.stop
            step = index.step if (index.step != None) else 1
            return Matrix([[ self.get_item(i) for i in range(start, stop, step) ]])

        if(not isinstance(index, tuple)): raise ValueError("None arguments given match __getitem__; Nothing returned")

        # return if 'int, slice' or 'int,  int'
        if(isinstance(index[0], int)):
            if(index[0] >= self.rows): raise ValueError("Index out of range")
            if(isinstance(index[1], int)):
                if(index[1] >= self.columns): raise ValueError("Index out of range")
                return self[index[0]*self.columns + index[1]]
            if(isinstance(index[1], slice)):
                return self[ (index[0]*self.columns):((index[0]+1)*self.columns)]
        
        # return if 'slice, int'
        if(isinstance(index[0], slice) and isinstance(index[1], int)):
            if(index[1] >= self.columns): raise ValueError("Index out of range")
            return self[ index[1]:(self.columns*self.rows):self.columns]

        raise ValueError("None arguments given match __getitem__; Nothing returned")
    
    def __setitem__(self, index: tuple[int|slice, int|slice] | int | slice, other: 'list[Any] | Any | Matrix' ) -> None:
        # handle list assignments
        if(isinstance(other, (list, Matrix))):

            # set while only 'slice' given
            if(isinstance(index, slice)):
                start = index.start
                stop = index.stop
                step = index.step if (index.step != None) else 1
                # [ self.get_item(i) for i in range(start, stop, step) ]

                if(abs(stop-start) != len(other)-1): raise ValueError("List length missmatch")

                for i in range(start, stop, step):
                    self.__data[i // self.columns][i % self.columns] = other[i]
                return
            
            # set if 'int, slice'
            if(not isinstance(index, tuple)): raise ValueError("None arguments given match __setitem__; Nothing set")
            if(isinstance(index[0], int) and isinstance(index[1], slice)):
                if(index[0] >= self.rows): raise ValueError("Index out of range")
                if(len(other) != self.columns): raise ValueError("List length missmatch")
                for i in range(self.columns):
                    self.__data[index[0]][i] = other[i]
                return
            
            # set if 'slice, int'
            if(isinstance(index[0], slice) and isinstance(index[1], int)):
                if(index[1] >= self.columns): raise ValueError("Index out of range")
                if(len(other) != self.rows): raise ValueError("List length missmatch")
                for i in range(self.rows):
                    self.__data[i][index[1]] = other[i]
                return 

            raise ValueError("None arguments given match __setitem__; Nothing set")


        # set while only 'int' given
        if(isinstance(index, int)): 
            self.__data[index // self.columns][index % self.columns] = other
            return 
        
        # set while only 'slice' given
        if(isinstance(index, slice)):
            # stes all item to other
            if((index.start == None) and (index.stop == None) and (index.step == None)):
                self.__data = [ [other for j in range(self.columns)]  for i in range(self.rows) ]
                return
            start = index.start
            stop = index.stop
            step = index.step if (index.step != None) else 1
            for i in range(start, stop, step):
                self.__data[i // self.columns][i % self.columns] = other
            return

        if(not isinstance(index, tuple)): raise ValueError("None arguments given match __setitem__; Nothing set")

        # set if 'int, slice' or 'int,  int'
        if(isinstance(index[0], int)):
            if(index[0] >= self.rows): raise ValueError("Index out of range")
            if(isinstance(index[1], int)):
                if(index[1] >= self.columns): raise ValueError("Index out of range")
                self.__data[index[0]][index[1]] = other
                return
            if(isinstance(index[1], slice)):
                for i in range(self.columns):
                    self.__data[index[0]][i] = other
                return
        
        # set if 'slice, int'
        if(isinstance(index[0], slice) and isinstance(index[1], int)):
            if(index[1] >= self.columns): raise ValueError("Index out of range")
            for i in range(self.rows):
                self.__data[i][index[0]] = other
            return


        raise ValueError("None arguments given match __setitem__; Nothing set")

    def __len__(self) -> int:
        return self.rows*self.columns
    
    def __iter__(self) -> Iterator:
        for i in range(len(self)):
            yield self.get_item(i)

    def get_item(self, index: int) -> Any:
        return self.__data[index // self.columns][index % self.columns]

    def transpose(self) -> 'Matrix':
        return Matrix([[self.__data[j][i] for j in range(self.rows)]  for i in range(self.columns)])
    
    def transpose_self(self) -> None:
        self.__data = [[self.__data[j][i] for j in range(self.rows)]  for i in range(self.columns)]
        a = self.columns
        self.columns = self.rows
        self.rows = a

