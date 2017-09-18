import sys
inputfile = sys.argv[1]

# transition probability of q0
q0 = {}

# transition probability matrix
transition = {}
# emission probability matrix
emission = {}
# List to store all the tags for smoothing
taglist = list()
# Set of all words
wordset = set()


# Used to spilt word and tag
def splitword(s):
    temp = s.split("/")
    word = s[0:len(s)-len(temp[len(temp)-1])-1]
    tag = temp[len(temp)-1]
    return word, tag

with open(inputfile, "r", encoding='utf-8')as infile:
    data = infile.read()
line = data.splitlines()

for l in line:
    wordlist = l.split()
    words = []
    tags = []
    for i in range(0, len(wordlist)):
        word, tag = splitword(wordlist[i])
        words.append(word)
        tags.append(tag)
        if word not in wordset:
            wordset.add(word)
        if tag not in taglist:
            taglist.append(tag)

    q0[tags[0]] = q0.get(tags[0], 0.0)
    q0[tags[0]] += 1

    for i in range(0, len(wordlist)-1):
        # Transition matrix
        outerkey = tags[i]
        innerkey = tags[i+1]
        transition[outerkey] = transition.get(outerkey, {})
        transition[outerkey][innerkey] = transition[outerkey].get(innerkey, 0.0)
        transition[outerkey][innerkey] += 1
        # Emission matrix
        outerkey = tags[i]
        innerkey = words[i]
        emission[outerkey] = emission.get(outerkey, {})
        emission[outerkey][innerkey] = emission[outerkey].get(innerkey, 0.0)
        emission[outerkey][innerkey] += 1

    outerkey = tags[len(wordlist)-1]
    innerkey = words[len(wordlist)-1]
    emission[outerkey] = emission.get(outerkey, {})
    emission[outerkey][innerkey] = emission[outerkey].get(innerkey, 0.0)
    emission[outerkey][innerkey] += 1

# Smooth the transition matrix and q0 by adding 1 for each possible transition
for i in range(0, len(taglist)):
    for j in range(0, len(taglist)):
        outerkey = taglist[i]
        innerkey = taglist[j]
        transition[outerkey] = transition.get(outerkey, {})
        transition[outerkey][innerkey] = transition[outerkey].get(innerkey, 0.0)
        transition[outerkey][innerkey] += 1

for i in range(0, len(taglist)):
    key = taglist[i]
    q0[key] = q0.get(key, 0.0)
    q0[key] += 1

# Convert to probability
for key in transition:
    di = transition[key]
    s = sum(di.values())
    for innkey in di:
        di[innkey] /= s
    transition[key] = di


for key in emission:
    di = emission[key]
    s = sum(di.values())
    for innkey in di:
        di[innkey] /= s
    emission[key] = di


s = sum(q0.values())
for key in q0:
   q0[key]/=s

with open("hmmmodel.txt", "w")as outfile:
    outfile.write("q0\n")
    for key in q0:
        outfile.write(key+"/")
        outfile.write("%.12f " %q0[key])
    outfile.write("\n")
    outfile.write("transition\n")
    for key in transition:
        outfile.write(key+" ")
        di = transition[key]
        for innkey in di:
            outfile.write(innkey + "/")
            outfile.write("%.12f " % di[innkey])
        outfile.write("\n")
    outfile.write("emission\n")
    for key in emission:
        outfile.write(key + " ")
        di = emission[key]
        for innkey in di:
            outfile.write(innkey + "/")
            outfile.write("%.12f " % di[innkey])
        outfile.write("\n")

