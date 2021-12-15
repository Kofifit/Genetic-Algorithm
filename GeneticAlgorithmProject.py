# Part 1

import random
import copy


class codonObject:
  def __init__(self,empty=False):
    self.empty = empty
    if self.empty==False:
      self.codon=codonObject.createCodon(self)
    else:
      self.codon=codonObject.createEmptyCodon(self)

  def __repr__(self):
    return str(self.codon)

  def createCodon(self): 
    '''creating a random codon'''
    Nucleotides=['A','T','C','G']
    num=0
    codon=[]
    while num<3:
      codon.append(Nucleotides[random.randrange(4)])
      num+=1
    return codon

  def createEmptyCodon(self):
    '''creating an empty codon, for later use'''
    num=0
    codon=[[]]
    while num<2: 
      codon.append([])
      num+=1
    return codon

# Part 2

class strandObject:
    def __init__(self,empty=False):
        self.empty=empty
        self.fitnessValue = 0
        self.sumValue = 0
        self.length=12 #default length. can be changed by demand
        self.codonNum=int(self.length/3)
        self.doubleStrand=[strandObject.createStrand(self),strandObject.createStrand(self)]        
      
    def __repr__(self):
      return str(self.doubleStrand[0])+'\n'+str(self.doubleStrand[1])

    def createStrand(self):
      strand=[]
      for i in range(self.codonNum):
        if self.empty==False:
          c=codonObject()
        else:
          c=codonObject(empty=True)
        strand.append(c)
      return strand

    def mutation(self):
        Nucleotides=['A','T','C','G']
        i=0
        while i<1:
          randStrand = random.randrange(2)
          randCodon = random.randrange(int(self.codonNum))
          randBase = random.randrange(3)
          newBase = Nucleotides[random.randrange(4)]
          self.doubleStrand[randStrand][randCodon].codon[randBase] = newBase
          i+=1
   
# Part 3

nucleotideDict={'A':'T','T':'A','C':'G','G':'C'} #to check whether the nucleotides matching is correct
posCodons=[['C', 'G', 'T'] ,['C', 'G', 'C'], ['C', 'G', 'A'], ['C', 'G', 'G'], ['A', 'G', 'A'], ['A', 'G', 'G'], ['C', 'A', 'T'], ['C', 'A', 'C'], ['A', 'A', 'A'], ['A', 'A', 'G']]##codons for posotive ACs: arginine, histidine and lysine # Part 4

class geneticAlgorithm():

    def __init__(self):
        self.population = []
        for i in range(100):
            newStrand = strandObject()
            self.population.append(newStrand)

    def __repr__(self):
      string=''
      for double_strand in self.population:
        string+=str(double_strand.doubleStrand[0])
        string+='\n'
        string+=str(double_strand.doubleStrand[1])
        string+='\n\n'
      return string


    def selection(self):
        sum =self.fitness()
        setPoint = random.randint(0,int(sum))
        for s in self.population:
            if int(s.sumValue) >= setPoint:
                return s

    def fitness(self):
        sum = 0
        for double_strand in self.population:
            fit_match = 0
            fit_positive = 0
            codonCounter=0

            for c in range(double_strand.codonNum): #changed to general number..
                counter = 0
                codon1 = double_strand.doubleStrand[0][c]
                codon2 = double_strand.doubleStrand[1][c]

                for b in range(3):
                    if codon2.codon[b] == nucleotideDict[codon1.codon[b]]:                      
                        fit_match += 1 
                        counter += 1
                    
                if counter == 3 or counter == 2:
                    fit_match += counter
                    if counter == 3:
                      codonCounter+=1
                      if codon1.codon in posCodons or codon2.codon in posCodons:           
                        fit_positive += 15

            if codonCounter == 2 or codonCounter == 3:
              fit_match += (codonCounter-1)*5
            elif codonCounter == 4:
              fit_match += codonCounter*5
                                       
            fitness = fit_match+fit_positive           
            sum += fitness 
            double_strand.fitnessValue = fitness
            double_strand.sumValue=sum 
        return sum

    def crossover(self):
        parent1=geneticAlgorithm().selection()
        parent2=geneticAlgorithm().selection()
        offspring=strandObject(empty=True)
        
        #update the offspring
        randCodon=random.randint(0,parent2.codonNum) #random index for the parent's codon
        for strand in range(2):
          randNuc=random.randrange(3)
          codonIndex=0
          for codon in range(offspring.codonNum):
            if codonIndex<randCodon:
              offspring.doubleStrand[strand][codon].codon=parent1.doubleStrand[strand][codon].codon
              codonIndex+=1
            else:
              offspring.doubleStrand[strand][codon].codon=parent2.doubleStrand[strand][codon].codon
              codonIndex+=1
        return offspring

    def nextGeneration(self):
      self.fitness()
      newPopulation=[]
      newPopulation.append(self.bestDoubleStrand())
  
      for ds in range(1,100): 
        new_ds=self.crossover()
        new_ds.mutation()
        newPopulation.append(new_ds)
      self.population=copy.deepcopy(newPopulation)
      self.fitness() #update the fitness score 
      return newPopulation

    def bestDoubleStrand(self):
      bestIndex=0
      for ds in range(1,100):
        if self.population[ds].fitnessValue>self.population[bestIndex].fitnessValue:
          bestIndex=ds
      bestDoubleStrand=self.population[bestIndex]
      return bestDoubleStrand

# Part 4
dna = geneticAlgorithm()
for i in range(0,100):
    dna.nextGeneration()
    print(dna.bestDoubleStrand().fitnessValue)
    print(dna.bestDoubleStrand())
dna.bestDoubleStrand()
print(dna.bestDoubleStrand().fitnessValue)
print(dna.bestDoubleStrand())


