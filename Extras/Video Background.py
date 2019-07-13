import bpy


def extra(data):
    image_scene = data['image_scene']
    camera = data['camera']
    extra_texture = data['extra_texture']
    bpy.context.window.scene = image_scene

    name = 'Video Background'
    location = (0, 0, -2.93)
    fullwidth = 2.12
    render = image_scene.render
    aspect_ratio = (render.pixel_aspect_x * render.resolution_x) / (render.pixel_aspect_y * render.resolution_y)
    if aspect_ratio < 1:
        #taller
        dimensions = ((aspect_ratio / 1) * fullwidth, fullwidth, 0)
    else:
        #wider
        dimensions = (fullwidth, (1 / aspect_ratio) * fullwidth, 0)

    bpy.ops.mesh.primitive_plane_add()
    video = bpy.context.active_object
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
    video.parent = camera
    material = bpy.data.materials.new(name)
    video.data.materials.append(material)
    material.use_nodes = True
    node_tree = material.node_tree
    nodes = node_tree.nodes
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    texture = nodes.new('ShaderNodeTexImage')
    node_tree.links.new(texture.outputs[0], emission.inputs[0])
    node_tree.links.new(emission.outputs[0], output.inputs[0])
    texture.image_user.use_auto_refresh = True

    if extra_texture is not None:
        texture.image = extra_texture
        texture.image.update()
        texture.image_user.frame_duration = texture.image.frame_duration
        texture.image_user.frame_offset = 0
