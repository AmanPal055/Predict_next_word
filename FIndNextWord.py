training_data = 'FindNextWord.txt'

initially_possible_words = {}
next_possible_words = {}
transitions = {}

def expandDictionary(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
def get_next_prob(given_list):   #returns dictionary
    prob_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        prob_dict[item] = prob_dict.get(item, 0) + 1
    for key, value in prob_dict.items():
        prob_dict[key] = value / given_list_length
    return prob_dict

def trainMarkovModel():
    for line in open(training_data):
        tokens = line.rstrip().lower().split()
        tokens_length = len(tokens)
        for i in range(tokens_length):
            token = tokens[i]
            if i == 0:
                initially_possible_words[token] = initially_possible_words.get(token, 0) + 1
            else:
                prev_token = tokens[i - 1]
                if i == tokens_length - 1:
                    expandDictionary(transitions, (prev_token, token), 'END')
                if i == 1:
                    expandDictionary(next_possible_words, prev_token, token)
                else:
                    prev_prev_token = tokens[i - 2]
                    expandDictionary(transitions, (prev_prev_token, prev_token), token)
    
    initially_possible_words_total = sum(initially_possible_words.values())
    for key, value in initially_possible_words.items():
        initially_possible_words[key] = value / initially_possible_words_total
        
    for prev_word, next_word_list in next_possible_words.items():
        next_possible_words[prev_word] = get_next_prob(next_word_list)
        
    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = get_next_prob(next_word_list)
    

def next_word(tpl):
    #print(transitions)
    if(type(tpl) == str):   #it is first word of string.. return from second word
        d = next_possible_words.get(tpl)
        if (d is not None):
            return list(d.keys())
    if(type(tpl) == tuple): #incoming words are combination of two words.. find next word now based on transitions
        d = transitions.get(tpl)
        if(d == None):
            return []
        return list(d.keys())
    return None #wrong input.. return nothing

trainMarkovModel()  #generate first, second words list and transitions

########## demo code below ################
print("Usage: start typing.. program will suggest words. Press tab to chose the first suggestion or keep typing\n")

import msvcrt   #use of mscvrt to get character from user on real time without pressing enter
c=''
sent=''
last_suggestion=[]
while(c != b'\r'):  #stop when user preses enter
    if(c != b'\t'): #if previous character was tab, then after autocompletion dont wait for user inpput.. just show suggestions
        c=msvcrt.getch()
    else:
        c = b' '
    if(c != b'\t'): #dont print tab etc
        print(str(c.decode('utf-8')), end='', flush=True)
    sent = sent + str(c.decode('utf-8'))  #create word on space
    if(c == b' '):
        tkns = sent.split()
        if(len(tkns) < 2):  #only first space encountered yet
            last_suggestion = next_word(tkns[0].lower())
            print(last_suggestion, end='  ', flush=True)
        else: #send a tuple
            last_suggestion = next_word((tkns[-2].lower(), tkns[-1].lower()))
            print(last_suggestion, end='  ', flush=True)
    if (c == b'\t' and len(last_suggestion) > 0):   #print last suggestion on tab
        print(last_suggestion[0], end='  ', flush=True)
        sent = sent + " " + last_suggestion[0]
 