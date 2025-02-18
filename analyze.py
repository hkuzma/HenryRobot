import numpy
import matplotlib.pyplot as m





backLegSensorValues = numpy.load("data\\backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data\\frontLegSensorValues.npy")

front_target_angles = numpy.load("data\\front_target_angles.npy")

back_target_angles = numpy.load("data\\back_target_angles.npy")
# m.plot(backLegSensorValues, linewidth=5)
# m.plot(frontLegSensorValues)

m.plot(front_target_angles)
m.plot(back_target_angles)


m.legend()
m.show()