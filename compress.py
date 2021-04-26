import os
import sys
import wave
import subprocess


_target_size = 497 * 1000


def compress(filename):
    f = wave.open(filename)
    rate = f.getframerate()

    s = os.stat(filename)
    if s.st_size < _target_size:
        return

    target_rate = rate * _target_size / s.st_size
    subprocess.check_output(['ffmpeg', '-i', filename, '-ar', str(int(target_rate)), 'compressed/{}'.format(filename)])


if __name__ == '__main__':
    compress(sys.argv[-1])
