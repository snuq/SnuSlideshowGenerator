import bpy


def extra(data):
    camera = data['camera']
    extra_amount = data['extra_amount']
    image_scene = data['image_scene']
    bpy.context.window.scene = image_scene

    #set up material
    circles_material = bpy.data.materials.new('Circles')
    circles_material.blend_method = 'BLEND'
    circles_material.use_nodes = True
    node_tree = circles_material.node_tree
    nodes = node_tree.nodes
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            shader = node
            shader.inputs["Base Color"].default_value = (0.411, 0.411, 0.411, 1)
            shader.inputs["Emission Strength"].default_value = 0.411
            shader.inputs["Roughness"].default_value = 0.2
            shader.inputs["Alpha"].default_value = 0.333

    #set up circle 1
    bpy.ops.mesh.primitive_circle_add(vertices=128, radius=1, enter_editmode=True)
    bpy.ops.mesh.extrude_region()
    bpy.ops.transform.resize(value=(4, 4, 4))
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    circle1 = bpy.context.active_object
    circle1.name = 'Circle 1'
    circle1.data.materials.append(circles_material)
    circle1.location = (0, 0, -0.73)
    circle1.animation_data_create()
    circle1.animation_data.action = bpy.data.actions.new('circle1')
    fcurvex = circle1.animation_data.action.fcurves.new('location', index=0)
    keyframe = fcurvex.keyframe_points.insert(1, value=-0.59)
    keyframe.co[1] = keyframe.co[1] - ((extra_amount - .5) / 3)
    modifier = fcurvex.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.1
    modifier.offset = 227.9
    fcurvey = circle1.animation_data.action.fcurves.new('location', index=1)
    fcurvey.keyframe_points.insert(1, value=0.535)
    if not circle1.animation_data.action_slot:
        circle1.animation_data.action_slot = circle1.animation_data.action.slots[0]
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
    circle2 = bpy.context.active_object
    circle2.name = 'Circle 2'
    circle2.data.materials.append(circles_material)
    circle2.location = (0, 0, -0.93)
    circle2.animation_data_create()
    circle2.animation_data.action = bpy.data.actions.new('circle2')
    fcurvex = circle2.animation_data.action.fcurves.new('location', index=0)
    keyframe = fcurvex.keyframe_points.insert(1, value=-0.714)
    keyframe.co[1] = keyframe.co[1] - ((extra_amount - .5) / 3)
    modifier = fcurvex.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.1
    modifier.offset = 0
    fcurvey = circle2.animation_data.action.fcurves.new('location', index=1)
    fcurvey.keyframe_points.insert(1, value=0.23)
    if not circle2.animation_data.action_slot:
        circle2.animation_data.action_slot = circle2.animation_data.action.slots[0]
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
    circle3 = bpy.context.active_object
    circle3.name = 'Circle 3'
    circle3.data.materials.append(circles_material)
    circle3.location = (0, 0, -1.1)
    circle3.animation_data_create()
    circle3.animation_data.action = bpy.data.actions.new('circle3')
    fcurvex = circle3.animation_data.action.fcurves.new('location', index=0)
    keyframe = fcurvex.keyframe_points.insert(1, value=-1.1)
    keyframe.co[1] = keyframe.co[1] - ((extra_amount - .5) / 3)
    modifier = fcurvex.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.1
    modifier.offset = 0
    fcurvey = circle3.animation_data.action.fcurves.new('location', index=1)
    fcurvey.keyframe_points.insert(1, value=-0.05)
    if not circle3.animation_data.action_slot:
        circle3.animation_data.action_slot = circle3.animation_data.action.slots[0]
    modifier = fcurvey.modifiers.new('NOISE')
    modifier.scale = 100
    modifier.strength = 0.2
    modifier.offset = 200
    circle3.parent = camera

    #set up lamp
    bpy.ops.object.light_add(type='SPOT', location=(-0.33888, 0, 0.32165), rotation=(0.0, -0.201527, 0))
    lamp = bpy.context.active_object
    lamp.name = 'Circles Lamp'
    lamp.data.use_shadow = False
    lamp.data.spot_blend = 1
    lamp.data.energy = 200
    lamp.parent = camera
