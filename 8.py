import numpy as np
import matplotlib.pyplot as plt
with open("settings.txt", "r") as settings:
    tmp = [float(i) for i in settings.read().split("\n")]
data_array = np.loadtxt("data.txt", dtype = int)


fig, ax = plt.subplots(figsize=(16,10), dpi = 400)
ax.plot(data_array)
fig.savefig("test.png")
plt.show()