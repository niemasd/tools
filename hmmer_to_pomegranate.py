#!/usr/bin/env python3
'''
Convert a profile HMM from the HMMER3 format to the pomegranate format.
'''
# convert HMMER3 profile HMM to pomegranate format
def hmmer2pom(hmm):
    # set up environment
    from math import exp
    from pomegranate import DiscreteDistribution,HiddenMarkovModel,State
    tags = dict(); header = 0; alphabet = None; hmmlines = list()

    # parse HMMER file
    for line in hmm.splitlines():
        l = line.strip()
        if len(l) == 0 or l[0] == '#':
            continue
        elif header == 0:
            if l.startswith('HMM') and l[3] != 'E': # beginning of actual HMM
                header = 1; alphabet = l.split()[1:]
            else:
                parts = l.strip().split()
                if parts[0] in tags:
                    if not isinstance(tags[parts[0]], list):
                        tags[parts[0]] = [tags[parts[0]]]
                    tags[parts[0]].append(' '.join(parts[1:]))
                else:
                    tags[parts[0]] = ' '.join(parts[1:])
        elif header == 1:
            header = 2
        else:
            if l.startswith('COMPO'):
                parts = l.strip().split(); tags[parts[0]] = ' '.join(parts[1:])
            else:
                hmmlines.append(l)

    # create all states
    model = HiddenMarkovModel(tags['NAME']); tmpstates = list(); K = 0
    i_emit = hmmlines[0].split(); tmpstates.append(State(DiscreteDistribution({alphabet[i] : exp(-1*float(i_emit[i])) for i in range(len(alphabet))}), name="I0")) # insertion state
    for l in range(2,len(hmmlines),3):
        m_emit,i_emit,state_trans = [hmmlines[l+i].split() for i in range(0,3)]; K = int(m_emit[0])
        tmpstates.append(State(DiscreteDistribution({alphabet[i] : exp(-1*float(m_emit[i+1])) for i in range(len(alphabet))}), name="M%d" % K)) # match state
        tmpstates.append(State(DiscreteDistribution({alphabet[i] : exp(-1*float(i_emit[i])) for i in range(len(alphabet))}), name="I%d" % K)) # insertion state
        tmpstates.append(State(None, name="D%d" % K)) # deletion state
    assert K != 0, "No match states in profile HMM"
    model.add_states(tmpstates); name2state = {state.name:state for state in tmpstates}; name2state["M0"] = model.start; name2state["M%d"%(K+1)] = model.end

    # create all transitions
    for l in range(1,len(hmmlines),3):
        k = int(l/3); parts = hmmlines[l].split()
        model.add_transition(name2state["M%d"%k], name2state["M%d"%(k+1)], exp(-1*float(parts[0])))     # 0: M_k -> M_k+1
        model.add_transition(name2state["M%d"%k], name2state["I%d"%k],     exp(-1*float(parts[1])))     # 1: M_k -> I_k
        if parts[2] != '*': # no D_k+1 in last row
            model.add_transition(name2state["M%d"%k], name2state["D%d"%(k+1)], exp(-1*float(parts[2]))) # 2: M_k -> D_k+1
        model.add_transition(name2state["I%d"%k], name2state["M%d"%(k+1)], exp(-1*float(parts[3])))     # 3: I_k -> M_k+1
        model.add_transition(name2state["I%d"%k], name2state["I%d"%k],     exp(-1*float(parts[4])))     # 4: I_k -> I_k
        if k != 0: # no D0 state
            model.add_transition(name2state["D%d"%k], name2state["M%d"%(k+1)], exp(-1*float(parts[5]))) # 5: D_k -> M_k+1
        if parts[6] != '*': # no D0 state and no D_k+1 in last row
            model.add_transition(name2state["D%d"%k], name2state["D%d"%(k+1)], exp(-1*float(parts[6]))) # 6: D_k -> D_k+1
    model.bake()
    return model.to_json()

# run actual code
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input HMMER3 HMM File")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output pomegranate File")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')
    hmms = [hmmer2pom(hmm) for hmm in infile.read().split('\n//')[:-1]]
    assert len(hmms) != 0, "No HMMs in input file: %s" % args.input
    if len(hmms) == 1:
        outfile.write(hmms[0])
    else:
        outfile.write('[%s]' % ','.join(hmms))
