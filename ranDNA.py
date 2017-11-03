#! /usr/bin/env python3
from random import choice
from common import roll

# parse user arguments
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-k', '--length', required=True, type=int, help="Sequence Length")
parser.add_argument('-n', '--num', required=False, type=int, default=1, help="Number of Sequences")
parser.add_argument('-pa', '--probA', required=False, type=float, default=None, help="Probability of A")
parser.add_argument('-pc', '--probC', required=False, type=float, default=None, help="Probability of C")
parser.add_argument('-pg', '--probG', required=False, type=float, default=None, help="Probability of G")
args = parser.parse_args()
assert args.length > 0, "Sequence length must be a positive integer"
assert args.num > 0, "Number of sequences must be a positive integer"
probs = None
if args.probA is not None or args.probC is not None or args.probG is not None:
    assert args.probA is not None and args.probC is not None and args.probG is not None, "If you specify probA, probC, or probG, you must specify all 3 (probT = 1 - probA - probC - probG)"
    assert args.probA >= 0 and args.probC >= 0 and args.probG >= 0, "Probabilities cannot be negative"
    probACG = sum((args.probA,args.probC,args.probG))
    assert probACG <= 1, "The total probability must be less than or equal to 1"
    probs = {'A':args.probA, 'C':args.probC, 'G':args.probG, 'T':(1-probACG)}

# generate sequences
for SEQ in range(args.num):
    if probs is None:
        l = [choice('ACGT') for _ in range(args.length)]
    else:
        l = [roll(probs) for _ in range(args.length)]
    print(''.join(l))
