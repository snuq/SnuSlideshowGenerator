import bpy


def extra(data):
    image_scene = data['image_scene']
    camera = data['camera']
    extra_amount = data['extra_amount']
    bpy.context.window.scene = image_scene
    bpy.ops.mesh.primitive_plane_add(size=2.5, location=(0, 0, -3))
    background_plane = bpy.context.active_object
    background_plane.name = 'Light Background'
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, -0.7))
    background_lamp = bpy.context.active_object
    background_lamp.data.spot_size = 1.48353
    background_lamp.data.energy = 50
    background_lamp.data.shadow_soft_size = 0.05
    background_plane.parent = camera
    background_lamp.parent = camera
    background_material = bpy.data.materials.new('Light Background')
    background_plane.data.materials.append(background_material)
    background_material.use_nodes = True
    node_tree = background_material.node_tree
    nodes = node_tree.nodes
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            background_shaded = node
    background_shaded.inputs["Emission Strength"].default_value = extra_amount
    background_shaded.inputs["Base Color"].default_value = (1, 1, 1, 1)
