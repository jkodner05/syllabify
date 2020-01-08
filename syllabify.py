import sys
import argparse


DEFAULT_VOWELS = set([u'a',u'e',u'i',u'o',u'u',u'A',u'E',u'I',u'O',u'U'])
DEFAULT_DIPHTHVOWELS = set([])
DEFAULT_DIPHTHONGS = set([])


def read_vowel_file(filename):
    with open(filename,'r') as f:
        return set([line.decode('utf8').strip() for line in f])


def find_nuclei(word, vowels=DEFAULT_VOWELS, diphthvowels=DEFAULT_DIPHTHVOWELS, diphthongs=DEFAULT_DIPHTHONGS):
    syllindices = [0]*len(word)
    #mark vowels as nuclei
    for i, char in enumerate(word):
        if char in vowels or char in diphthvowels:
            syllindices[i] = -1
    #number the nuclei
    nucnum = 1
    for i, index in enumerate(syllindices):
        if index == -1:
            #in conjunction with diphthvowels, handles many diphthongs 
            if i > 0 and syllindices[i-1] != 0:
                if word[i] in diphthvowels or word[i-1] in diphthvowels or word[i-1:i+1] in diphthongs:
                    nucnum = nucnum-1
            syllindices[i] = nucnum
            nucnum += 1
    #deal with final silent vowels. If not in a diphthong, shouldn't be part of a nucleus
    if word[-1] in finalsilents and len(word) > 1 and word[-2] not in diphthvowels and word[-1] not in diphthvowels:
        syllindices[-1] = 0
    return syllindices


def segment_cluster(cluster, onsets, codas):
    for split in range(len(cluster)):
        coda = cluster[:split]
        onset = cluster[split:]
        # if we can split it into attested coda and onset, favoring longer onsets
        if (not coda or coda in codas) and (not onset or onset in onsets):
            return split
    #default by splitting the cluster in half
    return len(cluster)/2


def syllabify(word, vowels=DEFAULT_VOWELS, diphthvowels=DEFAULT_DIPHTHVOWELS, diphthongs=DEFAULT_DIPHTHONGS, onsets=set([]), codas=set([])):
    syllindices = find_nuclei(word, vowels, diphthvowels, diphthongs)
    nucindices = [i for i,syllnum in enumerate(syllindices) if syllnum > 0]
    #degenerate case with no nuclei
    if not nucindices:
        return [word]
    #for each gap between nuclei, figure out how to split into coda and onset
    for i, nucindex in enumerate(nucindices):
        if i > 0:
            #mark the onset start index
            relativeonsetindex = segment_cluster(word[nucindices[i-1]+1:nucindex],onsets,codas)
            syllindices[nucindices[i-1]+relativeonsetindex+1] = syllindices[nucindex]
    #segment the word onset to onset
    syllindices[0] = 1
    maxsyll = syllindices[nucindices[-1]]
    syllindices.append(maxsyll+1)
#    for i in range(1,maxsyll+1):
#        print i, maxsyll
#        print word[syllindices.index(i):syllindices.index(i+1)], syllindices.index(i),syllindices.index(i+1)
    return [word[syllindices.index(i):syllindices.index(i+1)] for i in range(1,maxsyll+1)]


def syllabify_textfile(textfile, vowels, diphthvowels, diphthongs, onsets, codas):
    with open(textfile, 'r') as f:
        lines = []
        for line in f:
            words = []
            for word in line.strip().split(" "):
                if word.split():
                    #skip words with invalid unicode
                    try:
                        words.append(word.decode("utf8").strip())
                    except UnicodeDecodeError as e:
                        print e, "\tword: ", word
            lines.append([syllabify(word, vowels, diphthvowels, diphthongs, onsets, codas) for word in words])
        return lines


def train_clusters(textfile, vowels, diphthvowels, diphthongs):
    onsets = set([])
    codas = set([])
    with open(textfile, 'r') as f:
        words = []
        for word in f:
            if word.split():
                #skip words with invalid unicode
                try:
                    words.append(word.decode("utf8").strip())
                except UnicodeDecodeError as e:
                    print e, "\tword: ", word
    for word in words:
<<<<<<< HEAD
        nucindices = find_nuclei(word,vowels,diphthvowels, finalsilents=set([]))
=======
        nucindices = find_nuclei(word, vowels, diphthvowels, diphthongs)
>>>>>>> jk_parkes
        #skip if cannot be syllabified
        if max(nucindices) == 0:
            continue
#        print nucindices, word, word[:nucindices.index(1)], word[nucindices.index(max(nucindices))+1:]
        onsets.add(word[:nucindices.index(1)])
        codas.add(word[nucindices.index(max(nucindices))+1:])
    return onsets, codas


def write_output(syllabifiedlines, outputfile, delim):
    with open(outputfile, 'w') as f:
        for line in syllabifiedlines:
            words = []
            for word in line:
                words.append(delim.join(word).encode("utf8"))
            f.write(" ".join(words))
            if words:
                f.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Syllabify words in unicode text file, one word per line")
    parser.add_argument("textfile", help="input text file, one word per line")
    parser.add_argument("outputfile", help="output text file, one word per line, syllables separated by spaces", nargs="?")

    parser.add_argument('-v','--vowelfile', help="list of orthographic vowels, one per line", type=str)
    parser.add_argument('-d','--diphthongingvowelfile', help="list of vowels that tend to occur in diphthongs, one per line", type=str)
    parser.add_argument('-p','--diphthongfile', help="list of diphthongs, one per line", type=str)
    parser.add_argument('-o','--onsetfile', help="list of permitted onsets. Can be overwridden by trainclusters", type=str)
    parser.add_argument('-c','--codafile', help="list of permitted codas. Can be overwridden by trainclusters", type=str)
    parser.add_argument('-t','--trainclusters', help="learn potential onset and coda clusters from the data", action="store_true")
    parser.add_argument('--delim', help="delimiter (default: [space])",default=" ")
    
    args = parser.parse_args()

    vowels = DEFAULT_VOWELS
    diphthvowels = DEFAULT_DIPHTHVOWELS
    diphthongs = DEFAULT_DIPHTHONGS
    onsets = set([])
    codas = set([])
    if args.vowelfile:
        vowels = read_vowel_file(args.vowelfile)
    if args.diphthongingvowelfile:
        diphthvowels = read_vowel_file(args.diphthongingvowelfile)
    if args.diphthongfile:
        diphthongs = read_vowel_file(args.diphthongfile)
    if args.onsetfile:
        onsets = read_vowel_file(args.onsetfile)
    if args.codafile:
        codas = read_vowel_file(args.codafile)
    if args.trainclusters:
        print "Training Onsets..."
        onsets, codas = train_clusters(args.textfile, vowels, diphthvowels, diphthongs)
    print "\nSyllabifying..."
    syllabifiedlines = syllabify_textfile(args.textfile, vowels, diphthvowels, diphthongs, onsets, codas)

    if args.outputfile:
        write_output(syllabifiedlines, args.outputfile, args.delim)
    else:
        for word in syllabifiedwords:
            print " ".join(word)
