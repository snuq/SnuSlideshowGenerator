import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    name = 'White Background'
    bpy.context.screen.scene = image_scene
    bpy.ops.mesh.primitive_plane_add(radius=2, location=(0, 0, -2))
    background_plane = bpy.context.scene.objects.active
    background_plane.name = name
    modifier = background_plane.modifiers.new(name='', type='SUBSURF')
    modifier.render_levels = 1
    modifier.subdivision_type = 'SIMPLE'
    background_material = bpy.data.materials.new(name)
    background_plane.data.materials.append(background_material)

    background_material.diffuse_color = (extra_amount, extra_amount, extra_amount)
    background_material.diffuse_intensity = 1
    background_material.specular_intensity = 0
    background_material.use_transparent_shadows = True
    background_material.use_cast_buffer_shadows = False
    bpy.ops.object.lamp_add(type='SPOT', location=(0, 0, -0.2))
    background_lamp = bpy.context.scene.objects.active
    background_lamp.data.energy = 2
    background_lamp.data.shadow_buffer_type = 'REGULAR'
    background_lamp.data.shadow_filter_type = 'GAUSS'
    background_lamp.data.shadow_buffer_soft = 100
    background_lamp.data.shadow_buffer_samples = 16
    background_lamp.data.shadow_buffer_size = 1024
    background_lamp.data.shadow_buffer_clip_end = 5
    background_lamp.data.spot_size = 1.48353
    background_lamp.data.distance = 5
    background_plane.parent = camera
    background_lamp.parent = camera
