from pathlib import Path
from utils import *

def parse_lines_to_pieces(lines):
    def is_start_line(line): return line.startswith('M:')
    def is_line_in_piece(line): return not is_start_line(line)
    # def proc_line(line): return line.split(' '*3)[0]
    pieces = []
    piece = []
    in_piece = False
    for line in lines:
        if not in_piece:  # search for a start line
            if is_start_line(line):
                in_piece = True
                piece.append(line)
        else:  # check if the current line is in piece
            # NOTE: the last piece is not the last line, so
            # it should already be appended
            if is_line_in_piece(line):
                piece.append(line)
            else:
                pieces.append(piece)
                piece = [line]
                in_piece = True
    if len(piece) > 2:
        pieces.append(piece)
    return pieces


def save_pieces(pieces, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, piece in enumerate(pieces):
        out_fp = out_dir / f'{i}.abc'
        write_text(piece, out_fp)


if __name__ == '__main__':
    data_dir = Path('../session_book_txt_fix')
    out_dir = Path('../session_book_abc')
    out_dir.mkdir(parents=True, exist_ok=True)

    vol_fps = list(data_dir.glob('*.txt'))
    for vol_fp in vol_fps:
        _out_dir = out_dir / Path(vol_fp).stem
        _out_dir.mkdir(parents=True, exist_ok=True)
        lines = read_text(vol_fp)
        pieces = parse_lines_to_pieces(lines)
        save_pieces(pieces, _out_dir)

