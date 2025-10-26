#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gimp", "3.0")
gi.require_version("GimpUi", "3.0")
from gi.repository import Gimp, GimpUi, GLib, Gtk
import sys

class AddGridGuides(Gimp.PlugIn):

    def do_query_procedures(self):
        return ["plug-in-add-grid-guides"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )
        procedure.set_image_types("*")
        procedure.set_menu_label("Add Grid Guides")
        procedure.add_menu_path("<Image>/Filters/Guides/")
        procedure.set_documentation(
            "Add guides using rows/columns or pixel spacing",
            "Creates vertical and horizontal guides based on user input.",
            name
        )
        procedure.set_attribution("Madhusha", "Madhusha", "2025")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):

        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init("add_grid_guides")

            # Dialog
            dialog = GimpUi.Dialog(title="Add Grid Guides", use_header_bar=True)
            dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
            dialog.add_button("_OK", Gtk.ResponseType.OK)

            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=10)
            dialog.get_content_area().add(vbox)

            # Rows
            row_label = Gtk.Label(label="Rows:")
            row_spin = Gtk.SpinButton()
            row_spin.set_adjustment(Gtk.Adjustment(
            value=0, lower=0, upper=10000, step_increment=1, page_increment=10, page_size=0
            ))
            vbox.pack_start(row_label, False, False, 0)
            vbox.pack_start(row_spin, False, False, 0)

            # Columns
            col_label = Gtk.Label(label="Columns:")
            col_spin = Gtk.SpinButton()
            col_spin.set_adjustment(Gtk.Adjustment(
            value=0, lower=0, upper=10000, step_increment=1, page_increment=10, page_size=0
            ))
            vbox.pack_start(col_label, False, False, 0)
            vbox.pack_start(col_spin, False, False, 0)

            # Pixel spacing
            pix_label = Gtk.Label(label="Or pixel spacing (optional, leave 0 to ignore):")
            vbox.pack_start(pix_label, False, False, 0)
            h_pix_spin = Gtk.SpinButton()
            h_pix_spin.set_adjustment(Gtk.Adjustment(
            value=0, lower=0, upper=10000, step_increment=1, page_increment=10, page_size=0
            ))
            v_pix_spin = Gtk.SpinButton()
            v_pix_spin.set_adjustment(Gtk.Adjustment(
            value=0, lower=0, upper=10000, step_increment=1, page_increment=10, page_size=0
            ))
            vbox.pack_start(Gtk.Label(label="Horizontal spacing:"), False, False, 0)
            vbox.pack_start(h_pix_spin, False, False, 0)
            vbox.pack_start(Gtk.Label(label="Vertical spacing:"), False, False, 0)
            vbox.pack_start(v_pix_spin, False, False, 0)

            dialog.show_all()
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                rows = row_spin.get_value_as_int()
                cols = col_spin.get_value_as_int()
                h_spacing = h_pix_spin.get_value_as_int()
                v_spacing = v_pix_spin.get_value_as_int()
            else:
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, GLib.Error())
            dialog.destroy()
        else:
            # Defaults for non-interactive mode
            rows, cols = 0, 0
            h_spacing, v_spacing = 0, 0

        width = image.get_width()
        height = image.get_height()
        image.undo_group_start()

        # Add guides by pixel spacing if provided
        if h_spacing > 0:
            for x in range(h_spacing, width, h_spacing):
                image.add_vguide(x)
        elif cols > 0:
            for i in range(1, cols):
                image.add_vguide(int(width * i / (cols)))

        if v_spacing > 0:
            for y in range(v_spacing, height, v_spacing):
                image.add_hguide(y)
        elif rows > 0:
            for i in range(1, rows):
                image.add_hguide(int(height * i / (rows)))


        '''
        # Optional: borders
        image.add_vguide(0)
        image.add_vguide(width)
        image.add_hguide(0)
        image.add_hguide(height)
        '''
        
        image.undo_group_end()
        Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(AddGridGuides.__gtype__, sys.argv)
