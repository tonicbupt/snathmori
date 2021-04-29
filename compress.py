import os
import sys
import wave
import subprocess
import argparse


def compress(src, dst, size):
    f = wave.open(src)
    rate = f.getframerate()

    s = os.stat(src)
    if s.st_size < size:
        subprocess.check_call(['cp', '-f', src, dst])
        return

    target_rate = rate * size / s.st_size
    subprocess.check_call(['ffmpeg', '-y', '-i', src, '-ar', str(int(target_rate)), dst])


def compress_all(src, size):
    base = '{}.compressed'.format(src)
    os.makedirs(base, exist_ok=True)
    for root, dirs, files in os.walk(src):
        for d in dirs:
            os.makedirs(os.path.join(base, d), exist_ok=True)
        for f in files:
            path = os.path.join(root, f)
            target = os.path.join(root.replace(src, base), f)
            compress(path, target, size)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', dest='size', type=int, help='size after compressing')
    parser.add_argument('directory', help='directory, will compress all files within this directory recursively')
    args = parser.parse_args()

    compress_all(args.directory, args.size)


if __name__ == '__main__':
    main()
