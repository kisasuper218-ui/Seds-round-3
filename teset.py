import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from digi.xbee.devices import XBeeDevice
import serial

xbee = XBeeDevice("COM3", 9600)
xbee.open()

alts=[]
lats=[]
longs=[]

fig = plt.figure()
ax=fig.add_subplot(111, projection='3d')
line, = ax.plot([], [], [], color='blue', marker='o', linestyle='-')
ax.set_xlim([-90.0, 90.0]) 
ax.set_ylim([-180.0, 180.0]) 
ax.set_zlim([0, 1000])


plt.ion()   
plt.show()

def my_data_received_callback(xbee_message):
    try:    
        data = xbee_message.data.decode("utf-8").strip()
        fields = data.split(",")
        alt = fields[4]
        lat = fields[7]
        long = fields[8]

        alts.append(float(alt))
        lats.append(float(lat))
        longs.append(float(long))

        line.set_data(lats, longs)
        line.set_3d_properties(alts)

        fig.canvas.draw_idle()
        plt.pause(0.1)
    except:
        pass

xbee.add_data_received_callback(my_data_received_callback)

try:
    input("Running... Press Enter to exit.\n")
finally:
    xbee.close()


