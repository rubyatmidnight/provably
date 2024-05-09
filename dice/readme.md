# Dice

Dice works great, just run, from the command line from that folder (right click -> open in terminal)
`py dice.py`
And it will ask for unhashed server seed, hashed server seed, client seed, and desired number of rolls. 

It will then output all the rolls to a csv file, and will create new files separately if run multiple times (rolls.csv, rolls_new.csv, rolls_new2.csv or something).
It will also include the used seeds within the sheet for reference.


If you have excel, I have also included dice.xlsm (xlsm is the excel macro format, as I have clear ranges macros. It will not start with macros enabled for security reasons).

It is an incredibly inefficient, unoptimized sheet, and can only handle 50k~100k rolls before getting very slow, but it works nicely for at a glance analysis. It's a lot more robust than my limbo sheet, and I put more work into it. It is a little schizo though.

