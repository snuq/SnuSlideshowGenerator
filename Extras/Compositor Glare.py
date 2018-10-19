import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene
    image_scene.use_nodes = True
    nodes = image_scene.node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    node_input = nodes.new(type="CompositorNodeRLayers")
    node_input.location = (-100, 400)
    node_glare = nodes.new(type="CompositorNodeGlare")
    node_glare.location = (150, 400)
    node_glare.threshold = 1 - (extra_amount / 1.5)
    node_glare.quality = 'LOW'
    node_output = nodes.new(type="CompositorNodeComposite")
    node_output.location = (400, 400)
    links = image_scene.node_tree.links
    links.new(node_input.outputs['Image'], node_glare.inputs['Image'])
    links.new(node_glare.outputs['Image'], node_output.inputs['Image'])
