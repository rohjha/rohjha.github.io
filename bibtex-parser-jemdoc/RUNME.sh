#!/bin/bash 
echo "Generating jemdoc... " 
python format_bibtex.py jemdoc MHM research Mohammadi 1
echo "DONE!\n"
echo " Generating latex... "
python format_bibtex.py tex MHM research Mohammadi 0
echo "DONE!\n"
echo " Generating html... "
python format_bibtex.py html MHM research Mohammadi 1
echo "DONE!\n"