
'''
Code objective:
1. Understand how the cost and value of an assignment affect the student's submission rate (approximated by evolution of f) - by varying V,C (relative values)
2. Understand how the theeshold "l" affects student feedback submission rate
'''
from random import randint
import numpy as np #for random.permutation
import logging as log
import math as m

log.basicConfig(
    filename='results.TEXT',
    level=log.DEBUG,
    format=' %(message)s',
    filemode='w')
    #format='%(asctime)s - %(levelname)s - %(message)s')
#log.debug('This is a log message.')

log.info("**************************")

'''
TODOS: Performance
1. maybe use numpy, scipy for array operations
2. using many small fucntions for useless work (like "round") - eliminate smartly

TODOS: Readability
1. Have clear metrics variables - and named so
2. Remove all variables not being used
3. #TODO-use multiline comments preserving indentation - not fixing it right now

TODOS: Correctness:
1. TODO-ensure all default values are not crappy or wrong

TODOS: For fun
1. Write a functional version eliminatng ALL the global variables
2.

'''
#*******************************
NUM_ITERATIONS = 100
N = 100 #number of players
k = 10 #number of folks receiving feedback

#threshold to decide whether you will see feedbacks or not
l = 1

#*****************
#Setting up frequency, cost, value arrays

#frequency of providing feedback
f = [0.00] * N
#cost of providing feedback fpr "i"th player
c = [0] * N
#value of feedback of "i"th player
v = [0] * N
#payoff_value for players
payoff = [0] * N

#if using constant values for Cost and Value of feedback for all players
C = 1
V = 100

#populate all the values above
for i in range(0,N):
#TODO-this f[i] expression is way too complicated, but lazy
    f[i] = round(m.floor((i)*10.0/N)*(0.1),1) #hack to ensure fractional part is taken
    log.debug(f[i])
    c[i] = C
    v[i] = V

#count of how many feedbacks has "i"th player received
count = [0] * N
#value of feedbacks received by "i"th player
value = [0.00] * N
#cost incurred by "i"th in providing feedback
cost = [0.00] * N

#TODO-remove all variables not being used
#Store sum of payoffs and people kicked out to see correlations
sums_all = [0] * NUM_ITERATIONS
kicked_all = [-1] * NUM_ITERATIONS
replacers = [-1] * NUM_ITERATIONS
final_freq_matrix = [-1] * NUM_ITERATIONS
for i in range(0,NUM_ITERATIONS):
    final_freq_matrix[i] = [-1] * N

#***********************

#Metrics used
metric_pass_l_threshold = [0] * NUM_ITERATIONS
metric_fail_l_threshold = [0] * NUM_ITERATIONS


#*******

#Create a matrix of who gives feedback to whom - To preseve the condition that everyone receives just as many feedbacks
#k*n matrix, so, i-th column denotes who receives feedback from i-th player
#Conditions: 1. Player cannot give feedback to self 2.In one round, any player should only receive k feedbacks (fromk unique players)
#TODO-need to meet these conditions
feedback_matrix = [-1] * k
for i in range(0,k):
    feedback_matrix[i] = [-1] * N

for i in range(0,k):
    for j in range(0,N):
        feedback_matrix[i][j] = j
    #v print feedback_matrix[i]

log.info("####")

feedback_flag = -1  #a value of 1 denotes that the list needs to be repermuted
def create_feedback_matrix():
#creates
    for i in range(0,k):
        feedback_flag=1
        while(feedback_flag==1):
            feedback_matrix[i] = np.random.permutation(N)
            #print "permuuuuuu", feedback_matrix[i]
    #TODO-check if same number has been assigned by chance
            for jj in range(0,N):
    #TODO-ensure that you dont give feedback to same player across rounds
    #TODO-this  wrong feedbakc matrix crap needs to be fixed
                cur_list = [-1] * (i+1)
                for iii in range(1,i+1):
                    cur_list[iii] = feedback_matrix[iii-1][jj] #this list contains the elements chosen for the same player so far
                #v print "!!!!!!!"
                bool_check = feedback_matrix[i][jj] in cur_list
                #v print cur_list, feedback_matrix[i][jj], bool_check

                #v print "!!!!!"
                if((feedback_matrix[i][jj]==jj) or bool_check): #jj player cannot provide feedback to itself
                    #v print bool_check
                    feedback_flag=1
                else:
                    feedback_flag=0
log.info("$$$$")

#Main loop in which a new feedback matrix is created for every iteration
for ii in range(0,NUM_ITERATIONS):
    ##print "ITERATION ##########", ii
    create_feedback_matrix() #create new feedback matrix for every iteration
    #All the smartness is in create_feedback_matrix - I shouldnt need to do any checks below
    for i in range(0,N): #for every player, decide whom would it give feedback to
        #chosen_few = [-1] * k #choose k number of recipients randomly to provide feedback to
        for j in range(0,k):
            chosen = feedback_matrix[j][i] #TODO-clean this code, just lazy
            #chosen_few[j] = chosen
            count[chosen]+=1 #increment number of feedback received by chosen
            value[chosen]+=f[i]*v[i] #increment value of feedbacks received by chosen
            cost[i] += c[i]*f[i]#cost incurred to "i"th player in providing feedback
            #print count[chosen], value[chosen], cost [i], "count, value, cost new"
        #v print i, "   ", chosen_few
    #print feedback_matrix

    #TODO - all the above need to be reset to zero at the end of loop and beginning of next step

    # randomly selecting player to die
    die_player = randint(0,N-1)
    sum_p = 0

    #calculating payoff values in payoff[i]
    for i in range(0,N):
        payoff[i] = value[i] - cost[i]
        if (cost[i] >= l):
            #then the player crosses our threshold of providing feedback
            metric_pass_l_threshold[ii] +=1
        else:
            metric_fail_l_threshold[ii] += 1
        sum_p += payoff[i]
    ##print "number of players who passed and failed threshold are", metric_pass_l_threshold[ii], metric_fail_l_threshold[ii]


    #TODO-fix sum_p when you account for taking out die_player from the distribution
    #sum_p = sum_p - p[die_player] #take die_player out of probability distribution
    ##print sum_p, "<-- sum_p"


#TODO-following three lines are redundant
    #f[die_player] = 0
    #c[die_player] = 0
    #v[die_player] = 0


    #choosing new die_player using a prob distribution over existing players
    #TODO-not doing it entirely correctly now, since the two end points (min and max) have almost no chance of being chosen - How to fix
    #Payoffs can be negative: implies that the number line needs to be chosen wisely
    min = 0
    max = 0
    ##log.debug("printing payoffs")
    for i in range(0,N):
        if(i!=die_player):
            if payoff[i]<payoff[min]:
                min = i
            if payoff[i]>payoff[max]:
                max = i
        ##log.debug(payoff[i])
    #l log.debug("max and min payoffs are")
    #l log.debug("'{0}', '{1}'".format(payoff[max], payoff[min]))
    #Now we have the players with min and max payoffs, so divide up the number line

    #TODO-just crapy hacky code - need to get graphs
    payoff_max = payoff[max]
    payoff_min = payoff[min]

    #modify payoff matrix itself to keep things easy - also recompute sum_p (since it clearly changes)
    sum_p = 0
    for i in range(0,N):
        payoff[i] -= payoff_min
        sum_p += payoff[i]

    #l log.debug("new_shifted_payoff")
    #l log.debug(payoff)

    #TODO-currently the dist_array includes the current die_player, this needs to be tweaked out - but it's okay right now  - easy to fix
    distr_array = [0] * N #this array stores the end-point for ith player to be chosen
    distr_array[0] = payoff[0]
    for i in range(1,N):
        distr_array[i] = payoff[i] + distr_array[i-1]

    #TODO-check that the dist_array impl is right
    ##print "distr_array is ", distr_array

    #check to see if distr_array is correct - this should match wiht payoff matrix values
    #for i in range(0,N-1):
     #   print distr_array[i+1] - distr_array[i]

    #now get a random number in the range of the number line (0,sum_p) and see where it falls and chose die_player_new accordingly
    #die_player_new is basically one of the alie players who will replace die_player
    toss = randint(0,int(sum_p))
    ##print "toss is", toss
    die_player_new = -1
    for i in range(0,N):
        if toss < distr_array[i]:
            die_player_new = i
            break
    #assign the die_player the chosen guys value
    f[die_player] = f[die_player_new]
    c[die_player] = c[die_player_new]
    v[die_player] = v[die_player_new]

    #now we have our new die_player
    #v print f[die_player], c[die_player], v[die_player], p[die_player], "details of die_player now"
    ####log.debug("'{0}'".format(f), "entire freuqnecy array")
    #print count, "entire count array"

    #now, clear out the values for next iteration
    #TODO-maybe we want to store the round by round details - think?
    for i in range(0,N):
        value[i] = 0.0
        cost[i] = 0.0
        count[i] = 0.0

    sums_all[ii] = sum_p
    kicked_all[ii] = die_player
    replacers[ii] = die_player_new
    for xx in range(0,N):
        final_freq_matrix[ii][xx] = f[xx]
    #final_freq_matrix[ii] = f
    log.info("'{0}'".format(final_freq_matrix[ii]))


log.debug(metric_pass_l_threshold)
log.debug(metric_fail_l_threshold)
log.debug(final_freq_matrix)
log.debug("----")

for i in range(0,NUM_ITERATIONS):
    log.debug("'{0}', '{1}'".format(i, sums_all[i])) #(i, sums_all[i])
    log.debug("'{0}', '{1}'".format(kicked_all[i], replacers[i]))
    log.debug("'{0}'".format(final_freq_matrix[i]))
    #print " |"
    #print " |"
    #print "\ /"


#************
#Plots
import matplotlib.pyplot as pyplot
x = [-1] * NUM_ITERATIONS
for i in range(0,NUM_ITERATIONS):
    x[i] = i

##pyplot.plot(x,metric_pass_l_threshold)
#pyplot.show()
##pyplot.savefig('l='+str(l)+',V='+str(V)+',ITER='+str(NUM_ITERATIONS)+'.png')

#TODO-freq_bars depend upon number "k" - DO NOT FORGET
freq_bars = [0] * NUM_ITERATIONS
for i in range(0,NUM_ITERATIONS):
    freq_bars[i] = [0] * k

#print final_freq_matrix
#print freq_bars

#Plots for frequency
for ii in range(0,NUM_ITERATIONS):
    for j in range(0,N):
        #print int(final_freq_matrix[ii][j]*k)
        freq_bars[ii][int(final_freq_matrix[ii][j]*k)] += 1
#print freq_bars

#to plot this
#TODO-show error bars/variance,
#currently only showing average
avg_freq = [0] * k
for i in range(0,k):
    for j in range(0,NUM_ITERATIONS):
        avg_freq[i] += freq_bars[j][i]
    avg_freq[i] *= 1.0/NUM_ITERATIONS  #Again, float hack

##print avg_freq
##print sum(avg_freq)

x_k = [-1] * k
for i in range(0,k):
    x_k[i] = i

pyplot.plot(x_k,avg_freq, color='green', linewidth="5.0")
pyplot.xlabel("Frequency bins: 0.0 to 0.9")
pyplot.ylabel("Number of players")
pyplot.title("Average and per-iteration number of players in every frequency bin")
#print freq_bars
for i in range(0,NUM_ITERATIONS):
    pyplot.plot(x_k, freq_bars[i], color='yellow', linewidth="0.01", linestyle='dashed')
#pyplot.plot(x_k,freq_bars[0])
#pyplot.plot(x_k,freq_bars[1])
pyplot.savefig("images_a1l.png")

#pyplot.save("hashfail.png")
