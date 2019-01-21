import numpy as np
from mayavi import mlab
from traits.api import HasTraits, Range, Instance, on_trait_change
from traitsui.api import View, Item, Group

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

#%gui qt

data = np.load("data/twoballs.npy")
#np.

x = data[:, 1]
y = data[:, 2]
z = data[:, 0] * 1000
s = data[:, 3]

#x, y, z = [np.moveaxis(np.reshape(data[:100, i], (-1, 1, 1)), 0, i) for i in range(3)]

#mlab.points3d(x, y, z, mode="point")

src = mlab.pipeline.scalar_scatter(x, y, z, s)
glph = mlab.pipeline.glyph(src, mode="point")
delu = mlab.pipeline.delaunay3d(src)
sclf = mlab.pipeline.scalar_cut_plane(delu)
#cut = mlab.pipeline.cut_plane(glph)