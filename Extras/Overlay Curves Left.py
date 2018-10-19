import bpy


def extra(image_scene, image_plane, target_empty, camera, extra_amount, extra_text, extra_texture):
    bpy.context.screen.scene = image_scene

    #set up material
    circles_material = bpy.data.materials.new('Circles')
    circles_material.diffuse_color = (0.411, 0.411, 0.411)
    circles_material.diffuse_intensity = 1
    circles_material.specular_intensity = 1
    circles_material.specular_hardness = 10
    circles_material.use_transparency = True
    circles_material.specular_alpha = 0.28433
    circles_material.raytrace_transparency.fresnel = 2.2
    circles_material.use_cast_buffer_shadows = False
    circles_material.use_shadows = False

    #set up circle 1
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=1, enter_editmode=True)
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(4, 4, 4))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    circle1 = bpy.context.scene.objects.active
    circle1.name = 'Circle 1'
    circle1.data.materials.append(circles_material)
    circle1.location = (0, 0, -0.73)
    circle1.animation_data_create()
    circle1.animation_data.action = bpy.data.actions.new('circle1')
    fcurvex = circle1.animation_data.action.fcurves.new('location', index=0)
    keyframe = fcurvex.keyframe_points.insert(1, value=0.762)
    keyframe.co[1] = keyframe.co[1] + ((extra_amount - .5) / 3)
    modifier = fcurvex.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.1
    modifier.offset = 227.9
    fcurvey = circle1.animation_data.action.fcurves.new('location', index=1)
    fcurvey.keyframe_points.insert(1, value=0.33)
    modifier = fcurvey.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.2
    modifier.offset = 910.6
    circle1.parent = camera

    #set up circle2
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=1, enter_editmode=True)
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(4, 4, 4))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    circle2 = bpy.context.scene.objects.active
    circle2.name = 'Circle 2'
    circle2.data.materials.append(circles_material)
    circle2.location = (0, 0, -0.93)
    circle2.animation_data_create()
    circle2.animation_data.action = bpy.data.actions.new('circle2')
    fcurvex = circle2.animation_data.action.fcurves.new('location', index=0)
    keyframe = fcurvex.keyframe_points.insert(1, value=0.751)
    keyframe.co[1] = keyframe.co[1] + ((extra_amount - .5) / 3)
    modifier = fcurvex.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.1
    modifier.offset = 0
    fcurvey = circle2.animation_data.action.fcurves.new('location', index=1)
    fcurvey.keyframe_points.insert(1, value=0.19)
    modifier = fcurvey.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.2
    modifier.offset = 1200
    circle2.parent = camera

    #set up circle3
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=1.4, enter_editmode=True)
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(4, 4, 4))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    circle3 = bpy.context.scene.objects.active
    circle3.name = 'Circle 3'
    circle3.data.materials.append(circles_material)
    circle3.location = (0, 0, -1.1)
    circle3.animation_data_create()
    circle3.animation_data.action = bpy.data.actions.new('circle3')
    fcurvex = circle3.animation_data.action.fcurves.new('location', index=0)
    keyframe = fcurvex.keyframe_points.insert(1, value=1.1)
    keyframe.co[1] = keyframe.co[1] + ((extra_amount - .5) / 3)
    modifier = fcurvex.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.1
    modifier.offset = 0
    fcurvey = circle3.animation_data.action.fcurves.new('location', index=1)
    fcurvey.keyframe_points.insert(1, value=-0.002)
    modifier = fcurvey.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.2
    modifier.offset = 200
    circle3.parent = camera

    #set up lamp
    bpy.ops.object.lamp_add(type='SPOT', location=(0.33888, 0, 0.32165), rotation=(0.0, -0.201527, -3.141592))
    lamp = bpy.context.scene.objects.active
    lamp.name = 'Circles Lamp'
    lamp.data.shadow_method = 'NOSHADOW'
    lamp.data.spot_blend = 1
    lamp.data.energy = 2
    lamp.parent = camera
