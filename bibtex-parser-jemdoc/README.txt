Title:		Bibtex Parser & Publication Formatter
Filename:	format_bibtex.py
Formats:	Jemdoc, LaTex, HTML
Author:		Mohammad Hossain Mohammadi
Date:		November 2017
Version:	1.0.0

This Python script generates publication references using a Bibtex file.
You can modify it to add more formatting styles. 

Inputs:		-format is a string for the format required, e.g. jemodoc, tex, html
			-bibname is the Bibtex file name without any extension, e.g. MHM
			-outname is a string for the output file name, e.g. research
			-main_author is a string of the main author's last name used for bolding, e.g. Mohammadi or ""
			-initials is an integer which controls whether the first names are shown as initials, e.g. 1 or 0
Output:		-research file of publications in a specified formatting style

Steps for Generating Files
1. Extract all these files into a suitable directory.
2. Ensure that you have downloaded a Python intepreter from https://www.python.org (e.g. version 2.7).
3. Copy & paste a Bibtex file containing research publicaitons into this directory, e.g. MHM.bib.
4. Open RUNME.bat (Windows) or RUNME.sh (Linux).
5. Change the following arguments for your case:
		Format, e.g. jemdoc, tex, html
		Input Bibtex file name, e.g. MHM
		Output research file name, e.g. research
		Main author name to boldify, e.g. Mohammadi. Set as "" if you do not wish to boldify it
		Flag for displaying initials for the first names, e.g. 1 or 0
5. Double-click RUNME.bat (Windows) or RUNME.sh (Linux) to create the following:
		Jemdoc file, e.g. "research.jemdoc"
		LaTex file, e.g. "research.tex"
		HTML file, e.g. "research.html"