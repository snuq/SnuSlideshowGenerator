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
    background_material.use_shadeless = True
    background_plane.parent = camera
