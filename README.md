# rFactor2-Rank

o Download the binary from [releases](../../releases)

o Save the **create_file.exe** file to your **rFactor2/UserData/player** directory (the one that contains all those ".cch" files)

o Double click **create_file.exe** to create / update a **career.blt** file

o Head over to https://rf2.gplrank.info/ and upload your lap times by pointing the upload page to your **career.blt** file

# Developer notes 
I took Uwe's original files and tweaked them. They already worked fine, the main change was packaging it up as an exe but the error reporting is also improved.

Written for vanilla Python 3.6 and Windows. To create the exe file run makeexe.bat which sets up a virtual environment 'env' containing PyInstaller and runs it.
