import sys

import tqdm

from log_reader import read_log
from log_process import process_log_row


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recorder.py <log_file> [all]")
        sys.exit(1)
    db = sys.argv[1]
    read_all = False
    if len(sys.argv) > 2 and sys.argv[2] == "all":
        read_all = True

    for _row in tqdm.tqdm(read_log(db, read_all)):
        process_log_row(_row)
