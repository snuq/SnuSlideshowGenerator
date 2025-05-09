import bpy


def extra(data):
    image_scene = data['image_scene']
    bpy.context.window.scene = image_scene
    material_mix = data['material_mix']
    material_mix.inputs[0].default_value = 1
    material_shaded = data['material_shaded']
    material_shaded.inputs['Roughness'].default_value = 0.3

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 0))
    lamp = bpy.context.active_object
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 0))
    world_lamp = bpy.context.active_object
    world_lamp.data.specular_factor = 0
    world_lamp.data.energy = 3

    lamp.animation_data_create()
    lamp_action = bpy.data.actions.new('Sun Lamp Glint')
    lamp.animation_data.action = lamp_action
    fcurve = lamp_action.fcurves.new('rotation_euler', index=1)
    point = fcurve.keyframe_points.insert(frame=image_scene.frame_start, value=-3.1415926)
    point = fcurve.keyframe_points.insert(frame=image_scene.frame_end, value=3.1415926)
    if not lamp.animation_data.action_slot:
        lamp.animation_data.action_slot = lamp_action.slots[0]
