"""
Parse PDF files containing ABC scores
"""

import subprocess
from pathlib import Path

from utils import *


def parse_pdf(pdf_path, out_path):
    subprocess.check_call([
        'pdftotext', '-layout',
        str(pdf_path), str(out_path)
    ])


def parse_pdf_in_dir(dirpath, outdir):
    pdf_filepaths = Path(dirpath).glob('*.pdf')
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for pdf_filepath in pdf_filepaths:
        out_filepath = outdir / Path(pdf_filepath).with_suffix('.txt').name
        parse_pdf(pdf_filepath, out_filepath)


def fix_text(txt_path, out_fp):
    def remove_empty_lines(lines):
        return [l for l in lines if l]
    def replace_quote(lines):
        return [l.replace("’", "'") for l in lines if l]
    def is_line_in_piece(line): return '|' in line or ':' in line
    def remove_non_ascii(lines):
        lines = [l.replace("", "") for l in lines]
        lines = [l.replace("\n", "") for l in lines]
        lines = [l.replace("\r", "") for l in lines]
        lines = [l if is_line_in_piece(l) else "" for l in lines]
        return lines
    def remove_trailing_numbers(lines):
        return [l.split('   ')[0] for l in lines]
    
    lines = read_text(txt_path)
    lines = remove_non_ascii(lines)
    lines = replace_quote(lines)
    lines = remove_empty_lines(lines)
    lines = remove_trailing_numbers(lines)
    write_text(lines, out_fp)


def fix_txt_in_dir(dirpath, outdir):
    txt_filepaths = Path(dirpath).glob('*.txt')
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for txt_filepath in txt_filepaths:
        out_filepath = outdir / Path(txt_filepath).name
        fix_text(txt_filepath, out_filepath)


if __name__ == '__main__':
    parse_pdf_in_dir('../session_book_pdf', '../session_book_txt')
    fix_txt_in_dir('../session_book_txt', '../session_book_txt_fix')