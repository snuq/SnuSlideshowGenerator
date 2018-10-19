import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    #duplicate image_plane
    bpy.ops.object.select_all(action='DESELECT')
    image_plane.select = True
    bpy.ops.object.duplicate(linked=False)
    blurred_plane = bpy.context.selected_objects[0]
    modifier = blurred_plane.modifiers.new(name='', type='SUBSURF')
    modifier.render_levels = 1
    modifier.subdivision_type = 'SIMPLE'

    #remove constraints
    for constraint in blurred_plane.constraints:
        blurred_plane.constraints.remove(constraint)

    #set up blurred plane
    blurred_plane.parent = image_plane
    if blurred_plane.dimensions[0] > blurred_plane.dimensions[1]:
        blurred_size = blurred_plane.dimensions[0]
    else:
        blurred_size = blurred_plane.dimensions[1]
    scale_factor = (8 / blurred_size)
    blurred_plane.scale = (blurred_plane.scale * scale_factor)
    location = blurred_plane.location
    blurred_plane.location = (0, 0, (location[2] - 3))

    #set up defocus nodes
    image_scene.use_nodes = True
    nodes = image_scene.node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    node_input = nodes.new(type="CompositorNodeRLayers")
    node_input.location = (-100, 400)
    node_defocus = nodes.new(type="CompositorNodeDefocus")
    node_defocus.location = (150, 400)
    node_defocus.use_zbuffer = True
    node_defocus.use_preview = False
    node_defocus.f_stop = 8
    node_defocus.blur_max = (16 * (extra_amount * 2))
    node_defocus.use_preview = True
    node_output = nodes.new(type="CompositorNodeComposite")
    node_output.location = (400, 400)
    links = image_scene.node_tree.links
    links.new(node_input.outputs['Image'], node_defocus.inputs['Image'])
    links.new(node_input.outputs['Depth'], node_defocus.inputs['Z'])
    links.new(node_defocus.outputs['Image'], node_output.inputs['Image'])
