import bpy


def extra(data):
    image_scene = data['image_scene']
    camera = data['camera']
    extra_amount = data['extra_amount']
    bpy.context.window.scene = image_scene

    name = 'Vignette'
    location = (0, 0, -0.93)
    render = image_scene.render
    aspect_ratio = (render.pixel_aspect_x * render.resolution_x) / (render.pixel_aspect_y * render.resolution_y)
    if aspect_ratio < 1:
        #taller
        dimensions = (aspect_ratio / 1, 1, 0)
    else:
        #wider
        dimensions = (1, 1 / aspect_ratio, 0)

    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    vignette = bpy.context.active_object
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
    vignette.parent = camera
    material.use_nodes = True
    material.blend_method = 'BLEND'
    node_tree = material.node_tree
    nodes = node_tree.nodes
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    mix = nodes.new('ShaderNodeMixShader')
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (0, 0, 0, 1)
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    add = nodes.new('ShaderNodeMath')
    add.operation = 'ADD'
    add.use_clamp = True
    add.inputs[1].default_value = -0.5 + (1 - extra_amount)
    texture = nodes.new('ShaderNodeTexGradient')
    texture.gradient_type = 'QUADRATIC_SPHERE'
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Location'].default_value = (-0.5, -0.5, 0)
    coords = nodes.new('ShaderNodeTexCoord')
    node_tree.links.new(coords.outputs['UV'], mapping.inputs[0])
    node_tree.links.new(mapping.outputs[0], texture.inputs[0])
    node_tree.links.new(texture.outputs[0], add.inputs[0])
    node_tree.links.new(add.outputs[0], mix.inputs[0])
    node_tree.links.new(emission.outputs[0], mix.inputs[1])
    node_tree.links.new(transparent.outputs[0], mix.inputs[2])
    node_tree.links.new(mix.outputs[0], output.inputs[0])

