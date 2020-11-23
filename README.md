# jemoview
Jeti Model Viewer

Jeti RC transmitters store the model programs in folder _Model_ on the SD memory card. 
The name of each model file consists of a 4-digit number (corresponding to the order of the models in the
transmitter) followed by an alphanumeric text of maximum 4 characters (corresponding to the first 4
places of the model name) plus the extension jsn (for example 0007Pipe.jsn).
The ending jsn stands for JSON, which is a text format formed by pairs of keys and values. As a rule the content of such jsn files is a single long line, and therefore difficult to understand when opened with a usual text editor.

The program jemoview reads such model files, extracts the essential data and writes
the result as table into a new csv file, for example 0007Pipe.csv. The extension csv stands for "comma
separated values", i.e. the values in each line are separated by separators, where jemoview
uses the semicolon ; as its standard separator. The advantage of the csv format is that 
usual table programs such as _Excel_ (by MS) or _Calc_ (by Libre Office) will display the data as table
and on the other hand its data can be processed as text with usual search or comparison programs.
