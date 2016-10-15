from tables import *

class Animation(IsDescription):
    frame = Float64Col()

h5file = open_file("davidtest.hdf", mode = "r", title = "Test file")

# group = h5file.create_group("/", 'detector', 'Detector information')
#
# table = h5file.create_table(group, 'readout', Animation, "Readout example")

# animation = table.row
#
# for i in xrange(10):
#     animation['frame'] = i*0.1
#     animation.append()
# table.flush()
# print("PRINTSTART: ",h5file,"PRINTEND")


table = h5file.root.animation

frame = [x for x in table.iterrows()]

frame = x 

print(frame)
