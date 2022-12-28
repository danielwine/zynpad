#!/usr/bin/python3
# -*- coding: utf-8 -*-
#******************************************************************************
# ZYNTHIAN PROJECT: Zynthian GUI
#
# Zynthian GUI ZS3 learn screen
#
# Copyright (C) 2018-2022 Fernando Moyano <jofemodo@zynthian.org>
#
#******************************************************************************
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a full copy of the GNU General Public License see the LICENSE.txt file.
#
#******************************************************************************

import tkinter
import logging

# Zynthian specific modules
from zyngui import zynthian_gui_config
from zyngui.zynthian_gui_selector import zynthian_gui_selector

#------------------------------------------------------------------------------
# Zynthian Sub-SnapShot (ZS3) MIDI-learn GUI Class
#------------------------------------------------------------------------------

class zynthian_gui_zs3_learn(zynthian_gui_selector):

	def __init__(self):
		super().__init__('Program', True)
		
		self.zs3_waiting_label = tkinter.Label(self.main_frame,
			text = 'Waiting for MIDI Program Change...',
			font=(zynthian_gui_config.font_family, zynthian_gui_config.font_size-2),
			fg = zynthian_gui_config.color_ml,
			bg = zynthian_gui_config.color_panel_bg
		)
		if self.wide:
			padx = (0,2)
		else:
			padx = (2,2)
		self.zs3_waiting_label.grid(row=zynthian_gui_config.layout['list_pos'][0] + 4, column=zynthian_gui_config.layout['list_pos'][1], padx=padx, sticky='ew')


	def show(self):
		self.zyngui.state_manager.enter_midi_learn()
		super().show()


	def hide(self):
		if self.shown:
			self.zyngui.state_manager.exit_midi_learn()
			super().hide()


	def fill_list(self):
		self.list_data = []
		self.list_data.append(('SAVE_ZS3', None, "Save as new ZS3"))

		#Add list of programs
		if len(self.zyngui.state_manager.zs3) > 0:
			self.list_data.append((None, None, "> SAVED ZS3s"))
		for id, state in self.zyngui.state_manager.zs3.items():
			if id == "zs3-0":
				continue
			if id.startswith("zs3"):
				title = state['title']
			else:
				chan, prog = id.split('/')
				if zynthian_gui_config.midi_single_active_channel:
					title = f"{state['title']} -> PR#{prog}"
				else:
					title = f"{state['title']} -> CH#{chan}:PR#{prog}"
			self.list_data.append((id, state, title))

		super().fill_list()


	def select_action(self, i, t='S'):
		zs3_index = self.list_data[i][0]
		if zs3_index == "SAVE_ZS3":
			self.zyngui.state_manager.exit_midi_learn()
			self.zyngui.state_manager.save_zs3()
			self.zyngui.close_screen()
			return True
		else:
			if t  == 'S':
				self.zyngui.state_manager.exit_midi_learn()
				self.zyngui.state_manager.load_zs3(zs3_index)
				self.zyngui.close_screen()
			elif t == 'B':
				self.zyngui.state_manager.exit_midi_learn()
				self.zyngui.screens['zs3_options'].config(zs3_index)
				self.zyngui.show_screen('zs3_options')
				return True


	def set_select_path(self):
		if self.zyngui.get_current_processor():
			self.select_path.set(self.zyngui.get_current_processor().get_basepath() + "/PROG MIDI-Learn")
		else:
			self.select_path.set("PROG MIDI-Learn")


	def back_action(self):
		self.zyngui.state_manager.exit_midi_learn()
		return False


#-------------------------------------------------------------------------------
