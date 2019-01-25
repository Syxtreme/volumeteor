import numpy as np
from mayavi import mlab
from traits.api import HasTraits, Range, Instance, on_trait_change
from traitsui.api import View, Item, Group

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

#%gui qt

data = np.load("data/twoballs.npy")

z_scale = 5000

x = data[:, 1]
y = data[:, 2]
z = data[:, 0]# * 1000
s = data[:, 3]

#x, y, z = [np.moveaxis(np.reshape(data[:100, i], (-1, 1, 1)), 0, i) for i in range(3)]

#mlab.points3d(x, y, z * z_scale, mode="point")

if 0 in np.unique(s) and -1 not in np.unique(s):
    s[np.where(s == 0)] = -1

#src = mlab.pipeline.scalar_scatter(x, y, z, s)
#glph = mlab.pipeline.glyph(src, mode="point")
#delu = mlab.pipeline.delaunay3d(src)
#sclf = mlab.pipeline.scalar_cut_plane(delu)
#cut = mlab.pipeline.cut_plane(glph)

#px, py = np.ogrid[np.min(x):np.max(x), np.min(y):np.max(y)]
#ps = np.ones((np.max(x).astype(np.int), np.max(y).astype(np.int)))
#
dz = np.unique(z)[1:] - np.unique(z)[:-1]
#ndz = np.abs(dz - np.std(dz))

#for idx in np.where(dz > np.std(dz) * 3)[0]:
#    mlab.surf(px, py, ps * z[idx] * z_scale)
#    if idx > 100:
#        break

#start = 0
#end = 1000
#rdx = x[start:end]
#rdy = y[start:end]
#rdz = z[start:end]
z_step = np.median(dz) * 1000
vx, vy, vz = np.arange(0, np.max(x) + 1), np.arange(0, np.max(y) + 1), np.arange(np.min(z), np.max(z), z_step)
#vx, vy, vz = np.arange(np.min(x), np.max(x) + 1), np.arange(np.min(y), np.max(y) + 1), np.arange(np.min(z), np.max(z) + 1, z_step)
#vx, vy, vz = np.ogrid[np.min(x):np.max(x), np.min(y):np.max(y), np.min(z):np.max(z):z_step]
#vx, vy, vz = *np.ogrid[np.min(rdx):np.max(rdx), np.min(rdy):np.max(rdy)], np.moveaxis(np.atleast_3d(rdz), 1, 2)

#coords = zip(x, y, z)
scalars = np.zeros((np.size(vx), np.size(vy), np.size(vz)), dtype=np.int8)

scalar_z_idx = 0
scalar_tz = vz[scalar_z_idx]
scalar_z_th = scalar_tz + z_step
for z_idx, tz in enumerate(z):
    if tz >= scalar_z_th:
        scalar_z_idx += 1
        scalar_tz = vz[scalar_z_idx]
        scalar_z_th = scalar_tz + z_step
    
    tx, ty, ts = int(x[z_idx]), int(y[z_idx]), s[z_idx]
    scalars[tx, ty, scalar_z_idx] += ts
    
slicer = mlab.volume_slice(scalars, colormap="coolwarm", plane_orientation="z_axes", vmin=np.min(s), vmax=np.max(s),
                           extent=[np.min(x), np.max(x), np.min(y), np.max(y), 0, np.size(vz)])

