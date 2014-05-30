Cuttlefish
==========
A Sublime Text 3 package for easy switching between themes. Inspired by Camaléon, another Sublime Text package.

##Installation
Installation through Package Control (https://sublime.wbond.net/) is recommended.

##Usage
By default, Cuttlefish mostly uses the command palette to handle saving and changing presets.

To save your current theme, font face, and font size as a preset, use "Cuttlefish: Save Current Settings As Preset". For loading, deleting, and quick switching presets, use the respective similarly named commands. Just like with Camaléon, F8 and Shift+F8 cycle forwards and backwards through your presets by default.

##Customization
If you prefer to add presets manually, you can find the Cuttlefish user settings in the Preferences menu, under Package Settings. If you've already saved a preset, its format should be pretty self-evident. Each preset can specify `color_scheme`, `font_face`, and `font_size`.

If you'd like to add custom keybindings, Cuttlefish exposes the following commands:
`cuttlefish_cycle` takes an argument `direction` which can be either "next" or "previous". It cycles through your list of presets, switching to either the next or previous preset.
`cuttlefish_save` saves your current settings to a preset.
`cuttlefish_load` loads a saved preset.
`cuttlefish_delete` deletes a saved preset.

##License and Parting Wishes
Cuttlefish is released under the GPLv3. Have fun!
