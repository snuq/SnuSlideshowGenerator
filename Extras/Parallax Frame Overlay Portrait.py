import bpy
from math import pi


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    width = 0.667
    scale = 1.16
    #width = 1.667
    #scale = 1.06
    position = 0.2 + (extra_amount / 2.5)
    bpy.ops.mesh.primitive_circle_add(vertices=4, radius=0.46, location=(0, 0, position), rotation=(0, 0, pi/4), enter_editmode=True)
    bpy.ops.transform.resize(value=(width, 1, 1))
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(scale, 1.1, 1.1))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    frame = bpy.context.scene.objects.active
    frame.parent = image_plane

    bpy.ops.mesh.primitive_circle_add(vertices=4, radius=0.48, location=(0, 0, (position - 0.01)), rotation=(0, 0, pi/4), enter_editmode=True)
    bpy.ops.transform.resize(value=(width, 1, 1))
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(4, 4, 4))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    border = bpy.context.scene.objects.active
    border.parent = image_plane

    bpy.ops.object.lamp_add(type='POINT', location=(0, 0, 1))
    lamp = bpy.context.scene.objects.active
    lamp.parent = image_plane

    frame_material = bpy.data.materials.new('Frame')
    frame.data.materials.append(frame_material)
    frame_material.diffuse_intensity = 1

    border_material = bpy.data.materials.new('Border')
    border.data.materials.append(border_material)
    border_material.diffuse_color = (0, 0, 0)
    border_material.use_shadeless = True
