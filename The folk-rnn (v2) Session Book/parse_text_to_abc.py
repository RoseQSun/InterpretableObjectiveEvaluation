from pathlib import Path


def read_text(fp):
    lines = []
    with open(fp) as f:
        lines = f.readlines()
    return lines


def preproc_lines(lines):
    def remove_linebreaks(lines):
        return [l[:-1] for l in lines]
    def remove_empty_lines(lines):
        return [l for l in lines if l]
    def replace_quote(lines):
        return [l.replace("’", "'") for l in lines if l]
    return replace_quote(remove_empty_lines(remove_linebreaks(lines)))


def parse_lines_to_pieces(lines):
    def is_start_line(line): return line.startswith('M:')
    def is_line_in_piece(line): return '|' in line or ':' in line
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
                piece = []
                in_piece = False
    return pieces


def save_piece(lines, out_fp):
    with open(out_fp, 'w') as f:
        f.writelines([l + '\n' for l in lines])


def save_pieces(pieces, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, piece in enumerate(pieces):
        out_fp = out_dir / f'{i}.abc'
        save_piece(piece, out_fp)


if __name__ == '__main__':

    data_dir = Path('data')
    out_dir = Path('abc')
    out_dir.mkdir(parents=True, exist_ok=True)

    vol_fps = data_dir.glob('*.txt')
    for vol_fp in vol_fps:
        _out_dir = out_dir / Path(vol_fp).stem
        _out_dir.mkdir(parents=True, exist_ok=True)
        lines = preproc_lines(read_text(vol_fp))
        pieces = parse_lines_to_pieces(lines)
        save_pieces(pieces, _out_dir)

