"""
Array class for assignment 2
"""

from itertools import chain

class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        
        if str(type(values[0])) == """<class 'float'>""": #probably a better way to implement a type check but this was a quick and easy solution
            valuesType=float
        elif str(type(values[0])) == """<class 'int'>""":
            valuesType=int
        elif str(type(values[0])) == """<class 'complex'>""":
            valuesType=complex
        elif str(type(values[0])) == """<class 'bool'>""":
            valuesType=bool
        else:
            raise ValueError('Value type not recognized. Values must be integers, floats, complex numbers or boolean.')
            
        for i in values:
            if isinstance(i, valuesType) != True:
                raise ValueError('Values are not of same type')
        
        if isinstance(shape, tuple) == False:
            raise TypeError('shape is not a tuple')
           
        if len(shape) != 1: #if array is not 1d, finds "total" length of array if stretched to 1d and checks if it is equal to values in length
            len_to_match = 1
            for i in shape:
                len_to_match *= i
            
            if len(values) != len_to_match:
                raise ValueError('shape and length of values are not equal')
            
        elif len(values) != int(shape[0]):
            raise ValueError('shape and length of values are not equal')
            

        self.shape = shape
        self.totalValues = 1
        for i in shape:
            self.totalValues *= i
        self.values = values
        self.arrayList = []
        
        if len(shape) == 1:
            for i in self.values:
                self.arrayList.append(i)
        else: #this solution is (seemingly, atleast with the values I tried)
            arr = [] #only valid for matrices up to 3 dimensions. Couldn't get it 
            tarr = [] #to work for higher dimensions, sadly.
            k = 0 #after some reflection it seems likely that I'll need a recursive function
            for i in range(int(len(values)/shape[-1])): #to handle this, but I don't have the time to
                tarr.append((list(values[int(k):int(k+shape[-1])])))#implement it
                k+=shape[-1]

            arr = tarr
            tarr = []

            k=0
            for i in range(int(len(arr)/shape[-2])):
              tarr.append([arr[k+i]])
              for j in range(shape[-2]-1):
                tarr[i].append(arr[k+j+1])
              k+=shape[-2]
              
             
            self.arrayList = tarr

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        return (str(self.arrayList))
    
    
    def __getitem__(self, idx):
        """Returns the idx'th element of the array: array[idx]
        
        Args:
            idx (int): the index number in array
            
        Returns:
            bool, float, int, complex: the idx'th element"""
        if idx != 0:   
            if len(self.arrayList)-1 < idx:
                raise ValueError('Object does not have an element %d' %(idx))
        
        
        return self.arrayList[idx]
    
    def __add__(self, other):
        
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """

        # check that the method supports the given arguments (check for data type and shape of array)
        # if the array is a boolean you should return NotImplemented
        
        if type(other) == bool:
            return NotImplemented
        
        narray = self.arrayList
        
        
        
        if len(self.shape) > 1:
            narray = flat_array(self, self.arrayList)
            if not hasattr(other, '__len__'):
                other = [other]*len(narray)
        else:
            if not hasattr(other, '__len__'):
                other = [other]*len(self.arrayList)
        
        return(list(map(lambda x,y:x+y, narray, other)))

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        if type(other) == bool:
            return NotImplemented
        
        narray = self.arrayList
        
        
        
        if len(self.shape) > 1:
            narray = flat_array(self, self.arrayList)
            if not hasattr(other, '__len__'):
                other = [other]*len(narray)
        else:
            if not hasattr(other, '__len__'):
                other = [other]*len(self.arrayList)
        
        return(list(map(lambda x,y:x+y, narray, other)))
        

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if type(other) == bool:
            return NotImplemented
        narray = self.arrayList
        
        
        if len(self.shape) > 1:
            narray = flat_array(self, self.arrayList)
            if not hasattr(other, '__len__'):
                other = [other]*len(narray)
        else:
            if not hasattr(other, '__len__'):
                other = [other]*len(self.arrayList)
                
        return(list(map(lambda x,y:x-y, narray, other)))

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        if type(other) == bool:
            return NotImplemented
        narray = self.arrayList
        
        
        if len(self.shape) > 1:
            narray = flat_array(self, self.arrayList)
            if not hasattr(other, '__len__'):
                other = [other]*len(narray)
        else:
            if not hasattr(other, '__len__'):
                other = [other]*len(self.arrayList)
                
        return(list(map(lambda x,y:x-y, narray, other)))

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if type(other) == bool:
            return NotImplemented
        narray = self.arrayList
        
        
        if len(self.shape) > 1:
            narray = flat_array(self, self.arrayList)
            if not hasattr(other, '__len__'):
                other = [other]*len(narray)
        else:
            if not hasattr(other, '__len__'):
                other = [other]*len(self.arrayList)
                
        return(list(map(lambda x,y:x*y, narray, other)))

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if shapeChecker(other) != self.shape:
            raise ValueError('shapes of arrays are not equal')
        
        narray = self.arrayList
        
        if len(narray) != self.totalValues:    
            narray = flat_array(self, self.arrayList)
        
        
        if narray == list(other):
            return True
        else:
            return False
        
        
    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        
        boolArr = []
        narray = self.arrayList
        nother = False
        if len(narray) != self.totalValues:
            narray = flat_array(self, self.arrayList)
            if hasattr(other, '__len__'):
                nother = flat_array(self, other)
        
        
        if isinstance(other, int):
            for i in range(len(narray)):
                if narray[i] == other:
                    boolArr.append(True)
                else:
                    boolArr.append(False)
            
            return boolArr
        elif isinstance(other, float):
            for i in range(len(narray)):
                if narray[i] == other:
                    boolArr.append(True)
                else:
                    boolArr.append(False)
            
            return boolArr
        
        
        if shapeChecker(other) != self.shape:
            raise ValueError('shapes of arrays are not equal')
            
        for i in range(len(narray)):
            if nother != False:
                if narray[i] == nother[i]:
                    boolArr.append(True)
                else:
                    boolArr.append(False)
            else:
                if narray[i] == other[i]:
                    boolArr.append(True)
                else:
                    boolArr.append(False)
        
        return boolArr
        
        
        
            

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """

        narray = self.arrayList
        
        if len(narray) != self.totalValues:
            narray = flat_array(self, self.arrayList)
            
        min_val = narray[0]
        for i in narray[1:]:
            if i < min_val:
                min_val = i
                
        return min_val

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """
        
        narray = self.arrayList
        
        if len(narray) != self.totalValues:
            narray = flat_array(self, self.arrayList)
        sm = 0
        for i in narray:
            sm += i
        
        return sm/len(narray)


def flat_array(self, inArray):
   """Flattens the N-dimensional array of values into a 1-dimensional array.
   Returns:
       list: flat list of array values.
   """
   narray = [i for l1 in inArray for i in l1]
   if len(narray) != self.totalValues:
       narray = flat_array(self, narray)
   
   return narray

def shapeChecker(inArray, shape=()):
    if not hasattr(inArray, '__len__'):
        return shape
    
    shape += (len(inArray), )
    
    shape = shapeChecker(inArray[0], shape)
    
    return shape