import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    name = 'Vignette'
    location = (0, 0, -0.93)
    render = image_scene.render
    aspect_ratio = (render.pixel_aspect_x * render.resolution_x) / (render.pixel_aspect_y * render.resolution_y)

    fullwidth = 1.28
    if aspect_ratio > 1:
        dimy = aspect_ratio * fullwidth
        dimensions = (fullwidth, dimy, 0)
    else:
        dimx = aspect_ratio * fullwidth
        dimensions = (dimx, fullwidth, 0)
    texture_type = 'BLEND'

    bpy.ops.mesh.primitive_plane_add()
    vignette = bpy.context.scene.objects.active
    vignette.name = name
    modifier = vignette.modifiers.new(name='', type='SUBSURF')
    modifier.render_levels = 1
    modifier.subdivision_type = 'SIMPLE'
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap()
    bpy.ops.object.mode_set(mode='OBJECT')
    vignette.dimensions = dimensions
    bpy.ops.object.transform_apply(scale=True)
    vignette.location = location
    material = bpy.data.materials.new(name)
    vignette.data.materials.append(material)
    texture = bpy.data.textures.new(name+' Texture', type=texture_type)
    texture_slot = material.texture_slots.add()
    texture_slot.texture = texture
    texture_slot.color = (0, 0, 0)
    texture_slot.texture_coords = 'UV'
    texture_slot.invert = True
    material.use_shadeless = True
    material.use_transparency = True
    material.alpha = 0
    texture.use_preview_alpha = True
    material.diffuse_color = (0, 0, 0)
    texture.id_data.progression = 'QUADRATIC_SPHERE'
    texture.intensity = 2
    texture.contrast = 2.5 + extra_amount
    texture_slot.use_map_alpha = True
    texture_slot.alpha_factor = 1
    vignette.parent = camera
