import bpy


def extra(data):
    image_scene = data['image_scene']
    camera = data['camera']
    extra_amount = data['extra_amount']
    extra_text = data['extra_text']
    bpy.context.window.scene = image_scene

    render = image_scene.render
    aspect_ratio = (render.pixel_aspect_x * render.resolution_x) / (render.pixel_aspect_y * render.resolution_y)
    if aspect_ratio < 1:
        #taller
        height = 1
    else:
        #wider
        height = 1 / aspect_ratio

    vertical = -(height / 8)
    name = 'Text Bottom'
    location = (0, vertical, -0.43)
    scale = (0.022, 0.022, 0.022)

    bpy.ops.object.text_add()
    text = bpy.context.active_object
    text.location = location
    text.scale = scale
    text.name = name
    material = bpy.data.materials.new(name)
    text.data.materials.append(material)

    material.diffuse_color = (0.281, 0.281, 0.281, 1)
    material.specular_intensity = 1
    material.roughness = 0.4
    text.data.align_x = 'CENTER'
    text.data.body = extra_text
    text.data.extrude = (0.1 * (extra_amount * 2))
    text.data.bevel_depth = (0.01 * (extra_amount * 2))
    text.parent = camera

    bpy.ops.object.light_add(type='POINT')
    lamp1 = bpy.context.active_object
    lamp1.name = name+' Lamp Front Right'
    lamp1.parent = text
    lamp1.location = (1.454, 0.96, 10.557)
    lamp1.data.energy = 0.5
    bpy.ops.object.light_add(type='POINT')
    lamp2 = bpy.context.active_object
    lamp2.name = name+' Lamp Front Left'
    lamp2.parent = text
    lamp2.location = (-1.454, 0.96, 10.557)
    lamp2.data.energy = 0.5
    bpy.ops.object.light_add(type='POINT')
    lamp3 = bpy.context.active_object
    lamp3.name = name+' Lamp Back'
    lamp3.parent = text
    lamp3.location = (0, 0.334, -11.44)
    lamp3.data.energy = 2.14
