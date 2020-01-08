import syllabify

print "\nEXAMPLE 1"
#syllabify a word, default behavior
syllabified = syllabify.syllabify("hello")
print " ".join(syllabified)

print "\nEXAMPLE 2"
#default vowels are aeiouAEIOU
#syllabify with different vowels with the vowels argument
#this can be a list or a string or a set. sets are fastest
syllabified = syllabify.syllabify("happy")
print " ".join(syllabified)
syllabified = syllabify.syllabify("happy", vowels=set(["a","e","i","o","u","y"]))
print " ".join(syllabified)

print "\nEXAMPLE 3"
#by default, vowels in hiatus are treated as independent nuclei
#specify which vowels form diphthongs with the diphthvowels argument
syllabified = syllabify.syllabify("look")
print " ".join(syllabified)
syllabified = syllabify.syllabify("look", diphthvowels=["o"])
print " ".join(syllabified)

print "\nEXAMPLE 4"
#by default, intervocalic clusters are split down the middle
#to specify onsets and coda to look for instead, use the onsets and codas arguments
#these expect sets or lists. sets are faster
#if no valid coda+onset combination exists, it restorts to default behavior
syllabified = syllabify.syllabify("fishing")
print " ".join(syllabified)
syllabified = syllabify.syllabify("fishing", onsets=set(["sh"]))
print " ".join(syllabified)
syllabified = syllabify.syllabify("lathing", onsets=set(["sh"]))
print " ".join(syllabified)

print "\nEXAMPLE 5"
#to train a list of onsets and codas attested in the data, call train_clusters
#you must specify vowels and diphthvowels. 
#Defaults DEFAULT_VOWELS and DEFAULT_DIPHTHVOWELS are available
onsets, codas = syllabify.train_clusters("english_words.txt", vowels=syllabify.DEFAULT_VOWELS, diphthvowels=set(["y"]))
print onsets
print codas
syllabified = syllabify.syllabify("fishing", onsets=onsets, codas=codas)
print " ".join(syllabified)

print "\nExample 6"
#to ignore final vowels, like final e in English and french
#pass in a finalsilents set to syllabify.syllabify. 
syllabified = syllabify.syllabify("machine")
print " ".join(syllabified)
syllabified = syllabify.syllabify("machine", finalsilents=["e"])
print " ".join(syllabified)

print "\nFor more examples, see commandline_examples.sh"
