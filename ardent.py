
"""

simple and fast arduino programmer. python3 ard.py in your arduino project directory.
w

"""

import argparse
import sys
from subprocess import PIPE, Popen, STDOUT




def reset():
    return f" \u001b[0m"


def red(text: str):
    return f"""\u001b[31m{text}""" + reset()


def green(text: str):
    return f"""\u001b[32m{text}""" + reset()


def _cmd(cmd: str):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read().decode()
    if output is None:
        xerr = p.stderr.read().decode()
        print(xerr)
        return xerr
    print(output)
    return output


def _silent_cmd(cmd: str):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read().decode()
    if output is None:
        xerr = p.stderr.read().decode()
        return xerr
    return output

def arduino_compile(proj_dir, board):
    if not board or board is None:
        print(red('invalid empty board type passed'))
        return
    _silent_cmd(f'cd {proj_dir} && arduino-cli compile --fqbn {board}')
    return


def arduino_upload(proj_dir, port, board):
    if not port or port is None:
        print(red('empty port, must specify. i.e. `/dev/ttyACM1`'))
        return
    elif not board or board is None:
        print(red('must specify a board. i.e. `arduino:avr:mega`'))
        return
    _silent_cmd(f'cd {proj_dir} && arduino-cli upload -p {port} --fqbn {board}')
    return


class arduino_auto_programmer:
    def __init__(self, proj_dir='.'):
        self.project_dir = proj_dir
        self.port = ''
        self.board = ''

    def auto_find_board(self):
        res = _silent_cmd('arduino-cli board list')
        try:
            raw = res.split('\n')[1].split(' ')
            port = raw[0]
            board = raw[9]
            print(green(f'found board {board} on port {port}.'))
            self.port = port
            self.board = board
        except:
            print(red('no board found. Try plugging it in again'))
        return res

    def program_board(self):
        print('attempting to program arduino board...')
        print(f' {self.port}  ')
        if not self.board or not self.port:
            print(red('error: no board/port detected. run auto_find_board()'))
            return
        arduino_compile(self.project_dir, self.board)
        arduino_upload(self.project_dir, self.port, self.board)
        print()
        print(green('--- [ project uploaded ] ------------------------------------'))
        return


def auto_program_board(proj_dir='.'):
    prgm = arduino_auto_programmer()
    prgm.auto_find_board()
    prgm.program_board()
    return


if __name__ == '__main__':
    print('arduino fast programmer')
    print('v1.0')
    print()
    try:
        project_dir = sys.argv[1]
    except:
        print('using default arduino compile directory, ./ ')
        project_dir = '.'
    auto_program_board(proj_dir=project_dir)

