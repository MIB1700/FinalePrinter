"""Module providing a function for printing finale music files to pdf via a virtual pdf printer
PDFWriter - in this case -  on OSX!! This will ONLY WORK ON OSX!! Uses apple script to fascilitate the printing!

You need:
    a copy of the Finale MusicMaker app
    installed PDFWriter

HOW TO:
    1) cd into the directory where you want to start the search for finale files
        the script will search all files and folder starting from this location
        the script will only process .mus, .MUS, .bak, and .BAK files
        the script will only try to create  .pdf file if no pdf file with the same name as the finale file exists

        optionally, you can provide a path form where to search for finale files... (you can also just drop the folder from
        the finder onto the terminal once it asks for a path...)

    2) make sure that your default printer is the virtual printer (PDFWriter!!)

    3) run ptyhon ./path/to/script/FinalePrinter.py

    4) wait a while...
        depending how old your finale files are finale might ask you how to handle certain things... (e.g. smart phrasings, etc.)
        once all that has been set, it should be automatic

        the pdf files will be saved where the original file is located!!
        the original file will be left in place

Caveats:
    this script opens - and keeps open - all finale files
        this could mean that there might be memory issues if you have an ungodly amount of files...
        in that case quit, and restart the script and finale... since only files that don't have pdfs already will be converted we don't
        start over

        this is done because in my case I had old finale files in .mus instead of the new .musx format. Finale was asking to save each file
        when I tried to close them. If you have .musx files you can try and re-enable the closing of the file after each print:

        remove the # from:
        # close front document

        on line 85

    the script assumes a default location for the PDFWriter output as "~/Documents/PDFwriter/"

"""

import os
import subprocess
import sys
from pathlib import Path
import re


def find_mus_files(root_folder):
    """
    Recursively find all .mus files in the given root folder.
    """
    # return [str(p) for p in Path(root_folder).rglob("*.mus")]
    # mus_files = [str(p) for p in Path(root_folder).rglob("*.[mM][uU][sS](?:[xX])?")]

    # Compile a regular expression pattern for case-insensitive matching of file extensions
    pattern = re.compile(r"\.musx?$", re.IGNORECASE)

    # Find all files matching the pattern
    mus_files = [str(p) for p in Path(root_folder).rglob("*") if pattern.search(p.name)]
    bak_files = [str(p) for p in Path(root_folder).rglob("*.[bB][aA][kK]")]

    return mus_files + bak_files


def print_to_pdf(file_path):
    """
    Use AppleScript to open the .mus file in Finale, print it to PDF using PDFWriter,
    and then close the file.
    """
    # Extract the directory and base name of the .mus file
    file_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    pdf_path = os.path.join(file_dir, f"{base_name}.pdf")

    script = f"""
    tell application "Finale"
        open POSIX file "{file_path}"
        -- Print to PDF with the specified output file path
        print front document with properties {{target printer:"PDFWriter"}}
        # close front document
    end tell
    """

    # Execute the AppleScript
    process = subprocess.run(
        ["osascript", "-e", script], capture_output=True, text=True, check=False
    )

    # Move the generated PDF to the desired location
    generated_pdf_dir = os.path.expanduser("~/Documents/PDFwriter/")
    generated_pdf_files = [
        f for f in os.listdir(generated_pdf_dir) if f.startswith("Untitled")
    ]
    generated_full_path = os.path.join(generated_pdf_dir, generated_pdf_files[0])

    print(f"file: {generated_full_path}")

    if process.returncode == 0:
        try:
            if os.path.exists(generated_full_path):
                os.rename(generated_full_path, pdf_path)
                print(f"Successfully saved {pdf_path}")
            else:
                raise Exception(f"Expected PDF not found at {generated_pdf_files[0]}")
        except Exception as e:
            raise Exception(f"Error saving PDF {pdf_path}: {str(e)}")
    else:
        raise Exception(f"Error printing {file_path}: {process.stderr}")


def main(root_folder):
    """
    Main function to find and print all .mus files in the root folder.
    """
    all_files = find_mus_files(root_folder)
    num_files = len(all_files)
    print(f"\n\nFound {num_files} files.\n\n")

    if num_files > 0:
        continue_search = input("Do you want to continue? (y/n): ").strip().lower()
        if continue_search == "y":
            print("\n\nContinuing...\n\n")
            # Process the files further or perform other actions
        else:
            print("\n\nExiting...\n\n Have a nice day!")
            sys.exit(1)
    else:
        print("No files found.")

    for file_path in all_files:
        # Construct the corresponding PDF file path
        file_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        pdf_path = os.path.join(file_dir, f"{base_name}.pdf")

        # Check if the PDF already exists
        if os.path.exists(pdf_path):
            print(f"PDF already exists for {file_path}, skipping...")
            continue

        try:
            print(f"Processing {file_path}")
            print_to_pdf(file_path)

            num_files -= 1
            print(f"\n...{(num_files)} left\n")
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")


if __name__ == "__main__":
    # Initialize the root_folder variable
    root_folder = ""

    # Ask the user if they want to start in the current directory
    start_search = (
        input("Do you want to start in this directory? (y/n): ").strip().lower()
    )

    if start_search == "y":
        # If the user chooses to start in the current directory, set root_folder to the current working directory
        print("\n\nContinuing in the current directory...\n\n")
        root_folder = os.getcwd()
    else:
        # If the user chooses to specify a different directory, prompt for input
        root_folder = input("Enter the root folder to start from: ").strip()

    # Convert the root_folder to a Path object
    root_folder = Path(root_folder)

    print(f"\n\nroot folder: {root_folder}\n\n")

    # Call the main function with the specified root_folder
    main(root_folder)
