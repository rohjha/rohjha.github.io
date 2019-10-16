@echo off
echo|set /p="Generating jemdoc... " 
format_bibtex.py jemdoc MHM research Mohammadi 1
echo DONE!
echo|set /p="Generating tex... " 
format_bibtex.py tex MHM research Mohammadi 0
echo DONE!
echo|set /p="Generating html... " 
format_bibtex.py html MHM research Mohammadi 1
echo DONE!
PAUSE