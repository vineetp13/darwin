'''
Code objective:
1. Understand how the cost and value of an assignment
affect the student's submission rate (approximated
by evolution of f) - by varying V,C (relative values)
2. Understand how the theeshold "l" affects student
feedback submission rate
'''
from random import randint
import numpy as np  # for random.permutation
import logging as log
import math as m

'''
# TODOS: Performance 1. maybe use numpy, scipy for array operations 2. using
# many
small fucntions for useless work (like "round") - eliminate smartly 3. Remove
redundant calculations of sum_p, sum_fitness when distr_array is being calc
already 4. do distr_array choice and toss smartly

# TODOS: Readability
1. Have clear metrics variables - and named so
2. Remove all variables not being used
3. # TODO-use multiline comments preserving indentation - not fixing it right
now

TODOS: Correctness: 1. TODO-ensure all default values are not crappy or wrong
(eg: choosing a
default array index as -1 will lead to last element being selected)
2. TODO - fix minor issue in create_feedback_matrix constaints 3. TODO - not
accounting for die_player when choosing new players (currently including him
but okay at our scale)

TODOS: For fun
1. Write a functional version eliminatng ALL the global variables
2.
'''
# *******************************
#  linear is 1, epsilon is 2 and exp is 3
WHICH_FITNESS_FUNCTION = 3
WHICH_RUN = 1
NUM_ITERATIONS = 1000

N = 1000  # number of players
k = 10  # number of folks receiving feedback

#  Following-three are tweakable parameters
#  threshold to decide whether you will see feedbacks or not
l = 4
# if using constant values for Cost and Value of feedback for all players
C = 1
V = 10

# *****************
# Setting up frequency, cost, value arrays

# frequency of providing feedback
f = [0.00] * N
# cost of providing feedback fpr "i"th player
c = [0] * N
# value of feedback of "i"th player
v = [0] * N
# payoff_value for players
payoff = [0] * N
# introducing fitness to take over from payoff
fitness = [0] * N

# ******************
# Setting up logging
# I use log.info to print to the outputs file (to maintain record for
# graphs and oversee results in general), and debug to well.. debug
# TODO-make it consistent (debug vs info)

# filename='graphs_outputs/outputs'+'-l='+str(l)+'-V='+str(V)+'-N='+str(N)+'-fitness='+str(WHICH_FITNESS_FUNCTION)+'-ITER='+str(NUM_ITERATIONS)+'_1.TEXT',
PRINT_STRING = '-diminish-value-l='+str(l)+'-V='+str(V)+'-N='+str(N)+'-fitness='+str(WHICH_FITNESS_FUNCTION)+'-ITER='+str(NUM_ITERATIONS)+'_'+str(WHICH_RUN)
log.basicConfig(
    filename='graphs_outputs/outputs'+PRINT_STRING+'.TEXT',
    level=log.DEBUG,
    format=' %(message)s',
    filemode='w')
# format='%(asctime)s - %(levelname)s - %(message)s')
# log.debug('This is a log message.')

log.info("***********************")

# *************************
# populate all the values above
for i in range(0, N):
    # TODO-this f[i] expression is way too complicated, but lazy
    f[i] = round(m.floor((i)*10.0/N)*(0.1), 1)  # hack to ensure fractional
    # part is taken
    # log.debug(f[i])
    # print(f[i])
    c[i] = C
    v[i] = V

# count of how many feedbacks has "i"th player received
count = [0] * N
# value of feedbacks received by "i"th player
value = [0.00] * N
# cost incurred by "i"th in providing feedback
cost = [0.00] * N

# TODO-remove all variables not being used
# Store sum of payoffs and people kicked out to see correlations
sums_all = [0] * NUM_ITERATIONS
kicked_all = [-1] * NUM_ITERATIONS
replacers = [-1] * NUM_ITERATIONS
final_freq_matrix = [-1] * NUM_ITERATIONS
for i in range(0, NUM_ITERATIONS):
    final_freq_matrix[i] = [-1] * N

# ***********************
# Metrics used
metric_pass_l_threshold = [0] * NUM_ITERATIONS
metric_fail_l_threshold = [0] * NUM_ITERATIONS

# *******
# Create a matrix of who gives feedback to whom - To preseve the condition that
# everyone receives just as many feedbacks k*n matrix, so, i-th column denotes
# who receives feedback from i-th player Conditions: 1. Player cannot give
# feedback to self 2.In one round, any player should only receive k feedbacks
# (fromk unique players)
# TODO-need to meet these conditions
feedback_matrix = [-1] * k
for i in range(0, k):
    feedback_matrix[i] = [-1] * N

for i in range(0, k):
    for j in range(0, N):
        feedback_matrix[i][j] = j
    # v print feedback_matrix[i]

log.info("# # # # ")

feedback_flag = -1  # a value of 1 denotes that the list needs to be repermuted


def create_feedback_matrix():

    # creates
    for i in range(0, k):
        feedback_flag = 1
        while(feedback_flag == 1):
            feedback_matrix[i] = np.random.permutation(N)
            # print "permuuuuuu", feedback_matrix[i]
    # TODO-check if same number has been assigned by chance
            for jj in range(0, N):
                # TODO-ensure that you dont give feedback to same player across
                # rounds TODO-this  wrong feedbakc matrix crap needs to be
                # fixed
                cur_list = [-1] * (i+1)
                for iii in range(1, i+1):
                    cur_list[iii] = feedback_matrix[iii-1][jj]  # this list
                    # contains the elements chosen for the same player so far
                # v print "!!!!!!!"
                bool_check = feedback_matrix[i][jj] in cur_list
                # v print cur_list, feedback_matrix[i][jj], bool_check

                # v print "!!!!!"
                if((feedback_matrix[i][jj] == jj) or bool_check):  # jj player
                    # cannot provide feedback to itself
                    # v print bool_check
                    feedback_flag = 1
                else:
                    feedback_flag = 0

# *************************************
# Introducing different fitness functions

# WHICH_FITNESS_FUNCTION= 0, useless really


def fitness_mirror(pay):
    # trivial - just returns the same value - only doing to get basic case
    # running print "fitness_mirror"
    return pay

# WHICH_FITNESS_FUNCTION= 1, actually implemented in code itself as payoff


def fitness_linear_fit(pay):
    # fitness = payoff + c (where c is the minimum to be added to make all
    # payoffs non-negative)
    # idea: this fitness function
    print "fitness_linear_fit"
    # TODO-this is the complicated part - pull in code from existing main code

# TODO-how do you decide epsilon
epsilon = 0.001
# WHICH_FITNESS_FUNCTION=2, # TODO-implement


def fitness_epsilon_factor(pay):
    # fitness = 1 + w * payoff (where w is epsilon, a very small number)
    # idea: this fitness function reduces the dependence on payoff
    # print "fitness_epsilon_factor"
    return 1 + epsilon*pay

# WHICH_FITNESS_FUNCTION=3


def fitness_exp(pay):
    # fitness = exp(payoff)
    # idea: this fitness function accentuates the difference between payoffs -
    # expect to be BLOWN! print "fitness_exp"
    # print pay
    # TODO-we should not have a by 10 factor in general - ask Krish - also
    # adding a constant
    return m.exp((pay))

# ************************************

# Main loop in which all the action happens:
#  a new feedback matrix is created for every iteration .. and yadayada
# TODO-fix above comment
# TODO-fix loop var names - pretty arbit right now
for ii in range(0, NUM_ITERATIONS):
    # print "ITERATION # # # # # # # # # # ", ii
    create_feedback_matrix()  # create new feedback matrix for every iteration
    # All the smartness is in create_feedback_matrix - I shouldnt need to do
    # any checks below
    for i in range(0, N):  # for every player, decide whom would it give
        # feedback to
        # chosen_few = [-1] * k  # choose k number of recipients randomly to
        # provide feedback to
        for j in range(0, k):
            chosen = feedback_matrix[j][i]  # TODO-clean this code, just lazy
            # chosen_few[j] = chosen
            count[chosen] += 1  # increment number of feedback received by
            # chosen
            # TODO-introduce count dependent value
            value[chosen] += f[i]*v[i]*(1.0/count[chosen])  # increment value
            # of feedbacks received by chosen
            cost[i] += c[i]*f[i]  # cost incurred to "i"th player in providing
            # feedback
            # print count[chosen], value[chosen], cost [i], "count, value, cost
            # new"
        # v print i, "   ", chosen_few
    # print feedback_matrix

    # TODO - all the above need to be reset to zero at the end of loop and
    # beginning of next step

    #  randomly selecting player to die
    die_player = randint(0, N-1)
    sum_p = 0
    sum_fitness = 0

    # calculating payoff values in payoff[i]
    for i in range(0, N):
        if (cost[i] >= l):
            # then the player crosses our threshold of providing feedback
            payoff[i] = value[i] - cost[i]
            metric_pass_l_threshold[ii] += 1
        else:
            payoff[i] = 0 - cost[i]
            metric_fail_l_threshold[ii] += 1
        sum_p += payoff[i]
    # print "number of players who passed and failed threshold are",
    # metric_pass_l_threshold[ii], metric_fail_l_threshold[ii]

    # print "ii and payoff matrix", ii, payoff

    # TODO-fix sum_p when you account for taking out die_player from the
    # distribution sum_p = sum_p - p[die_player] # take die_player out of
    # probability distribution
    # # print sum_p, "<-- sum_p"
    # print fitness
    log.debug(str(ii))
    '''
    print "prev feq",final_freq_matrix[ii-2]
    print "freq", f
    print "value", value
    print "cost", cost
    print payoff
    '''
    if (WHICH_FITNESS_FUNCTION == 0):
        print "does not work"
        break
        # for i in range(0, N):
        # fitness[i] = fitness_mirror(payoff[i])
    # if (WHICH_FITNESS_FUNCTION== 1): # No need to add this case
        # print "goes to normal part of code - payoffs not fitness"
        # break
    if (WHICH_FITNESS_FUNCTION == 2):
        for i in range(0, N):
            fitness[i] = fitness_epsilon_factor(payoff[i])
            # TODO-check if above works
    if (WHICH_FITNESS_FUNCTION == 3):
        for i in range(0, N):
            fitness[i] = fitness_exp(payoff[i])
            if fitness[i] <= 0:
                print "FITNESS NEGATIVE"
                break
    # TODO-check if fitness is actually positibe or not
    # # print "ii and fitness", ii, fitness

    # choosing new die_player using a prob distribution over existing players
    # TODO-not doing it entirely correctly now, since the two end points (min
    # and max) have almost no chance of being chosen - How to fix Payoffs can
    # be negative: implies that the number line needs to be chosen wisely
    min = 0
    max = 0
    for i in range(0, N):
        # TODO-possible bug here with the die_player being included, but
        # doesn't affect result at our scale
        # if(i!=die_player):
        if payoff[i] < payoff[min]:
            min = i
        if payoff[i] > payoff[max]:
            max = i
        # logging.debug(payoff[i])
        # else:
            # print "Did not enter"
            # print i,die_player,payoff[die_player]
    # l log.debug("max and min payoffs are")
    # l log.debug("'{0}', '{1}'".format(payoff[max], payoff[min]))
    # Now we have the players with min and max payoffs, so divide up the number
    # line

    # TODO-just crapy hacky code - need to get graphs
    payoff_max = payoff[max]
    payoff_min = payoff[min]

    # modify payoff matrix itself to keep things easy - also recompute sum_p
    # (since it clearly changes)
    sum_p = 0
    for i in range(0, N):
        payoff[i] -= payoff_min
        sum_p += payoff[i]

    # l log.debug("new_shifted_payoff")
    # print("new_shifted_payoff")
    # l log.debug(payoff)
    # print(payoff)

    # TODO-IMP--pull the above code inside linear fitness - later, if needed
    # TODO-just transform the payoff into fitness

    for i in range(0, N):
        sum_fitness += fitness[i]
    # # print "sum_fitness and ii", ii, sum_fitness

    # TODO-currently the dist_array includes the current die_player, this needs
    # to be tweaked out - but it's okay right now  - easy to fix later - not
    # imp at our scale of N
    # TODO-At this point i am assuming that the fitness
    # returned will be positive, so I can do the following simply
    distr_array = [0] * N  # this array stores the end-point for ith player to
    # be chosen

    if (WHICH_FITNESS_FUNCTION == 1):
        distr_array[0] = payoff[0]  # fitness[0]
        for i in range(1, N):
            distr_array[i] = distr_array[i-1] + payoff[i]  # fitness[i]
    else:
        # # print "fitness=3"
        distr_array[0] = fitness[0]
        for i in range(1, N):
            distr_array[i] = distr_array[i-1] + fitness[i]  # payoff[i]

    # # print "distr_array is ", distr_array

    # check to see if distr_array is correct - this should match wiht payoff
    # matrix values

    # for i in range(0,N-1):
    #    print distr_array[i+1] - distr_array[i]

    # now get a random number in the range of the number line (0,sum_p) and see
    # where it falls and chose die_player_new accordingly
    # die_player_new is basically one of the alie players who will replace
    # die_player
    if WHICH_FITNESS_FUNCTION == 1:
        toss = randint(0, int(sum_p))  # TODO-check this
    else:
        toss = randint(0, int(sum_fitness))
        # TODO-the else clause will cause problems

    # print "toss is", toss
    die_player_new = -1
    for i in range(0, N):
        if toss <= distr_array[i]:  # missing equality condition initially, led
            # to bug
            die_player_new = i
            break

    if die_player_new == -1:
        print "---------1"
        print toss, die_player
        break

    if sum_p == 0:
        print "sum_p is 0"
        print toss, die_player, die_player_new
        break

    # assign the die_player the chosen guys value
    f[die_player] = f[die_player_new]
    c[die_player] = c[die_player_new]
    v[die_player] = v[die_player_new]

    # now we have our new die_player
    # v print f[die_player], c[die_player], v[die_player], p[die_player],
    # "details of die_player now"

    # # # # log.debug("'{0}'".format(f), "entire freuqnecy array")
    # print count, "entire count array"

    # now, clear out the values for next iteration
    # TODO-maybe we want to store the round by round details - think?
    for i in range(0, N):
        value[i] = 0.0
        cost[i] = 0.0
        count[i] = 0.0

    sums_all[ii] = sum_p
    kicked_all[ii] = die_player
    replacers[ii] = die_player_new
    for xx in range(0, N):
        final_freq_matrix[ii][xx] = f[xx]
    # final_freq_matrix[ii] = f
    log.info("'{0}'".format(final_freq_matrix[ii]))


log.debug(metric_pass_l_threshold)
log.debug(metric_fail_l_threshold)
log.debug(final_freq_matrix)
log.debug("----")

for i in range(0, NUM_ITERATIONS):
    log.debug("'{0}', '{1}'".format(i, sums_all[i]))  # (i, sums_all[i])
    log.debug("'{0}', '{1}'".format(kicked_all[i], replacers[i]))
    log.debug("'{0}'".format(final_freq_matrix[i]))
    # print " |"
    # print " |"
    # print "\ /"


# ************
# Plots
import matplotlib.pyplot as pyplot
x = [-1] * NUM_ITERATIONS
for i in range(0, NUM_ITERATIONS):
    x[i] = i

pyplot.plot(x, metric_pass_l_threshold)
pyplot.xlabel("Number of Iterations: 0 to "+str(NUM_ITERATIONS-1))
pyplot.ylabel("Number of players who beat the threshold")
pyplot.title("Success against threshold vs number of iterations")
pyplot.savefig('graphs_outputs/success'+PRINT_STRING+'.png')

pyplot.clf()
pyplot.cla()
pyplot.close()

# TODO-freq_bars depend upon number "k" - DO NOT FORGET
freq_bars = [0] * NUM_ITERATIONS
for i in range(0, NUM_ITERATIONS):
    freq_bars[i] = [0] * k

# print final_freq_matrix
# print freq_bars

# Plots for frequency
for ii in range(0, NUM_ITERATIONS):
    for j in range(0, N):
        # print int(final_freq_matrix[ii][j]*k)
        freq_bars[ii][int(final_freq_matrix[ii][j]*k)] += 1
# print freq_bars

# to plot this
# TODO-show error bars/variance,
# currently showing average with all other iterations results
avg_freq = [0] * k
for i in range(0, k):
    for j in range(0, NUM_ITERATIONS):
        avg_freq[i] += freq_bars[j][i]
    avg_freq[i] *= 1.0/NUM_ITERATIONS  # Again, float hack

# print avg_freq
# print sum(avg_freq)

x_k = [-1] * k
for i in range(0, k):
    x_k[i] = i

pyplot.plot(x_k, avg_freq, color='green', linewidth="5.0")
pyplot.xlabel("Frequency bins: 0.0 to 0.9")
pyplot.ylabel("Number of players")
pyplot.title("Average and per-iteration number of players in every frequency" +
             "bin")
# print freq_bars
for i in range(0, NUM_ITERATIONS):
    width = i*(1.0/N)
    pyplot.plot(x_k, freq_bars[i], color='blue', linewidth=width,
                linestyle='dashed')  # , label=str(i))
    pyplot.savefig('graphs_outputs/graph'+PRINT_STRING+'.png')
