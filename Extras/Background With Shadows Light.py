import bpy


def extra(data):
    image_scene = data['image_scene']
    camera = data['camera']
    bpy.context.window.scene = image_scene
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, -3))
    background_plane = bpy.context.active_object
    background_plane.name = 'Textured Light Background'
    modifier = background_plane.modifiers.new(name='', type='SUBSURF')
    modifier.render_levels = 1
    modifier.subdivision_type = 'SIMPLE'
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, -0.7))
    background_lamp = bpy.context.active_object
    background_lamp.data.spot_size = 1.48353
    background_lamp.data.energy = 50
    background_lamp.data.distance = 5
    background_plane.parent = camera
    background_lamp.parent = camera
    background_material = bpy.data.materials.new('Textured Light Background')
    background_plane.data.materials.append(background_material)
    background_material.use_nodes = True
    node_tree = background_material.node_tree
    nodes = node_tree.nodes
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            background_shaded = node
    background_tex_one = nodes.new("ShaderNodeTexVoronoi")
    background_tex_one.inputs["Scale"].default_value = 150
    background_tex_two = nodes.new("ShaderNodeTexNoise")
    background_tex_two.inputs["Scale"].default_value = 35
    background_tex_two.inputs["Detail"].default_value = 8
    background_tex_two.inputs["Distortion"].default_value = 0.2
    background_tex_mix = nodes.new("ShaderNodeMixRGB")
    background_tex_mix.inputs["Fac"].default_value = 0.8
    background_bump = nodes.new("ShaderNodeBump")
    background_bump.invert = True
    background_bump.inputs["Strength"].default_value = 0.5
    node_tree.links.new(background_tex_one.outputs["Fac"], background_tex_mix.inputs[1])
    node_tree.links.new(background_tex_two.outputs["Fac"], background_tex_mix.inputs[2])
    node_tree.links.new(background_tex_mix.outputs[0], background_bump.inputs["Height"])
    node_tree.links.new(background_bump.outputs["Normal"], background_shaded.inputs["Normal"])
    background_shaded.inputs["Roughness"].default_value = 0.4
    background_shaded.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
