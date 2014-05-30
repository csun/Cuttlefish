# Some code based on Camaleón, another Sublime Text plugin.
# https://github.com/SublimeText/Camaleon

import sublime, sublime_plugin

SUBLIME_PREFS_FILENAME = "Preferences.sublime-settings"
CUTTLEFISH_PREFS_FILENAME = "Cuttlefish.sublime-settings"

class Preset:
    CONTROLLED_SETTINGS = ["color_scheme", "font_face", "font_size"]

    def __init__(self, data):
        self.raw_data = data


    def load(self):
        sublime_preferences = sublime.load_settings(SUBLIME_PREFS_FILENAME)

        for setting in Preset.CONTROLLED_SETTINGS:
            if not (setting in self.raw_data): return
            sublime_preferences.set(setting, self.raw_data[setting])

        sublime.save_settings(SUBLIME_PREFS_FILENAME)

    def save_as(self, name):
        if len(name) > 0:
            cuttlefish_prefs = sublime.load_settings(CUTTLEFISH_PREFS_FILENAME)
            presets = cuttlefish_prefs.get("presets")

            presets = list(filter((lambda preset: preset["name"] != name), presets))

            data = self.raw_data
            data["name"] = name

            presets.append(data)

            cuttlefish_prefs.set("presets", presets)
            sublime.save_settings(CUTTLEFISH_PREFS_FILENAME)


class CuttlefishCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window

        self.reload_data_from_preferences()

    def reload_data_from_preferences(self):
        self.preferences = sublime.load_settings(CUTTLEFISH_PREFS_FILENAME)
        self.current_preset = self.preferences.get("current_preset", 0)
        self.presets = self.preferences.get("presets", [])

    def run(self):
        self.reload_data_from_preferences()

    def switch_to_preset(self, preset_number):
        num_presets = len(self.presets)

        if num_presets == 0:
            return

        if preset_number >= num_presets:
            preset_number = 0
        elif preset_number < 0:
            preset_number = num_presets - 1

        preset = Preset(self.presets[preset_number])
        preset.load()

        self.current_preset = preset_number
        self.preferences.set("current_preset", preset_number)

        sublime.save_settings(CUTTLEFISH_PREFS_FILENAME)

 

class CuttlefishCycleCommand(CuttlefishCommand):
    def run(self, direction="next"):
        super().run()

        next_preset = self.current_preset

        if direction == "next":
            next_preset += 1
        else:
            next_preset -= 1

        self.switch_to_preset(next_preset)

class CuttlefishLoadCommand(CuttlefishCommand):
    def run(self):
        super().run()

        self.reload_data_from_preferences()

        names = list(map((lambda preset: preset["name"]), self.presets))

        def callback(choice):
            if choice != -1: self.switch_to_preset(choice)

        self.window.show_quick_panel(names, callback)

class CuttlefishSaveCommand(CuttlefishCommand):
    def run(self):
        super().run()

        self.reload_data_from_preferences()

        active_view = self.window.active_view()
        data = {
            "color_scheme": active_view.settings().get("color_scheme"),
            "font_face": active_view.settings().get("font_face"),
            "font_size": active_view.settings().get("font_size")
        } 

        preset = Preset(data)
        self.window.show_input_panel("Preset name:","",preset.save_as,None,None)
