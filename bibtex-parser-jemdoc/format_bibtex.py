"""
#############################################################################
#                                FORMAT BIBTEX                              #
#############################################################################
Author:     Mohammad Hossain Mohammadi
Date:       November 2017
"""""

# Edited by Raunak Kumar.

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import os
import sys
#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

def format_bibtex(pub, format, main_author_fname, main_author_lname):
    """
    Format a publication dictionary in a required formatting style
    Args:       -pub is a publication data structure constaining Bibtex fields
                -format is a string for the format required, e.g. 'jemdoc', 'tex', 'html'
                -main_author_fname is a string of the main author's first name
                -main_author_lname is a string of the main author's last name
    Returns:    -ref is a string of the publication reference
                -entry_type is a string for the Bibtex publication entrytype
                -year is an integer for the publication year (useful for sorting)
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Initialization
    ref = ''
    entry_type = pub["ENTRYTYPE"]
    authors = ''
    title = ''
    journal = ''
    booktitle = ''
    publisher = ''
    school = ''
    address = ''
    volume = ''
    number = ''
    pages = ''
    month = ''
    year = ''
    doi = ''
    link = ''
    note = ''
    id_ = ''
    institution = ''
    year = '0'

    # Set Bibtex Values if Existing in Pub Dictionary
    if entry_type == 'article' or entry_type == 'inproceedings' or entry_type == 'incollection':
        if 'month' in pub:     # e.g. Jan. for January
            month = pub["month"][0:3] + '.'
    if 'doi' in pub:
        doi = pub["doi"]
    if 'address' in pub:
        address = pub["address"]
    if 'title' in pub:
        title = pub["title"]
    if 'publisher' in pub:
        publisher = pub["publisher"]
    if 'year' in pub:
        year = pub["year"]
    if 'volume' in pub:
        volume = pub["volume"]
    if 'pages' in pub:
        pages = pub["pages"]
    if 'number' in pub:
        number = pub["number"]
    if 'journal' in pub:
        journal = pub["journal"]
    if 'booktitle' in pub:
        booktitle = pub["booktitle"]
    if 'link' in pub:
        link = pub["link"]
    if 'school' in pub:
        school = pub["school"]
    if 'note' in pub:
        note = pub["note"]
    if 'ID' in pub:
        id_ = pub["ID"]
    if 'institution' in pub:
	institution = pub['institution']

    # Format Author Names based on Formatting Style
    authors_ = pub["author"].split(' and ')
    for iA, author_ in enumerate(authors_):
        if ',' in author_:  # Order: LastName, FirstName
            anames = author_.split(', ')
            fname = anames[1]           # First name string
            lname = anames[0]           # Last name string
        else:               # Order: FirstName LastName
            anames = author_.split(' ')
            lname = anames[-1]          # Last name string
            fname = anames[:-1]         # First name string
            fname = ' '.join(fname)

        if lname[-1] == '*':
            lname = lname[:-1] + "\\*"

        # Boldify main  author (depends on formatting style)
        author = fname + ' ' + lname
        if main_author_lname == lname or (main_author_lname == lname[:-2] and lname[-2:] == '\*'):
            last_name_match = True
        if main_author_fname == fname and last_name_match:
            if format == 'jemdoc':
                author = '*' + author + '*'
            elif format == 'tex':
                author = '\\textbf{' + author + '}'
            elif format == 'html':
                author = '<strong>' + author + '</strong>'

        # Combine author list into 1 string
        authors += author
        if iA<(len(authors_)-2):
            authors += ', '     # Separation b/w author full names
        elif iA==(len(authors_)-2):
            authors += ' and '  # Separation for last author

    # Format Other Bibtex Fields based on Formatting Style
    if format == 'jemdoc':
	if entry_type == 'techreport':
		title = '/' + title + '/'
        journal = '/' + journal + '/'
        booktitle = '/' + booktitle + '/'
        doi = '[https://doi.org/' + doi + ' ' + doi + ']'
        link = '[' + link + ' link]'
    elif format == 'tex':
        title = '\\textit{' + title + '}'
        journal = '\\textit{' + journal + '}'
        booktitle = '\\textit{' + booktitle + '}'
        note = '\\textit{' + note + '}'
        doi = '\\href{https://doi.org/' + doi + '}{\\underline{' + doi + '}}'
        link = '\\href{' + link + '}{\\underline{link}}'
    elif format == 'html':
        title = '<em>' + title + '</em>'
        journal = '<em>' + journal + '</em>'
        booktitle = '<em>' + booktitle + '</em>'
        note = '<em>' + note + '</em>'
        doi = '<a href="https://doi.org/' + doi + '">' + doi + '</a>'
        link = '<a href="' + link + '">link</a>'

    # Create Reference based on Formatting Style
    if entry_type == 'book':
        ref = authors + '. ' + title + '. ' + address + ': ' + publisher + ', ' + year + '.'
    elif entry_type == 'article':
        ref = authors + ', "' + title + '," ' + journal + ', pp. ' + pages + ', vol. ' + volume + ', no. ' + number + ', ' + month + ' ' + year + ', doi: ' + doi + '.'
    elif entry_type == 'inproceedings' or entry_type == 'incollection':
	ref = authors + '. "' + title + '". ' + 'In: ' + booktitle + '. ' + year + '.'
        # ref = authors + ', "' + title + '," in ' + booktitle + ', ' + address + ', ' + month + ' ' + year + ', doi: ' + doi + '.'
    elif entry_type == 'mastersthesis':
        ref = authors + '. "' + title + '." Master\'s Thesis, ' + school + ', ' + address + ', ' + year + ', ' + link + '.'
    elif entry_type == 'phdthesis':
        ref = authors + '. "' + title + '." PhD Thesis, ' + school + ', ' + address + ', ' + year + ', ' + link + '.'
    elif entry_type == 'unpublished':
        ref = authors + '. "' + title + '". ' + note + '. ' + year
    elif entry_type == 'techreport':
	ref = authors + '. ' + title + '. ' + 'Tech. rep. ' + note + '. ' + year + '.'

    return ref, entry_type, int(year), id_


def create_research_file(db, format, outname, main_author_fname, main_author_lname, documents_dir):
    """
    Creates a file of research publications
    Args:       -db is the publication data structure containing Bibtex fields
                -format is a string for the format required, e.g. 'jemodoc', 'tex', 'html'
                -outname is a string for the output file name, e.g. 'research'
                -main_author_fname is the main author's first name string
                -main_author_lname is the main author's last name string
                -documents_dir is a path to the documents directory
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Sorting Key
    def access_year(elem):
        return elem[2]

    # Initialization
    books = []
    journals = []
    conferences = []
    theses = []
    workshop_and_tech_reports = []
    paper_links, code_links = dict(), dict()

    # Create Separate Lists for Publication Type
    for pub in db.entries:
        # Format publication dictionary using a formatting style
        ref, entry_type, year, id_ = format_bibtex(pub, format, main_author_fname, main_author_lname)

        # Append publication reference into lists
        if entry_type == 'book':
            books.append([ref, entry_type, year, id_])
        elif entry_type == 'article':
            journals.append([ref, entry_type, year, id_])
        elif entry_type == 'inproceedings' or entry_type == 'incollection':
            conferences.append([ref, entry_type, year, id_])
        elif entry_type == 'mastersthesis' or entry_type == 'phdthesis':
            theses.append([ref, entry_type, year, id_])
        elif entry_type == 'techreport':
            workshop_and_tech_reports.append([ref, entry_type, year, id_])

    for file in os.listdir(os.path.join(documents_dir, 'papers')):
        if file.endswith('.pdf'):
            paper_links[file[:-4]] = os.path.join(documents_dir, 'papers', file)

    with open(os.path.join(documents_dir, 'codelinks.txt')) as f:
        for line in f.readlines():
            code_links[line[0]] = line[1]

    def write_paper_code_links(id_, the_file):
        paper_and_code = ''
        if id_ in paper_links.keys():
    	    paper_and_code = '  [{} (pdf)]'.format(paper_links[id_])
        if id_ in code_links.keys():
    	    paper_and_code += ' [{} (code)]'.format(code_links[id_])
        if len(paper_and_code) > 0:
    	    the_file.write(paper_and_code + '\n')

    # Create Sorted Research File
    outfile = outname + '.' + format
    with open(outfile, 'w') as the_file:
        if format == 'jemdoc':
            the_file.write('# jemdoc: menu{MENU}{'+ outname + '.html}, notime\n')
            the_file.write('==Research Publications\n\n')

            if workshop_and_tech_reports:
                workshop_and_tech_reports.sort(reverse=True, key=access_year)
                the_file.write('== Workshop Papers and Technical Reports\n')
                for paper in workshop_and_tech_reports:
                    the_file.write('. ' + paper[0] + '\n')
                    write_paper_code_links(paper[3], the_file)
                the_file.write('\n')

            if books:
                books.sort(reverse=True, key=access_year)
                the_file.write('== Books\n')
                for book in books:
                    the_file.write('. ' + book[0] + '\n')
                    write_paper_code_links(book[3], the_file)
                the_file.write('\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('== Journals\n')
                for journal in journals:
                    the_file.write('. ' + journal[0] + '\n')
                    write_paper_code_links(journal[3], the_file)
                the_file.write('\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('== Conferences\n')
                for conference in conferences:
                    the_file.write('. ' + conference[0] + '\n')
                    write_paper_code_links(conference[3], the_file)
                the_file.write('\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('== Theses\n')
                for thesis in theses:
                    the_file.write('. ' + thesis[0] + '\n')
                    write_paper_code_links(thesis[3], the_file)
                the_file.write('\n')

        elif format == 'tex':
            if books:
                books.sort(reverse=True, key=access_year)
                the_file.write('\\section{BOOKS}\n\n')
                for book in books:
                    the_file.write(book[0] + '\n\n')
                the_file.write('\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('\\section{JOURNALS}\n\n')
                for journal in journals:
                    the_file.write(journal[0] + '\n\n')
                the_file.write('\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('\\section{CONFERENCES}\n\n')
                for conference in conferences:
                    the_file.write(conference[0] + '\n\n')
                the_file.write('\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('\\section{THESES}\n\n')
                for thesis in theses:
                    the_file.write(thesis[0] + '\n\n')
                the_file.write('\n')

        elif format == 'html':
            the_file.write('<!-- Question -->\n')
            the_file.write('<div class="panel panel-default">\n')
            the_file.write('\t<div class="panel-heading">\n')
            the_file.write('\t<h4 class="panel-title">\n')
            the_file.write('\t<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion1" href="#collapse' + bibname + '">\n')
            the_file.write('\t' + bibname + ' Calendar Year\n')
            the_file.write('\t</a>\n')
            the_file.write('\t</h4>\n')
            the_file.write('\t</div>\n')
            the_file.write('\t<!-- Answer -->\n')
            the_file.write('\t<div id="collapse' + bibname + '" class="panel-collapse collapse">\n')
            the_file.write('\t\t<div class="panel-body">\n')

            if books:
                books.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Book publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for book in books:
                    the_file.write('\t\t\t<li>' + book[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Journal publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for journal in journals:
                    the_file.write('\t\t\t<li>' + journal[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Conference publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for conference in conferences:
                    the_file.write('\t\t\t<li>' + conference[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Thesis publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for thesis in theses:
                    the_file.write('\t\t\t<li>' + thesis[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            the_file.write('\t\t</div>\n')
            the_file.write('\t</div>\n')
            the_file.write('</div>\n')


def main(format, bibname, outname, main_author_fname, main_author_lname, documents_dir):
    """
    Format publication references in a formatting style
    Args:       -format is a string for the format required, e.g. jemodoc, tex, html
                -bibname is the Bibtex file name without any extension, e.g. MHM
                -outname is a string for the output file name, e.g. research
                -main_author_fname is a string of the main author's first name used for bolding 
                -main_author_lname is a string of the main author's last name used for bolding
                -documents_dir is the path to the documents directory
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Load Bibtex File
    with open(bibname + ".bib") as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        db = bibtexparser.load(bibtex_file, parser=parser)

    # Creates a Research File of Publication References
    create_research_file(db, format, outname, main_author_fname, main_author_lname, documents_dir)


# Handle Arguments & Call Main Function
if __name__ == '__main__':
    format = str(sys.argv[1])
    bibname = str(sys.argv[2])
    outname = str(sys.argv[3])
    main_author_fname = str(sys.argv[4])
    main_author_lname = str(sys.argv[5])
    documents_dir = str(sys.argv[6])

    sys.exit(main(format, bibname, outname, main_author_fname, main_author_lname, documents_dir))
