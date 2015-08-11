
'''
Code objective:
1. Understand how the cost and value of an assignment affect the student's submission rate (approximated by evolution of f) - by varying V,C (relative values)
2. Understand how the theeshold "l" affects student feedback submission rate
'''
from random import randint
import numpy as np #for random.permutation
import logging as log

log.basicConfig(
    filename='results.TEXT',
    level=log.DEBUG,
    format=' %(message)s',
    filemode='w')
    #format='%(asctime)s - %(levelname)s - %(message)s')
log.debug('This is a log message.')

log.info("**************************")

'''
TODOS: Performance
1. maybe use numpy, scipy for array operations
2. using many small fucntions for useless work (like "round") - eliminate smartly

TODOS: Readability
1. Have clear metrics variables - and named so
2. Remove all variables not being used

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
    f[i] = round((i)*1.0/N,1) #hack to ensure fractional part is taken
    #log.debug(f[i])
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

#Create a matrix of who gives feedback to whom - To preseve the condition that everyone receives just as many feedbacks
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


for ii in range(0,NUM_ITERATIONS):
    ##print "ITERATION ##########", ii
    create_feedback_matrix() #create new feedback matrix for every iteration
    for i in range(0,N):
        #choose k number of recipients randomly to provide feedback to
        chosen_few = [-1] * k
        for j in range(0,k):
            #TODO-dont need to do the chosen crap anymore - can just delete this during code clean up
            #chosen = randint(0,N-1)
            #while(chosen in chosen_few or chosen==i):# or count_feedback[chosen]==k):
            #    chosen = randint(0,N-1)
            chosen = feedback_matrix[j][i]
            chosen_few[j] = chosen
            # and (chosen not in chosen_few)): cannot provide feedback to self and to someone else already provided feedback to
            #print count[chosen], value[chosen], cost [i], "count, value, cost"
            count[chosen]+=1 #increment number of feedback received by chosen
            value[chosen]+=f[i]*v[i] #increment value of feedbacks received by chosen
            cost[i] += c[i]*f[i]#cost incurred to "i"th player in providing feedback
            #print count[chosen], value[chosen], cost [i], "count, value, cost new"
        #v print i, "   ", chosen_few
    #print feedback_matrix

    #TODO-ensure all default values are not crappy or wrong
    #TODO - all the above need to be reset to zero at the end of loop and beginning of next step

#TODO--does avg_score help with anything
    avg_score = [-1] * N

    # randomly selecting player to die
    die_player = randint(0,N-1)
    sum_p = 0

    pass_l_threshold = 0
    fail_l_threshold = 0

#calculating payoff values in payoff[i]
    for i in range(0,N):
        #print payoff[i], value[i], cost[i], "<-- payoff[i]"
        ##print "original cost", cost [i]
        payoff[i] = value[i] - cost[i]
        if (cost[i] >= l):
            #then the player crosses our threshold of providing feedback
            pass_l_threshold +=1
        else:
            fail_l_threshold += 1
        avg_score[i] = value[i]/k
        sum_p += payoff[i]
    print "number of players who passed and failed threshold are", pass_l_threshold, fail_l_threshold
    #print sum_p, "<-- sum_p"

    #TODO-fix sum_p when you account for taking out die_player from the distribution
    #sum_p = sum_p - p[die_player] #take die_player out of probability distribution
    ##print sum_p, "<-- sum_p"

    #v print p, "entire payoff array"
    #v print f, "frequency array"
    #v print f[die_player], c[die_player], v[die_player], p[die_player],"details of die_player before"

#TODO-following three lines are redundant
    #f[die_player] = 0
    #c[die_player] = 0
    #v[die_player] = 0

    #TODO-replace the die_player with a new player using a probability distribution over the remaining folks

    #This weighted approach is wrong
    #for i in range(0,N):
     #   if (i != die_player):
      #      #print i, "inside"
       #     #print f[i],c[i],v[i], payoff[i], "f,c,v,payoff[i]"
       #     f[die_player] += f[i]*payoff[i]
        #    c[die_player] += c[i]*payoff[i]
         #   v[die_player] += v[i]*payoff[i]
          #  #print f[die_player], c[die_player], v[die_player], "inside loop"
    #print f[die_player], c[die_player], v[die_player], "before div"
    #f[die_player] *= (1.0)/sum_p
    #c[die_player] *= (1.0)/sum_p
    #v[die_player] *= (1.0)/sum_p
    #p[die_player] = 0.0
    #print f[die_player], c[die_player], v[die_player], "after div"
    ##print "****"

    #TODO-use multiline comments preserving indentation - not fixing it right now

    #choosing new die_player using a prob distribution over existing players
    #TODO-not doing it entirely correctly now, since the two end points (min and max) have almost no chance of being chosen - How to fix
        #Maybe the above will be auto fixed when the algo ensures everyone receives feedback ensuring that no one has negative payoffs
    #TODO - skip current die_player

#TODO-Payoffs can be negative: implies that the number line needs to be chosen wisely
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
    log.debug("max and min payoffs are")
    log.debug("'{0}', '{1}'".format(payoff[max], payoff[min]))
    #Now we have the players with min and max payoffs, so divide up the number line

    payoff_max = payoff[max]
    payoff_min = payoff[min]

    #modify payoff matrix itself to keep things easy - also recompute sum_p (since it clearly changes)
    sum_p = 0
    for i in range(0,N):
        payoff[i] -= payoff_min
        sum_p += payoff[i]

    log.debug("new_shifted_payoff")
    log.debug(payoff)

    #TODO-currently the dist_array includes the current die_player, this needs to be tweaked out - but it's okay right now  - easy to fix
    distr_array = [0] * N #this array stores the end-point for ith player to be chosen
    distr_array[0] = payoff[0]
    for i in range(1,N):
        distr_array[i] = payoff[i] + distr_array[i-1]

    #TODO-check that the dist_array impl is right
    ##print "distr_array is ", distr_array

    #for i in range(0,N-1):
     #   print distr_array[i+1] - distr_array[i]

    #now get a random number in the range of the number line (0,sum_p) and see where it fails
    toss = randint(0,int(sum_p))
    ##print "toss is", toss
    die_player_new = -1

    for i in range(0,N):
        if toss < distr_array[i]:
            die_player_new = i
            break

    #die_player = die_player_new
    #v print "new die_player is", die_player_new

    #assign the die_player the chosen guys value
    f[die_player] = f[die_player_new]
    c[die_player] = c[die_player_new]
    v[die_player] = v[die_player_new]

    #now we have our new die_player
    #v print f[die_player], c[die_player], v[die_player], p[die_player], "details of die_player now"
    ####log.debug("'{0}'".format(f), "entire freuqnecy array")
    #print count, "entire count array"

    #TODO-now, clear out the values for next iteration
    #TODO-maybe we want to store the round by round details - think?
    for i in range(0,N):
        value[i] = 0.0
        cost[i] = 0.0
        count[i] = 0.0


    sums_all[ii] = sum_p
    kicked_all[ii] = die_player
    replacers[ii] = die_player_new
    final_freq_matrix[ii] = f
    log.info("'{0}'".format(final_freq_matrix[ii]))

log.debug("!!!!")

#Now repeat the whole experiment again with NUM_ITERATIONS loop above
#print "%.2f" % sums_all
#print sums_all
#print kicked_all

#TODO-fix final_freq_matrix storing+printing..
log.debug(final_freq_matrix)

for i in range(0,NUM_ITERATIONS):
    log.debug("'{0}', '{1}'".format(i, sums_all[i])) #(i, sums_all[i])
    log.debug("'{0}', '{1}'".format(kicked_all[i], replacers[i]))
    log.debug("'{0}'".format(final_freq_matrix[i]))
    #print " |"
    #print " |"
    #print "\ /"


#TODO-potential optimizations
#1. use numpy/scipy

