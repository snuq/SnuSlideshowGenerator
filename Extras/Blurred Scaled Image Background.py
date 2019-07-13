import bpy


def extra(data):
    image_scene = data['image_scene']
    camera = data['camera']
    image_plane = data['image_plane']
    extra_amount = data['extra_amount']
    bpy.context.window.scene = image_scene

    #duplicate image_plane
    bpy.ops.object.select_all(action='DESELECT')
    image_plane.select_set(True)
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
    scale_factor = (120 / blurred_size)
    blurred_plane.scale = (blurred_plane.scale * scale_factor)
    location = blurred_plane.location
    blurred_plane.location = (0, 0, (location[2] - 100))

    #set up depth of field
    camera.data.dof.use_dof = True
    camera.data.dof.aperture_fstop = 3 - (extra_amount * 2)
