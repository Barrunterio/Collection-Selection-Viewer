
import bpy, addon_utils
from bpy.types import AddonPreferences

bl_info = {
    "name": "Collection Viewer Selection", "author": "Barrunterio",
    "version": (0, 1), "blender": (2, 80, 0), "location": "Outliner",
    "description": "Modal Operator to make active only selected collections",
    "warning": "", "wiki_url": "", "category": ""}


def calc_children(col, list):
    calc_col(col, list)
    if col.children:
        for col in col.children:
            calc_col(col, list)
            calc_children(col, list)
        
def calc_col(col, list):
    if col.name in list:
        col.exclude = False
    else:
        col.exclude = True    

class brt_colection_selector_viewer(bpy.types.Operator):
    """Operator which exclude all the non selected collections"""
    bl_idname = "wm.brt_collection_selection"
    bl_label = "Collection Viewer Selection"

    _timer = None
    
    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            list = [None] * len(bpy.context.selected_ids)
            print("hello")
            for i,sel_col in enumerate(bpy.context.selected_ids):
                list[i] = sel_col.name
            for col in bpy.context.view_layer.layer_collection.children:
                calc_children(col, list)

        return {'PASS_THROUGH'}

    def execute(self, context):
        area = bpy.context.area
        old_type = area.type 
        area.type = 'OUTLINER'
        
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager

def menu_func(self, context):
    self.layout.operator(brt_colection_selector_viewer.bl_idname, text=brt_colection_selector_viewer.bl_label)
    
def BRT_OUTLINER_UI_HEADER(self, context):
    layout = self.layout
    layout.operator("wm.brt_collection_selection",text="",icon='VIS_SEL_11')

class BRT_Collection_Viewer_Selection_PreferencesPanel(AddonPreferences):
    bl_idname = __name__
    bl_label = "Intruction to use"
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='INFO')
        layout.label(text="Instruction to use")
    def draw(self, context):
        layout = self.layout
        row = layout.row(align= True)
        row.label(icon='X')
        row.label(text="In order to exit mode, press ESC or Rigth Mouse Click")

def register():
    bpy.utils.register_class(brt_colection_selector_viewer)
    bpy.utils.register_class(BRT_Collection_Viewer_Selection_PreferencesPanel)
    bpy.types.OUTLINER_HT_header.append(BRT_OUTLINER_UI_HEADER)


def unregister():
    bpy.utils.unregister_class(brt_colection_selector_viewer)
    bpy.utils.unregister_class(BRT_Collection_Viewer_Selection_PreferencesPanel)
    bpy.types.OUTLINER_HT_header.remove(BRT_OUTLINER_UI_HEADER)


if __name__ == "__main__":
    register()
