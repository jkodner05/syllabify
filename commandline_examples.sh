#!/usr/bin/sh

echo "EXAMPLE 1"
#-h for list of arguments
python syllabify.py -h

echo "EXAMPLE 2"
#default settings, output to screen
#input: english_words.txt
python syllabify.py english_words.txt

echo "EXAMPLE 3"
#default settings, output to file
#input: english_words.txt
#output: test_english1.txt
python syllabify.py english_words.txt test_english1.txt

echo "EXAMPLE 4"
#default settings use a built in list of vowels, each vowel is treated as a nucleus
#defautl vowels: aeiouAEIOU
#to treat some vowel combinations as diphthongs, provide a list, one per line, of vowels which can form diphthongs after -d
#english diphthonging vowels, output to file
#input: english_words.txt
#output: test_english2.txt
#diphthonging vowels: english_diphthonging_vowels.txt
python syllabify.py english_words.txt test_english2.txt -d english_diphthonging_vowels.txt

echo "EXAMPLE 5"
#to replace the list of default vowels, use -v followed by a list of vowels
#these cannot form diphthongs. Add them after -d if you want that behavior
#german vowels, output to file
#input german_words.txt
#output test_german.txt
#vowels: german_vowels.txt
python syllabify.py german_words.txt test_german.txt -v german_vowels.txt

echo "EXAMPLE 6"
#by default, intervocalic clusters are split into coda and onset halfway through
#to instead learn and use potential onsets and codas from the data, use -t
#then the script will try to split clusters into attested coda+onset pairs which maximize the onset
#but if no attested coda + attested onset pair is found, it resorts to default behavior
#-t is a bad idea if the data is likely to have spurious onsets. Do not use with morphochallenge English, for example.
#english diphthonging vowels, learn clusters from data, output to file
#input: english_words.txt
#output: test_english2.txt
#diphthonging vowels: english_diphthonging_vowels.txt
python syllabify.py english_words.txt test_english3.txt -d english_diphthonging_vowels.txt -t
