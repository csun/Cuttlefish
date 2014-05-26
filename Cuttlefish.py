# Some code based on Camaleón, another Sublime Text plugin.
# https://github.com/SublimeText/Camaleon

import sublime, sublime_plugin

SUBLIME_PREFS_FILENAME = "Preferences.sublime-settings"
CUTTLEFISH_PREFS_FILENAME = "Cuttlefish.sublime-settings"

class Preset:
    def __init__(self, data, defaults):
        self.raw_data = data
        self.defaults = defaults

    def load(self):
        self.sublime_preferences = sublime.load_settings(SUBLIME_PREFS_FILENAME)

        self.set_preference("color_scheme")
        self.set_preference("font_face")
        self.set_preference("font_size")

        sublime.save_settings(SUBLIME_PREFS_FILENAME)

    def set_preference(self, preference_name):
        if preference_name in self.raw_data:
            self.sublime_preferences.set(preference_name, self.raw_data[preference_name])
        elif preference_name in self.defaults:
            self.sublime_preferences.set(preference_name, self.defaults[preference_name])


class CuttlefishCycleCommand(sublime_plugin.WindowCommand):
    def run(self, direction="next"):
        preferences = sublime.load_settings(CUTTLEFISH_PREFS_FILENAME)
        current_preset_index = preferences.get("current_preset", 0)
        all_presets = preferences.get("presets", [])
        defaults = preferences.get("defaults", {})

        if len(all_presets) == 0:
            return
        elif direction == "next":
            current_preset_index += 1
        else:
            current_preset_index -= 1

        if current_preset_index >= len(all_presets):
            current_preset_index = 0
        elif current_preset_index < 0:
            current_preset_index = len(all_presets) - 1


        preset = Preset(all_presets[current_preset_index], defaults)
        preset.load()

        preferences.set("current_preset", current_preset_index)
        sublime.save_settings(CUTTLEFISH_PREFS_FILENAME)