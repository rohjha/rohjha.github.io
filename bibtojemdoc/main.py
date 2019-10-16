"""
The bib file should follow the following format:
@papertype{paper_id,
  author = "author names here",
  title = "title here",
  note = "other fields entered similarly",
}

@papertype{paper_id_2,
  author = "author names here",
  title = "title here",
  note = "other fields entered similarly",
}

For each paper, a field and its value should be on a single line. Papers should be separated by a blank line.
"""

import argparse
import os

paper_types = ['inproceedings', 'unpublished', 'techreport']
my_fname = ''
my_lname = ''

# TODO: Maybe use regular expressions here.
def get_papers(lines):

  papers = []
  i = 0
  while i < len(lines):
    line = lines[i]
    if line.startswith('@'):
      paper_type, paper_id = line.split('{')
      paper_type, paper_id = paper_type[1:], paper_id[:-2]
      cur_paper = {'type' : paper_type, 'id' : paper_id}
    elif line.strip() == '}':
      papers.append(cur_paper)
      cur_paper = dict()
      i += 1
    else:
      line = line.strip()
      k, v = line.split(' = ')
      if v.endswith(','):
        v = v[:-1]
      v = v[1:-1]
      cur_paper[k] = v 
    i += 1

  return papers

def get_authors(authors):
  author_list_initial = authors.split(' and ')
  author_list = []
  for author in author_list_initial:
    if 'myname' in author:
      fname = '*Raunak'
      lname = 'Kumar*'
      if '*' in author:
        lname = lname[:-1] + "\\*" + '*'
    else:
      lname, fname = author.split(', ')
      if lname[-1] == '*':
        lname = lname[:-1] + "\\*"
    author_list.append('{} {}'.format(fname, lname))

    if len(author_list) == 1:
      author_list_str = author_list[0]
    elif len(author_list) == 2:
      author_list_str = '{} and {}'.format(author_list[0], author_list[1])
    else:
      author_list_str = ', '.join(author_list[:-1])
      author_list_str += ' and {}'.format(author_list[-1])

  return author_list_str

def format_paper(paper, documents_dir):
  res = ''

  authors = get_authors(paper['author'])
  title = paper['title']
  if 'note' in paper.keys():
    note = paper['note']
  if 'year' in paper.keys():
    year = paper['year']
  if 'booktitle' in paper.keys():
    booktitle = paper['booktitle']
  if 'institution' in paper.keys():
    institution = paper['institution']

  if paper['type'] == 'unpublished':
    title = '"{}"'.format(title)
    res += '{}. {}.'.format(authors, title)
    if 'note' in paper.keys():
      res += ' {}.'.format(note)
    if 'year' in paper.keys():
      res += ' {}.'.format(year)
  elif paper['type'] == 'inproceedings':
    title = '"{}"'.format(title)
    booktitle = '/{}/'.format(booktitle)
    res += '{}. {}. In: {}. {}.'.format(authors, title, booktitle, year)
    if 'note' in paper.keys():
      res += ' {}.'.format(note)
  elif paper['type'] == 'techreport':
    title = '/{}/'.format(title)
    res += '{}. {}. Tech. rep. {}. {}, {}.'.format(authors, title, note, institution, year)

  paper_id = paper['id']
  if os.path.isdir(os.path.join(documents_dir, 'papers')):
    for fname in os.listdir(os.path.join(documents_dir, 'papers')):
      if fname.startswith(paper_id):
        res += ' [documents/papers/{} \[pdf\]]'.format(fname)
    if os.path.isfile(os.path.join(documents_dir, 'arxivlinks.txt')):
      with open(os.path.join(documents_dir, 'arxivlinks.txt'), 'r') as f:
        for line in f.readlines():
          id_, link = line.split()
          if id_ == paper_id:
            res += ' [{} \[pdf\]]'.format(link)
            break
    if os.path.isfile(os.path.join(documents_dir, 'codelinks.txt')):
      with open(os.path.join(documents_dir, 'codelinks.txt'), 'r') as f:
        for line in f.readlines():
          id_, link = line.split()
          if id_ == paper_id:
            res += ' [{} \[code\]]'.format(link)
            break

  return res

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--bib', type=str, help='path to bib file.', default='publicationsbib.bib')
  parser.add_argument('--output', type=str, help='output file name', default='publications.jemdoc')
  parser.add_argument('--fname', type=str, help='first name', default='Raunak')
  parser.add_argument('--lname', type=str, help='last name', default='Kumar')
  parser.add_argument('--documents_dir', type=str, help='documents directory with papers and codelinks', default='/people/rk749/documents')
  args = parser.parse_args()

  my_fname, my_lname = args.fname, args.lname

  with open(args.bib, 'r') as f:
    lines = f.readlines()

  papers = get_papers(lines)
  formatted_papers = [format_paper(paper, args.documents_dir) for paper in papers]

  with open(args.output, 'w') as f:
    f.write('# jemdoc: menu{MENU}{./publications.html}, notime\n')
    f.write('==Publications\n')
    f.write('\n')
    for formatted_paper in formatted_papers:
      f.write('. ' + formatted_paper + '\n')

if __name__ == '__main__':
  main()
