# Space Block Jumper

Navigational package for the Sublime text editor.

This package lets you jump with the cursor vertically across space separated blocks, skipping empty lines. It also lets you select while jumping and has a command that selects current block. Consecutive usage of the block selection command indents selection or splits selection into multiple lines. This can be cycled.

# Usage
Jumping inside a block takes you to the its edge. When jumping from an edge of a block the cursor skips the closest edge in the new block. Consecutive empty lines are always skipped.

### Settings
Settings | Description
------- | ------
Skip Closest Edge | Disable this to jump to every edge of every block irregardless of where you jump from. (Default: on)
Jump To Block Separator | Enable this to always jump to empty lines. (Default: off)
Show Cursor At Center | When jumping (Default: on)

### Keybinds
Keybind | Action
--------- | ------
<kbd>Alt</kbd>+<kbd>Up</kbd> | Jump up
<kbd>Alt</kbd>+<kbd>Down</kbd> | Jump down
<kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>Up</kbd> | Jump and select up
<kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>Down</kbd> | Jump and select down
<kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>d</kbd> | Select block around cursor, consecutive usage indents selection and/or splits selection into multiple lines

# Ideas
* Implement selection retraction
* Support for multiple blocks with alt+shift+d
* Improve selection expansion with alt+shift+d
* Improve empty lines selection with alt+shift+d
