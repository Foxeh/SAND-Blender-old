
#EXTREMELY SIMPLE SCRIPT


bl_info = {
    "name": "Burn_e_Rig_UI",
    "author": "Paul Dunne a.k.a Well Dunne",
    "blender": (2, 6, 3),
    "location": "Tool Shelf",
    "description": "Simple UI",
    "category": "Rigging"}

import bpy

#var
rig_id = "RIG"

#BONE LAYERS
class BoneLayerPanel(bpy.types.Panel):
    bl_idname = "Bone Layers"
    bl_label = "Bone Layers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(self,context):
        if context.mode != 'OBJECT' and context.mode != 'EDIT' and context.mode != 'POSE':
            return False
        try:
            return (context.active_object.name == rig_id)
        except (AttributeError,KeyError,TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='HEAD',icon = 'BONE_DATA')
        row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='BODY',icon = 'BONE_DATA')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='ARMS',icon = 'BONE_DATA')
        row.prop(context.active_object.data, 'layers', index=3, toggle=True, text='HANDS',icon = 'BONE_DATA')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=4, toggle=True, text='ROOT',icon = 'BONE_DATA')
        row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='GASLINES',icon = 'BONE_DATA')
        row = col.row()
        row.label(text="-----------------------------------------------------")           
        col = layout.column(align=True) 
        col.label (text="EYE SLIDERS:",icon = 'RESTRICT_VIEW_OFF')        
     
        row = layout.row(align=True) 
        row.prop(context.active_object.data, '["BLINK"]', slider=True, text="BLINK",)
        row = layout.row(align=True) 
        row.prop(context.active_object.data, '["SCALE UP"]', slider=True, text="SCALE",)           
        row = layout.row(align=True) 
        row.prop(context.active_object.data, '["mad"]', slider=True, text="MAD",)               
                
        
        
        
                       
        
bpy.utils.register_class(BoneLayerPanel)        