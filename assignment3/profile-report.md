# Profiling report

## Questions

A few questions below to help understand the kind of information we can get from profiling outputs.
 We are not asking for lots of detail, just 1-2 sentences each.

### Question 1

> Which profiler produced the most useful output, and why?

I prefer line_profiler since it gives the percentage of total runtime for a given function, which allows us to more easily gauge at a glance which functions/lines are "problem lines"

cProfile technically does practically the same thing, but is harder to read at a glance.

### Question 2

> Pick one profiler output (e.g. `cprofile numpy_color2sepia`).
  Based on this profile, where should we focus effort on improving performance?

> **Hint:** two things to consider when picking an optimization:

> - how much time is spent in the step? (reducing a step that takes 1% of the time all the way to 0 can only improve performance by 1%)
> - are there other ways to do it? (simple steps may already be optimal. Complex steps often have many implementations with different performance)

selected profile: lineprofiler numpy_color2sepia

The most glaring performance problem here is of course the "dotting" of the sepia matrix and the vectorized pixel. I suppose the natural way to make this less intensive would be to reduce the number of times this line is particular is called

One of the most obvious ways to do this is to lower the amount of for-loop and instead iterate once in a more efficient way.

Another pretty obvious solution would be to parallelize the code. I did some testing and although numpy can do this on its own, in my case I only ever saw activity on one to two cores (out of 16).

## Profile output

Paste the outputs of `python3 -m instapy.profiling` below:

<details>
<summary>cProfile output</summary>
 
```
 
Begin cProfile
Profiling python color2gray with cprofile:
         1536014 function calls in 4.145 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.546    0.546    4.145    4.145 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\python_filters.py:7(python_color2gray)
   307200    0.839    0.000    3.598    0.000 {built-in method builtins.sum}
  1228800    2.759    0.000    2.759    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\python_filters.py:26(<genexpr>)
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:132(deepcopy)
        1    0.000    0.000    0.000    0.000 {method '__deepcopy__' of 'numpy.ndarray' objects}
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:252(_keep_alive)
        3    0.000    0.000    0.000    0.000 {built-in method builtins.id}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.issubclass}
        2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}


Profiling numpy color2gray with cprofile:
         6253 function calls in 0.008 seconds

   Ordered by: cumulative time
   List reduced from 20 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003    0.008    0.008 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numpy_filters.py:7(numpy_color2gray)
      960    0.003    0.000    0.005    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
      480    0.000    0.000    0.003    0.000 <__array_function__ internals>:2(dot)
      480    0.000    0.000    0.002    0.000 <__array_function__ internals>:2(transpose)
      480    0.000    0.000    0.002    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:601(transpose)
      480    0.000    0.000    0.002    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:51(_wrapfunc)
      480    0.000    0.000    0.001    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:38(_wrapit)
      480    0.001    0.000    0.001    0.000 {built-in method numpy.asarray}
      961    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
      480    0.000    0.000    0.000    0.000 {method 'transpose' of 'numpy.ndarray' objects}


Profiling numba color2gray with cprofile:
         6253 function calls (6252 primitive calls) in 0.009 seconds

   Ordered by: cumulative time
   List reduced from 19 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      2/1    0.003    0.002    0.009    0.009 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numba_filters.py:13(numba_color2gray)
      960    0.003    0.000    0.005    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
      480    0.000    0.000    0.003    0.000 <__array_function__ internals>:2(dot)
      480    0.000    0.000    0.002    0.000 <__array_function__ internals>:2(transpose)
      480    0.000    0.000    0.002    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:601(transpose)
      480    0.000    0.000    0.002    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:51(_wrapfunc)
      480    0.000    0.000    0.001    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:38(_wrapit)
      480    0.001    0.000    0.001    0.000 {built-in method numpy.asarray}
      961    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
      480    0.000    0.000    0.000    0.000 {method 'transpose' of 'numpy.ndarray' objects}


Profiling cython color2gray with cprofile:
         6252 function calls in 0.008 seconds

   Ordered by: cumulative time
   List reduced from 19 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003    0.008    0.008 instapy\cython_filters.pyx:8(cython_color2gray)
      960    0.003    0.000    0.005    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
      480    0.000    0.000    0.003    0.000 <__array_function__ internals>:2(dot)
      480    0.000    0.000    0.002    0.000 <__array_function__ internals>:2(transpose)
      480    0.000    0.000    0.002    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:601(transpose)
      480    0.000    0.000    0.002    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:51(_wrapfunc)
      480    0.000    0.000    0.001    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\fromnumeric.py:38(_wrapit)
      480    0.001    0.000    0.001    0.000 {built-in method numpy.asarray}
      961    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
      480    0.000    0.000    0.000    0.000 {method 'transpose' of 'numpy.ndarray' objects}


Profiling python color2sepia with cprofile:
         1843693 function calls in 4.655 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    3.423    3.423    4.655    4.655 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\python_filters.py:33(python_color2sepia)
   921600    1.188    0.000    1.188    0.000 {built-in method builtins.sum}
   921600    0.044    0.000    0.044    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:132(deepcopy)
        1    0.000    0.000    0.000    0.000 {method '__deepcopy__' of 'numpy.ndarray' objects}
      481    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:252(_keep_alive)
        3    0.000    0.000    0.000    0.000 {built-in method builtins.id}
        2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}


Profiling numpy color2sepia with cprofile:
         922093 function calls in 2.134 seconds

   Ordered by: cumulative time
   List reduced from 13 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.721    0.721    2.134    2.134 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numpy_filters.py:34(numpy_color2sepia)
   307200    0.097    0.000    1.413    0.000 <__array_function__ internals>:2(dot)
   307200    1.297    0.000    1.297    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
   307200    0.019    0.000    0.019    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\multiarray.py:736(dot)
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:132(deepcopy)
        1    0.000    0.000    0.000    0.000 {method '__deepcopy__' of 'numpy.ndarray' objects}
      481    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:252(_keep_alive)
        2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        3    0.000    0.000    0.000    0.000 {built-in method builtins.id}


Profiling numba color2sepia with cprofile:
         921613 function calls (921612 primitive calls) in 2.136 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      2/1    0.736    0.368    2.136    2.136 C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numba_filters.py:32(numba_color2sepia)
   307200    0.096    0.000    1.399    0.000 <__array_function__ internals>:2(dot)
   307200    1.285    0.000    1.285    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
   307200    0.019    0.000    0.019    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\multiarray.py:736(dot)
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:132(deepcopy)
        1    0.000    0.000    0.000    0.000 {method '__deepcopy__' of 'numpy.ndarray' objects}
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:252(_keep_alive)
        3    0.000    0.000    0.000    0.000 {built-in method builtins.id}
        2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}


Profiling cython color2sepia with cprofile:
         921612 function calls in 2.122 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.714    0.714    2.122    2.122 instapy\cython_filters.pyx:20(cython_color2sepia)
   307200    0.096    0.000    1.408    0.000 <__array_function__ internals>:2(dot)
   307200    1.293    0.000    1.293    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
   307200    0.019    0.000    0.019    0.000 C:\Users\Simen\Anaconda3\lib\site-packages\numpy\core\multiarray.py:736(dot)
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:132(deepcopy)
        1    0.000    0.000    0.000    0.000 {method '__deepcopy__' of 'numpy.ndarray' objects}
        1    0.000    0.000    0.000    0.000 C:\Users\Simen\Anaconda3\lib\copy.py:252(_keep_alive)
        2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        3    0.000    0.000    0.000    0.000 {built-in method builtins.id}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}


End cProfile
 
```
 
</details>

<details>
<summary>line_profiler output</summary>
 
```
 
Begin line_profiler
Profiling python color2gray with line_profiler:
Timer unit: 1e-07 s

Total time: 5.43667 s
File: C:\Users\Simen\Anaconda3\lib\site-packages\instapy\python_filters.py
Function: python_color2gray at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           def python_color2gray(image: np.array) -> np.array:
     8                                               """Convert rgb pixel array to grayscale
     9                                           
    10                                               Args:
    11                                                   image (np.array)
    12                                               Returns:
    13                                                   np.array: image
    14                                               """
    15         1         14.0     14.0      0.0      togray = (0.21,0.72,0.07)
    16                                               
    17         1       1010.0   1010.0      0.0      image = deepcopy(image) #this is because of a dumb error where image outside of our function gets changed
    18                                               
    19         1         24.0     24.0      0.0      width = len(image[0,:])
    20         1         12.0     12.0      0.0      height = len(image[:,:])
    21                                               
    22                                               
    23       481       2985.0      6.2      0.0      for i in range(width):
    24    307680    1984706.0      6.5      3.7          for j in range(height):
    25    307200    2613218.0      8.5      4.8              p = image[j,i]
    26    307200    2820365.0      9.2      5.2              p = (np.uint8((a*b)/3) for a, b in zip(p,togray)) #list comprehension (very pythonic!)
    27    307200   40814407.0    132.9     75.1              p = sum(p)
    28    307200    6129952.0     20.0     11.3              image[j,i] = 3*[p]
    29                                                       
    30                                           
    31         1          6.0      6.0      0.0      return image

Profiling numpy color2gray with line_profiler:
Timer unit: 1e-07 s

Total time: 0.0102695 s
File: C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numpy_filters.py
Function: numpy_color2gray at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           def numpy_color2gray(image: np.array) -> np.array:
     8                                               """Convert rgb pixel array to grayscale
     9                                           
    10                                               Args:
    11                                                   image (np.array)
    12                                               Returns:
    13                                                   np.array: image
    14                                               """
    15                                           
    16         1         12.0     12.0      0.0      togray = (0.21,0.72,0.07)
    17                                               
    18         1        471.0    471.0      0.5      image = deepcopy(image)
    19                                               
    20       481       2758.0      5.7      2.7      for i in range(len(image[0,:])):
    21       480      50726.0    105.7     49.4              p = np.uint8((np.dot(image[:,i], togray))/3)
    22       480      48723.0    101.5     47.4              image[:,i] = np.transpose([p]*3)
    23                                                   
    24         1          5.0      5.0      0.0      return image
    25                                                   
    26                                                   
    27                                               
    28                                               # Hint: use numpy slicing in order to have fast vectorized code
    29                                               ...
    30                                               # Return image (make sure it's the right type!)
    31                                               return image

Profiling numba color2gray with line_profiler:
Timer unit: 1e-07 s

Total time: 0 s
File: C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numba_filters.py
Function: numba_color2gray at line 13

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    13                                           @jit
    14                                           def numba_color2gray(image: np.array) -> np.array:
    15                                               """Convert rgb pixel array to grayscale
    16                                           
    17                                               Args:
    18                                                   image (np.array)
    19                                               Returns:
    20                                                   np.array: image
    21                                               """
    22                                               togray = [0.21,0.72,0.07]
    23                                               
    24                                               image = deepcopy(image)
    25                                               
    26                                               for i in range(len(image[0,:])):
    27                                                       p = np.uint8((np.dot(image[:,i], togray))/3)
    28                                                       image[:,i] = np.transpose([p]*3)
    29                                                   
    30                                               return image

Profiling cython color2gray with line_profiler:
Timer unit: 1e-07 s

Total time: 0.0093917 s

Could not find file instapy\cython_filters.pyx
Are you sure you are running this program from the same directory
that you ran the profiler from?
Continuing without the function's contents.

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     8                                           
     9                                           
    10         1         11.0     11.0      0.0  
    11                                           
    12         1        633.0    633.0      0.7  
    13                                           
    14         1         10.0     10.0      0.0  
    15       480      47814.0     99.6     50.9  
    16       480      45444.0     94.7     48.4  
    17                                           
    18         1          5.0      5.0      0.0  

Profiling python color2sepia with line_profiler:
Timer unit: 1e-07 s

Total time: 7.32123 s
File: C:\Users\Simen\Anaconda3\lib\site-packages\instapy\python_filters.py
Function: python_color2sepia at line 33

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    33                                           def python_color2sepia(image: np.array) -> np.array:
    34                                               """Convert rgb pixel array to sepia
    35                                           
    36                                               Args:
    37                                                   image (np.array)
    38                                               Returns:
    39                                                   np.array: image
    40                                               """
    41                                               sepia_matrix = [
    42         1         19.0     19.0      0.0      [ 0.393, 0.769, 0.189],
    43         1         13.0     13.0      0.0      [ 0.349, 0.686, 0.168],
    44         1         10.0     10.0      0.0      [ 0.272, 0.534, 0.131],
    45                                           ]
    46                                               
    47         1        850.0    850.0      0.0      image = deepcopy(image)
    48         1         11.0     11.0      0.0      scaler = 1.5   #to avoid numbers greater than 255, whilst keeping the ratio intact 
    49                                                   
    50       481       4677.0      9.7      0.0      for i in range(len(image[0,:])):
    51    307680    3105000.0     10.1      4.2          for j in range(len(image[:,0])):  
    52    307200    3071788.0     10.0      4.2              p = []
    53   1228800   12632825.0     10.3     17.3              for a in sepia_matrix:
    54    921600   49037972.0     53.2     67.0                  p.append(np.uint8(sum(a*image[j,i])/scaler))
    55                                                           
    56    307200    5359171.0     17.4      7.3              image[j,i] = p
    57                                           
    58                                               # Return image
    59                                               # don't forget to make sure it's the right type!
    60         1         10.0     10.0      0.0      return image

Profiling numpy color2sepia with line_profiler:
Timer unit: 1e-07 s

Total time: 3.39617 s
File: C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numpy_filters.py
Function: numpy_color2sepia at line 34

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    34                                           def numpy_color2sepia(image: np.array, k=1) -> np.array:
    35                                               """Convert rgb pixel array to sepia
    36                                           
    37                                               Args:
    38                                                   image (np.array)
    39                                                   k (float): amount of sepia filter to apply (optional)
    40                                           
    41                                               The amount of sepia is given as a fraction, k=0 yields no sepia while
    42                                               k=1 yields full sepia.
    43                                           
    44                                               (note: implementing 'k' is a bonus task,
    45                                               you may ignore it for Task 9)
    46                                           
    47                                               Returns:
    48                                                   np.array: image
    49                                               """
    50                                           
    51         1         22.0     22.0      0.0      if not 0 <= k <= 1:
    52                                                   raise ValueError("k must be between [0-1], %g" %(k))
    53                                                   
    54                                               
    55                                           
    56                                               sepia_matrix = [
    57         1         16.0     16.0      0.0      [ 0.393, 0.769, 0.189],
    58         1         12.0     12.0      0.0      [ 0.349, 0.686, 0.168],
    59         1         13.0     13.0      0.0      [ 0.272, 0.534, 0.131],
    60                                           ]
    61                                               
    62         1         12.0     12.0      0.0      if k == 0:
    63                                                   scaler = 1
    64                                               else:
    65         1         11.0     11.0      0.0          scaler = 1.5
    66                                               
    67         1         12.0     12.0      0.0      if k != 1:
    68                                                   I = np.array(((1,0,0),(0,1,0),(0,0,1)))
    69                                                   sepiaNumpy = np.array(sepia_matrix)
    70                                                   dif = sepiaNumpy-I
    71                                                   sepia_matrix = I+dif*k
    72                                                   sepia_matrix = sepia_matrix.tolist()
    73                                               
    74         1        804.0    804.0      0.0      image = deepcopy(image)
    75                                               
    76       481       5197.0     10.8      0.0      for i in range(len(image[0,:])):
    77    307680    3427843.0     11.1     10.1          for j in range(len(image[:,0])):  
    78    307200   25146177.0     81.9     74.0              p = np.uint8((np.dot(sepia_matrix,image[j,i]))/scaler)
    79    307200    5381548.0     17.5     15.8              image[j,i] = p
    80         1         11.0     11.0      0.0      return image

Profiling numba color2sepia with line_profiler:
Timer unit: 1e-07 s

Total time: 0 s
File: C:\Users\Simen\Anaconda3\lib\site-packages\instapy\numba_filters.py
Function: numba_color2sepia at line 32

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    32                                           @jit
    33                                           def numba_color2sepia(image: np.array) -> np.array:
    34                                               """Convert rgb pixel array to sepia
    35                                           
    36                                               Args:
    37                                                   image (np.array)
    38                                               Returns:
    39                                                   np.array: sepia_image
    40                                               """
    41                                               sepia_matrix = [
    42                                               [ 0.393, 0.769, 0.189],
    43                                               [ 0.349, 0.686, 0.168],
    44                                               [ 0.272, 0.534, 0.131],
    45                                           ]
    46                                               
    47                                               scaler=1.5  
    48                                               
    49                                               image = deepcopy(image)
    50                                               
    51                                               for i in range(len(image[0,:])):
    52                                                   for j in range(len(image[:,0])):  
    53                                                       p = np.uint8((np.dot(sepia_matrix,image[j,i]))/scaler)
    54                                                       image[j,i] = p
    55                                               return image

Profiling cython color2sepia with line_profiler:
Timer unit: 1e-07 s

Total time: 2.41722 s

Could not find file instapy\cython_filters.pyx
Are you sure you are running this program from the same directory
that you ran the profiler from?
Continuing without the function's contents.

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    20                                           
    21                                           
    22                                           
    23                                           
    24                                           
    25                                           
    26                                           
    27                                           
    28         1          6.0      6.0      0.0  
    29         1         14.0     14.0      0.0  
    30         1          6.0      6.0      0.0  
    31         1          4.0      4.0      0.0  
    32                                           
    33         1          3.0      3.0      0.0  
    34                                           
    35         1       1198.0   1198.0      0.0  
    36                                           
    37         1         14.0     14.0      0.0  
    38       480       2349.0      4.9      0.0  
    39    307200   21718701.0     70.7     89.8  
    40    307200    2449898.0      8.0     10.1  
    41         1          8.0      8.0      0.0  

End line_profiler
 
```
 
</details>