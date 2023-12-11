import argparse
import bibtexparser
from bibtexparser import Library
from pathlib import Path
import re

def main(args):
    library = bibtexparser.parse_file(Path(args.input_bib))

    #extract all the citation used in the tex file
    citation_keys = []
    cite_commands = ['cite', 'citet', 'citep', 'citet*', 'citep*', 'citeauthor', 'citeyear']
    
    with open(Path(args.tex_file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            for c in cite_commands:
                pattern = r'\\' + c + r'\{(.*?)\}'
                matches = re.findall(pattern, line)
                sub_list = []
                for m in matches:
                    l = m.split(',')
                    l = [x.strip() for x in l]
                    sub_list.extend(l)
                citation_keys.extend(sub_list)

    #write cleaned bib file
    citation_keys = set(citation_keys)
    new_lib = Library()
    entry_dict = library.entries_dict
    for key in citation_keys:
        new_lib.add(entry_dict[key])

    bibtexparser.write_file(args.output_bib, new_lib)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Bib file clean')
    parser.add_argument('--input_bib', type=str, default = 'references.bib', help = 'The large bib file to be cleaned')
    parser.add_argument('--tex_file', type=str, default = 'main.tex', help = 'The tex file')
    parser.add_argument('--output_bib', type=str, default = 'cleaned_bib.bib', help = 'The output cleaned bib file name')
    #parser.add_argument('--cite_command', type=str, default = 'cite', help = 'The citation command used in your tex file')

    args = parser.parse_args()
    main(args)
      