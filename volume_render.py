#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:43:47 2019

@author: syxtreme
"""

import numpy as np
from mayavi import mlab
from traits.api import HasTraits, Range, Instance, on_trait_change, Button, Event, Str
from traitsui.api import View, Item, Group, HSplit, InstanceEditor
from traitsui.menu import Menu, MenuBar, Action, ToolBar
from pyface.api import FileDialog, OK

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
import os


class Panel(HasTraits):
    open_file_event = Event
    view = View()


open_file = Action(name="Load data", action='openFile')


class VolumeRender(HasTraits):

    def __init__(self):
        super(VolumeRender, self).__init__()

    panel = Instance(Panel, ())
    scatter_scene = Instance(MlabSceneModel, ())
    volume_scene = Instance(MlabSceneModel, ())
    reset_plane_butt = Button('Reset plane')
    z_reduction = Range(1, 2000, 1000, mode="slider")

    def openFile(self):
        wildcard = 'MayaVi2 files (*.npy)|*.npy|' + FileDialog.WILDCARD_ALL
        dialog = FileDialog(title='Open numpy data file',
                            action='open', wildcard=wildcard)

        if dialog.open() == OK:
            if not os.path.isfile(dialog.path):
                raise Exception("File '%s' does not exist" % dialog.path)
                return

            self.loadData(dialog.path)
            self.generatePlotData()
            self.reset_plane()

    @on_trait_change('reset_plane_butt')
    def reset_plane(self):
        self.slicer.ipw.plane_orientation = "z_axes"
        self.volume_scene.camera.position = [808.944540639155, 829.3458612118793, 775.2145331434656]
        self.volume_scene.camera.focal_point = [240.5, 180.5, 1.0]
        self.volume_scene.camera.view_angle = 30.0
        self.volume_scene.camera.view_up = [-0.4774879890979074, -0.468564520936391, 0.7432714914396268]
        self.volume_scene.camera.clipping_range = [712.7852412300919, 1723.7390002418533]
        self.volume_scene.camera.compute_view_plane_normal()
        self.volume_scene.render()

    def loadData(self, path):
        data = np.load(path)

        self.x = data[:, 1]
        self.y = data[:, 2]
        self.z = data[:, 0]
        self.s = data[:, 3]

        if 0 in np.unique(self.s) and -1 not in np.unique(self.s):
            self.s[np.where(self.s == 0)] = -1
        self.dz = np.unique(self.z)[1:] - np.unique(self.z)[:-1]

    def generatePlotData(self):
        z_step = np.median(self.dz) * self.z_reduction
        vx, vy, vz = np.arange(0, np.max(self.x) + 1), np.arange(
            0, np.max(self.y) + 1), np.arange(np.min(self.z), np.max(self.z), z_step)
        scalars = np.zeros(
            (np.size(vx), np.size(vy), np.size(vz)), dtype=np.int8)

        scalar_z_idx = 0
        scalar_tz = vz[scalar_z_idx]
        scalar_z_th = scalar_tz + z_step
        for z_idx, tz in enumerate(self.z):
            if tz >= scalar_z_th:
                scalar_z_idx += 1
                scalar_tz = vz[scalar_z_idx]
                scalar_z_th = scalar_tz + z_step

            tx, ty, ts = int(self.x[z_idx]), int(self.y[z_idx]), self.s[z_idx]
            scalars[tx, ty, scalar_z_idx] += ts

        mlab.clf(figure=self.volume_scene.mayavi_scene)
        valueLimit = max(abs(np.min(scalars)), np.max(scalars))
        self.slicer = mlab.volume_slice(scalars, figure=self.volume_scene.mayavi_scene, colormap="coolwarm", plane_orientation="z_axes", vmin=-valueLimit, vmax=valueLimit, extent=[np.min(self.x), np.max(self.x), np.min(self.y), np.max(self.y), 0, np.size(vz)])
        # self.points = mlab.points3d(scalars, figure=self.volume_scene.mayavi_scene, colormap="coolwarm", vmin=np.min(self.s), vmax=np.max(self.s))


if __name__ == "__main__":
    resolution = (1900, 1000)
    view = View(
        Item(
            'panel',
            editor=InstanceEditor(),
            style='custom',
            show_label=False,
        ),
        HSplit(
            Group(
                Item('scatter_scene',
                     editor=SceneEditor(),
                     height=resolution[1] - 300,
                     width=resolution[0] / 2 - 100),
                'z_reduction',
                show_labels=False,
            ),
            Group(
                Item('volume_scene',
                     editor=SceneEditor(),
                     height=resolution[1] - 300,
                     width=resolution[0] / 2 - 100, show_label=False),
                'reset_plane_butt',
                show_labels=False,
            ),
        ),
        toolbar=ToolBar(open_file),
        resizable=True,
        title="Volumeteor"
    )

    m = VolumeRender()
    m.configure_traits(view=view)
