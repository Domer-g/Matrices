from typing import Any, Iterator
# https://www.pythonmorsels.com/every-dunder-method/#context-managers

class Matrix:
    def __Matrix_same_size_check(A: 'Matrix', B: 'Matrix') -> bool: # type: ignore
        if(A.rows != B.rows): return False
        if(A.columns != B.columns): return False
        return True


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

    def __getitem__(self, index: tuple[int|slice, slice|int] | int | slice) -> 'Matrix | Any':
        """Gets an entry from the matrix.        
        - If (int), returns the stored value at that position. (look iterator for indexing)
        - If (slice), returns a Matrix containing elements of coresponding indecies.
        - If (int, int), returns the stored value at that position.
        - If (int, slice), returns a row as a Matrix.
        - If (slice, int), returns a column as a Matrix.
        """

        # return while only 'int' given; returns any
        if(isinstance(index, int)): return self.get_item(index)
        
        # return while only 'slice' given; returns matrix
        if(isinstance(index, slice)):
            start = index.start
            stop = index.stop
            step = index.step if (index.step != None) else 1
            return Matrix([[ self.get_item(i) for i in range(start, stop, step) ]])

        if(not isinstance(index, tuple)): raise ValueError("None arguments given match __getitem__; Nothing returned")

        # return if 'int, slice' or 'int,  int'
        if(isinstance(index[0], int)):
            if(isinstance(index[1], int)): return self[ index[0]*self.columns + index[1] ]
            if(isinstance(index[1], slice)): return self[ (index[0]*self.columns):((index[0]+1)*self.columns) ]
        
        # return if 'slice, int'
        if(isinstance(index[0], slice) and isinstance(index[1], int)): 
            return self[ index[1]:(self.columns*self.rows):self.columns ]

        raise ValueError("None arguments given match __getitem__; Nothing returned")
    
    def __setitem__(self, index: tuple[int|slice, int|slice] | int | slice, other: 'list[Any] | Any | Matrix' ) -> None:
        """
        Allows for setting values
        - [int] - set from index of entry (look iterator for indexing)
        - [slice] - sets all entries to other, or only the slice when given a list
        - [int, int] - sets the given entry to other
        - [int, slice] - sets the row to other. List/matrix or any
        - [slice, int] - sets the column to other. List/matrix or any
        """
        # handle list assignments
        if(isinstance(other, (list, Matrix))):

            # set while only 'slice' given
            if(isinstance(index, slice)):
                start = index.start
                stop = index.stop
                step = index.step if (index.step != None) else 1

                if(abs(stop-start) != len(other)-1): raise ValueError("List length missmatch")

                for i in range(start, stop, step): self.__setitem(i, other[i])
                return
            
            # set if 'int, slice'
            if(not isinstance(index, tuple)): raise ValueError("None arguments given match __setitem__; Nothing set")
            
            if(isinstance(index[0], int) and isinstance(index[1], slice)):
                if(len(other) != self.columns): raise ValueError("List length missmatch")
                for i in range(self.columns):
                    self.__data[index[0]][i] = other[i]
                return
            
            # set if 'slice, int'
            if(isinstance(index[0], slice) and isinstance(index[1], int)):
                if(len(other) != self.rows): raise ValueError("List length missmatch")
                for i in range(self.rows):
                    self.__data[i][index[1]] = other[i]
                return 

            raise ValueError("None arguments given match __setitem__; Nothing set")


        # set while only 'int' given
        if(isinstance(index, int)): 
            self.__setitem(index, other)
            return 
        
        # set while only 'slice' given
        if(isinstance(index, slice)):
            # stes all item to other
            if((index.start == None) and (index.stop == None) and (index.step == None)):
                self.__data = [ [other for j in range(self.columns)] for i in range(self.rows) ]
                return
            start = index.start if (index.step != None) else 0
            stop = index.stop if (index.step != None) else len(self)
            step = index.step if (index.step != None) else 1
            for i in range(start, stop, step):
                self.__setitem(i, other)
            return

        if(not isinstance(index, tuple)): raise ValueError("None arguments given match __setitem__; Nothing set")

        # set if 'int, slice' or 'int,  int'
        if(isinstance(index[0], int)):
            if(isinstance(index[1], int)):
                self.__data[index[0]][index[1]] = other
                return
            if(isinstance(index[1], slice)):
                for i in range(self.columns):
                    self.__data[index[0]][i] = other
                return
        
        # set if 'slice, int'
        if(isinstance(index[0], slice) and isinstance(index[1], int)):
            for i in range(self.rows):
                self.__data[i][index[1]] = other
            return

        raise ValueError("None arguments given match __setitem__; Nothing set")

    def __len__(self) -> int:
        """Return the number of entries in the matrix"""
        return self.rows*self.columns
    
    def __iter__(self) -> Iterator:
        """Iterates over all matrix entries starting from A[0,0] and going like this A[0,1], A[0,2]..."""
        for i in range(len(self)):
            yield self.get_item(i)

    def __str__(self) -> str:
        str_max_len: int = max([len(str(i)) for i in self])
        out_string: str = '|-' + self.columns*str_max_len*' ' + (self.columns-1)*' ' + '-'
        for  i, elem in enumerate(self):
            if(i%self.columns == 0): out_string += '|\n| '
            temp_str = str(elem)
            out_string += temp_str + (str_max_len - len(temp_str) + 1)*' '
        out_string += '|\n|-' + self.columns*str_max_len*' ' + (self.columns-1)*' ' + '-|'

        return out_string

    def __repr__(self) -> str:
        return f"{self.rows}x{self.columns} Matrix"

    def get_item(self, index: int) -> Any:
        return self.__data[index // self.columns][index % self.columns]
    
    def get_item2(self, index0: int, index1: int) -> Any:
        return self.__data[index0][index1]

    def transpose(self) -> 'Matrix':
        """Returns a transposed matrix without changing the oryginal"""
        return Matrix([[self.__data[j][i] for j in range(self.rows)]  for i in range(self.columns)])
    
    def transpose_self(self) -> None:
        """Changes the oryginal matrix to be transposed"""
        self.__data = [[self.__data[j][i] for j in range(self.rows)]  for i in range(self.columns)]
        a = self.columns
        self.columns = self.rows
        self.rows = a

    def __setitem(self, index: int, other: Any) -> None:
        self.__data[index // self.columns][index % self.columns] = other

    def __setitem2(self, index0: int, index1: int, other: Any) -> None:
        self.__data[index0][index1] = other

    # Arthmetic operations
    def __add__(self, other: 'Matrix | Any') -> 'Matrix':
        if(isinstance(other, Matrix)):
            if(not Matrix.__Matrix_same_size_check(self, other)): raise ValueError("Cannot add matrices that are not of the same dimention")
            outcome: Matrix = Matrix(self)
            for i, elem in enumerate(other): outcome.__setitem(i, outcome.get_item(i)+elem)
            return outcome
        
        outcome: Matrix = Matrix(self)
        for i, _ in enumerate(self): outcome.__setitem(i, outcome.get_item(i)+other)
        return outcome
    
    def __sub__(self, other: 'Matrix | Any') -> 'Matrix':
        if(isinstance(other, Matrix)):
            if(not Matrix.__Matrix_same_size_check(self, other)): raise ValueError("Cannot add matrices that are not of the same dimention")
            outcome: Matrix = Matrix(self)
            for i, elem in enumerate(other): outcome.__setitem(i, outcome.get_item(i)-elem)
            return outcome
        
        outcome: Matrix = Matrix(self)
        for i, _ in enumerate(self): outcome.__setitem(i, outcome.get_item(i)-other)
        return outcome
    
    def __mul__(self, other: 'Matrix | Any') -> 'Matrix':
        if(isinstance(other, Matrix)):
            if(self.columns != other.rows): 
                if(self.columns == other.columns):
                    print("-------------------- ERROR --------------------\nSECOND MATRIX WAS NOT TRANPOSED!")
                    other.transpose_self()
                else:
                    raise ValueError("Cannot add matrices that are not of the same dimention")
            outcome: Matrix = Matrix(self.rows, other.columns)
            other.transpose_self()
            for i, row_self in enumerate(self.__data):
                for j, col_other in enumerate(other.__data):
                    for a, b in zip(row_self, col_other):
                        outcome.__setitem(i*outcome.columns+j, outcome.get_item(i*outcome.columns+j)+a*b)

            other.transpose_self()
            return outcome
        
        outcome: Matrix = Matrix(self)
        for i, _ in enumerate(self): outcome.__setitem(i, outcome.get_item(i)*other)
        return outcome

    def __truediv__(self, other: Any) -> 'Matrix':     
        outcome: Matrix = Matrix(self)
        for i, _ in enumerate(self): outcome.__setitem(i, outcome.get_item(i)/other)
        return outcome
    
    def __mod__(self, other: Any) -> 'Matrix':     
        outcome: Matrix = Matrix(self)
        for i, _ in enumerate(self): outcome.__setitem(i, outcome.get_item(i)%other)
        return outcome

    def __floordiv__(self, other: Any) -> 'Matrix':
        outcome: Matrix = Matrix(self)
        for i, _ in enumerate(self): outcome.__setitem(i, outcome.get_item(i//other))
        return outcome

    def __pow__(self, other: int) -> 'Matrix':
        if(self.columns != self.rows): raise ValueError("Cannot rive a non square matrix to a poewer")
        if(other < 0): raise NotImplementedError("Rising a matrix to a negative power not implemented")
        if(other == 0): 
            outecome: Matrix = Matrix(self)
            outecome[:] = 0
            for i in range(self.columns): outecome.__setitem(i*outecome.columns + i, 1)
            return outecome
        outecome: Matrix = Matrix(self)
        other -= 1
        for i in range(other): outecome *= self
        return outecome
    
    def perform_operation(self, func) -> 'Matrix':
        """Perform operation from a given function on all its elements and returns other matrix"""
        outcome: Matrix = Matrix(self)
        for i, elem in enumerate(outcome):
            outcome.__setitem(i, func(outcome.get_item(i)))
        return outcome
    
    def perform_operation_self(self, func) -> None:
        """Perform operation from a given function on all its elements"""
        for i, elem in enumerate(self):
            self.__setitem(i, func(self.get_item(i)))
        return 