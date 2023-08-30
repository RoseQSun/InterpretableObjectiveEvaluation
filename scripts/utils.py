def read_text(fp):
    lines = []
    with open(fp) as f:
        lines = f.readlines()
    lines = [l.replace('\n', '') for l in lines]
    return lines


def write_text(lines, out_fp):
    with open(out_fp, 'w') as f:
        f.writelines([l + '\n' for l in lines])
