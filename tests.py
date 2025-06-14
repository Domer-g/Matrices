import numpy as np
from main import *

def main():
    cols = 8
    rows = 10
    data = [ [cols*i+j for j in range(cols)]  for i in range(rows) ]
    A = Matrix(data)
    print(A)
    B = Matrix(A)
    print(B)
    B = A[1:47]
    print(B)
    B = A[1,:]
    print(B)
    B = A[3,:]
    print(B)
    B = A[:,0]
    print(B)
    B = A[:,A.columns-1]
    print(B)

    B = A.transpose()
    print(B)
    B.transpose_self()
    print(B)

    # assing test
    #B[0] = [123123, 12] #error
    B[0] = 12
    print(B)
    #B[0,0] = [1,23,4] #error
    B[0,0] = 123 
    print(B)

    B[0:6] = [2,3,4,5,6,7,8]
    print(B)

    B[0,:] = 0
    print(B)
    B[:] = 0 # sets all to 0
    print(B)

    B[:,0] = [134, 134, 134, 134, 134, 134, 134, 134, 134, 134] # sets column
    B[3,:] = [555, 555, 555, 555, 555, 555, 555, 555] # sets row
    print(B)

    B = A
    print(B)
    B[:] = 0 # sets all to 0
    print(B)
    from math import exp
    B = B.perform_operation(lambda x: exp(x))
    print(B)

    A = Matrix([[2,0,3],[0,2,1]])
    print(A)
    B = Matrix([[1,0],[1,1],[2,3]])

    print(A)
    print(B)

    C = A*B
    print(C)
    return

def rank_test():
    from random import randint

    for i in range(1000):
        A = Matrix(randint(1,40), randint(1,40))
        A.perform_operation_self(lambda x: randint(-40,40))

        B:np.matrix = np.matrix(A._Matrix__data) # type: ignore
        if(np.linalg.matrix_rank(B) != Check_rank(A)):
            print("WRONG!")
        

#main()
rank_test()