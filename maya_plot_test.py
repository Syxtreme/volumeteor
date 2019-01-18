import numpy as np
from mayavi import mlab
from traits.api import HasTraits, Range, Instance, on_trait_change
from traitsui.api import View, Item, Group

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

data = np.load("C:/Users/admin/Documents/vyuka/dvs/Prophesee/samples/twoballs.npy")

# x = np.squeeze(data[np.where(np.logical_and(data[:, 0] > data[100, 0], data[:, 0] < data[200, 0])), 1])
# y = np.squeeze(data[np.where(np.logical_and(data[:, 0] > data[100, 0], data[:, 0] < data[200, 0])), 2])
# z = np.squeeze(data[np.where(np.logical_and(data[:, 0] > data[100, 0], data[:, 0] < data[200, 0])), 0])
x = data[:, 1]
y = data[:, 2]
z = data[:, 0]

def slice_data(idx, z_scale):
    x = np.squeeze(data[np.where(np.logical_and(data[:, 0] > data[idx, 0], data[:, 0] < data[idx + 100, 0])), 1])
    y = np.squeeze(data[np.where(np.logical_and(data[:, 0] > data[idx, 0], data[:, 0] < data[idx + 100, 0])), 2])
    z = np.squeeze(data[np.where(np.logical_and(data[:, 0] > data[idx, 0], data[:, 0] < data[idx + 100, 0])), 0]) * z_scale
    return x, y, z


class MyModel(HasTraits):
    slice_idx = Range(0, 5000, 6, mode='slider')
    z_scale = Range(100, 10000, 1000, mode='slider')

    scene = Instance(MlabSceneModel, ())
    plot = Instance(PipelineBase)

    # The layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=600, width=800, show_label=False),
                Group(
                        'slice_idx', 'z_scale',
                     ),
                resizable=True,
                )

    def __init__(self, **traits):
        HasTraits.__init__(self, **traits)
        x, y, z = slice_data(self.slice_idx, self.z_scale)
        self.plot = self.scene.mlab.points3d(x, y, z, mode="point", opacity=0.9)

    # When the scene is activated, or when the parameters are changed, we
    # update the plot.
    @on_trait_change('slice_idx,z_scale,scene.activated')
    def update_plot(self):
        x, y, z = slice_data(self.slice_idx, self.z_scale)
        # if self.plot is None:
        # self.plot = self.scene.mlab.points3d(x, y, z, mode="point", opacity=0.9)
        # else:
        self.plot.mlab_source.trait_set(x=x, y=y, z=z)
        self.scene.update_plot()

my_model = MyModel()
my_model.configure_traits()
