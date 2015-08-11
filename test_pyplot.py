
import matplotlib.pyplot as pyplot
x = [0] * 100
for i in range(0,100):
    x[i] = i
y = [0] * 100
for i in range(0,100):
    y[i] = i
pyplot.plot(x,y)
pyplot.show()
