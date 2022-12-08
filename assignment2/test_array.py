"""
Tests for our array class
"""

from array_class import Array

#getitem test:

def test_getitem(): #tests the element 3 against the expected value
    arrObj = Array((6,),2,4,2,6,8,10); solution = 6
    assert arrObj.__getitem__(3) == solution, 'Something went wrong with test_getitem()'

# 1D tests (Task 4)
    

def test_str_1d(): #tests whether __str__() returns the expected string
    arrObj = Array((6,),2,4,2,6,8,10); solution = '[2, 4, 2, 6, 8, 10]'
    assert arrObj.__str__() == solution, 'Something went wrong with test_str_1d()'


def test_add_1d(): #tests addition against expected solutions
    arrObj = Array((6,),2,4,2,6,8,10); solution = [7, 9, 7, 11, 13, 15]; solution2 = [3, 6, 5, 10, 13, 16]
    assert arrObj.__add__(5) == solution, 'Something went wrong with test_add_1d()' #adding an integer, floats work too
    
    assert arrObj.__add__((1,2,3,4,5,6)) == solution2, 'Something went wrong with test_add_1d()' #adding an array
    
    #full disclosure: I didn't really understand the reflection function and why we do it (cont.)
    #when __add__ing below seemingly(?) doesn't even call __add__ so I can't redirect it to __radd__ within the method (cont.)
    #and it has to be done outside(??)
    i = 5
    if str(i.__add__(arrObj)) == 'NotImplemented': #not my finest work
        assert arrObj.__radd__(i) == solution, 'Something went wrong with test_add_1d()' #__radd__ method, should also work with tuple arrays as above

def test_sub_1d(): #tests subtraction against expected solutions
    arrObj = Array((6,),2,4,2,6,8,10); solution = [-8, -6, -8, -4, -2, 0]; solution2 = [1, 2, -1, 2, 3, 4]
    assert arrObj.__sub__(10) == solution, 'Something went wrong with test_sub_1d()' #subtracting an integer, floats work too
    
    assert arrObj.__sub__((1,2,3,4,5,6)) == solution2, 'Something went wrong with test_sub_1d()' #subtracting an array
    
    i = 10
    if str(i.__sub__(arrObj)) == 'NotImplemented':
        assert arrObj.__rsub__(i) == solution, 'Something went wrong with test_sub_1d()' #__rsub__ method, should also work with tuple arrays as above

def test_mul_1d(): #tests multiplication against expected solutions
    arrObj = Array((6,),2,4,2,6,8,10); solution = [6, 12, 6, 18, 24, 30]; solution2 = [4, 16, 4, 36, 64, 100]
    assert arrObj.__mul__(3) == solution, 'Something went wrong with test_mul_1d()' #multiplying with an integer, floats work too
    
    assert arrObj.__mul__((2,4,2,6,8,10)) == solution2, 'Something went wrong with test_mul_1d()' #multiplying element-wise with an array
    
    i = 3
    if str(i.__mul__(arrObj)) == 'NotImplemented':
        assert arrObj.__rmul__(i) == solution, 'Something went wrong with test_sub_1d()' #__rmul__ method, should also work with tuple arrays as above

def test_eq_1d(): #tests if the expected value is returned when two arrays are compared
    arrObj = Array((6,),2,4,2,6,8,10); solution = True
    assert arrObj.__eq__((2,4,2,6,8,10)) == solution, 'Something went wrong with test_eq_1d()'

def test_same_1d(): #tests if the expected booleans are returned when two arrays are compared element-wise
    arrObj = Array((6,),2,4,2,6,8,10); solution = [True,False,True,False,False,False]
    assert arrObj.is_equal((2,2,2,2,2,2)) == solution, 'Something went wrong with test_same_1d()'
    
    assert arrObj.is_equal(2) == solution, 'Something went wrong with test_same_1d()'

def test_smallest_1d(): #tests if the returned element is the smallest element in an array
    arrObj = Array((6,),2,4,2,6,8,10); solution = 2
    assert arrObj.min_element() == solution, 'Something went wrong with test_smallest_1d()'


def test_mean_1d(): #tests if the returned value is the mean value of an array
    arrObj = Array((6,),2,4,2,6,8,10); solution = 16/3
    assert arrObj.mean_element() == solution, 'Something went wrong with test_mean_1d()'


# 2D tests (Task 6)


def test_add_2d(): #tests two dimensional addition against expected values
    arrObj = Array((2,5),2,4,6,1,2,3,7,8,9,10); solution = [8,10,12,7,8,9,13,14,15,16]; solution2 = [3,5,7,2,3,4,8,9,10,11]
    assert arrObj.__add__(6) == solution, 'Something went wrong with test_add_2d()'
    
    assert arrObj.__add__((1,1,1,1,1,1,1,1,1,1)) == solution2, 'Something went wrong with test_add_2d()'
    
    i = 6
    if str(i.__add__(arrObj)) == 'NotImplemented':
        assert arrObj.__radd__(i) == solution, 'Something went wrong with test_add_1d()' #__radd__ method, should also work with tuple arrays as above


def test_mult_2d(): #tests two dimensional multiplication against expected values
    arrObj = Array((2,5),1,2,3,4,5,6,7,8,9,10); solution = [2,4,6,8,10,12,14,16,18,20]; solution2 = [1,-2,3,-4,5,-6,7,-8,9,-10]
    assert arrObj.__mul__(2) == solution, 'Something went wrong with test_mul_2d()'
    
    assert arrObj.__mul__((1,-1,1,-1,1,-1,1,-1,1,-1)) == solution2, 'Something went wrong with test_mul_2d()'

    i = 2
    if str(i.__mul__(arrObj)) == 'NotImplemented':
        assert arrObj.__rmul__(i) == solution, 'Something went wrong with test_sub_1d()' #__rmul__ method, should also work with tuple arrays as above
    
    
def test_same_2d(): #tests if the expected booleans are returned when two 2D arrays are compared element-wise
    arrObj = Array((2,2),4,3,2,1); solution = [False,True,True,False]; solution2 = [False, False, True, False]
    assert arrObj.is_equal(([1,3],[2,4])) == solution, 'Something went wrong with test_same_2d()'
    
    assert arrObj.is_equal(2) == solution2, 'Something went wrong with test_same_2d()'

def test_mean_2d(): #tests if the returned value is the mean value of a 2D array
    arrObj = Array((2,5),2,4,6,1,2,3,7,8,9,10); solution = 26/5
    assert arrObj.mean_element() == solution, 'Something went wrong with test_mean_2d()'


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """
    #getitem test
    test_getitem()
    
    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
    
    print('All tests successfully ran')
