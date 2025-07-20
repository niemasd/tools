#! /usr/bin/env python3
'''
Use ffmpeg to split chapters of a given file
'''

# imports
from os import getcwd
from os.path import abspath, expanduser, isdir, isfile
from subprocess import run
import argparse

# constants
EXTS = {'avi', 'mkv', 'mov', 'mp4', 'wmv'}

# parse user args
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=str, help="Input File")
    parser.add_argument('-o', '--output_directory', required=False, type=str, default=getcwd(), help="Output Directory")
    parser.add_argument('-p', '--prefix', required=False, type=str, default='', help="Output Prefix")
    parser.add_argument('-cv', '--copy_video_codec', action='store_true', help="Copy Video Codec")
    parser.add_argument('-ca', '--copy_audio_codec', action='store_true', help="Copy Audio Codec")
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress Log Messages")
    parser.add_argument('--preseek', required=False, type=float, default=30, help="Preseek Seconds (larger = slower but more accurate at beginning of output)")
    parser.add_argument('--dry_run', action='store_true', help="Dry Run (just print ffmpeg commands)")
    args = parser.parse_args()

    # check args before returning
    if not isfile(args.input):
        raise ValueError("File not found: %s" % args.input)
    if not isdir(args.output_directory):
        raise ValueError("Directory not found: %s" % args.output_directory)
    if args.input.split('.')[-1].strip().lower() not in EXTS:
        raise ValueError("Unsupported file extension: %s" % args.input)
    args.input = abspath(expanduser(args.input))
    args.output_directory = abspath(expanduser(args.output_directory))
    return args

# main execution
if __name__ == "__main__":
    args = parse_args()
    input_ext = args.input.split('.')[-1].strip()
    get_chapters_command = ['ffmpeg', '-i', args.input]
    get_chapters_lines = run(get_chapters_command, capture_output=True).stderr.decode().split('  Chapters:')[1].splitlines()
    chapter_times = [[float(t) for t in l.strip().split('start ')[1].split(', end ')] for l in get_chapters_lines if l.startswith('    Chapter #')]
    for curr_ind, curr_times in enumerate(chapter_times):
        start_time, end_time = curr_times; duration = end_time - start_time
        if start_time <= args.preseek:
            preseek_start = None; postseek_start = start_time
        else:
            preseek_start = start_time - args.preseek; postseek_start = args.preseek
        curr_fn = '%s/%s%s.%s' % (args.output_directory, args.prefix, str(curr_ind+1).zfill(len(str(len(chapter_times)))), input_ext)
        curr_command = ['ffmpeg']
        if preseek_start is not None:
            curr_command += ['-ss', str(preseek_start)]
        curr_comand += ['-i', args.input, '-ss', str(postseek_start), '-t', str(duration)]
        if args.copy_video_codec:
            curr_command += ['-c:v', 'copy']
        if args.copy_audio_codec:
            curr_command += ['-c:a', 'copy']
        curr_command += [curr_fn]
        if not args.quiet:
            print(' '.join(curr_command))
        if not args.dry_run:
            run(curr_command, capture_output=args.quiet)
