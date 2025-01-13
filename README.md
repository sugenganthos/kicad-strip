# kicad-strip
Example python script for removing object from schematic

## Requirement
Install kicad-skip through pip. Use KiCad command prompt. See https://github.com/psychogenic/kicad-skip for kicad-skip detail.
You must know python. Because this is example code. No UI at all.

## Usage
1. Copy the script to project folder. Along with schematic.
2. Edit the script to adjust it.
3. Run from KiCad command prompt (direct the cmd to work from project folder)

```
> strip_script.py targetFolderName
```

The default script will works without edit. It will remove text box with border color: Red 4. So make sure your confidential note is text box with border color.
All schematic will be stripped.


