import bpy


def extra(data):
    image_scene = data['image_scene']
    extra_amount = data['extra_amount']
    bpy.context.window.scene = image_scene
    node_tree = bpy.data.node_groups.new(name=image_scene.name, type='CompositorNodeTree')
    image_scene.compositing_node_group = node_tree
    nodes = node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    node_input = nodes.new(type="CompositorNodeRLayers")
    node_input.location = (-100, 400)
    node_glare = nodes.new(type="CompositorNodeGlare")
    node_glare.location = (150, 400)
    node_glare.inputs['Quality'].default_value = 'Low'
    node_glare.inputs['Threshold'].default_value = 1 - (extra_amount / 1.5)
    node_glare.inputs['Strength'].default_value = 2
    node_output = nodes.new(type="NodeGroupOutput")
    node_output.location = (400, 400)
    links = node_tree.links
    links.new(node_input.outputs['Image'], node_glare.inputs['Image'])
    links.new(node_glare.outputs['Image'], node_output.inputs[0], handle_dynamic_sockets=True)
