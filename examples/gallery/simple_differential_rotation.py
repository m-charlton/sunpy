"""
============================
Simple Differential Rotation
============================

The Sun is known to rotate differentially, meaning that the rotation rate
near the poles (rotation period of approximately 35 days) is not the same as
the rotation rate near the equator (rotation period of approximately 25 days).
This is possible because the Sun is not a solid body. Though it is still poorly
understood, it is fairly well measured and must be taken into account
when comparing observations of features on the Sun over time.
A good review can be found in Beck 1999 Solar Physics 191, 47–70.
This example illustrates solar differential rotation.
"""

##############################################################################
# Start by importing the necessary modules.
from __future__ import print_function, division
from datetime import timedelta

import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u

import sunpy.map
import sunpy.data.sample
from sunpy.physics.differential_rotation import diff_rot, rot_hpc

##############################################################################
# Next lets explore solar differential rotation by replicating Figure 1
# in Beck 1999
latitudes = u.Quantity(np.arange(0, 90, 1), 'deg')
dt = 1 * u.day
rotation_rate = [diff_rot(dt, this_lat) / dt for this_lat in latitudes]
rotation_period = [360 * u.deg / this_rate for this_rate in rotation_rate]

fig = plt.figure()
plt.plot(np.sin(latitudes), [this_period.value for this_period in rotation_period])
plt.ylim(38, 24)
plt.ylabel('Rotation Period [{0}]'.format(rotation_period[0].unit))
plt.xlabel('Sin(Latitude)')
plt.title('Solar Differential Rotation Rate')

##############################################################################
# Next let's show how to this looks like on the Sun.
# Load in an AIA map:
aia_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)

##############################################################################
# Let's define our starting coordinates
hpc_y = u.Quantity(np.arange(-700, 800, 100), u.arcsec)
hpc_x = np.zeros_like(hpc_y)

##############################################################################
# Let's define how many days in the future we want to rotate to
dt = timedelta(days=4)
future_date = aia_map.date + dt

##############################################################################
# Now let's plot the original and rotated positions on the AIA map.
fig = plt.figure()
ax = plt.subplot()
aia_map.plot()
ax.set_title('The effect of {0} days of differential rotation'.format(dt.days))
aia_map.draw_grid()
for this_hpc_x, this_hpc_y in zip(hpc_x, hpc_y):
    new_hpc_x, new_hpc_y = rot_hpc(this_hpc_x, this_hpc_y, aia_map.date, future_date)
    plt.plot([this_hpc_x.value, new_hpc_x.value], [this_hpc_y.value, new_hpc_y.value], 'o-')
plt.ylim(-1000, 1000)
plt.xlim(-1000, 1000)
plt.show()
