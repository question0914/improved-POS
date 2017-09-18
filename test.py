import sys
inputfile = sys.argv[1]

with open(inputfile, "r", encoding='UTF-8')as infile:
    data = infile.read()
line = data.splitlines()

word = []
for l in line:
    wordlist = l.split()
    word.append(wordlist[0].replace("·"," "))

with open("name entity.txt", "w")as outfile:
    for w in word:
        outfile.write(w)
        outfile.write("\n")