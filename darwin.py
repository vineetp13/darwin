
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

#*******************************
NUM_ITERATIONS = 1
N = 10 #number of players
k = 3 #number of folks receiving feedback

#threshold to decide whether you will see feedbacks or not
#TODO-this will affect the payoffs - make note of that - and edit payoffs accordingly
l = 9

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
V = 10

#populate all the values above
for i in range(0,N):
    f[i] = round((i)*1.0/N) #hack to ensure fractional part is taken
    #log.debug(f[i]);
    #TODO-change deno value above..
    c[i] = C
    v[i] = V

#TODO-how should I vary c and v above in interesting and useful ways

#count of how many feedbacks has "i"th player received
count = [0] * N
#value of feedbacks received by "i"th player
value = [0.00] * N
#cost incurred by "i"th in providing feedback
cost = [0.00] * N

#Store sum of payoffs and people kicked out to see correlations
sums_all = [0] * NUM_ITERATIONS
kicked_all = [-1] * NUM_ITERATIONS
replacers = [-1] * NUM_ITERATIONS
final_freq_matrix = [-1] * NUM_ITERATIONS
for i in range(0,NUM_ITERATIONS):
    final_freq_matrix[i] = [-1] * N

#TODO-remove all variables not being used
#***********************

#TODO-create a matrix of who gives feedback to whom - To preseve the condition that everyone receives just as many feedbacks
feedback_matrix = [-1] * k
for i in range(0,k):
    feedback_matrix[i] = [-1] * N

count_feedback = [0] * N # how many feedbacks has ith player received

for i in range(0,k):
    for j in range(0,N):
        feedback_matrix[i][j] = j
    #v print feedback_matrix[i]

log.info("####")

#feedback_flag = 1 #flag =1  denotes that the list needs to be repermuted


def create_feedback_matrix():
    for i in range(0,k):
        feedback_flag=1
        while(feedback_flag==1):
            #v print i
            feedback_matrix[i] = np.random.permutation(N)
            #print "permuuuuuu", feedback_matrix[i]
    #TODO-check if same number has been assigned by chance
            for jj in range(0,N):
    #TODO-ensure that you dont give feedback to same player across rounds
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

#TODO-have clear metrics variables - and named so
#TODO-maybe use numpy, scipy for performance

#TODO-dont call it die_player - its not die_player bro

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
            count_feedback[chosen] +=1
            # and (chosen not in chosen_few)): cannot provide feedback to self and to someone else already provided feedback to
            #print count[chosen], value[chosen], cost [i], "count, value, cost"
            count[chosen]+=1 #increment number of feedback received by chosen
            value[chosen]+=f[i]*v[i] #increment value of feedbacks received by chosen
            cost[i] += c[i]*f[i]#cost incurred to "i"th player in providing feedback
            #print count[chosen], value[chosen], cost [i], "count, value, cost new"
        #v print i, "   ", chosen_few
    #print count_feedback
    #print feedback_matrix

    #TODO-ensure all default values are not crappy or wrong
    #TODO - all the above need to be reset to zero at the end of loop and beginning of next step

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
        if (cost[i] > l):
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
    log.debug("printing payoffs")
    for i in range(0,N):
        if(i!=die_player):
            if payoff[i]<payoff[min]:
                min = i
            if payoff[i]>payoff[max]:
                max = i
        log.debug(payoff[i])
    #Now we have the players with min and max payoffs, so divide up the number line


    #TODO-check if i have negative payoff values and to handle them...
    #currently assuming positive values only, not using "start" and "end"
    start = 0
    end = payoff[max]-payoff[min]

    #TODO-currently the dist_array includes the current die_player, this needs to be tweaked out - but it's okay right now  - easy to fix
    distr_array = [0] * N #this array stores the end-point for ith player to be chosen
    distr_array[0] = payoff[0]
    for i in range(1,N):
        distr_array[i] = payoff[i] + distr_array[i-1]

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

