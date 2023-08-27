 
# jemoview
Jeti Model Viewer

Jeti RC transmitters store the model programs in folder _Model_ on the SD memory card. 
The name of each model file consists of a 4-digit number (corresponding to the order of the models in the
transmitter) followed by an alphanumeric text of maximum 4 characters (corresponding to the first 4
places of the model name) plus the extension jsn (for example 0007Pipe.jsn).
The ending jsn stands for JSON, which is a text format formed by pairs of keys and values. 
As a rule the content of such jsn files consists of a single long line, and therefore it is difficult to understand 
when opened with a usual text editor.

The program jemoview reads such model files, extracts the essential data and writes
the result as table into a new csv (spreadsheet) file, for example 0007Pipe.csv. The extension csv stands for "comma
separated values", i.e. the values in each line are separated by special characters. Jemoview
uses the semicolon ; as its standard separator. The advantage of the csv format is that 
usual table programs such as _Excel_ (by MS) or _Calc_ (by Libre Office) will display the data as table
and on the other hand its data can be processed as text with usual search or comparison programs.

Before processing, the jemoview program checks whether a file named settings.txt exists. This file
can contain options for controlling jemoview, such as the language (German or English), the
destination folder of the csv files to be created, and above all the installation direction of the
switches. Normally, the switches are installed correctly ex works, but it can happen that they are
rotated by 180 degrees. E.g. option "SA": 0 would correct the wrong mounting direction of switch
SA, while option "SB": 1 indicates that switch SB is mounted correctly. Such a switch correction
only refers to the display in the evaluation of jemoview. In fact, jemoview shows the switch-on
position for "Top" by means of an arrow ↑. However, if the switch is mounted in a rotated position,
"Top" is in the lower position, so that in this case the switch-on position would be better displayed
with arrow ↓. If no settings.txt file exists or its content is invalid, the standard options are used and a
message "File settings.txt not found" appears in the terminal window. If a settings.txt file exists, its
valid options are displayed in the terminal window. The settings file is in JSON format, so no
special characters such as "{}:," should be deleted or changed. An example of settings can be found
in the github folder.


Version history:

2020-06-11:  
initial version without GUI

2020-07-08:  
GUI added, German language only
    
2020-11-30:  
some new features of transmitter version 5.03, bugfixes
    
2021-01-16:  
English language added, bugfixes
    
2021-03-17:  
compatibility with transmitter version 5.03 improved, bugfixes

2021-03-23:  
crash barrier "zefix" introduced, bugfixes

2021-07-08:  
accelerometer evaluated, list of controls and switches added, bugfixes

2021-12-07:  
position of switches displayed, more details for digital trim, sensor ID displayed, 
settings.txt introduced, bugfixes

2022-01-05:  
numbering of functions corrected, 
points pairs of curves displayed below curves, bugfixes

2022-11-18:  
the first parameter of the Lua functions is displayed as well as all used controllers and switches, bugfixes

2023-01-31:  
more transmitter type codes added according to Jeti email

2023-08-09:  
transmitter type code of DC-24 V2 added from jsn example of a user

2023-08-27:  
a few extra columns appended to line 1 as a hint for Excel (had problems with LUA details)
