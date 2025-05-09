import bpy


def extra(data):
    image_scene = data['image_scene']
    extra_amount = data['extra_amount']
    bpy.context.window.scene = image_scene
    image_scene.use_nodes = True
    nodes = image_scene.node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    node_input = nodes.new(type="CompositorNodeRLayers")
    node_input.location = (-100, 400)
    node_glare = nodes.new(type="CompositorNodeGlare")
    node_glare.location = (150, 400)
    node_glare.quality = 'LOW'
    node_glare.inputs['Threshold'].default_value = 1 - (extra_amount / 1.5)
    node_glare.inputs['Strength'].default_value = 2
    node_output = nodes.new(type="CompositorNodeComposite")
    node_output.location = (400, 400)
    links = image_scene.node_tree.links
    links.new(node_input.outputs['Image'], node_glare.inputs['Image'])
    links.new(node_glare.outputs['Image'], node_output.inputs['Image'])
