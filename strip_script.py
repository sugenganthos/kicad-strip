from pathlib import Path    # pathlib adalah modul sejak python 3.4, Path ialah class di dalam modul pathlib 
from skip import Schematic  # modul skip harus diinstall dulu. Ref: https://github.com/psychogenic/kicad-skip
import sys      # for accessing parameter arguments
import shutil   # for copy file

cwd = Path.cwd()            # get current working directory 
#print(cwd)                  # tampilkan ke prompt
projectDirName = cwd.name      # nama project = nama folder (setting defaut)
#print(projectDirName)

try:
    outputFolder = sys.argv[1]  # try if exist
except Exception :    
    outputFolder = "outputFolderStripped"   # default if output folder unspecified

#make output folder 
OutputPath = cwd.joinpath(outputFolder)
OutputPath.mkdir(exist_ok=True)     # other parameter is default   
print("output path: ",OutputPath)

# list all files
allFiles = cwd.iterdir()

deletedTextBoxCount = 0
#check each file
for fileItem in allFiles:
    targetFilePath = OutputPath.joinpath(fileItem.name)   # set up target path for later
    match fileItem.suffix:      # see file extension for matching
        case '.kicad_sch':
            schemObj = Schematic(str(fileItem))
            #print("sche: ",schemObj)  
            try:
                for textBoxItem in schemObj.text_box[:]:    # create slice or shallow copy for list of text box. Because we will del the item
                    print("text boxes: ",textBoxItem) 
                    try:                   # check because not every textboxes contain stroke property  
                        borderColor = textBoxItem.stroke.color  # get border color
                        print("border color: ",borderColor) 
                        if (borderColor[0] == 255) and (borderColor[1] == 0) and (borderColor[2] == 0) and (borderColor[3] == 1):   # Check for Red 4 color
                            textBoxItem.delete()                # delete textBox with border color = Red 4
                            deletedTextBoxCount = deletedTextBoxCount + 1
                    except Exception as e:
                        print(e)
                        #pass                
            except Exception:
                pass
            schemObj.write(targetFilePath)    # write stripped schematics to output folder
            print("processed: ",targetFilePath)      
        case '.kicad_pcb' | '.kicad_pro':    # case for pcb and project, just copy to output
            shutil.copy2(fileItem,OutputPath)
            #fileItem.replace(targetFilePath)
            print("processed: ",targetFilePath)  
        # for pcb house, usually just 3 kind: schematic, project, and pcb.
        # for sharing to your colleague, maybe other file also needed: library, setting, lib table, etc
    
# For complete syntax, use schematic editor. Add an item and comfigure its properties. Then open the schematic as text
# Find the property you need to know. Supposed you add some unique value while adding.
# example:
# - Finding textBox border color: text_box.stroke.color
# - Finding textBox background color: text_box.fill.color
# - Finding textBox font color: text_box.effects.font.color
# print(mainschem.text_box[0].effects.font.color)
# print(mainschem.text_box[0].effects.font.color[0])    # show R color (color format: RGBA) (accessed with index because doesn't have name)

print("deleted text: ", deletedTextBoxCount)
print("due to bug, single text_box in schematic maybe not detected ('str' object has no attribute 'stroke')")
print("Make sure to have other textbox along with toDel text box (happens per schematic)")
print("I have check, no problem with scematic. Perhaps it was kicad-skip")
        
        
