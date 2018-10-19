import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    bpy.ops.object.lamp_add(type='SUN', location=(0, 0, 0))
    lamp = bpy.context.scene.objects.active
    lamp.data.use_diffuse = False

    material = image_plane.material_slots[0].material
    material.use_shadeless = False
    material.emit = 1
    material.specular_intensity = 1
    material.specular_hardness = 201 - (extra_amount * 200)

    lamp.animation_data_create()
    lamp_action = bpy.data.actions.new('Sun Lamp Glint')
    lamp.animation_data.action = lamp_action
    fcurve = lamp_action.fcurves.new('rotation_euler', index=1)
    point = fcurve.keyframe_points.insert(frame=image_scene.frame_start, value=-3.1415926)
    point = fcurve.keyframe_points.insert(frame=image_scene.frame_end, value=3.1415926)

