import matplotlib.pyplot as plt
import numpy as np
from math import exp
import pandas

# fig = plt.figure()
# fig.suptitle("Changing Frequencies of Code Metrics")
# fig, ax_lst = plt.subplots(2, 2)
# a = pandas.DataFrame(np.random.rand(4,5), columns = list('abcde'))
# a_asarray = a.values
# b = np.matrix([[1,2],[3,4]])
# b_asarray = np.asarray(b)
# # fig.show()

x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')
plt.plot(x, exp(x), label='exponential')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()