# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#Known bugs:
#   aspect ratio isnt detected properly for videos with non-square pixels... not sure how to detect this.
"""
todo: move generator panel to a 3d view tools panel, this will ensure the user has at least one 3d view open, rethink scene view snapping also
todo: update extras:
    Text Normal
    Video
"""

import bpy
import random
import glob
import os
import sys
import math
from bpy_extras.image_utils import load_image
from bpy.app.handlers import persistent


bl_info = {
    "name": "Snu Slideshow Generator",
    "description": "Assists in creating image slideshows with a variety of options.",
    "author": "Hudson Barkley (Snu)",
    "version": (0, 8, 2),
    "blender": (2, 80, 0),
    "location": "Properties Area, Scene Tab, 'Snu Slideshow Generator' Panel.",
    "wiki_url": "https://github.com/snuq/SnuSlideshowGenerator",
    "category": "Import-Export"
}


#This is a list of transform dictionary objects
transforms = [
    {
        'name': 'None',
        'influence': [(0, 1)],
        'zLoc': [(0, 1)],
        'zRot': [(0, 1)],
        'xLoc': [(0, 1)]
    },
    {
        'name': 'Move Left Complete With Pause',
        'xLoc': [(-1, 0), (0, 1), (1, 0)]
    },
    {
        'name': 'Move Right Complete With Pause',
        'xLoc': [(1, 0), (0, 1), (-1, 0)]
    },
    {
        'name': 'Move Left Little',
        'xLoc': [(-0.15, 1), (0.15, 1)]
    },
    {
        'name': 'Move Right Little',
        'xLoc': [(0.15, 1), (-0.15, 1)]
    },
    {
        'name': 'Rotate Left Around Top',
        'zLoc': [(-0.1, 1)],
        'zRot': [(-10, 1), (10, 1)],
        'xLoc': [(-0.1, 1), (0.1, 1)]
    },
    {
        'name': 'Rotate Left Around Bottom',
        'zLoc': [(-0.1, 1)],
        'zRot': [(10, 1), (-10, 1)],
        'xLoc': [(-0.1, 1), (0.1, 1)]
    },
    {
        'name': 'Rotate Right Around Top',
        'zLoc': [(-0.1, 1)],
        'zRot': [(10, 1), (-10, 1)],
        'xLoc': [(0.1, 1), (-0.1, 1)]
    },
    {
        'name': 'Rotate Right Around Bottom',
        'zLoc': [(-0.1, 1)],
        'zRot': [(-10, 1), (10, 1)],
        'xLoc': [(0.1, 1), (-0.1, 1)]
    },
    {
        'name': 'Pan To Target',
        'influence': [(0, 1), (1, 1)]
    },
    {
        'name': 'Rotate Left',
        'zLoc': [(-0.1, 1)],
        'zRot': [(10, 1), (-10, 1)]
    },
    {
        'name': 'Rotate Right',
        'zLoc': [(-0.1, 1)],
        'zRot': [(-10, 1), (10, 1)]
    },
    {
        'name': 'Zoom In',
        'influence': [(0, 1), (1, 1)],
        'zLoc': [(0, 1), (-0.3, 1)]
    },
    {
        'name': 'Zoom Out',
        'influence': [(1, 1), (0, 1)],
        'zLoc': [(-0.3, 1), (0, 1)]
    },
    {
        'name': 'Zoom In And Rotate Left',
        'influence': [(0, 1), (1, 1)],
        'zLoc': [(0, 1), (-0.3, 1)],
        'zRot': [(0, 1), (-10, 1)]
    },
    {
        'name': 'Zoom In And Rotate Right',
        'influence': [(0, 1), (1, 1)],
        'zLoc': [(0, 1), (-0.3, 1)],
        'zRot': [(0, 1), (10, 1)]
    },
    {
        'name': 'Zoom Out And Rotate Left',
        'influence': [(1, 1), (0, 1)],
        'zLoc': [(-0.3, 1), (0, 1)],
        'zRot': [(10, 1), (0, 1)]
    },
    {
        'name': 'Zoom Out And Rotate Right',
        'influence': [(1, 1), (0, 1)],
        'zLoc': [(-0.3, 1), (0, 1)],
        'zRot': [(-10, 1), (0, 1)]
    }
]


def update_scene(scene):
    for view_layer in scene.view_layers:
        view_layer.update()
        view_layer.objects.update()


def select_plane(image_plane, scene):
    if image_plane:
        if image_plane.name in bpy.context.view_layer.objects:  #Bug in Blender 2.8... seems this doesnt get updated when called from a panel
            image_plane.select_set(True)
            bpy.context.view_layer.objects.active = image_plane


def is_generator_scene(scene):
    if scene.name == 'Slideshow Generator':
        return True
    else:
        return False


@persistent
def slideshow_autoupdate(_):
    #Auto-running modal function to update the slideshow scene so the slides stay ordered properly
    if is_generator_scene(bpy.context.scene):
        update_order()
        lock_view()


def lock_view():
    space = get_first_3d_view()
    if space:
        space.region_3d.view_rotation = (1.0, 0, 0, 0)
        space.region_3d.view_perspective = 'ORTHO'


def format_seconds(seconds):
    if seconds > 60:
        minutes, extra_seconds = divmod(seconds, 60)
        length_formatted = str(int(minutes))+" Minutes, "+str(int(extra_seconds))+" Seconds"
    else:
        length_formatted = str(round(seconds, 2)) + " Seconds"
    return length_formatted


def get_fps(scene):
    return scene.render.fps / scene.render.fps_base


def create_scene(oldscene, scenename):
    #Creates a new scene and copies over render settings from current scene
    newscene = bpy.data.scenes.new(scenename)
    bpy.context.window.scene = newscene

    #These loops are needed because there apparently is no way to easily copy the render settings from one scene to another
    for prop in oldscene.render.bl_rna.properties:
        #Copy the general render settings
        if not prop.is_readonly:
            value = eval('oldscene.render.'+prop.identifier)
            setattr(newscene.render, prop.identifier, value)
    for prop in oldscene.render.image_settings.bl_rna.properties:
        #Copy the image/video encoding settings
        if not prop.is_readonly:
            value = eval('oldscene.render.image_settings.'+prop.identifier)
            setattr(newscene.render.image_settings, prop.identifier, value)
    for prop in oldscene.render.ffmpeg.bl_rna.properties:
        #Copy the video encoder settings
        if not prop.is_readonly:
            value = eval('oldscene.render.ffmpeg.'+prop.identifier)
            setattr(newscene.render.ffmpeg, prop.identifier, value)

    newscene.view_settings.view_transform = oldscene.view_settings.view_transform  #really not sure why this is needed, but it is...?

    #Set variables that are specific to the slideshow scene
    newscene.render.film_transparent = False
    newscene.render.engine = 'BLENDER_EEVEE'
    newscene.render.resolution_percentage = 100
    newscene.render.image_settings.color_mode = 'RGB'
    return newscene


def aspect_ratio(scene):
    render = scene.render
    return (render.pixel_aspect_x * render.resolution_x) / (render.pixel_aspect_y * render.resolution_y)


def get_material_elements(material, image_name):
    #Gets the material nodes for the given material.  If the material is corrupted, will recreate and return the fixed one, if image cannot be found, returns None.
    tree = material.node_tree
    nodes = tree.nodes
    texture = None
    shadeless = None
    shaded = None
    mix = None
    output = None
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            texture = node
        if node.type == 'EMISSION':
            shadeless = node
        if node.type == 'BSDF_PRINCIPLED':
            shaded = node
        if node.type == 'MIX_SHADER':
            mix = node
        if node.type == 'OUTPUT_MATERIAL':
            output = node
    if texture is None or shadeless is None or shaded is None or mix is None or output is None:
        if texture is not None:
            image = texture.image
        elif image_name in bpy.data.images:
            image = bpy.data.images[image_name]
        else:
            return None
        return setup_material(material, image)
    else:
        material_nodes = {
            'texture': texture,
            'shadeless': shadeless,
            'shaded': shaded,
            'mix': mix,
            'output': output
        }
        return material_nodes


def setup_material(material, image):
    #Setup an image/video material
    material.use_nodes = True
    tree = material.node_tree
    nodes = tree.nodes
    nodes.clear()

    #Create nodes
    texture = nodes.new('ShaderNodeTexImage')
    texture.image = image
    texture.image_user.frame_duration = image.frame_duration
    texture.image_user.frame_offset = 0
    texture.image_user.use_auto_refresh = True
    texture.location = (-400, 0)
    shadeless = nodes.new('ShaderNodeEmission')
    shadeless.location = (0, 0)
    shaded = nodes.new('ShaderNodeBsdfPrincipled')
    shaded.location = (-100, -150)
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (200, 0)
    mix.inputs[0].default_value = 0
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    #Connect nodes
    tree.links.new(texture.outputs[0], shadeless.inputs[0])
    tree.links.new(texture.outputs[0], shaded.inputs[0])
    tree.links.new(shadeless.outputs[0], mix.inputs[1])
    tree.links.new(shaded.outputs[0], mix.inputs[2])
    tree.links.new(mix.outputs[0], output.inputs[0])
    material_nodes = {
        'texture': texture,
        'shadeless': shadeless,
        'shaded': shaded,
        'mix': mix,
        'output': output
    }
    return material_nodes


def import_slideshow_image(image, image_number, slide_length, generator_scene, video=False, last_image=None):
    #This function will import an image into the generator scene and create the objects needed for modifying slides in the generator
    if len(image.name) > 20:
        image.name = image.name[0:19]
    if video:
        print('Importing video '+str(image_number)+', filename: '+image.name)
    else:
        print('Importing image '+str(image_number)+', filename: '+image.name)

    #create and set up image plane
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    image_mesh = bpy.data.meshes.new(name=image.name)
    ix = ((image.size[0] / image.size[1])/2)
    iy = 0.5
    verts = [(-ix, iy, 0.0), (ix, iy, 0.0), (ix, -iy, 0.0), (-ix, -iy, 0.0)]
    faces = [(3, 2, 1, 0)]
    image_mesh.from_pydata(verts, [], faces)
    image_plane = bpy.data.objects.new(name=image.name, object_data=image_mesh)
    generator_scene.collection.objects.link(image_plane)
    image_plane.slideshow.name = image_plane.name

    add_constraints(image_plane, 'Plane')

    if video:
        image_plane.slideshow.locklength = True
        image_plane.slideshow.lockextra = True
        image_plane.slideshow.locktransform = True
        image_plane.slideshow.videomaxlength = image.frame_duration
        image_plane.slideshow.videofile = image.filepath
        slide_length = image.frame_duration / get_fps(generator_scene)

    #set up and apply material to plane
    image_material = bpy.data.materials.new(image_plane.name)
    image_plane.data.uv_layers.new()
    image_plane.data.materials.append(image_material)  #set material to plane
    setup_material(image_material, image)

    #set up transform and extras
    if not video:
        randomized = []
        hidden = generator_scene.snu_slideshow_generator.hidden_transforms.split(";")
        for transform in transforms:
            if transform['name'] not in hidden:
                if last_image:
                    if transform['name'] != last_image.slideshow.transform:
                        randomized.append(transform)
                else:
                    randomized.append(transform)
        if len(randomized) == 0:
            transform = transforms[0]
        else:
            transform = randomized[random.randint(0, (len(randomized) - 1))]

        randomized = []
        hidden = generator_scene.snu_slideshow_generator.hidden_extras.split(";")
        extras = list_extras()
        for extra in extras:
            if extra not in hidden:
                if last_image:
                    if extra != last_image.slideshow.extra:
                        randomized.append(extra)
                else:
                    randomized.append(extra)
        if len(randomized) == 0:
            extra = "None"
        else:
            extra = randomized[random.randint(0, (len(randomized) - 1))]

        randomized = []
        for extra_texture_preset in generator_scene.snu_slideshow_generator.extra_texture_presets:
            if last_image:
                if extra_texture_preset.path != last_image.slideshow.extratexture:
                    randomized.append(extra_texture_preset.path)
            else:
                randomized.append(extra_texture_preset.path)
        if len(randomized) == 0:
            extra_texture = 'None'
        else:
            if len(generator_scene.snu_slideshow_generator.extra_texture_presets) > 1:
                extra_texture = randomized[random.randint(0, (len(randomized) - 1))]
            else:
                extra_texture = generator_scene.snu_slideshow_generator.extra_texture_presets[0].path

        #add target empty
        target_empty = bpy.data.objects.new(name=image_plane.name+' Target', object_data=None)
        target_empty.parent = image_plane
        target_empty.empty_display_size = 1
        add_constraints(target_empty, 'Target')
        image_plane.slideshow.target = target_empty.name
        generator_scene.collection.objects.link(target_empty)

        #add view empty
        view_empty = bpy.data.objects.new(name=image_plane.name+' View', object_data=None)
        view_empty.parent = image_plane
        view_empty.empty_display_size = 1
        view_empty.scale = aspect_ratio(generator_scene) / 2, .5, .001
        view_empty.empty_display_type = 'CUBE'
        add_constraints(view_empty, 'View')
        image_plane.slideshow.view = view_empty.name
        generator_scene.collection.objects.link(view_empty)

    #add text next to plane saying which index number it is
    index_text_name = image_plane.name+' Index'
    index_text_data = bpy.data.curves.new(name=index_text_name, type='FONT')
    index_text = bpy.data.objects.new(name=index_text_name, object_data=index_text_data)
    generator_scene.collection.objects.link(index_text)
    index_text.parent = image_plane
    index_text.location = (-1, -.33, 0)
    index_text.data.align_x = 'RIGHT'
    add_constraints(index_text, 'Text')

    if not video:
        #add text next to plane saying which transform was picked
        transform_text_name = image_plane.name+' Transform'
        transform_text_data = bpy.data.curves.new(name=transform_text_name, type='FONT')
        transform_text = bpy.data.objects.new(name=transform_text_name, object_data=transform_text_data)
        generator_scene.collection.objects.link(transform_text)
        transform_text.parent = image_plane
        transform_text.location = (1, 0, 0)
        transform_text.scale = .15, .15, 1
        add_constraints(transform_text, 'Text')

        #add text next to plane saying which extra was picked
        extra_text_name = image_plane.name+' Extra'
        extra_text_data = bpy.data.curves.new(name=extra_text_name, type='FONT')
        extra_text = bpy.data.objects.new(name=extra_text_name, object_data=extra_text_data)
        generator_scene.collection.objects.link(extra_text)
        extra_text.parent = image_plane
        extra_text.location = (1, -.25, 0)
        extra_text.scale = .15, .15, 1
        add_constraints(extra_text, 'Text')

    #add text next to plane saying how long the slide is
    length_text_name = image_plane.name+' Length'
    length_text_data = bpy.data.curves.new(name=length_text_name, type='FONT')
    length_text = bpy.data.objects.new(name=length_text_name, object_data=length_text_data)
    generator_scene.collection.objects.link(length_text)
    length_text.parent = image_plane
    length_text.location = (1, .25, 0)
    length_text.scale = .15, .15, 1
    add_constraints(length_text, 'Text')

    #create group and add everything to it
    image_group = bpy.data.collections.new(image_plane.name)
    image_group.objects.link(image_plane)
    image_group.objects.link(index_text)
    image_group.objects.link(length_text)
    if not video:
        image_group.objects.link(target_empty)
        image_group.objects.link(transform_text)
        image_group.objects.link(extra_text)
        image_group.objects.link(view_empty)

    #additional settings
    image_plane.slideshow.index = image_number + 1
    if not video:
        image_plane.slideshow.length = slide_length
        image_plane.slideshow.transform = transform['name']
        image_plane.slideshow.extra = extra
        image_plane.slideshow.extratexture = extra_texture
    else:
        image_plane.slideshow.videolength = image.frame_duration
    return image_plane


def add_constraints(constraint_object, constraint_type):
    #This function handles adding constraints to the various objects of the slideshow generator scene
    bpy.context.view_layer.objects.active = constraint_object
    rotation_constraint = constraint_object.constraints.new(type='LIMIT_ROTATION')
    location_constraint = constraint_object.constraints.new(type='LIMIT_LOCATION')
    scale_constraint = constraint_object.constraints.new(type='LIMIT_SCALE')

    #set up rotation constraint
    rotation_constraint.use_limit_x = True
    rotation_constraint.use_limit_y = True
    if constraint_type != 'View':
        rotation_constraint.use_limit_z = True

    #set up local location constraint
    constraint_object.constraints[1].owner_space = 'LOCAL'
    if constraint_type == 'Target' or constraint_type == 'View':
        location_constraint.min_x = -1 * (aspect_ratio(bpy.context.scene)/2)
        location_constraint.max_x = aspect_ratio(bpy.context.scene) / 2
        location_constraint.min_y = -.5
        location_constraint.max_y = .5
    else:
        location_constraint.min_x = constraint_object.location[0]
        location_constraint.max_x = constraint_object.location[0]
        location_constraint.min_y = constraint_object.location[1]
        location_constraint.max_y = constraint_object.location[1]
    location_constraint.use_max_x = True
    location_constraint.use_min_x = True
    if constraint_type != 'Plane':
        location_constraint.use_max_y = True
        location_constraint.use_min_y = True
    location_constraint.use_max_z = True
    location_constraint.use_min_z = True

    #set up limit scale constraint
    scale_constraint.min_x = constraint_object.scale[0]
    scale_constraint.max_x = constraint_object.scale[0]
    scale_constraint.min_y = constraint_object.scale[1]
    scale_constraint.max_y = constraint_object.scale[1]
    scale_constraint.min_z = constraint_object.scale[2]
    scale_constraint.max_z = constraint_object.scale[2]
    if constraint_type != 'View':
        scale_constraint.use_min_x = True
        scale_constraint.use_max_x = True
        scale_constraint.use_min_y = True
        scale_constraint.use_max_y = True
        scale_constraint.use_min_z = True
        scale_constraint.use_max_z = True

    #set up text world location limit
    if constraint_type == 'Text':
        limit_location_constraint = constraint_object.constraints.new(type='LIMIT_LOCATION')
        limit_location_constraint.owner_space = 'WORLD'
        limit_location_constraint.use_max_x = True
        limit_location_constraint.use_min_x = True
        limit_location_constraint.min_x = constraint_object.location[0]
        limit_location_constraint.max_x = constraint_object.location[0]


def is_video_file(file):
    if os.path.isfile(file):
        extensions = bpy.path.extensions_movie
        extension = os.path.splitext(file)[1]
        if extension.lower() in extensions:
            return True
    return False


def create_slideshow_slide(image_plane, i, generator_scene, slideshow_scene, image_scene_start, images, previous_image_clip, previous_image_plane):
    #This function makes the slideshow image scene and adds it to the sequencer of the slideshow_scene scene
    image_scene_name = image_plane.name

    if not slideshow_scene.sequence_editor:
        slideshow_scene.sequence_editor_create()

    if not image_plane.slideshow.videofile:
        print('Generating scene for: '+image_scene_name)
        if bpy.data.scenes.find(image_scene_name) != -1:
            bpy.data.scenes.remove(bpy.data.scenes[image_scene_name])
        image_scene = create_scene(generator_scene, image_scene_name)

        #Set up image_scene render settings
        image_scene_frames = (get_fps(image_scene) * image_plane.slideshow.length)
        image_scene.frame_end = image_scene_frames

        bpy.context.window.scene = generator_scene
        bpy.ops.object.select_all(action='DESELECT')
        image_plane.select_set(True)
        target_empty = generator_scene.objects[image_plane.slideshow.target]
        target_empty.select_set(True)
        view_empty = generator_scene.objects[image_plane.slideshow.view]
        view_empty.select_set(True)
        bpy.ops.object.make_links_scene(scene=image_scene.name)

        #set scene
        bpy.context.window.scene = image_scene

        #set up scene world
        world = bpy.data.worlds.new(image_scene.name)
        image_scene.world = world
        world.use_nodes = False
        world.color = (0, 0, 0)

        #create transforms
        bpy.ops.object.select_all(action='DESELECT')
        image_scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.object.empty_add()
        transform_empty = bpy.context.active_object
        transform_index = get_transform(image_plane.slideshow.transform)
        if transform_index >= 0:
            transform = transforms[transform_index]
        else:
            transform = transforms[0]
        image_scene.frame_current = 1
        transform_empty.name = transform['name']
        transform_empty.animation_data_create()
        transform_action = bpy.data.actions.new(transform['name'])
        transform_empty.animation_data.action = transform_action
        aspect = aspect_ratio(image_scene)
        if aspect > 1:
            zoffset = aspect * 1.09
        else:
            zoffset = 1.09
        transform_empty.location = (0, 0, zoffset)
        if 'zLoc' in transform.keys():
            locations = len(transform['zLoc'])
            fcurve = transform_action.fcurves.new('location', index=2)
            for index, location in enumerate(transform['zLoc']):
                if locations == 1:
                    pointx = 1
                else:
                    pointx = ((index * image_scene_frames)/(locations - 1)) + 1
                pointy = transform['zLoc'][index][0] + zoffset
                pointsize = (transform['zLoc'][index][1]) * (image_scene_frames / locations / 2)
                point = fcurve.keyframe_points.insert(frame=pointx, value=pointy)
                point.handle_left_type = 'FREE'
                point.handle_right_type = 'FREE'
                point.handle_left = (pointx - pointsize, pointy)
                point.handle_right = (pointx + pointsize, pointy)
        if 'zRot' in transform.keys():
            locations = len(transform['zRot'])
            fcurve = transform_action.fcurves.new('rotation_euler', index=2)
            for index, location in enumerate(transform['zRot']):
                if locations == 1:
                    pointx = 1
                else:
                    pointx = ((index * image_scene_frames)/(locations - 1)) + 1
                pointy = 3.14159265358979 * (transform['zRot'][index][0]) / 180
                pointsize = (transform['zRot'][index][1]) * (image_scene_frames / locations / 2)
                point = fcurve.keyframe_points.insert(frame=pointx, value=pointy)
                point.handle_left_type = 'FREE'
                point.handle_right_type = 'FREE'
                point.handle_left = (pointx - pointsize, pointy)
                point.handle_right = (pointx + pointsize, pointy)
        if 'xLoc' in transform.keys():
            locations = len(transform['xLoc'])
            fcurve = transform_action.fcurves.new('location', index=0)
            for index, location in enumerate(transform['xLoc']):
                if locations == 1:
                    pointx = 1
                else:
                    pointx = ((index * image_scene_frames)/(locations - 1)) + 1
                pointy = (transform['xLoc'][index][0]) * aspect_ratio(bpy.context.scene)
                pointsize = (transform['xLoc'][index][1]) * (image_scene_frames / locations / 2)
                point = fcurve.keyframe_points.insert(frame=pointx, value=pointy)
                point.handle_left_type = 'FREE'
                point.handle_right_type = 'FREE'
                point.handle_left = (pointx - pointsize, pointy)
                point.handle_right = (pointx + pointsize, pointy)
        if 'influence' in transform.keys():
            constraint = transform_empty.constraints.new(type='COPY_LOCATION')
            constraint.use_z = False
            constraint.target = target_empty
            constraint.influence = 0
            locations = len(transform['influence'])
            fcurve = transform_action.fcurves.new('constraints[0].influence')
            for index, location in enumerate(transform['influence']):
                if locations == 1:
                    pointx = 1
                else:
                    pointx = ((index * image_scene_frames)/(locations - 1)) + 1
                pointy = transform['influence'][index][0]
                pointsize = (transform['influence'][index][1]) * (image_scene_frames / locations / 2)
                point = fcurve.keyframe_points.insert(frame=pointx, value=pointy)
                point.handle_left_type = 'FREE'
                point.handle_right_type = 'FREE'
                point.handle_left = (pointx - pointsize, pointy)
                point.handle_right = (pointx + pointsize, pointy)

        #set up camera location scale and animation
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        bpy.ops.object.camera_add()
        camera = bpy.context.active_object
        camera.parent = transform_empty
        image_scene.camera = camera
        camera.data.dof.focus_object = image_plane
        camera.data.dof.use_dof = False

        #add camera_scale empty that will scale the transform and camera
        bpy.ops.object.empty_add()
        camera_scale = bpy.context.active_object
        camera_scale.parent = image_plane
        transform_empty.parent = camera_scale
        camera_scale.location = view_empty.location
        camera_scale.rotation_euler = view_empty.rotation_euler
        camera_scale_value = (view_empty.scale[1] * 2)
        camera_scale.scale = (camera_scale_value, camera_scale_value, camera_scale_value)

        #run extras script
        if image_plane.slideshow.extra != 'None':
            extra = get_extra(image_plane.slideshow.extra)
            if extra:
                try:
                    folder = os.path.split(extra)[0]
                    file = os.path.splitext(os.path.split(extra)[1])[0]
                    sys.path.insert(0, folder)
                    script = __import__(file)
                    sys.path.remove(folder)
                    image = load_image(bpy.path.abspath(image_plane.slideshow.extratexture))
                    material = image_plane.material_slots[0].material
                    material_nodes = get_material_elements(material, image_plane.slideshow.name)
                    if material_nodes is not None:
                        data = {
                            'image_scene': image_scene,
                            'image_plane': image_plane,
                            'material': material,
                            'material_texture': material_nodes['texture'],
                            'material_shadeless': material_nodes['shadeless'],
                            'material_shaded': material_nodes['shaded'],
                            'material_mix': material_nodes['mix'],
                            'material_output': material_nodes['output'],
                            'target_empty': target_empty,
                            'camera': camera,
                            'extra_amount': image_plane.slideshow.extraamount,
                            'extra_text': image_plane.slideshow.extratext,
                            'extra_texture': image}
                        script.extra(data)
                    del script
                except ImportError:
                    pass
        update_scene(image_scene)

        #Add the image scene to the slideshow scene
        clip = slideshow_scene.sequence_editor.sequences.new_scene(scene=image_scene, name=image_scene.name, channel=((i % 2) + 1), frame_start=image_scene_start)

    else:
        clipx = image_plane.dimensions[0]
        clipy = image_plane.dimensions[1]
        aspect = aspect_ratio(slideshow_scene)
        clip_aspect = clipx / clipy
        clip_aspect_flipped = clipy / clipx
        aspect_difference = abs(aspect - clip_aspect)
        if aspect_difference > 0.1:
            blur_background = image_plane.slideshow.videobackground
        else:
            blur_background = False
        bpy.ops.sequencer.select_all(action='DESELECT')
        print('Importing Clip: '+image_scene_name)
        #Import video clip
        base_channel = ((i % 2) + 1)
        blur_base_channel = base_channel
        if blur_background:
            base_channel = base_channel + 4
        clip = slideshow_scene.sequence_editor.sequences.new_movie(filepath=image_plane.slideshow.videofile, name=image_plane.name, channel=base_channel, frame_start=image_scene_start)
        if blur_background:
            blur_clip = slideshow_scene.sequence_editor.sequences.new_movie(filepath=image_plane.slideshow.videofile, name=image_plane.name, channel=blur_base_channel, frame_start=image_scene_start)
        else:
            blur_clip = None
        image_scene_frames = image_plane.slideshow.videolength

        speed_clip = None
        audioclip = None
        blur_speed_clip = None
        blur_blur_clip = None
        if image_plane.slideshow.videoaudio:
            audioclip = slideshow_scene.sequence_editor.sequences.new_sound(filepath=image_plane.slideshow.videofile, name=image_plane.name, channel=base_channel + 4, frame_start=image_scene_start)
            if audioclip.frame_duration == 0:
                slideshow_scene.sequence_editor.sequences.remove(audioclip)
                print('No Audio Found For This Clip')
                audioclip = None

            else:
                bpy.context.window.scene = slideshow_scene
                #Add fadein/out to audio clip
                slideshow_scene.frame_current = image_scene_start
                audioclip.volume = 0
                audioclip.keyframe_insert(data_path='volume')
                slideshow_scene.frame_current = image_scene_start + slideshow_scene.snu_slideshow_generator.crossfade_length
                audioclip.volume = 1
                audioclip.keyframe_insert(data_path='volume')
                slideshow_scene.frame_current = audioclip.frame_final_end - slideshow_scene.snu_slideshow_generator.crossfade_length
                audioclip.keyframe_insert(data_path='volume')
                slideshow_scene.frame_current = audioclip.frame_final_end
                audioclip.volume = 0
                audioclip.keyframe_insert(data_path='volume')
                length_percent = image_scene_frames / clip.frame_final_duration
                if audioclip.frame_final_duration != clip.frame_final_duration:
                    speed_clip = slideshow_scene.sequence_editor.sequences.new_effect(name='Speed', type='SPEED', channel=clip.channel+1, seq1=clip, frame_start=clip.frame_final_start)
                    clip.frame_final_duration = audioclip.frame_final_duration
                    if blur_background:
                        blur_speed_clip = slideshow_scene.sequence_editor.sequences.new_effect(name='Speed', type='SPEED', channel=blur_clip.channel+1, seq1=blur_clip, frame_start=blur_clip.frame_final_start)
                        blur_clip.frame_final_duration = audioclip.frame_final_duration
                image_scene_frames = audioclip.frame_final_duration * length_percent

        if speed_clip:
            apply_transform = speed_clip
            if blur_background:
                blur_apply_transform = blur_speed_clip
            else:
                blur_apply_transform = None
        else:
            apply_transform = clip
            if blur_background:
                blur_apply_transform = blur_clip
            else:
                blur_apply_transform = None
        #Properly scale the clip
        apply_transform.select = True
        if blur_background:
            blur_apply_transform.select = True
        scale_clip = slideshow_scene.sequence_editor.sequences.new_effect(name='Transform', type='TRANSFORM', channel=apply_transform.channel+1, seq1=apply_transform, frame_start=apply_transform.frame_final_start)
        if blur_background:
            scale_clip.blend_type = 'ALPHA_OVER'
            clip.mute = True
            if speed_clip:
                speed_clip.mute = True
            blur_scale_clip = slideshow_scene.sequence_editor.sequences.new_effect(name='Transform', type='TRANSFORM', channel=blur_apply_transform.channel+1, seq1=blur_apply_transform, frame_start=blur_apply_transform.frame_final_start)
            blur_blur_clip = slideshow_scene.sequence_editor.sequences.new_effect(name='Blur', type='GAUSSIAN_BLUR', channel=blur_apply_transform.channel+2, seq1=blur_scale_clip, frame_start=blur_apply_transform.frame_final_start)
            blur_blur_clip.size_x = 40
            blur_blur_clip.size_y = 40
        else:
            blur_scale_clip = None
        rotate = image_plane.slideshow.rotate
        if rotate == '90':
            scale_clip.rotation_start = -90
            if blur_background:
                blur_scale_clip.rotation_start = -90
        elif rotate == '180':
            scale_clip.rotation_start = 180
            if blur_background:
                blur_scale_clip.rotation_start = 180
        elif rotate == '-90':
            scale_clip.rotation_start = 90
            if blur_background:
                blur_scale_clip.rotation_start = 90
        if rotate == '90' or rotate == '-90':
            multiplier = aspect
            if aspect < clip_aspect_flipped:
                #clip is wider than the scene
                scalex = clip_aspect_flipped / aspect
                scaley = 1
                blur_scalex = 1
                blur_scaley = aspect / clip_aspect_flipped
            else:
                #scene is wider than the clip
                scalex = aspect / clip_aspect_flipped
                scaley = 1
                blur_scalex = 1
                blur_scaley = clip_aspect_flipped / aspect
            scale_clip.scale_start_x = scaley / multiplier
            scale_clip.scale_start_y = scalex / multiplier
            if blur_background:
                blur_scale_clip.scale_start_x = blur_scaley * multiplier
                blur_scale_clip.scale_start_y = blur_scalex * multiplier

        else:
            if clip_aspect > aspect:
                #clip is wider than the scene
                scalex = 1
                scaley = aspect / clip_aspect
                blur_scalex = clip_aspect / aspect
                blur_scaley = 1
            else:
                #scene is wider than the clip
                scalex = clip_aspect / aspect
                scaley = 1
                blur_scalex = 1
                blur_scaley = aspect / clip_aspect
            scale_clip.scale_start_x = scalex
            scale_clip.scale_start_y = scaley
            if blur_background:
                blur_scale_clip.scale_start_x = blur_scalex
                blur_scale_clip.scale_start_y = blur_scaley

        #Create meta strip
        slideshow_scene.sequence_editor.active_strip = clip
        if blur_clip:
            blur_clip.select = True
        if blur_scale_clip:
            blur_scale_clip.select = True
        if blur_speed_clip:
            blur_speed_clip.select = True
        if blur_blur_clip:
            blur_blur_clip.select = True
        if speed_clip:
            speed_clip.select = True
        if scale_clip:
            scale_clip.select = True
        if audioclip:
            audioclip.select = True
        clip.select = True
        bpy.ops.sequencer.meta_make()
        clip = slideshow_scene.sequence_editor.active_strip

        #Trim video clip
        offset = image_plane.slideshow.videooffset
        clip.frame_offset_start = offset
        clip.frame_start = image_scene_start - offset
        #image_scene_frames = int(image_plane.slideshow.length * get_fps(slideshow_scene))
        clip.frame_final_end = clip.frame_final_start + image_scene_frames
        if blur_background:
            clip.channel = blur_base_channel
        else:
            clip.channel = base_channel

    bpy.context.window.scene = slideshow_scene

    #Add fade in
    if i == 0:
        clip.blend_type = 'ALPHA_OVER'
        slideshow_scene.frame_current = 1
        clip.blend_alpha = 0
        clip.keyframe_insert(data_path='blend_alpha')
        slideshow_scene.frame_current = generator_scene.snu_slideshow_generator.crossfade_length
        clip.blend_alpha = 1
        clip.keyframe_insert(data_path='blend_alpha')

    #Add transition
    if generator_scene.snu_slideshow_generator.crossfade_length > 0:
        if previous_image_clip and previous_image_plane:
            first_sequence = previous_image_clip
            second_sequence = clip
            if previous_image_plane.slideshow.transition == "GAMMA_CROSS":
                effect = slideshow_scene.sequence_editor.sequences.new_effect(name=previous_image_clip.name+' to '+clip.name, channel=3, frame_start=second_sequence.frame_final_start, frame_end=first_sequence.frame_final_end, type='GAMMA_CROSS', seq1=first_sequence, seq2=second_sequence)
                effect.frame_still_end = first_sequence.frame_final_end  #apparently needed since the frame_end doesnt get set in the previous function...
            elif previous_image_plane.slideshow.transition == "WIPE":
                effect = slideshow_scene.sequence_editor.sequences.new_effect(name=previous_image_clip.name+' to '+clip.name, channel=3, frame_start=second_sequence.frame_final_start, frame_end=first_sequence.frame_final_end, type='WIPE', seq1=first_sequence, seq2=second_sequence)
                effect.frame_still_end = first_sequence.frame_final_end  #apparently needed since the frame_end doesnt get set in the previous function...
                effect.transition_type = previous_image_plane.slideshow.wipe_type
                effect.direction = previous_image_plane.slideshow.wipe_direction
                if previous_image_plane.slideshow.wipe_soft:
                    effect.blur_width = 0.2
                if previous_image_plane.slideshow.wipe_angle == 'RIGHT':
                    effect.angle = 0 - (math.pi / 2)
                elif previous_image_plane.slideshow.wipe_angle == 'LEFT':
                    effect.angle = math.pi / 2
                elif previous_image_plane.slideshow.wipe_angle == 'UP':
                    effect.angle = 0
                    if effect.direction == 'IN':
                        effect.direction = 'OUT'
                    else:
                        effect.direction = 'IN'
                else:
                    effect.angle = 0
            elif previous_image_plane.slideshow.transition == "CUSTOM" and is_video_file(previous_image_plane.slideshow.custom_transition_file):
                effect_channel = first_sequence.channel
                if second_sequence.channel > effect_channel:
                    effect_channel = second_sequence.channel
                if second_sequence.channel > first_sequence.channel:
                    #second sequence is above first, transitions are normal
                    inverted = False
                    start_color = (0, 0, 0)
                    end_color = (1, 1, 1)
                    apply_mask_to = second_sequence
                else:
                    #first sequence is above second, transitions are inverted
                    inverted = True
                    start_color = (1, 1, 1)
                    end_color = (0, 0, 0)
                    apply_mask_to = first_sequence
                bpy.ops.sequencer.select_all(action='DESELECT')
                file_path = previous_image_plane.slideshow.custom_transition_file
                effect = slideshow_scene.sequence_editor.sequences.new_movie(filepath=file_path, name=previous_image_plane.name+' Transition', channel=effect_channel + 1, frame_start=second_sequence.frame_final_start + 1)
                effect.frame_final_end = first_sequence.frame_final_end - 1
                if inverted:
                    invert_modifier = effect.modifiers.new(name='Invert Colors', type='CURVES')
                    invert_modifier.curve_mapping.curves[3].points[0].location = (0, 1)
                    invert_modifier.curve_mapping.curves[3].points[1].location = (1, 0)
                effect_speed = slideshow_scene.sequence_editor.sequences.new_effect(name='Speed', type='SPEED', channel=effect.channel + 1, seq1=effect, frame_start=effect.frame_final_start)
                effect_final = slideshow_scene.sequence_editor.sequences.new_effect(name='Color', type='COLOR', channel=effect.channel, frame_start=effect.frame_final_end, frame_end=effect.frame_final_end + 1)
                effect_final.frame_final_end = effect_final.frame_final_start + 1
                effect_final.color = end_color
                effect_start = slideshow_scene.sequence_editor.sequences.new_effect(name='Color', type='COLOR', channel=effect.channel, frame_start=effect.frame_final_start - 1, frame_end=effect.frame_final_start)
                effect_start.frame_final_end = effect_start.frame_final_start + 1
                effect_start.color = start_color
                effect.select = True
                effect_speed.select = True
                effect_final.select = True
                effect_start.select = True
                bpy.ops.sequencer.meta_make()
                effect = slideshow_scene.sequence_editor.active_strip
                effect.name = previous_image_clip.name+' to '+clip.name
                effect.channel = effect_channel + 1
                effect.mute = True
                apply_mask_to.blend_type = 'ALPHA_OVER'
                modifier = apply_mask_to.modifiers.new(name='Transition from '+first_sequence.name, type='MASK')
                modifier.input_mask_type = 'STRIP'
                modifier.input_mask_strip = effect
            else:
                effect = slideshow_scene.sequence_editor.sequences.new_effect(name=previous_image_clip.name+' to '+clip.name, channel=3, frame_start=second_sequence.frame_final_start, frame_end=first_sequence.frame_final_end, type='CROSS', seq1=first_sequence, seq2=second_sequence)
                effect.frame_still_end = first_sequence.frame_final_end  #apparently needed since the frame_end doesnt get set in the previous function...

    #Add fade out
    if i == (len(images) - 1):
        clip.blend_type = 'ALPHA_OVER'
        slideshow_scene.frame_current = image_scene_start + image_scene_frames
        clip.blend_alpha = 0
        clip.keyframe_insert(data_path='blend_alpha')
        slideshow_scene.frame_current = image_scene_start + image_scene_frames - generator_scene.snu_slideshow_generator.crossfade_length
        clip.blend_alpha = 1
        clip.keyframe_insert(data_path='blend_alpha')
        slideshow_scene.frame_current = 1

    return clip


def extras_path():
    #This function will return the path to the Extras files
    for path in bpy.utils.script_paths():
        if os.path.exists(path+"\\addons\\slideshow\\Extras"):
            return path+"\\addons\\slideshow\\Extras\\*"
        if os.path.exists(path+"\\addons\\Extras"):
            return path+"\\addons\\Extras\\*"
    return os.path.split(bpy.data.filepath)[0]+"\\Extras\\*"


def list_extras():
    #This function will return a list of Extras found in the extras path location
    extras = []
    extraspath = extras_path()
    extrafiles = glob.glob(extraspath)
    for file in extrafiles:
        if os.path.splitext(file)[1] == '.py':
            extras.append(os.path.splitext(os.path.split(file)[1])[0])
    return extras


def get_extra(filename):
    #This function will return the full path to an extra from the filename
    extra = None
    extraspath = extras_path()
    extrafiles = glob.glob(extraspath)
    for file in extrafiles:
        if os.path.splitext(os.path.split(file)[1])[0] == filename:
            extra = file
    return extra


def get_transform(name):
    #This function will return a transform from the name
    for index, transform in enumerate(transforms):
        if transform['name'] == name:
            return index
    return -1


def update_slide_length(self, context):
    #Callback for SlideshowImage.length to update the length display text
    del context
    current_scene = bpy.data.scenes['Slideshow Generator']
    length_text = current_scene.objects[self.name+" Length"]
    length_text.data.body = "Length: "+str(round(self.length, 2))+" Seconds"


def update_video_length(self, context):
    #callback for SlideshowImage.videolength to update the length display text
    del context
    current_scene = bpy.data.scenes['Slideshow Generator']
    length_text = current_scene.objects[self.name+" Length"]
    if self.videolength > self.videomaxlength:
        self.videolength = self.videomaxlength
    length_text.data.body = "Length: "+str(self.videolength)+" Frames"


def update_offset(self, context):
    #Callback for SlideshowImage.videooffset to update the image texture's offset
    current_scene = bpy.data.scenes['Slideshow Generator']
    image_plane = current_scene.objects[self.name]
    material = image_plane.material_slots[0].material
    material_nodes = get_material_elements(material, image_plane.slideshow.name)
    if material_nodes is None:
        return
    maxlength = round(self.videomaxlength / get_fps(current_scene), 2) - 1
    if round(self.videooffset, 2) > maxlength:
        self.videooffset = maxlength
        offset = int(self.length * get_fps(current_scene))
    else:
        offset = int(self.videooffset * get_fps(current_scene))
    material_nodes['texture'].image_user.frame_offset = offset
    update_slide_length(self, context)


def update_extra(self, context):
    #Callback for SlideshowImage.extra to update the extra display text
    del context
    try:
        current_scene = bpy.data.scenes['Slideshow Generator']
        extra_text = current_scene.objects[self.name+" Extra"]
        extra_text.data.body = "Extra: "+self.extra
    except:
        pass


def update_transform(self, context):
    #Callback for SlideshowImage.transform to update the transform display text
    del context
    try:
        current_scene = bpy.data.scenes['Slideshow Generator']
        transform_text = current_scene.objects[self.name+" Transform"]
        transform_text.data.body = "Transform: "+self.transform
    except:
        pass


def update_index(self, context):
    #Callback for SlideshowImage.index to update the index display text, and the position of the image plane
    del context
    current_scene = bpy.data.scenes['Slideshow Generator']
    image_plane = current_scene.objects[self.name]
    position = -self.index
    image_plane.location = (0.0, position, 0.0)
    index_text = current_scene.objects[self.name+" Index"]
    index_text.data.body = str(self.index + 1)


def update_rotate(self, context):
    #Callback for SlideshowImage.rotate to update the rotation of the image plane
    del context
    current_scene = bpy.data.scenes['Slideshow Generator']
    image_plane = current_scene.objects[self.name]
    mesh = image_plane.data
    material = image_plane.material_slots[0].material
    material_nodes = get_material_elements(material, image_plane.slideshow.name)
    if material_nodes is None:
        return
    image = material_nodes['texture'].image
    iy = 0.5
    if self.rotate == '0':
        ix = ((image.size[0] / image.size[1])/2)
        mesh.vertices[0].co = (-ix, iy, 0)
        mesh.vertices[1].co = (ix, iy, 0)
        mesh.vertices[2].co = (ix, -iy, 0)
        mesh.vertices[3].co = (-ix, -iy, 0)
    elif self.rotate == '-90':
        ix = ((image.size[1] / image.size[0])/2)
        mesh.vertices[0].co = (-ix, -iy, 0)
        mesh.vertices[1].co = (-ix, iy, 0)
        mesh.vertices[2].co = (ix, iy, 0)
        mesh.vertices[3].co = (ix, -iy, 0)
    elif self.rotate == '180':
        ix = ((image.size[0] / image.size[1])/2)
        mesh.vertices[0].co = (ix, -iy, 0)
        mesh.vertices[1].co = (-ix, -iy, 0)
        mesh.vertices[2].co = (-ix, iy, 0)
        mesh.vertices[3].co = (ix, iy, 0)
    else:
        ix = ((image.size[1] / image.size[0])/2)
        mesh.vertices[0].co = (ix, iy, 0)
        mesh.vertices[1].co = (ix, -iy, 0)
        mesh.vertices[2].co = (-ix, -iy, 0)
        mesh.vertices[3].co = (-ix, iy, 0)


def list_slides(scene):
    #This function returns an unordered list of the slideshow images in the generator scene
    slides = []
    for slide_object in scene.objects:
        if slide_object.slideshow.name == slide_object.name:
            slides.append(slide_object)
    return slides


def slideshow_length(slides=None):
    scene = bpy.context.scene
    if not slides:
        slides = list_slides(scene)
    length = 0.0
    crossfade_length = (scene.snu_slideshow_generator.crossfade_length / get_fps(scene))
    default_length = scene.snu_slideshow_generator.slide_length
    for index, slide in enumerate(slides):
        if hasattr(slide, 'slideshow'):
            length = length + slide.slideshow.length
        else:
            length = length + default_length
        if index > 0:
            length = length - crossfade_length
    return length


def update_aspect(slide, scene, aspect):
    try:
        view_empty = scene.objects[slide.slideshow.view]
        scale_basis = view_empty.scale[1]
        view_empty.scale = aspect * scale_basis, scale_basis, .001
    except:
        pass


def update_order(mode='none', current_scene=None):
    #This function is called by the modal autoupdate and by various operators.  It arranges and positions the slides in the way they need to be.
    #   Setting 'mode' to 'none' will place the slides in the exact positions they should be, and update their index values
    #   Setting 'mode' to 'random' will rearrange the slides in a random order
    #   Setting 'mode' to 'alphabetical' will arrange the slides in alphabetical order
    #   Setting 'mode' to 'reverse' will arrange the slides in reverse alphabetical order

    if not current_scene:
        current_scene = bpy.context.scene
    slides = list_slides(current_scene)

    if mode == 'none':
        #Sort slides by their current location only
        changed = False
        oldorder = []
        aspect = aspect_ratio(current_scene)
        for slide in slides:
            update_aspect(slide, current_scene, aspect)
            loc = -slide.location[1]
            oldorder.append([loc, slide])
        neworder = sorted(oldorder, key=lambda x: x[0])
        for i, slide in enumerate(neworder):
            if slide[0] != i:
                slide[1].slideshow.index = i
                changed = True
        if changed:
            update_scene(current_scene)
    else:
        #Resort the slides in a specific way

        #Solt the slides by index to start with
        slides.sort(key=lambda x: x.slideshow.index)

        #Make a list of only the slides that are not locked
        unfrozen_indices, unfrozen_subset = zip(*[(i, e) for i, e in enumerate(slides) if not e.slideshow.lockposition])
        unfrozen_indices = list(unfrozen_indices)
        unfrozen_subset = list(unfrozen_subset)

        if mode == 'random':
            #Shuffle the index values of the unlocked slides
            random.shuffle(unfrozen_indices)
        elif mode == 'alphabetical':
            unfrozen_subset.sort(key=lambda x: x.slideshow.name)
        elif mode == 'reverse':
            unfrozen_subset.sort(key=lambda x: x.slideshow.name)
            unfrozen_subset.reverse()

        #Recombine the sorted indexes and slides
        for i, e in zip(unfrozen_indices, unfrozen_subset):
            slides[i] = e

        #Reenter the slide indexes
        for i, slide in enumerate(slides):
            slide.slideshow.index = i


def get_first_3d_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    return space
    return None


class SnuSlideshowExtraTexturePreset(bpy.types.PropertyGroup):
    #A property group for a texture preset for the extra scenes
    name: bpy.props.StringProperty(
        name="Texture Name",
        default="None")
    path: bpy.props.StringProperty(
        name="Texture Path",
        default="None")


class SnuSlideshowImage(bpy.types.PropertyGroup):
    #A property group that contains the information needed for a slideshow image.  This is appended to a slide image plane object.
    name: bpy.props.StringProperty(
        name="Image Name",
        default="None")
    transform: bpy.props.StringProperty(
        name="Transform Type Name",
        default="None",
        update=update_transform)
    length: bpy.props.FloatProperty(
        name="Slide Length (Seconds)", 
        default=4, 
        min=1,
        update=update_slide_length,
        description="Slide Length In Seconds")
    videooffset: bpy.props.IntProperty(
        name="Video Offset (Frames)",
        default=0,
        min=0,
        description="Video Offset In Frames",
        update=update_offset)
    videoaudio: bpy.props.BoolProperty(
        name="Enable Audio",
        default=True,
        description="Import Audio Track When Importing Video")
    videomaxlength: bpy.props.IntProperty(
        name="Video Maximum Length",
        default=0)
    videolength: bpy.props.IntProperty(
        name="Slide Length (Frames)",
        default=1,
        min=0,
        update=update_video_length,
        description="Video Slide Length In Frames")
    videofile: bpy.props.StringProperty(
        name="Video Filename",
        default="")
    extra: bpy.props.StringProperty(
        name="Extra Type", 
        default="None",
        update=update_extra)
    imageplane: bpy.props.StringProperty(
        name="Image Plane Name", 
        default="None")
    target: bpy.props.StringProperty(
        name="Target Empty Name", 
        default="None")
    view: bpy.props.StringProperty(
        name="View Window Empty Name", 
        default="None")
    extraamount: bpy.props.FloatProperty(
        name="Amount For The Extra Scene",
        default=0.5,
        max=1,
        min=0,
        description="Determines the power of the effect for the extra scene - 0.5 is average")
    extratext: bpy.props.StringProperty(
        name="Text For The Extra Scene",
        default="None",
        description="Used for extra scenes with a text object")
    extratexture: bpy.props.StringProperty(
        name="Texture For The Extra Scene",
        default="None",
        description="Used for extra scenes with a video background or overlay")
    index: bpy.props.IntProperty(
        name="Image Index",
        default=0,
        update=update_index)
    lockposition: bpy.props.BoolProperty(
        name="Lock Position",
        default=False)
    locktransform: bpy.props.BoolProperty(
        name="Lock Transform",
        default=False)
    lockextra: bpy.props.BoolProperty(
        name="Lock Extra",
        default=False)
    locklength: bpy.props.BoolProperty(
        name="Lock Length",
        default=False)
    locktransition: bpy.props.BoolProperty(
        name="Lock Transition",
        default=False)
    rotate: bpy.props.EnumProperty(
        name="Rotation",
        items=[('0', '0', '0'), ('90', '90', '90'), ('180', '180', '180'), ('-90', '-90', '-90')],
        update=update_rotate)
    videobackground: bpy.props.BoolProperty(
        name="Blurred Background",
        default=True,
        description="When the video is smaller than the render resolution, add a blurred scaled background instead of black")
    transition: bpy.props.EnumProperty(
        name="Transition Type",
        default="CROSS",
        items=[("CROSS", "Crossfade", "", 1), ("GAMMA_CROSS", "Gamma Cross", "", 2), ("WIPE", "Wipe", "", 3), ("CUSTOM", "Custom", "", 4)])
    wipe_type: bpy.props.EnumProperty(
        name="Wipe Type",
        default="SINGLE",
        items=[("SINGLE", "Single", "", 1), ("DOUBLE", "Double", "", 2), ("IRIS", "Iris", "", 3), ("CLOCK", "Clock", "", 4)])
    wipe_direction: bpy.props.EnumProperty(
        name="Wipe Direction",
        default="OUT",
        items=[("OUT", "Out", "", 1), ("IN", "In", "", 2)])
    wipe_soft: bpy.props.BoolProperty(
        name="Soft Wipe",
        default=True)
    wipe_angle: bpy.props.EnumProperty(
        name="Wipe Angle",
        default="DOWN",
        items=[("DOWN", "Down", "", 1), ("RIGHT", "Right", "", 2), ("UP", "Up", "", 3), ("LEFT", "Left", "", 4)])
    custom_transition_file: bpy.props.StringProperty(
        name="Transition File",
        default="",
        description="Location of custom transition file.",
        subtype='FILE_PATH')


class SSG_PT_VSEPanel(bpy.types.Panel):
    #This is the panel that is visible in the VSE of the 'Slideshow' scene.
    bl_label = "Snu Slideshow Generator"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Strip"

    @classmethod
    def poll(cls, context):
        #Check if in slideshow scene
        if context.scene.name == 'Slideshow':
            try:
                if len(context.scene.sequence_editor.sequences_all) > 0:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def draw(self, context):
        del context
        layout = self.layout
        layout.operator('slideshow.preview_mode', text="Apply 50% Render Size").mode = 'halfsize'
        layout.operator('slideshow.preview_mode', text="Apply 100% Render Size").mode = 'fullsize'
        layout.operator('slideshow.gotogenerator', text="Return To The Generator Scene")


class SnuSlideshowGotoGenerator(bpy.types.Operator):
    #This operator will attempt to go back to the slideshow scene and default screen mode so the slides can be edited and re-generated
    bl_idname = 'slideshow.gotogenerator'
    bl_label = "Return To The Generator Scene"

    def execute(self, context):
        if "Slideshow Generator" in bpy.data.scenes:
            generator_scene = bpy.data.scenes['Slideshow Generator']
            context.window.scene = generator_scene
            workspace_name = generator_scene.snu_slideshow_generator.generator_workspace
            if workspace_name in bpy.data.workspaces:
                workspace = bpy.data.workspaces[workspace_name]
                context.window.workspace = workspace
        return{'FINISHED'}


class SnuSlideshowPreviewMode(bpy.types.Operator):
    #This operator will enable or disable 'preview' mode on all scene strips in the sequencer.
    #'mode' can be set to:
    #   halfsize - Set the rendering to 50% size
    #   fullsize - Set the rendering to 100% size
    bl_idname = 'slideshow.preview_mode'
    bl_label = 'Enable or Disable Preview On All Scenes'

    mode: bpy.props.StringProperty()

    def execute(self, context):
        sequences = context.scene.sequence_editor.sequences_all
        for sequence in sequences:
            if sequence.type == 'SCENE':
                scene = sequence.scene
                if self.mode == 'halfsize':
                    scene.render.resolution_percentage = 50
                elif self.mode == 'fullsize':
                    scene.render.resolution_percentage = 100
        return{'FINISHED'}


class SSG_PT_Panel(bpy.types.Panel):
    #This is the main configuration panel for the slideshow generator and generator creator
    bl_label = "Snu Slideshow Generator"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        current_scene = context.scene
        if is_generator_scene(current_scene):
            #Panel is in slideshow generator mode
            slides = list_slides(current_scene)
            row = layout.row()
            if len(slides):
                layout.operator_context = 'INVOKE_SCREEN'  #needed to solve issues with context.scene not updating
                row.operator('slideshow.create')

                row = layout.row()
                #Calculate and display slideshow length
                slideshow_seconds = slideshow_length(slides=slides)
                slideshow_length_formatted = format_seconds(slideshow_seconds)
                row.label(text=str(len(slides)) + " Slides, Total Length: "+slideshow_length_formatted)
            else:
                row.label(text="No Slides Found")

            row = layout.row()
            row.prop(context.scene.snu_slideshow_generator, "crossfade_length")
            row = layout.row()
            box = row.box()
            row = box.row()
            row.prop(context.scene.snu_slideshow_generator, "audio_enabled", text="Enable Audio Track")
            row = box.row()
            split = row.split(factor=.9, align=True)
            split.prop(context.scene.snu_slideshow_generator, "audio_track", text="Audio Track")
            split.operator('slideshow.open_audio', text="", icon='FILEBROWSER')
            if not context.scene.snu_slideshow_generator.audio_enabled:
                row.enabled = False
            row = box.row()
            row.prop(context.scene.snu_slideshow_generator, "audio_loop_fade")
            row.prop(context.scene.snu_slideshow_generator, "audio_fade_length")
            if not context.scene.snu_slideshow_generator.audio_enabled:
                row.enabled = False
            row = layout.row()
            row.separator()

            if len(slides):
                #Sorting options
                row = layout.row(align=True)
                row.label(text='Sort:')
                row.operator('slideshow.update_order', text='Randomize').mode = 'random'
                row.operator('slideshow.update_order', text='Alphabetical').mode = 'alphabetical'
                row.operator('slideshow.update_order', text='Reverse Alpha').mode = 'reverse'
                row = layout.row(align=True)
                row.label(text='Randomize:')
                row.operator('slideshow.apply_transform', text='Transforms').transform = 'Random'
                row.operator('slideshow.apply_extra', text='Extras').extra = 'Random'

            row = layout.row(align=True)
            row.operator('slideshow.add_slide')

            if context.selected_objects:
                row.operator('slideshow.delete_slide')
                row = layout.row()
                row.separator()
                selected = context.active_object
                if selected.slideshow.name != "None":
                    #If a slide image is selected, display configuration options
                    current_slide = selected.slideshow
                    box = layout.box()
                    row = box.row()
                    row.label(text="Image: "+current_slide.name)
                    row = box.row()
                    row.prop(current_slide, 'rotate')
                    row = box.row()
                    split = row.split(factor=.5)
                    subsplit = split.split(align=True)
                    subsplit.label(text=""+str(current_slide.index + 1))
                    subsplit.operator("slideshow.move_slide", text="", icon="REW").move = "beginning"
                    subsplit.operator("slideshow.move_slide", text="", icon="PLAY_REVERSE").move = "backward"
                    subsplit.operator("slideshow.move_slide", text="", icon="PLAY").move = "forward"
                    subsplit.operator("slideshow.move_slide", text="", icon="FF").move = "end"
                    split = split.split()
                    split.prop(current_slide, "lockposition")
                    innerbox = box.box()
                    row = innerbox.row()
                    if current_slide.videofile:
                        row.prop(current_slide, "videolength")
                    else:
                        row.prop(current_slide, "length")
                        row = innerbox.row()
                        row.operator('slideshow.apply_slide_length', text="Apply To Selected").mode = 'Selected'
                        row.operator('slideshow.apply_slide_length').mode = 'None'
                        row.prop(current_slide, "locklength")

                    if not current_slide.videofile:
                        innerbox = box.box()
                        row = innerbox.row()
                        row.label(text="Transform: "+current_slide.transform)
                        row = innerbox.row()
                        row.menu('SSG_MT_transforms_menu', text="Change Transform")
                        row = innerbox.row()
                        row.operator('slideshow.apply_transform', text="Apply To Selected").transform = 'Selected'
                        row.operator('slideshow.apply_transform').transform = 'None'
                        row.prop(current_slide, "locktransform")
                        innerbox = box.box()
                        row = innerbox.row()
                        row.label(text="Extra: "+current_slide.extra)
                        row = innerbox.row()
                        row.menu('SSG_MT_extra_menu', text="Change Extra")
                        row = innerbox.row()
                        row.operator('slideshow.apply_extra', text="Apply To Selected").extra = 'Selected'
                        row.operator('slideshow.apply_extra').extra = 'None'
                        row.prop(current_slide, "lockextra")
                        row = innerbox.row()
                        row.separator()
                        row = innerbox.row()
                        row.prop(current_slide, "extratext", text='Extra Text')
                        row = innerbox.split(factor=0.8)
                        split = row.split(factor=.9, align=True)
                        split.prop(current_slide, "extratexture", text='Extra Texture')
                        split.operator('slideshow.open_extra_texture', text="", icon='FILEBROWSER').target = 'slide'
                        split = row.split(factor=1, align=True)
                        split.operator('slideshow.add_extra_texture').texture = current_slide.extratexture
                        row = innerbox.row()
                        row.menu('SSG_MT_extra_texture_menu', text="Apply Extra Texture Preset")
                        row = innerbox.row()
                        row.prop(current_slide, "extraamount", text='Extra Amount')

                    else:
                        innerbox = box.box()
                        row = innerbox.row()
                        row.prop(current_slide, "videooffset", text='Video Offset')
                        row = innerbox.row()
                        row.prop(current_slide, "videoaudio", text='Import Audio From Video File')
                        row = innerbox.row()
                        row.prop(current_slide, "videobackground", text='Add Blurred Background If Needed')
                    innerbox = box.box()
                    row = innerbox.row()
                    row.label(text="Transition To Next Slide:")
                    row = innerbox.row()
                    row.prop(current_slide, "transition", text="")
                    row = innerbox.row()
                    row.operator('slideshow.apply_transition', text="Apply To Selected").transition = 'Selected'
                    row.operator('slideshow.apply_transition').transition = 'None'
                    row.prop(current_slide, "locktransition")
                    transition = current_slide.transition
                    if transition == "WIPE":
                        row = innerbox.row()
                        row.prop(current_slide, "wipe_type", text='Type')
                        row.prop(current_slide, 'wipe_soft', toggle=True)
                        row = innerbox.row()
                        row.prop(current_slide, "wipe_direction", expand=True)
                        row = innerbox.row()
                        row.prop(current_slide, 'wipe_angle', expand=True)
                    if transition == "CUSTOM":
                        row = innerbox.row()
                        row.prop(current_slide, 'custom_transition_file', text='Transition Video')
                    row = layout.row()
                    row.separator()
                    row = layout.box()
                    row.label(text="Drag an image up or down to rearrange it in the timeline.")

                elif 'View' in selected.name:
                    #The view area rectangle is probably selected
                    row = layout.box()
                    row.label(text="The rectangle is the area the camera will see.")
                    row.label(text="It can be scaled down to crop the image,")
                    row.label(text="or rotated to rotate the camera,")
                    row.label(text="or moved to focus on a specific area.")

                elif 'Target' in selected.name:
                    #The zoom to target is probably selected
                    row = layout.box()
                    row.label(text="The cross is the target for transforms like zoom in.")
                    row.label(text="It can be moved around the image.")

                else:
                    #Something else is selected
                    row = layout.box()
                    row.label(text="Select An Image To Customize It")

            else:
                #Nothing is selected
                row = layout.row()
                row.separator()
                row = layout.box()
                row.label(text="Select An Image To Customize It")

        else:
            #Panel is in create generator mode
            row = layout.row()
            row.prop(context.scene.snu_slideshow_generator, "image_directory")
            row = layout.row()
            row.prop(context.scene.snu_slideshow_generator, "slide_length")
            row = layout.row()
            row.operator('slideshow.generator')
            #get list of images in image_directory, gray out generator button if none found
            image_types = list(bpy.path.extensions_image)
            image_list = []
            for image_type in image_types:
                image_list.extend(glob.glob(bpy.path.abspath(context.scene.snu_slideshow_generator.image_directory)+'*'+image_type))
            video_types = list(bpy.path.extensions_movie)
            for video_type in video_types:
                image_list.extend(glob.glob(bpy.path.abspath(context.scene.snu_slideshow_generator.image_directory)+'*'+video_type))
            if not image_list:
                #row.enabled = False
                row = layout.row()
                row.label(text="Image Directory Invalid Or Empty")
            else:
                #row.enabled = True
                row = layout.row()
                slideshow_seconds = slideshow_length(slides=image_list)
                slideshow_length_formatted = format_seconds(slideshow_seconds)
                row.label(text=str(len(image_list)) + " Images In Directory")
                row = layout.row()
                row.label(text="Estimated Length: "+slideshow_length_formatted)

            row = layout.row()
            row.separator()
            box = layout.box()
            row = box.row()
            row.menu('SSG_MT_transforms_menu', text="Toggle Transforms")
            row = box.row()
            row.menu('SSG_MT_extra_menu', text="Toggle Extras")
            row = layout.row()
            row.separator()
            box = layout.box()
            row = box.split(factor=0.8)
            split = row.split(factor=.9, align=True)
            split.prop(context.scene.snu_slideshow_generator, "extra_texture", text='Extra Texture')
            split.operator('slideshow.open_extra_texture', text="", icon='FILEBROWSER').target = 'scene'
            split = row.split(factor=1, align=True)
            split.operator('slideshow.add_extra_texture').texture = context.scene.snu_slideshow_generator.extra_texture
            row = box.row()
            row.menu('SSG_MT_extra_texture_menu', text="Extra Texture Presets")


class SnuSlideshowMoveSlide(bpy.types.Operator):
    #Operator for moving the current active slideshow slide up or down in the generator scene.
    #'move' can be:
    #   'forward' for moving it one space forward
    #   'backward' for moving it one space back
    #   'beginning' for moving it to the start of the slideshow
    #   'end' for moving it to the end of the slideshow
    bl_idname = 'slideshow.move_slide'
    bl_label = "Move The Active Slide"

    move: bpy.props.StringProperty()

    def execute(self, context):
        selected = context.active_object
        slide = selected.slideshow
        slides = list_slides(context.scene)
        if self.move == "forward":
            selected.location[1] = selected.location[1] - 1.1
            update_order()
        elif self.move == "backward":
            selected.location[1] = selected.location[1] + 1.1
            update_order()
        elif self.move == "beginning":
            slide.index = -1
        elif self.move == "end":
            slide.index = len(slides) + 1
        return {'FINISHED'}


class SnuSlideshowOpenExtraTexture(bpy.types.Operator):
    #This operator will open a filebrowser to select the scene.snu_slideshow_generator.extra_texture variable
    bl_idname = 'slideshow.open_extra_texture'
    bl_label = 'Browse For An Image Or Video File'

    #The browsed to file is stored in this variable
    filepath: bpy.props.StringProperty()

    target: bpy.props.StringProperty()

    def invoke(self, context, event):
        del event
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        context.space_data.params.use_filter = True
        context.space_data.params.use_filter_image = True
        context.space_data.params.use_filter_movie = True
        context.space_data.params.use_filter_folder = True

    def execute(self, context):
        #This function is called when the file browser dialog is closed with an ok
        if self.target == 'slide':
            current_slide = context.active_object
            current_slide.slideshow.extratexture = self.filepath
        else:
            context.scene.snu_slideshow_generator.extra_texture = self.filepath

        return{'FINISHED'}


class SnuSlideshowOpenAudio(bpy.types.Operator):
    #This operator will open a filebrowser to select the scene.snu_slideshow_generator.audio_track variable
    bl_idname = 'slideshow.open_audio'
    bl_label = 'Browse For An Audio File'

    #The browsed to file is stored in this variable
    filepath: bpy.props.StringProperty()

    def invoke(self, context, event):
        del event
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        context.space_data.params.use_filter = True
        context.space_data.params.use_filter_sound = True
        context.space_data.params.use_filter_folder = True

    def execute(self, context):
        #This function is called when the file browser dialog is closed with an ok
        del context
        generator_scene = bpy.data.scenes['Slideshow Generator']
        generator_scene.snu_slideshow_generator.audio_track = self.filepath
        return{'FINISHED'}


class SnuSlideshowAddSlide(bpy.types.Operator):
    #This operator will add a new slide to the slideshow generator scene.
    bl_idname = 'slideshow.add_slide'
    bl_label = 'Add New Slide(s)'

    #The files selected by the browser are stored in this
    files: bpy.props.CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement)

    #The browsed to directory is stored in this variable
    directory: bpy.props.StringProperty(
        subtype="DIR_PATH")

    def invoke(self, context, event):
        del event
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        context.space_data.params.use_filter = True
        context.space_data.params.use_filter_image = True
        context.space_data.params.use_filter_movie = True
        context.space_data.params.use_filter_folder = True

    def execute(self, context):
        #This function is called when the file browser dialog is closed with an ok
        del context
        generator_scene = bpy.data.scenes['Slideshow Generator']
        import os

        #iterate through the selected files and attempt to load them into the generator scene
        last_image = None
        for fileelement in self.files:
            filename = os.path.join(self.directory, fileelement.name)
            if os.path.isfile(filename):
                #The file is a real file
                extension = os.path.splitext(filename)[1].lower()
                if extension in bpy.path.extensions_image:
                    #The file is a known image file type, load it
                    image = load_image(filename)
                    image_number = len(list_slides(generator_scene))
                    last_image = import_slideshow_image(image, image_number, generator_scene.snu_slideshow_generator.slide_length, generator_scene, video=False, last_image=last_image)
                elif extension in bpy.path.extensions_movie:
                    #The file is a known video file type, load it
                    image = load_image(filename)
                    image_number = len(list_slides(generator_scene))
                    last_image = import_slideshow_image(image, image_number, generator_scene.snu_slideshow_generator.slide_length, generator_scene, video=True, last_image=last_image)
                else:
                    #oops, this file is not an image or video
                    self.report({'WARNING'}, os.path.split(filename)[1]+' Is Not An Image')
        select_plane(last_image, generator_scene)
        return{'FINISHED'}


class SnuSlideshowExtraMenu(bpy.types.Menu):
    #This is the popup menu for selecting or toggling extras
    bl_idname = 'SSG_MT_extra_menu'
    bl_label = 'List of available extras'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        split = layout.split()
        column = split.column()

        #Display the 'None' extra
        is_generator = is_generator_scene(scene)
        if is_generator:
            #This is the slideshow generator scene, the extra can be selected
            column.operator("slideshow.change_extra", text="None").extra = "None"
        else:
            #This is not the slideshow generator scene, the extra can only be toggled
            column.operator("slideshow.hide_extra", text="None").extra = "None"
        extras = list_extras()

        #Iterate through the extras to display the extra name column
        for extra in extras:
            if extra != 'None':
                if is_generator:
                    #This is the slideshow generator scene, the extra can be selected
                    column.operator("slideshow.change_extra", text=extra).extra = extra
                else:
                    #This is not the slideshow generator scene, the extra can only be toggled
                    column.operator("slideshow.hide_extra", text=extra).extra = extra
        column = split.column()

        #Display the toggled extra checkboxes
        hidden = scene.snu_slideshow_generator.hidden_extras.split(";")

        #Display the 'None' extra checkbox
        if "None" in hidden:
            column.operator("slideshow.hide_extra", text="", icon="CHECKBOX_DEHLT").extra = "None"
        else:
            column.operator("slideshow.hide_extra", text="", icon="CHECKBOX_HLT").extra = "None"

        #Iterate through the extras and display the toggle extra checkboxes
        for extra in extras:
            if extra != 'None':
                if extra in hidden:
                    #This extra is currently disabled
                    column.operator("slideshow.hide_extra", text="", icon="CHECKBOX_DEHLT").extra = extra
                else:
                    #This extra is currently enabled
                    column.operator("slideshow.hide_extra", text="", icon="CHECKBOX_HLT").extra = extra

        #This will toggle all extras on and off
        column.operator("slideshow.hide_all_extras", text="Toggle All")


class SnuSlideshowHideAllExtras(bpy.types.Operator):
    #This operator will enable all extras if none are enabled, otherwise it will disable all
    bl_idname = 'slideshow.hide_all_extras'
    bl_label = 'Toggle Hide All Extras From Randomize Operations'
    bl_description = 'Toggle Hide All Extras From Randomize Operations'

    def execute(self, context):
        scene = context.scene
        if len(scene.snu_slideshow_generator.hidden_extras) == 0:
            hidden = list_extras()
            scene.snu_slideshow_generator.hidden_extras = ';'.join(hidden)
        else:
            scene.snu_slideshow_generator.hidden_extras = ""
        return{'FINISHED'}


class SnuSlideshowHideExtra(bpy.types.Operator):
    #This operator will toggle an extra in the hidden list
    bl_idname = 'slideshow.hide_extra'
    bl_label = 'Hide Extra From Randomize Operations'
    bl_description = 'Hide Extra From Randomize Operations'

    extra: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        hidden = scene.snu_slideshow_generator.hidden_extras.split(';')
        if self.extra in hidden:
            hidden.remove(self.extra)
        else:
            hidden.append(self.extra)
        scene.snu_slideshow_generator.hidden_extras = ';'.join(hidden)
        return{'FINISHED'}


class SnuSlideshowChangeExtra(bpy.types.Operator):
    #This operator will change the listed extra in the currently selected object
    bl_idname = 'slideshow.change_extra'
    bl_label = 'Change Extra'

    extra: bpy.props.StringProperty()

    def execute(self, context):
        current_image = context.active_object
        current_image.slideshow.extra = self.extra
        return{'FINISHED'}


class SnuSlideshowTransformsMenu(bpy.types.Menu):
    #This is a menu of the transforms and allows for them to be disabled
    bl_idname = 'SSG_MT_transforms_menu'
    bl_label = 'List of available transforms'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        split = layout.split()
        column = split.column()

        #Iterate through transforms and display the transforms name column
        is_generator = is_generator_scene(scene)
        for index, transform in enumerate(transforms):
            if is_generator:
                #This is the slideshow generator scene, the transforms can be selected
                column.operator("slideshow.change_transform", text=transform['name']).transform = transform['name']
            else:
                #This is not the slideshow generator scene, the transforms can only be toggled
                column.operator("slideshow.hide_transform", text=transform['name']).transform = transform['name']

        column = split.column()
        hidden = scene.snu_slideshow_generator.hidden_transforms.split(';')

        #iterate through transforms and display enable/disable column
        for index, transform in enumerate(transforms):
            if transform['name'] in hidden:
                #This transform is not enabled
                column.operator("slideshow.hide_transform", text="", icon="CHECKBOX_DEHLT").transform = transform['name']
            else:
                #This transform is enabled
                column.operator("slideshow.hide_transform", text="", icon="CHECKBOX_HLT").transform = transform['name']
        column.operator("slideshow.hide_all_transforms", text="Toggle All")


class SnuSlideshowHideAllTransforms(bpy.types.Operator):
    #This operator will enable all transforms if none are enabled, otherwise it will disable all
    bl_idname = 'slideshow.hide_all_transforms'
    bl_label = 'Toggle Hide All Transforms From Randomize Operations'
    bl_description = 'Toggle Hide All Transforms From Randomize Operations'

    def execute(self, context):
        scene = context.scene
        if len(scene.snu_slideshow_generator.hidden_transforms) == 0:
            hidden = []
            for transform in transforms:
                hidden.append(transform['name'])
            scene.snu_slideshow_generator.hidden_transforms = ';'.join(hidden)
        else:
            scene.snu_slideshow_generator.hidden_transforms = ""
        return{'FINISHED'}


class SnuSlideshowHideTransform(bpy.types.Operator):
    #This operator will toggle a transform in the hidden list
    bl_idname = 'slideshow.hide_transform'
    bl_label = 'Hide Transform From Randomize Operations'
    bl_description = 'Hide Transform From Randomize Operations'

    transform: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        hidden = scene.snu_slideshow_generator.hidden_transforms.split(';')
        if self.transform in hidden:
            hidden.remove(self.transform)
        else:
            hidden.append(self.transform)
        scene.snu_slideshow_generator.hidden_transforms = ';'.join(hidden)
        return{'FINISHED'}


class SnuSlideshowChangeTransform(bpy.types.Operator):
    #This operator will change the listed transform in the currently selected object
    bl_idname = 'slideshow.change_transform'
    bl_label = 'Change Transform'

    transform: bpy.props.StringProperty()

    def execute(self, context):
        current_image = context.active_object
        current_image.slideshow.transform = self.transform
        return{'FINISHED'}


class SnuSlideshowApplyExtra(bpy.types.Operator):
    #This operator will apply an extra, or randomize extras on all slides that do not have locked extras
    bl_idname = 'slideshow.apply_extra'
    bl_label = 'Apply To All'
    bl_description = 'Applies an extra to all slides'

    extra: bpy.props.StringProperty()

    def execute(self, context):
        update_order()
        current_scene = context.scene
        slides = list_slides(current_scene)
        slides.sort(key=lambda x: x.slideshow.index)
        extras = list_extras()
        hidden = context.scene.snu_slideshow_generator.hidden_extras.split(";")
        randomized = []
        current_slide = context.active_object

        if self.extra == 'Selected':
            objects = current_scene.objects
            for scene_object in objects:
                if scene_object.select_get():
                    if scene_object.slideshow.name != "None":
                        if not scene_object.slideshow.lockextra:
                            scene_object.slideshow.extra = current_slide.slideshow.extra
                            scene_object.slideshow.extraamount = current_slide.slideshow.extraamount
                            scene_object.slideshow.extratexture = current_slide.slideshow.extratexture
                            scene_object.slideshow.extratext = current_slide.slideshow.extratext

        else:
            #Get list of extras that are not disabled for randomization purposes
            for extra in extras:
                if extra not in hidden and extra != "None":
                    randomized.append(extra)
            if "None" not in hidden:
                randomized.append("None")
            lastextra = ""
            lastextratexture = ""

            extratextures = []
            for extra_texture_preset in current_scene.snu_slideshow_generator.extra_texture_presets:
                extratextures.append(extra_texture_preset.path)

            #Iterate through all slides
            for slide in slides:
                if not slide.slideshow.lockextra:
                    #Only check slides that are not locked
                    if self.extra == 'Random':
                        #Apply a random extra
                        if len(randomized) > 0:
                            #Make sure at least one extra is enabled

                            #Randomize extra texture
                            lessrandomized = [x for x in extratextures if x != lastextratexture]
                            if len(lessrandomized) > 0:
                                newextratexture = lessrandomized[random.randint(0, (len(lessrandomized)-1))]
                                slide.slideshow.extratexture = newextratexture

                            #Randomize extra
                            if len(randomized) > 1:
                                #More than one extra is enabled, so dont use the same extra twice in a row
                                lessrandomized = [x for x in randomized if x != lastextra]
                                newextra = lessrandomized[random.randint(0, (len(lessrandomized)-1))]
                                slide.slideshow.extra = newextra
                                slide.slideshow.extraamount = 0.5
                                lastextra = newextra

                            else:
                                #Only one extra is enabled, use it
                                slide.slideshow.extra = randomized[0]
                                slide.slideshow.extraamount = 0.5

                    else:
                        #Apply the extra from current_slide to the slide
                        slide.slideshow.extra = current_slide.slideshow.extra
                        slide.slideshow.extraamount = current_slide.slideshow.extraamount
                        slide.slideshow.extratexture = current_slide.slideshow.extratexture
                        slide.slideshow.extratext = current_slide.slideshow.extratext

        return{'FINISHED'}


class SnuSlideshowApplyTransform(bpy.types.Operator):
    #This operator will apply a transform, or randomize transforms on all slides that do not have locked transforms
    bl_idname = 'slideshow.apply_transform'
    bl_label = 'Apply To All'
    bl_description = 'Applies a transform to all slides'

    transform: bpy.props.StringProperty()

    def execute(self, context):
        update_order()
        current_scene = context.scene
        current_slide = context.active_object
        slides = list_slides(current_scene)
        slides.sort(key=lambda x: x.slideshow.index)
        hidden = context.scene.snu_slideshow_generator.hidden_transforms.split(";")
        randomized = []

        if self.transform == 'Selected':
            objects = current_scene.objects
            for scene_object in objects:
                if scene_object.select_get():
                    if scene_object.slideshow.name != "None":
                        if not scene_object.slideshow.locktransform:
                            scene_object.slideshow.transform = current_slide.slideshow.transform

        else:
            #Iterate through transforms to get a list of non-disabled ones
            for transform in transforms:
                if transform['name'] not in hidden:
                    randomized.append(transform)
            lasttransform = {"name": ""}

            #Iterate through all slides
            for slide in slides:
                if not slide.slideshow.locktransform:
                    #Only modify slides without a locked transform
                    if self.transform == 'Random':
                        #Apply a randomized transform to all slides
                        if len(randomized) > 0:
                            #Only can be applied if at least one transform is enabled
                            if len(randomized) > 1:
                                #More than one transform is enabled, apply a random one while making sure it is not the same as the last applied transform
                                lessrandomized = [x for x in randomized if x['name'] != lasttransform['name']]
                                newtransform = lessrandomized[random.randint(0, (len(lessrandomized)-1))]
                                slide.slideshow.transform = newtransform['name']
                                lasttransform = newtransform
                            else:
                                #Only one transform is enabled, just apply it
                                slide.slideshow.transform = randomized[0]['name']
                    else:
                        #Apply the named transform to the slide
                        slide.slideshow.transform = current_slide.slideshow.transform

        return{'FINISHED'}


class SnuSlideshowApplyTransition(bpy.types.Operator):
    #This operator will apply a transition to all slides that do not have locked transitions
    bl_idname = 'slideshow.apply_transition'
    bl_label = 'Apply To All'
    bl_description = 'Applies a transition to all slides'

    transition: bpy.props.StringProperty()

    def apply_transition(self, selected, target):
        #copies transition details from selected to target
        target.transition = selected.transition
        target.wipe_type = selected.wipe_type
        target.wipe_direction = selected.wipe_direction
        target.wipe_soft = selected.wipe_soft
        target.wipe_angle = selected.wipe_angle
        target.custom_transition_file = selected.custom_transition_file

    def execute(self, context):
        update_order()
        current_scene = context.scene
        current_slide = context.active_object
        slides = list_slides(current_scene)
        slides.sort(key=lambda x: x.slideshow.index)

        for slide in slides:
            if not slide.slideshow.locktransition:
                if (self.transition == 'Selected' and slide.select_get()) or self.transition != 'Selected':
                    self.apply_transition(current_slide.slideshow, slide.slideshow)

        return{'FINISHED'}


class SnuSlideshowApplySlideLength(bpy.types.Operator):
    #This operator will apply a slide length to all slides that do not have a locked length
    bl_idname = 'slideshow.apply_slide_length'
    bl_label = 'Apply To All'
    bl_description = 'Applies current slide length to all slides'

    mode: bpy.props.StringProperty()

    def execute(self, context):
        current_scene = context.scene
        current_slide = context.active_object
        if self.mode == 'Selected':
            objects = current_scene.objects
            for scene_object in objects:
                if scene_object.select_get():
                    if scene_object.slideshow.name != "None":
                        if not scene_object.slideshow.locklength:
                            scene_object.slideshow.length = current_slide.slideshow.length

        else:
            slides = list_slides(current_scene)

            for slide in slides:
                if not slide.slideshow.locklength:
                    slide.slideshow.length = current_slide.slideshow.length
        return{'FINISHED'}


class SnuSlideshowUpdateOrder(bpy.types.Operator):
    #This operator just runs the 'update_order' function
    bl_idname = 'slideshow.update_order'
    bl_label = 'Update Slide Order'

    mode: bpy.props.StringProperty()

    def execute(self, context):
        del context
        update_order(self.mode)
        return{'FINISHED'}


class SnuSlideshowDeleteSlide(bpy.types.Operator):
    #This operator will remove all selected slides from the generator scene
    bl_idname = 'slideshow.delete_slide'
    bl_label = 'Delete Selected Slide(s)'
    bl_description = 'Deletes selected slides and rearranges the list'

    def execute(self, context):
        selected_objects = context.selected_objects

        #Iterate through selected objects
        for selected in selected_objects:
            if len(selected_objects) == 1 and selected.slideshow.name == "None" and selected.parent:
                #Only one object is selected, and the selected object is one of the sub objects of a slide - the user probably wants to delete that slide, so change the selection to that
                selected = selected.parent

            if selected.slideshow.name != "None":
                #The selected object is a slide, delete it and all its sub-objects
                bpy.ops.object.select_all(action='DESELECT')
                group = selected.users_collection[0]
                for group_object in group.objects:
                    group_object.select_set(True)
                bpy.ops.object.delete()
                update_order()
        return{'FINISHED'}


class SnuSlideshowAddExtraTexture(bpy.types.Operator):
    #This operator will add a texture preset to the extra textures
    bl_idname = 'slideshow.add_extra_texture'
    bl_label = '+'
    bl_description = 'Adds a texture preset to the extra textures'

    texture: bpy.props.StringProperty()

    def execute(self, context):
        texturename = os.path.split(self.texture)[1]
        if texturename != 'None':
            if context.scene.snu_slideshow_generator.extra_texture_presets.find(texturename) == -1:
                newtexture = context.scene.snu_slideshow_generator.extra_texture_presets.add()
                newtexture.name = texturename
                newtexture.path = self.texture
                self.report({'INFO'}, "Added Preset: "+texturename)
            else:
                self.report({'INFO'}, "Preset Already Exists: "+texturename)
        return{'FINISHED'}


class SnuSlideshowRemoveExtraTexture(bpy.types.Operator):
    #This operator will attempt to find and remove a texture preset from the list
    bl_idname = 'slideshow.remove_extra_texture'
    bl_label = '-'
    bl_description = 'Removes a texture preset from the extra textures'

    texture: bpy.props.StringProperty()

    def execute(self, context):
        remove = os.path.split(self.texture)[1]
        index = context.scene.snu_slideshow_generator.extra_texture_presets.find(remove)
        if index >= 0:
            context.scene.snu_slideshow_generator.extra_texture_presets.remove(index)
            self.report({'INFO'}, "Removed Preset: "+remove)
        else:
            self.report({'INFO'}, "Could Not Find Preset: "+remove)
        return{'FINISHED'}


class SnuSlideshowExtraTextureMenu(bpy.types.Menu):
    #This is a menu to list extra texture presets
    bl_idname = 'SSG_MT_extra_texture_menu'
    bl_label = 'List of saved extra textures'

    def draw(self, context):
        layout = self.layout
        split = layout.split()
        column = split.column()
        for texture in context.scene.snu_slideshow_generator.extra_texture_presets:
            column.operator("slideshow.change_extra_texture", text=texture.name).texture = texture.path
        column.separator()
        column.operator("slideshow.change_extra_texture", text="None").texture = "None"
        column = split.column()
        for texture in context.scene.snu_slideshow_generator.extra_texture_presets:
            column.operator('slideshow.remove_extra_texture', text='X').texture = texture.path


class SnuSlideshowChangeExtraTexture(bpy.types.Operator):
    #Set the extra texture for the currently active slide
    bl_idname = 'slideshow.change_extra_texture'
    bl_label = 'Change Extra Texture'

    texture: bpy.props.StringProperty()

    def execute(self, context):
        current_scene = context.scene
        if is_generator_scene(current_scene):
            current_image = context.active_object
            current_image.slideshow.extratexture = self.texture
        else:
            current_scene.snu_slideshow_generator.extra_texture = self.texture
        return{'FINISHED'}


class SnuSlideshowCreate(bpy.types.Operator):
    #This operator creates a slideshow scene and all the image scenes from the generator scene
    bl_idname = 'slideshow.create'
    bl_label = 'Create Slideshow'
    bl_description = 'Turns the Slideshow Generator scene into a full slideshow'

    def execute(self, context):
        generator_scene = bpy.data.scenes['Slideshow Generator']
        generator_scene.snu_slideshow_generator.generator_workspace = context.workspace.name

        #Set up the Slideshow scene
        if 'Slideshow' in bpy.data.scenes:
            bpy.data.scenes.remove(bpy.data.scenes['Slideshow'])
        slideshow_scene = create_scene(generator_scene, 'Slideshow')
        image_scene_start = 1

        #Create a copy of the currently active and selected objects so they can be re-set later
        active = context.active_object
        selected = []
        for scene_object in context.scene.objects:
            if scene_object.select_get():
                selected.append(scene_object)

        context.window.scene = slideshow_scene

        #Iterate through image list, create scene for each image, and import into VSE
        images = list_slides(generator_scene)
        images.sort(key=lambda x: x.slideshow.index)
        previous_image_clip = None
        previous_image_plane = None
        for i, image_plane in enumerate(images):
            previous_image_clip = create_slideshow_slide(image_plane, i, generator_scene, slideshow_scene, image_scene_start, images, previous_image_clip, previous_image_plane)
            previous_image_plane = image_plane
            image_scene_start = previous_image_clip.frame_final_end - generator_scene.snu_slideshow_generator.crossfade_length
        bpy.ops.sequencer.select_all(action='DESELECT')

        self.report({'INFO'}, "Slideshow created")

        #Set slideshow length
        slideshow_scene.frame_end = image_scene_start + generator_scene.snu_slideshow_generator.crossfade_length
        slideshow_scene.sync_mode = 'AUDIO_SYNC'

        #Add slideshow audio if enabled
        if generator_scene.snu_slideshow_generator.audio_enabled:
            filename = os.path.realpath(bpy.path.abspath(generator_scene.snu_slideshow_generator.audio_track))
            if os.path.exists(filename):
                extension = os.path.splitext(generator_scene.snu_slideshow_generator.audio_track)[1].lower()
                if extension in bpy.path.extensions_audio:
                    #audio is enabled, the file exists, and is an audio format blender recognizes
                    audio_frame_end = 0

                    #This loop will repeat adding the audio track until the end of the slideshow is reached
                    i = 0
                    audio_sequence = None
                    while audio_frame_end < slideshow_scene.frame_end:
                        if audio_frame_end == 0:
                            #Set the starting point for the first loop
                            frame_start = 1
                        else:
                            #Set the starting point for a repeating audio loop
                            frame_start = audio_frame_end+1-generator_scene.snu_slideshow_generator.audio_loop_fade

                        audio_sequence = slideshow_scene.sequence_editor.sequences.new_sound(name='Audio', filepath=filename, channel=6+(i % 2), frame_start=frame_start)

                        if audio_sequence.frame_duration > 0:
                            #The audio sequence was added correctly, set the ending point
                            audio_frame_end = audio_sequence.frame_final_end
                        else:
                            #Something went wrong, abort adding audio sequences
                            audio_frame_end = slideshow_scene.frame_end
                        i += 1

                    #Add a fadeout to the last audio sequence
                    if audio_sequence:
                        audio_sequence.frame_final_end = slideshow_scene.frame_end
                        slideshow_scene.frame_current = slideshow_scene.frame_end - generator_scene.snu_slideshow_generator.audio_fade_length
                        audio_sequence.keyframe_insert(data_path='volume')
                        slideshow_scene.frame_current = slideshow_scene.frame_end
                        audio_sequence.volume = 0
                        audio_sequence.keyframe_insert(data_path='volume')

        #Attempt to switch to the video editor screen layout
        try:
            context.window.workspace = bpy.data.workspaces['Video Editing']
        except KeyError:
            pass

        slideshow_scene.render.sequencer_gl_preview = 'MATERIAL'
        try:
            slideshow_scene.render.use_sequencer_gl_preview = True
        except:
            pass

        #Return the selected and active objects to the way they were before the slideshow generation
        for scene_object in context.scene.objects:
            if scene_object in selected:
                scene_object.select_set(True)
            else:
                scene_object.select_set(False)
        context.view_layer.objects.active = active

        return{'FINISHED'}


class SnuSlideshowGenerator(bpy.types.Operator):
    #This operator will import images, and create the slideshow generator scene and everything in it
    bl_idname = 'slideshow.generator'
    bl_label = 'Create Slideshow Generator'
    bl_description = 'Imports images and creates a scene for setting up the slideshow'

    def execute(self, context):
        #check if slideshow generator scene exists, warn and cancel if it does
        if bpy.data.scenes.find('Slideshow Generator') != -1:
            self.report({'WARNING'}, 'Slideshow Generator Scene Already Exists')
            return{'CANCELLED'}

        slide_length = context.scene.snu_slideshow_generator.slide_length
        image_directory = context.scene.snu_slideshow_generator.image_directory
        image_types = list(bpy.path.extensions_image)
        video_types = list(bpy.path.extensions_movie)

        #get list of images in image_directory
        image_list = []
        video_list = []
        for image_type in image_types:
            #Search directory for files matching all image types, and add them to the list
            image_list.extend(glob.glob(bpy.path.abspath(image_directory)+'*'+image_type))
        for video_type in video_types:
            video_list.extend(glob.glob(bpy.path.abspath(image_directory)+'*'+video_type))

        imports = []
        for image in image_list:
            imports.append([image, False])
        for video in video_list:
            imports.append([video, True])
        total_images = len(imports)
        imports.sort(key=lambda x: x[0])

        self.report({'INFO'}, 'Importing '+str(total_images)+' images')

        #create scene, switch to it, and set up properties
        oldscene = context.scene
        generator_scene = create_scene(oldscene, 'Slideshow Generator')
        #context.window.scene = generator_scene
        generator_scene.snu_slideshow_generator.crossfade_length = 10
        generator_scene.snu_slideshow_generator.slide_length = slide_length
        generator_scene.snu_slideshow_generator.hidden_transforms = oldscene.snu_slideshow_generator.hidden_transforms
        generator_scene.snu_slideshow_generator.hidden_extras = oldscene.snu_slideshow_generator.hidden_extras
        for extra_texture_preset in oldscene.snu_slideshow_generator.extra_texture_presets:
            new_preset = generator_scene.snu_slideshow_generator.extra_texture_presets.add()
            new_preset.name = extra_texture_preset.name
            new_preset.path = extra_texture_preset.path

        #Attempt to switch to the correct viewport view and settings
        space = get_first_3d_view()
        #for area in context.screen.areas:
        #    if area.type == 'VIEW_3D':
        #        for space in area.spaces:
        #            if space.type == 'VIEW_3D':
        if space:
            if space.shading.type not in ['MATERIAL', 'RENDERED']:
                space.shading.type = 'MATERIAL'
            space.region_3d.view_rotation = (1.0, 0, 0, 0)
            space.region_3d.view_perspective = 'ORTHO'
            space.overlay.show_floor = False
            space.overlay.show_cursor = False
            space.overlay.show_relationship_lines = False
            space.lock_cursor = True

        #Add header instruction text
        instructions_data = bpy.data.curves.new(name='Instructions', type='FONT')
        instructions = bpy.data.objects.new(name='Instructions', object_data=instructions_data)
        generator_scene.collection.objects.link(instructions)
        instructions.location = (-1, 1.25, 0.0)
        instructions.scale = (.15, .15, .15)
        instructions.data.body = "Select an image and see the Scene tab in the properties area for details.\nDrag an image to rearrange it in the timeline.\nThe center cross on each image represents the focal point for transformations.\nThe box surrounding each image represents the viewable area for the cameara.\nMove, scale, and rotate this to change the viewable area."

        #Iterate through the list and import the images
        image_number = 1
        last_image = None
        for import_data in imports:
            image_file, is_video = import_data
            image = load_image(image_file)
            last_image = import_slideshow_image(image, image_number, slide_length, generator_scene, video=is_video, last_image=last_image)
            image_number += 1

        select_plane(last_image, generator_scene)
        context.scene.cursor.location = (0, 0, 0)
        print("Now displaying images, this may take a while...")

        update_scene(generator_scene)
        update_order(current_scene=generator_scene)

        return{'FINISHED'}


class SnuSlideshowGeneratorSettings(bpy.types.PropertyGroup):
    #snu_slideshow_generator.audio_loop_fade
    hidden_transforms: bpy.props.StringProperty(
        name="Hidden Transforms",
        default="",
        description="List of transforms to not use in randomize operations")
    hidden_extras: bpy.props.StringProperty(
        name="Hidden Extras",
        default="Text Normal Bottom;Text Normal Top;Video Background;Video Foreground;Compositor Glare;Overlay Curves Left;Overlay Curves Right",
        description="List of extras to not use in randomize operations")
    image_directory: bpy.props.StringProperty(
        name="Image Directory",
        default='/Images/',
        description="Location of images used in slideshow",
        subtype='DIR_PATH')
    slide_length: bpy.props.FloatProperty(
        name="Slide Length (Seconds)",
        default=4,
        min=1,
        max=20,
        description="Slide Scene Length In Seconds")
    crossfade_length: bpy.props.IntProperty(
        name="Crossfade Length (Frames)",
        default=10,
        min=0,
        max=120)
    extra_texture: bpy.props.StringProperty(
        name="Extra Texture",
        default="None")
    extra_texture_presets: bpy.props.CollectionProperty(
        type=SnuSlideshowExtraTexturePreset)
    audio_enabled: bpy.props.BoolProperty(
        default=False)
    audio_track: bpy.props.StringProperty(
        name="Audio Track",
        default="None")
    audio_fade_length: bpy.props.IntProperty(
        name="Fade Out",
        description="Length of audio fade out in frames",
        default=30,
        min=0,
        max=600)
    audio_loop_fade: bpy.props.IntProperty(
        name="Loop Overlap",
        description="Length of audio overlap when track is looped in frames",
        default=60,
        min=0,
        max=600)
    generator_workspace: bpy.props.StringProperty(
        name="Generator Scene Workspace",
        default='')


classes = [SnuSlideshowExtraTexturePreset, SnuSlideshowImage, SSG_PT_VSEPanel, SnuSlideshowGotoGenerator,
           SnuSlideshowPreviewMode, SSG_PT_Panel, SnuSlideshowMoveSlide, SnuSlideshowOpenExtraTexture,
           SnuSlideshowOpenAudio, SnuSlideshowAddSlide, SnuSlideshowExtraMenu, SnuSlideshowHideAllExtras,
           SnuSlideshowHideExtra, SnuSlideshowChangeExtra, SnuSlideshowTransformsMenu, SnuSlideshowHideAllTransforms,
           SnuSlideshowHideTransform, SnuSlideshowChangeTransform, SnuSlideshowApplyExtra, SnuSlideshowApplyTransform,
           SnuSlideshowApplySlideLength, SnuSlideshowApplyTransition, SnuSlideshowUpdateOrder, SnuSlideshowDeleteSlide,
           SnuSlideshowAddExtraTexture, SnuSlideshowRemoveExtraTexture, SnuSlideshowExtraTextureMenu,
           SnuSlideshowChangeExtraTexture, SnuSlideshowCreate, SnuSlideshowGenerator, SnuSlideshowGeneratorSettings]


def register():
    #Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.snu_slideshow_generator = bpy.props.PointerProperty(type=SnuSlideshowGeneratorSettings)

    bpy.types.Object.slideshow = bpy.props.PointerProperty(type=SnuSlideshowImage)

    handlers = bpy.app.handlers.depsgraph_update_post
    for handler in handlers:
        if " slideshow_autoupdate " in str(handler):
            handlers.remove(handler)
    handlers.append(slideshow_autoupdate)


def unregister():
    handlers = bpy.app.handlers.depsgraph_update_post
    for handler in handlers:
        if " slideshow_autoupdate " in str(handler):
            handlers.remove(handler)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
