import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    #This is meant as a template for new extras, the extra with the filename 'None' will always be ignored by the generator.
    #
    #Rules:
    #   This script's filename will determine the name of the extra listed in the UI.
    #   This script may import data from a .blend file of the same file name as the script.
    #   This script may add whatever it pleases to the passed in scene, but it should not adjust any other scene.
    #   The image_plane will be located at the point (0, 0, 0).  It will be 1 blender unit long on it's y axis, and it will be facing in the positive global z direction.
    #   The camera will be located about 1.93 blender units (depending on the transform) above the plane in the global z direction, and pointing in the global negative z direction.
    #
    #Passed in variables are described as follows:
    #   image_scene - <bpy_struct, Struct("Scene")>
    #       This is the scene that the slide has been placed in.
    #       The script should be working in this scene, so starting with setting the current scene to image_scene is a good idea.
    #
    #   image_plane - <bpy_struct, Struct("Object")>
    #       Specifically a mesh plane.
    #       This is the plane object that the slide image is on.
    #       This plane is not animated in any way.
    #
    #   target_empty - <bpy_struct, Struct("Object")>
    #       Specifically a 'plain axes' empty.
    #       This is the empty that is shown in the slideshow generator as the cross.
    #       This is meant specifically for the transforms, but may have other uses.
    #
    #   camera - <bpy_struct, Struct("Object")>
    #       Specifically a camera.
    #       This is the scene camera.
    #       This is already set up and parented to the transform, and will be moving and/or scaled in most cases.
    #       If you wish for an object to be stationary relative to the camera, make sure to parent it to this.
    #
    #   extra_amount - Float variable between 0.0 and 1.0
    #       This is exposed to the UI and is meant to control the 'strength' of the extra scene - for instance the amount of blur on a blurred background, or the extrusion amount of text.
    #       The value of 0.5 should be a nice average amount, 0 should be too little for normal usage, and 1 should be too much for normal usage.
    #
    #   extra_text - A string variable.
    #       This is exposed to the UI and can be used for text objects in the extra scene.
    #
    #   extra_texture - <bpy_struct, Struct("Image")>, or a None if not able to be loaded.
    #       This is exposed to the UI and can be a still image or a video.
