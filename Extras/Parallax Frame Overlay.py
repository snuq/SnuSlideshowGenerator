import bpy
from math import pi


def extra(data):
    image_scene = data['image_scene']
    image_plane = data['image_plane']
    extra_amount = data['extra_amount']
    bpy.context.window.scene = image_scene

    aspect_ratio = image_plane.dimensions[0] / image_plane.dimensions[1]
    if aspect_ratio < 1:
        #taller
        width = aspect_ratio / 1
        height = 1
    else:
        #wider
        width = aspect_ratio
        height = 1

    base_size = 0.9
    width = width * base_size
    height = height * base_size
    position = 0.5 + (extra_amount / 2.5)
    bpy.ops.mesh.primitive_circle_add(vertices=4, radius=0.46, location=(0, 0, position), rotation=(0, 0, pi/4), enter_editmode=True)
    bpy.ops.transform.resize(value=(width, height, 1))
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(1.1, 1.1, 1.1))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    frame = bpy.context.active_object
    frame.parent = image_plane

    bpy.ops.mesh.primitive_circle_add(vertices=4, radius=0.48, location=(0, 0, (position - 0.01)), rotation=(0, 0, pi/4), enter_editmode=True)
    bpy.ops.transform.resize(value=(width, height, 1))
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(4, 4, 4))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    border = bpy.context.active_object
    border.parent = image_plane

    bpy.ops.object.light_add(type='POINT', location=(0, 0, 1))
    lamp = bpy.context.active_object
    lamp.parent = image_plane

    frame_material = bpy.data.materials.new('Frame')
    frame.data.materials.append(frame_material)

    border_material = bpy.data.materials.new('Border')
    border.data.materials.append(border_material)
    border_material.diffuse_color = (0, 0, 0, 1)
    border_material.specular_intensity = 0
