import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    name = 'Video Foreground'
    location = (0, 0, -0.93)
    dimensions = (0.856, 0.481, 0)
    texture_type = 'IMAGE'

    bpy.ops.mesh.primitive_plane_add()
    video = bpy.context.scene.objects.active
    video.name = name
    modifier = video.modifiers.new(name='', type='SUBSURF')
    modifier.render_levels = 1
    modifier.subdivision_type = 'SIMPLE'
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap()
    bpy.ops.object.mode_set(mode='OBJECT')
    video.dimensions = dimensions
    bpy.ops.object.transform_apply(scale=True)
    video.location = location
    material = bpy.data.materials.new(name)
    video.data.materials.append(material)
    texture = bpy.data.textures.new(name+' Texture', type=texture_type)
    texture_slot = material.texture_slots.add()
    texture_slot.texture = texture

    texture_slot.texture_coords = 'UV'
    texture.image_user.use_auto_refresh = True
    material.use_shadeless = True
    material.use_transparency = True
    material.alpha = 0
    texture.use_preview_alpha = True
    texture.use_alpha = True
    texture.use_calculate_alpha = True
    material.diffuse_color = (0, 0, 0)
    if extra_texture is not None:
        texture.image = extra_texture
        texture.image.update()
        texture.image_user.frame_duration = texture.image.frame_duration
        texture.image_user.frame_offset = 0
    texture_slot.use_map_alpha = True
    texture_slot.alpha_factor = extra_amount
    video.parent = camera
