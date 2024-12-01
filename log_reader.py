from pathlib import Path


SEEK = Path(__file__).parent / "data"/ "seek"


def get_last_position():
    if SEEK.exists():
        with open(SEEK, 'r') as pos_file:
            position = int(pos_file.read())
            return position
    return 0


def save_position(position):
    with open(SEEK, 'w') as pos_file:
        pos_file.write(str(position))


def read_log(f_log: str, read_all: bool):
    position = get_last_position()
    if read_all:
        position = 0

    lines: list[str] = []
    with open(f_log, 'r') as log_file:
        log_file.seek(position)

        # 逐行读取文件
        for line in log_file:
            lines.append(line.strip())  # 这里处理日志内容
        save_position(log_file.tell())

    return lines
