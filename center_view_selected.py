"""Center viewport on selected object."""
import bpy


bl_info = {
    "name": "Center View to Selected",
    "blender": (3, 00, 0),
    "category": "Object",
}


class CenterViewSelected(bpy.types.Operator):
    """Center viewport on selected object."""

    bl_idname = "object.center_view_selected"
    bl_label = "Center View to Selected"

    def execute(self, context):

        # Copy the current cursor position
        cursor_position = context.scene.cursor.location.copy()

        # Move the cursor position to that of the selected object
        bpy.ops.view3d.snap_cursor_to_selected()

        # Center the viewport over the current cursor position
        bpy.ops.view3d.view_center_cursor()

        # Move the cursor back to its earlier position
        context.scene.cursor.location = cursor_position

        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(CenterViewSelected.bl_idname)


# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(CenterViewSelected)
    bpy.types.VIEW3D_MT_view_align.append(menu_func)

    # Handle the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            CenterViewSelected.bl_idname, type="PERIOD", value="PRESS", shift=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(CenterViewSelected)
    bpy.types.VIEW3D_MT_view_align.remove(menu_func)

    # Handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
