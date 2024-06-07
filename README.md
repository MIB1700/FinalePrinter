# FinalePrinter

Module providing a function for printing finale music files to pdf via a virtual pdf printer
PDFWriter - in this case -  on OSX!! This will ONLY WORK ON OSX!! Uses apple script to fascilitate the printing!

This will search through all folders and files for finale files, starting at the designated path. All



## You need:
    a copy of the Finale MusicMaker app (https://www.finalemusic.com)
    installed PDFWriter (https://github.com/rodyager/RWTS-PDFwriter)

## HOW TO:
    1. **cd** into the directory where you want to start the search for finale files
        the script will search all files and folder starting from this location
        the script will only process *.mus, .MUS, .bak, and .BAK files*
        the script will only try to create  .pdf file if no pdf file with the same name as the finale file exists

        optionally, you can provide a path form where to search for finale files (you can also just drop the folder from
        the finder onto the terminal once it asks for a path)

    2. make sure that your default printer is the virtual printer (PDFWriter!!)

    3. run ptyhon ./path/to/script/FinalePrinter.py

    4. wait a while
        depending how old your finale files are finale might ask you how to handle certain things (e.g. smart phrasings, etc.)
        once all that has been set, it should be automatic

        the pdf files will be saved where the original file is located!!
        the original file will be left in place

## Caveats:
    this script opens - and keeps open - all finale files
        this could mean that there might be memory issues if you have an ungodly amount of files
        in that case quit, and restart the script and finale... since only files that don't have pdfs already will be converted we don't
        start over

        this is done because in my case I had old finale files in .mus instead of the new .musx format. Finale was asking to save each file
        when I tried to close them. If you have .musx files you can try and re-enable the closing of the file after each print:

        remove the # from:
        # close front document

        **on line 85**

    the script assumes a default location for the PDFWriter output as "~/Documents/PDFwriter/"

    script does not check if finale is open! it will fale if it is not running!
