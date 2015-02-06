import random

from deap import base
from deap import creator
from deap import tools

def gen(cropList, ls):
    landSize=int(ls)

    #global variables
    maxCropSize =landSize
    numCrops= len(cropList)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register("attr_bool", random.randint, 0, maxCropSize)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual,
        toolbox.attr_bool, numCrops)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # def penalty(diff):
    #     diff=diff*2
    #     return diff

    def evalOneMax(individual):
        total = 0
        indiSum = 0
        for x in range(numCrops):
            total += individual[x] * int(cropList[x].price)
            indiSum += individual[x] * cropList[x].size

        if indiSum > landSize:
                return 0,

        return total,

    toolbox.register("evaluate", evalOneMax)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    def main():
        pop = toolbox.population(n=200)
        cxpb =0.6
        mupb =0.01
        ngen =300
        g =1
        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))

        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # Begin the evolution
        for g in range(ngen):
            print("-- Generation %i --" % g)
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < mupb:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

                    # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < mupb:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            pop[:] = offspring

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]

            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5

            # print("  Min %s" % min(fits))
            # print("  Max %s" % max(fits))
            # print("  Avg %s" % mean)
            # print("  Std %s" % std)
        json = ""
        sortedPop = sorted(pop, key=lambda ind:ind.fitness)
        for y in range(3):
            current =sortedPop[y]
            json+='{'
            for x in range(len(current)):
                if current[x] > 0:
                    p=current[x]*cropList[x].price
                   # json += '"name'+str(x+1)+'":'+str(cropList[x].name)+', "price'+str(x+1)+'":'+str(p)+',"amount'+str(x+1)+'":'+str(cropList[x].price)
                    json += 'name'+str(x+1)+':'+str(cropList[x].name)+', price'+str(x+1)+':'+str(p)+',amount'+str(x+1)+':'+str(cropList[x].price)
            json+='},'
        print json
        return json

    return main()