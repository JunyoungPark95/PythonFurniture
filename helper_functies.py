import bpy
import math
from math import *
import mathutils
from mathutils import Vector
import matplotlib.pyplot as plt

def zero(my_dpi):
    #bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    cam = bpy.data.objects['Camera']
    cam.location = [7.4811, -6.5076, 5.3437] # Default, maar dan een list

    #looking through all objects
    for obj in bpy.data.objects:
        #if the object is a mesh and not a lamp or camera etc.
        if obj.name != 'Camera' and obj.name != 'Lamp':
            obj.select = True
            bpy.ops.object.delete() 
        #if obj.type == 'MESH':
            #obj.select = True
            #bpy.ops.object.delete() 
    
    plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
    
    return cam
            
def point_at(obj, target, roll=0):
    """
    Rotate obj to look at target

    :arg obj: the object to be rotated. Usually the camera
    :arg target: the location (3-tuple or Vector) to be looked at
    :arg roll: The angle of rotation about the axis from obj to target in radians. 

    Based on: https://blender.stackexchange.com/a/5220/12947 (ideasman42)      
    """
    if not isinstance(target, mathutils.Vector):
        target = mathutils.Vector(target)
    loc = obj.location
    # direction points from the object to the target
    direction = target - loc

    quat = direction.to_track_quat('-Z', 'Y')

    # /usr/share/blender/scripts/addons/add_advanced_objects_menu/arrange_on_curve.py
    quat = quat.to_matrix().to_4x4()
    rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')

    # remember the current location, since assigning to obj.matrix_world changes it
    loc = loc.to_tuple()
    obj.matrix_world = quat * rollMatrix
    obj.location = loc    
    
def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()
    
def coloredEyes(name):
    bpy.context.scene.objects.active = bpy.data.objects[name]
    me = bpy.context.object

    # changes are visible after switch to the edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    polygons_eyes = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]

    ob = bpy.context.active_object
    mat = bpy.data.materials.get("Material")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="redis")
        mat.rgbCol = [0.8, 0.2, 0.2]
        mat.setAdd(0.8)

    # Assign it to object
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)
    
    # blue Eyes
    for poly in me.data.polygons:
        if poly.index in polygons_eyes:
            poly.material_index = 2
            #print(poly.index, polygons_eyes)
            
def add_vectors(vectors):
    for start, stop in vectors:
        start, stop = Vector(start), Vector(stop)
        #conestop = stop.copy()
        #for count, value in enumerate(stop):
        #    if value >= 0.4:
        #        stop[count] -= 0.4
        x = start[0] + stop[0]
        y = start[1] + stop[1]
        z = start[2] + stop[2]
        length = sqrt(z*z+y*y+x*x)

        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.04, depth=length, end_fill_type='NGON', view_align=False, enter_editmode=False, location=start)
        cyl = bpy.context.active_object
        cyl.rotation_mode = 'QUATERNION'
        cyl.rotation_quaternion = (start-stop).to_track_quat('Z','Y')
        bpy.ops.transform.translate(value=(start+stop)/2)

        bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.1, radius2=0, depth=0.4, end_fill_type='NGON', view_align=False, enter_editmode=False, location=stop)
        cone = bpy.context.active_object
        cone.rotation_mode = 'QUATERNION'
        cone.rotation_quaternion = (start-stop).to_track_quat('-Z','Y')
        cone.location = start + stop 