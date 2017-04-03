# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

__author__ = "Keith McDuffee <keith@realistek.com>"
__plugin_name__ = "OctoBlynk"
__plugin_version__ = "0.1.1"
__plugin_description__ = "Control and receive info from OctoPi using Blynk."
__plugin_license__ = "AGPLv3"

from blynkapi import Blynk

class OctoBlynkPlugin(octoprint.plugin.SettingsPlugin,
                      octoprint.plugin.AssetPlugin,
                      octoprint.plugin.TemplatePlugin,
                      octoprint.plugin.EventHandlerPlugin,
                      octoprint.plugin.ProgressPlugin):

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
                        auth_token=None
		)

        def get_settings_restricted_paths(self):
                # only used in OctoPrint versions > 1.2.16
                return dict(admin=[["auth_token"]])

        def on_settings_load(self):
                data = octoprint.plugin.SettingsPlugin.on_settings_load(self)

                # only return our restricted settings to admin users - this is only needed for OctoPrint <= 1.2.16
                restricted = ("auth_token")
                for r in restricted:
                        if r in data and (current_user is None or current_user.is_anonymous() or not current_user.is_admin()):
                                data[r] = None

                return data

        def on_settings_save(self, data):
                octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/OctoBlynk.js"],
			css=["css/OctoBlynk.css"],
			less=["less/OctoBlynk.less"]
		)

        ###~~ EventHandlerPlugin

	def on_event(self, event, payload):
		if event == octoprint.events.Events.PRINT_STARTED:
			self._send_message(payload["origin"], payload["path"], 0)
		elif event == octoprint.events.Events.PRINT_DONE:
			self._send_message(payload["origin"], payload["path"], 100)

	##~~ ProgressPlugin

	def on_print_progress(self, storage, path, progress):
		if not self._printer.is_printing():
			return
		self._send_message(storage, path, progress)

	##~~ Helpers

	def _send_message(self, storage, path, progress):
		message = self._settings.get(["message"]).format(progress=progress,
		                                                 storage=storage,
		                                                 path=path)
		
		##self._printer.commands("M117 {}".format(message))
		## SEND BLYNK
		self._settings.get(["auth_token"])
		percent_done = Blynk(self._settings.get(["auth_token"]), pin = "V3")
                percent_done.set_val([progress])

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			OctoBlynk=dict(
				displayName="OctoBlynk",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="gudlyf",
				repo="OctoPrint-Blynk",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/gudlyf/OctoPrint-Blynk/archive/{target_version}.zip"
			)
		)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctoBlynkPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

