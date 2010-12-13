#!/usr/bin/env python
# coding=utf-8

import sys, os, time, string
import operator

savedir  = os.path.join(os.environ["HOME"], ".julekalender")
daynum   = time.localtime()[2]
ydaynum  = time.localtime(time.time()-86400)[2]

# colors
b = "\002"  # bold
c = "\003"  # clean
r = "\0034" # red

def save_answer(nick, host, answer):
    today    = time.strftime("%Y.%m.%d")
    question = os.path.join(savedir, today + ".txt")

    if not os.path.isdir(savedir):
        print "Noe gikk skikkelig feil!"
        sys.exit(0)
    elif not os.path.isfile(question):
        print "Det var ikke noe spørsmål i dag!"
        sys.exit(0)
    elif len(answer) <= 0:
        print "Du må oppgi et svar"
        sys.exit(0)

    if not os.path.isdir(os.path.join(savedir, today)):
        os.mkdir(os.path.join(savedir,today))

    filename = os.path.join(savedir, today, nick + ".txt")
    atime = time.strftime("%d.%m.%Y %H:%M:%S")

    file = open(filename, "a")
    file.write(atime + " " + host + ": " + answer + "\n")
    file.close()

    print b + "Svar lagret" + c
    
def show_answer(number):
    check_num(number)
    
    day = time.strftime("%Y.%m.") + "%02d" % number
    answer = os.path.join(savedir, day + "." + "fasit.txt")
    
    if number >= daynum:
        print "Lov å prøve seg..."
        sys.exit(0)
    elif not os.path.isfile(answer):
        print "Ikke noen fasit for luke %d" % number
        sys.exit(0)

    file = open(answer, "r")
    print_question(number, file.read().strip())
    file.close()

def ask_question(number):
    check_num(number)

    day = time.strftime("%Y.%m.") + "%02d" % number
    question = os.path.join(savedir, day + ".txt")
    
    if number > daynum:
        print "Må nok vente litt til."
        sys.exit(0)
    if not os.path.isfile(question):
        print "Ikke noen spørsmål for luke %d" % number
        sys.exit(0)
    
    file = open(question, "r")
    print_question(number, file.read().strip())
    file.close()

def show_scores():
    scores = os.path.join(savedir, "%s.scores.txt" % time.strftime("%Y"))

    try:
        mtime=time.localtime(os.path.getmtime(scores))
        lastmod = " [Luke %d]" % (int(time.strftime("%d", mtime))-1)
    except:
        lastmod = ""

    if not os.path.isfile(scores):
        print "Fant ikke noen resutater."
        sys.exit(0)
    
    results = []

    file = open(scores, "r")
    for line in file:
        tmp = line.strip().split(":")
        results.append( (tmp[0], float(tmp[1])) )
    
    results = sorted(results, key=operator.itemgetter(1), reverse=True)
    results = ", ".join(["%s: %g" % (x, y) for x, y in results])

    print r + "Resultater: " + c + b + results + b + lastmod
    file.close()

def check_num(number):
    if number > 24 or number < 1:
        sys.exit(0)

def print_question(number, question):
    print r + "Luke " + "%d" % number + ": " + c + b + question + c

if __name__ == "__main__":
    try: 
        arg = sys.argv[1]
    except:
        sys.exit(0)

    # ask question
    if arg == "ask":
        try:
            number = int(sys.argv[2])
        except:
            number = daynum
        
        ask_question(number)
    
    # give answer
    elif arg == "answer":
        try:
            number = int(sys.argv[2])
        except:
            number = ydaynum
        
        show_answer(number)
    
    # save answer
    elif arg == "save":
        try:
            nick = sys.argv[2]
            host = sys.argv[3]
            answer = string.join(sys.argv[4:])
        except:
            print "Noe gikk skikkelig feil!"
            sys.exit(0)
        
        save_answer(nick, host, answer)

    elif arg == "score":
        show_scores()

