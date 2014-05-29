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

class CuttlefishCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window

        self.preferences = sublime.load_settings(CUTTLEFISH_PREFS_FILENAME)
        self.current_preset = self.preferences.get("current_preset", 0)
        self.defaults = self.preferences.get("defaults", {})
        self.presets = self.preferences.get("presets", [])

    def run(self):
        pass

    def switch_to_preset(self, preset_number):
        num_presets = len(self.presets)

        if num_presets == 0:
            return

        if preset_number >= num_presets:
            preset_number = 0
        elif preset_number < 0:
            preset_number = num_presets - 1

        preset = Preset(self.presets[preset_number], self.defaults)
        preset.load()

        self.current_preset = preset_number
        self.preferences.set("current_preset", preset_number)
        sublime.save_settings(CUTTLEFISH_PREFS_FILENAME)

 

class CuttlefishCycleCommand(CuttlefishCommand):
    def __init__(self, window):
        CuttlefishCommand.__init__(self, window)

    def run(self, direction="next"):
        next_preset = self.current_preset

        if direction == "next":
            next_preset += 1
        else:
            next_preset -= 1

        self.switch_to_preset(next_preset)

class CuttlefishLoadCommand(CuttlefishCommand):
    def __init__(self, window):
        CuttlefishCommand.__init__(self, window)

    def run(self):
        names = list(map((lambda preset: preset["name"]), self.presets))
        self.window.show_quick_panel(names, self.switch_to_preset)
        # Use show_quick_panel
