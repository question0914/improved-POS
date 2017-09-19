import sys
inputfile = sys.argv[1]

# tags and known words
tags = set()
known = set()
# transition probability of q0
q0 = {}
# transition probability matrix
transition = {}
# emission probability matrix
emission = {}

# output log
log = list()

# Used to spilt word and probability
def splitword(s):
    temp = s.split("/")
    word = s[0:len(s)-len(temp[len(temp)-1])-1]
    prob = temp[len(temp)-1]
    return word, prob


# Create model
with open("hmmmodel.txt", 'r', encoding='utf-8')as modelfile:
    data = modelfile.read()
lines = data.splitlines()

for i in range(0, len(lines)):
    if lines[i] == "emission":
        em = i
        break

initials = lines[1].split()
for initial in initials:
    q0[initial.split("/")[0]] = q0.get(initial.split("/")[0], 0.0)
    q0[initial.split("/")[0]] = float(initial.split("/")[1])
    tags.add(initial.split("/")[0])

for i in range(3, em):
    wordlist = lines[i].split()
    outerkey = wordlist[0]
    for j in range(1, len(wordlist)):
        innerkey = wordlist[j].split("/")[0]
        transition[outerkey] = transition.get(outerkey, {})
        transition[outerkey][innerkey] = transition[outerkey].get(innerkey, 0.0)
        transition[outerkey][innerkey] = float(wordlist[j].split("/")[1])
for i in range(em+1, len(lines)):
    wordlist = lines[i].split()
    outerkey = wordlist[0]
    for j in range(1, len(wordlist)):
        innerkey, prob = splitword(wordlist[j])
        if innerkey not in known:
            known.add(innerkey)
        emission[outerkey] = emission.get(outerkey, {})
        emission[outerkey][innerkey] = emission[outerkey].get(innerkey, 0.0)
        emission[outerkey][innerkey] = float(prob)
    for outerkey in tags:
        for innerkey in known:
            emission[outerkey] = emission.get(outerkey, {})
            emission[outerkey][innerkey] = emission[outerkey].get(innerkey, 0.0)

# Read input file
with open(inputfile, 'r', encoding='utf-8')as infile:
    rawfile = infile.read()
lines = rawfile.splitlines()


for line in lines:
   # words = []
    V = [{}]
    backpointer = {}
    w = line.split()
    outtags = ['']
    outtags *= len(w)
    # Initialization for t=0
    #words.append(w[0])
    if w[0] not in known:
        for y in tags:
            emission[y] = emission.get(y, {})
            emission[y][w[0]] = emission[y].get(w[0], 0.0)
            emission[y][w[0]] = 1.0
    for y in tags:
        V[0][y] = q0[y] * emission[y][w[0]]
        backpointer[0] = backpointer.get(0, {})
        backpointer[0][y] = backpointer[0].get(y, "")
        backpointer[0][y] = "end"
    for i in range(1, len(w)):
        #words.append(w[i])
        # Unknown word
        if w[i] not in known:
            for y in tags:
                emission[y] = emission.get(y, {})
                emission[y][w[i]] = emission[y].get(w[i], 0.0)
                emission[y][w[i]] = 1.0
        V.append({})

        for y in tags:
            (prob, state) = max((V[i - 1][y0] * transition[y0][y] * emission[y][w[i]]*100000, y0) for y0 in tags)
            V[i][y] = prob
            backpointer[i] = backpointer.get(i, {})
            backpointer[i][y] = backpointer[0].get(y, "")
            backpointer[i][y] = state



    (prob, state) = max((V[i][y], y) for y in tags)
    reversedout = []
    for i in range(0, len(w))[::-1]:
        reversedout.append(state)
        state = backpointer[i][state]
    for i in range(0, len(w)):
        outtags[i] = reversedout[len(w)-i-1]
    for i in range(0, len(w)):
        log.append(w[i]+"/"+outtags[i]+" ")
    log.append("\n")
with open("hmmoutput.txt", "w")as outfile:
    for l in log:
        outfile.write(l)

