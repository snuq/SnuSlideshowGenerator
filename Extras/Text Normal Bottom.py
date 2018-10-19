import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    name = 'Text Bottom'
    location = (0, -0.0892, -0.43)
    scale = (0.022, 0.022, 0.022)

    bpy.ops.object.text_add()
    text = bpy.context.scene.objects.active
    text.location = location
    text.scale = scale
    text.name = name
    material = bpy.data.materials.new(name)
    text.data.materials.append(material)

    material.diffuse_color = (0.281, 0.281, 0.281)
    material.diffuse_intensity = 1
    material.specular_intensity = 1
    material.specular_hardness = 93
    text.data.align_x = 'CENTER'
    text.data.body = extra_text
    text.data.extrude = (0.1 * (extra_amount * 2))
    text.data.bevel_depth = (0.01 * (extra_amount * 2))
    text.parent = camera
    text.layers = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]

    bpy.ops.object.lamp_add(type='POINT')
    lamp1 = bpy.context.scene.objects.active
    lamp1.name = name+' Lamp Front Right'
    lamp1.parent = text
    lamp1.location = (1.454, 0.96, 10.557)
    lamp1.data.energy = 0.5
    lamp1.data.use_own_layer = True
    lamp1.layers = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]
    bpy.ops.object.lamp_add(type='POINT')
    lamp2 = bpy.context.scene.objects.active
    lamp2.name = name+' Lamp Front Left'
    lamp2.parent = text
    lamp2.location = (-1.454, 0.96, 10.557)
    lamp2.data.energy = 0.5
    lamp2.data.use_own_layer = True
    lamp2.layers = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]
    bpy.ops.object.lamp_add(type='POINT')
    lamp3 = bpy.context.scene.objects.active
    lamp3.name = name+' Lamp Back'
    lamp3.parent = text
    lamp3.location = (0, 0.334, -11.44)
    lamp3.data.energy = 2.14
    lamp3.data.use_own_layer = True
    lamp3.data.distance = 56
    lamp3.layers = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]
