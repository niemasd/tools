'''
Common functions used by multiple tools
Niema Moshiri 2017
'''
from math import log
from random import choice,uniform

# constants
DNA = {'-','?','A','C','B','D','G','H','K','M','N','S','R','T','W','V','Y','X','a','c','b','d','g','h','k','m','n','s','r','t','w','v','y'}
RNA = {'-','?','A','C','B','D','G','H','K','M','N','S','R','U','W','V','Y','X','a','c','b','d','g','h','k','m','n','s','r','u','w','v','y'}
AMINO = {'-','?','A','C','B','E','D','G','F','I','H','K','M','L','N','Q','P','S','R','T','W','V','Y','X','Z','a','c','b','e','d','g','f','i','h','k','m','l','n','q','p','s','r','t','w','v','y','x','z'}

# remove gaps from FASTA
def remove_gaps(stream):
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            print(l)
        else:
            print(l.replace('-',''))

# convert FASTA to upper case
def convert_fasta_upper(stream):
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            print(l)
        else:
            print(l.upper())

# convert multiline FASTA to one-line
def convert_fasta_1ln(stream):
    seq = ''
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            if len(seq) != 0:
                print(seq)
            print(l)
            seq = ''
        else:
            seq += l.strip().replace(' ','')
    if len(seq) != 0:
        print(seq)

# compute the hamming distance of a pair of sequences
def hamming(x,y,prop=True):
    assert len(x) == len(y), "x and y must be the same length"
    d = 0; l = len(x)
    for i in range(len(x)):
        if x[i] == '-' and y[i] == '-':
            l -= 1
        elif x[i] != y[i]:
            d += 1
    if prop:
        return d/float(l)
    else:
        return d

# compute the JC69 distance of a pair of sequences
def jc69(x,y,a):
    assert len(x) == len(y), "x and y must be the same length"
    assert a > 0, "Gamma alpha parameter must be positive"
    d = hamming(x,y,prop=True)
    if a == float('inf'):
        return -3*log(1-(4*d/3))/4
    else:
        return (3*a/4.)*(((1-(4*d/3.))**(-1./a))-1)

# read FASTA stream and return (ID,seq) dictionary
def readFASTA(stream):
    seqs = {}
    name = None
    seq = ''
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            if name is not None:
                assert len(seq) != 0, "Malformed FASTA"
                seqs[name] = seq
            name = l[1:]
            assert name not in seqs, "Duplicate sequence ID: %s" % name
            seq = ''
        else:
            seq += l
    assert name is not None and len(seq) != 0, "Malformed FASTA"
    seqs[name] = seq
    return seqs

# roll a weighted die (keys = faces, values = probabilities)
def roll(die):
    faces = sorted(die.keys())
    probs = [die[key] for key in faces]
    cdf = [probs[0]]
    while len(cdf) < len(probs):
        cdf.append(cdf[-1] + probs[len(cdf)])
    num = uniform(0, 1)
    index = 0
    while cdf[index] < num:
        index += 1
    return faces[index]

# generate random string of length k from alphabet a
def ran_str(a,k):
    return ''.join([choice(a) for _ in range(k)])
