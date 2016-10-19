#All abilities are the intellectual property of Jagex Ltd.
#Program copyright 2016 Hebisonic

import math
import time

start_time = time.process_time()

#format: (cooldown in ticks, average ability dmg as percentage, duration in ticks)

abilities = {                   #dictionary of all abilities with their cooldowns, average dmg, and duration
        "sever"                 : (25, 112.8, 3),       
        'slice'                 : (5, 75, 3),           
        "dismember"             : (25, 120.6, 3),       
        "fury"                  : (9, 147.6, 6),        
        "barge"                 : (34, 75, 3),
        "smash"                 : (17, 75, 3),          
        "cleave"                : (12, 112.8, 3),       
        "havoc"                 : (17, 75, 3 ),         
        "decimate"              : (12, 112.8, 3),       
        "chain"                 : (17, 60, 3),          
        "combust"               : (25, 120.6, 3),       
        "dragonbreath"          : (17, 112.8, 3),       
        "impact"                : (25, 60, 3),          
        "wrack"                 : (5, 56.4, 3),         
        "corruptionblast"       : (25, 200, 3),
        "sonicwave"             : (9, 94.2, 3),         
        "concblast"             : (9, 147.6, 6),        
        "bindingshot"           : (25, 60, 3),          
        "fragshot"              : (25, 120.6, 3),       
        "piercingshot"          : (5, 56.4, 3),         
        "ricochet"              : (17, 60, 3),          
        "snipe"                 : (17, 172, 6),         
        "corruptionshot"        : (25, 200, 3),         
        "dazingshot"            : (9, 94.2, 3),         
        "needlestrike"          : (9, 99.2, 3),         
        "freedom"               : (50, 0, 3),
        "anticipate"            : (40, 0, 3),
        "provoke"               : (17, 0, 3),
        "preparation"           : (34, 0, 3),
        "resonance"             : (50, 0, 3),
        "escape/surge"          : (34, 0, 3),
        "siphon"                : (100, 0, 3),
        "bash"                  : (25, 144, 3),         
        "sacrifice"             : (50, 60, 3),          
        "tuskaswrath"           : (25, 60, 3)           
        }

melee_base = ["sever", "slice", "dismember", "fury", "barge"] #this and following lists are for assembling a list of proper permutations appropriate for combat style
melee_2h = ["smash", "cleave"]
melee_dual = ["havoc", "decimate"]

magic_base = ["chain", "combust", "dragonbreath", "impact", "wrack"]
magic_2h = ["sonicwave"]
magic_dual = ["concblast"]
        
range_base = ["bindingshot", "fragshot", "piercingshot", "ricochet", "snipe", "corruptionshot"]
range_2h = ["dazingshot"]
range_dual = ["needlestrike"]
        
zerodmg = ["freedom", "anticipate", "provoke", "preparation", "resonance", "escape/surge", "siphon"]
defence_shield = ["bash"]
cons_base = ["sacrifice", "tuskaswrath"]

def adv(cds, t): #function that decrements all cooldowns by relevant amount, but not less than 0
        cdst = list(map(lambda x: x-t if x >= t else 0, cds))
        return cdst
        
def simulate(bar, runtime): #function to simulate the usage of an action bar, and return whether or not it worked, as well as statistics about it
        t = 0
        cds = [0 for i in bar]
        uselist = [False for i in bar]
        ad = 0
        while t < runtime:
                try:
                        ablind = cds.index(0) #find leftmost ability in bar with cooldown of 0
                        if verbosity >= 2: #print extra information if verbosity levels are high enough
                            printinfo = bar[ablind] + " was used, put on cd, and contributed to avg. ability damage." if verbosity == 2 else bar[ablind] + " was used and put on a cooldown of " + str(abilities[bar[ablind]][0]) + " ticks after a duration of " + \
                                str(abilities[bar[ablind]][2]) + " ticks, adding " + str(abilities[bar[ablind]][1]) + "% avg. ability damage."
                            print(printinfo)
                except ValueError: #if no cooldown is 0, return that bar is broken with statistics
                        return ad/t, t, False, False not in uselist
                ad += abilities[bar[ablind]][1] #if bar works, set ability on appropriate cooldown and increment statistics by proper amounts
                cds[ablind] = abilities[bar[ablind]][0]
                cds = adv(cds, abilities[bar[ablind]][2])
                t += abilities[bar[ablind]][2]
                uselist[ablind] = True
        return ad/t, t, True, False not in uselist #if bar doesn't break, will return that bar works as well as its statistics

def simulateprec(bar, runtime): #same as simulate, but uses math.fsum to slightly increase precision
        t = 0
        cds = [0 for i in bar]
        uselist = [False for i in bar]
        ad = []
        while t < runtime:
                try:
                        ablind = cds.index(0)
                        if verbosity >= 2:
                            printinfo = bar[ablind] + " was used, put on cd, and contributed to avg. ability damage." if verbosity == 2 else bar[ablind] + " was used and put on a cooldown of " + str(abilities[bar[ablind]][0]) + " ticks after a duration of " + \
                                str(abilities[bar[ablind]][2]) + " ticks, adding " + str(abilities[bar[ablind]][1]) + "% avg. ability damage."
                            print(printinfo)
                except ValueError:
                        return math.fsum(ad)/t, t, False, False not in uselist
                ad.append(abilities[bar[ablind]][1])
                cds[ablind] = abilities[bar[ablind]][0]
                cds = adv(cds, abilities[bar[ablind]][2])
                t += abilities[bar[ablind]][2]
                uselist[ablind] = True
        return math.fsum(ad)/t, t, True, False not in uselist
        
if __name__ == "__main__":
        import argparse
        import itertools
        
        parser = argparse.ArgumentParser(description = 'Valid abilities for specification options are ' + str(list(abilities.keys())) + 
                                         "\n\nProgram will error out on specifications of zero damage abilities (" + str(zerodmg) + ") unless you specifically tell the program to include them with the respective option.")
        
        parser.add_argument("cbstyle", nargs = 1, choices = ['melee', 'mage', 'range']) #2 arguments to select combat style and wielding style respectively
        parser.add_argument("wieldstyle", nargs = 1, choices = ['2h', 'dual', '1hshld'])
        
        xopts = parser.add_argument_group("execution options") #options changing execution of the program
        xopts.add_argument("-t", "--t", type = int, default = 3000, help = "specify amount of ticks to run for calculating AADPT, default 3000")
        xopts.add_argument("-p", "--p", action = 'store_true', help = "enable precision AADPT calculation")
        xopts.add_argument("-v", "--v", action = 'count', help = "set verbosity level. Default only outputs final action bar, level one (-v/--v) prints results for each action bar as it's evaluated, \
            level two (-vv/--vv) additionally outputs abilities as they're used, and level three (-vvv/--vvv) additionally outputs numeric info about abilities as they're used")
        xopts.add_argument("-r", "--r", type = int, default = 1, help = "specify number of bar tiers to display at end in decreasing order of AADPT, default 1")
        
        bopts = parser.add_argument_group("action bar options") #options restricting the action bars possible to calculate
        bopts.add_argument("-e", "--e", nargs = '+', help = "specify required ability exclusions")
        bopts.add_argument("-i", "--i", nargs = '+', help = "specify required ability inclusions")
        bopts.add_argument("-rp", "--rp", nargs = 2, action = 'append', help = "specify required ability inclusions with their positions in the form 'ability 0-indexed-position'. Option can be specified multiple times")
        bopts.add_argument("-ml", "--ml", type = int, help = "set max bar length (must be at least 2)")
        bopts.add_argument("-z", "--z", nargs = '+', help = "specify inclusion of specified 0 damage ability or abilities, recommended against use for execution time unless you are going to force inclusion of specified abilities")
        
        arguments = parser.parse_args()

        cb = arguments.cbstyle
        wld = arguments.wieldstyle
        runtime = arguments.t
        prec = arguments.p
        rankings = arguments.r
                
        if arguments.e:
                excl = arguments.e
        else:
                excl = None
                
        if arguments.i:
            incl = arguments.i
        else:
            incl = None
                                
        if arguments.rp:
                rpl = arguments.rp
        else:
                rpl = None
                
        if arguments.z:
                zeros = arguments.z
        else:
                zeros = None
                
        if arguments.v != None:
            verbosity = arguments.v if arguments.v <= 3 else 3
        else:
            verbosity = False

        permulist = []
        if 'range' in cb: #generate list of abilities eligible for action bar
                permulist += range_base
                if '2h' in wld:
                        permulist += range_2h
                elif 'dual' in wld:
                        permulist += range_dual
        elif 'melee' in cb:
                permulist += melee_base
                if '2h' in wld:
                        permulist += melee_2h
                elif 'dual' in wld:
                        permulist += melee_dual
        else:
                permulist += magic_base
                if '2h' in wld:
                        permulist += magic_2h
                elif 'dual' in wld:
                        permulist += magic_dual
        if '1hshld' in wld:
                permulist += defence_shield
        permulist += cons_base
        if zeros != None:
                permulist += zeros

        if excl != None: #remove abilities that user has specified are not to be used
                permulist = [i for i in permulist if i not in excl]

        permulen = arguments.ml if arguments.ml != None else len(permulist) if len(permulist) <= 9 else 9 #restrict maximum permutation length if user specified, else maximum permutation length is number of available abilities available but not more than 9
        permu = []
        for i in range(1, int(permulen) + 1): #generate all ability bar permutations
                permu += (list(itertools.permutations(permulist, i)))

        if rpl != None: #if user specified that a specific ability must be in a specific spot, remove all ability bars that don't match that criteria
            for spec in rpl:
                permu = [i for i in permu if len(i) >= len(rpl)]
                permu = [i for i in permu if i[int(spec[1])] == spec[0]]
        
        if incl != None:
            permu = [i for i in permu if set(incl) <= set(i)]

        barlist = []
        AADPTlist = []
        for testbar in permu: #test action bars. If they work, add them to a list of ones that worked with a matching index entry of their avg. damage in another list
                if not prec:
                    AADPT, bartime, stable, abilsused = simulate(testbar, runtime)
                else:
                    AADPT, bartime, stable, abilsused = simulateprec(testbar, runtime)
                if verbosity:
                    print(testbar, "| T =", bartime, "| Stable =", stable, "| AADPT =", str(AADPT) + "%")
                if stable and abilsused:
                        barlist.append(testbar)
                        AADPTlist.append(AADPT)

        try:
            AADPTmax = max(AADPTlist) #find and print best bar from the list
            maxbar = barlist[AADPTlist.index(AADPTmax)]
            print(''.join(['='*79]))
            print("The highest AADPT bar meeting the specifications was " + str(maxbar) + " with an AADPT of " + str(AADPTmax) + "%.")
            AADPTlist.remove(AADPTmax)
            barlist.remove(maxbar)
            while AADPTmax in AADPTlist:
                maxbar = barlist[AADPTlist.index(AADPTmax)]
                print()
                print("Tied with " + str(maxbar))
                AADPTlist.remove(AADPTmax)
                barlist.remove(maxbar)
            rankings -= 1
            while rankings > 0:
                print(''.join(['-'*79]))
                try:
                    AADPTmax = max(AADPTlist)
                    maxbar = barlist[AADPTlist.index(AADPTmax)]
                    print("The next best bar was " + str(maxbar) + " with an AADPT of " + str(AADPTmax) + "%.")
                    AADPTlist.remove(AADPTmax)
                    barlist.remove(maxbar)
                    while AADPTmax in AADPTlist:
                        maxbar = barlist[AADPTlist.index(AADPTmax)]
                        print()
                        print("Tied with " + str(maxbar))
                        AADPTlist.remove(AADPTmax)
                        barlist.remove(maxbar)
                    rankings -= 1
                except ValueError:
                    print(''.join(['-'*79]))
                    print("There was no more stable action bars meeting the specifications.")
                    rankings = 0
            print()
            print("--- {} seconds ---".format(time.process_time() - start_time))
            print(''.join(['='*79]))
        except ValueError:
            print("There was not a stable action bar meeting the specifications!")
                
