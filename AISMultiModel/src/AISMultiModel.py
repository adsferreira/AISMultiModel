from multiprocessing import Process, Pipe
from itertools import izip
from time import time, strftime, localtime
import subprocess
import numpy as np
from ainet_validation import OptAiNetUtils

def spawn(f):
    def fun(pipe, x):
        pipe.send(f(x))
        pipe.close()
    return fun

def parmap(f, X):
    pipe = [Pipe() for x in X]
    proc = [Process(target = spawn(f), args=(c, x)) for x,(p, c) in izip(X, pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [p.recv() for (p, c) in pipe]

class AISMultiModel:
    def __init__(self, Abs, nr_centers, nr_Ab, nr_clones, nr_gen, beta, d, x_bounds, y_bounds, dim):
        self.nr_centers = nr_centers
        self.nr_models = len(self.nr_centers)
        self.nr_Ab = nr_Ab
        self.nr_clones = nr_clones
        self.nr_gen = nr_gen
        self.beta = float(beta)
        self.d = d
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.dim = dim
        self.nr_attr = self.nr_centers * dim + self.nr_centers
        self.pm = np.array([float(1.0) for _ in self.nr_centers])
        self.pm_q = np.divide(float(1), self.nr_attr) ** (float(1) / self.nr_gen)
        self.fit = np.empty([self.nr_models, self.nr_Ab])
        self.opt_ainet_utils = OptAiNetUtils()
        self.best_ids = np.array([[0 for _ in range(self.nr_Ab)] for _ in self.nr_centers])
        self.stable_ab_counter = np.array([[int(0) for _ in range(self.nr_Ab)] for _ in self.nr_centers])
        #self.pm_cell = [[self.pm for _ in range(self.nr_Ab)] for _ in self.nr_centers]
        self.beta_cell = np.array([[self.beta for _ in range(self.nr_Ab)] for _ in self.nr_centers])
        # matrix of memory cells and respective clones for every model
        self.Absc = [[[[0. for _ in range(c * dim + c)] for _ in range(nr_clones + 1)] for _ in range(nr_Ab)] for c in nr_centers]
        self.clones_fit = [[[0. for _ in range(nr_clones + 1)] for _ in range(nr_Ab)] for _ in range(self.nr_models)]         
        if len(Abs) == 0:
            # memory cells for each model of photonic crystal
            self.Abs = [[[0. for _ in range(c * self.dim + c)] for _ in range(self.nr_Ab)] for c in self.nr_centers] 
                           
            for i in range(self.nr_models):
                while True:
                    # initial population of antibodies Ab for model i
                    self.init_antibodies(i)
                    Ab_t = self.index_antibodies(self.Abs[i], self.nr_centers[i])                
                    
                    if __name__ == '__main__':                    
                        self.fit[i] = parmap(self.fitness, Ab_t)
                       
                    print "Initial population %d: %d centers\n" % (i, self.nr_centers[i])
                    self.print_ab_fit(self.Abs[i], self.fit[i])
                    print "------------------------------------"
                    # a maximum fit greater than zero is needed because it will be used as denominator
                    # fitness lesser or equals 1.0 may represent false-positive band gaps
                    if max(self.fit[i]) > 0.0:
                        break 
        else:
            self.Abs = Abs
            
            for i in range(self.nr_models):
                Ab_t = self.index_antibodies(self.Abs[i], self.nr_centers[i])
            
                if __name__ == '__main__':                    
                    self.fit = parmap(self.fitness, Ab_t)
            
                self.print_ab_fit(self.Ab, self.fit) 
    
    def init_antibodies(self, id_model):
        # for the problem of photonic crystal, we have a set of centers and related radii of a unit cell
        # centers and radii have different ranges in initialization, so we need to set them separately
        # center is represented in 2D 
        c_nr_centers = self.nr_centers[id_model] 
        for j in range(self.nr_Ab):
            # all antibodies must respect the bounds of the domain
            while True:                    
                centers = np.random.uniform(self.x_bounds[0], self.x_bounds[1], [c_nr_centers * self.dim])
                radii = np.random.uniform(0, self.x_bounds[1], [c_nr_centers])
                self.Abs[id_model][j] = np.concatenate((centers, radii))               
                    
                is_inside_bounds = self.opt_ainet_utils.is_inside_bounds(self.Abs[id_model][j],   \
                                                                         self.x_bounds[0],        \
                                                                         self.x_bounds[1],        \
                                                                         self.y_bounds[0],        \
                                                                         self.y_bounds[1],        \
                                                                         c_nr_centers,            \
                                                                         self.dim)
                if (is_inside_bounds):                    
                    break
    
    def index_antibodies(self, Ab, c_nr_centers):
        # antibody collection to be indexed
        Ab_t = [[0. for _ in range((c_nr_centers * self.dim) + c_nr_centers + 1)] for _ in range(len(Ab))]
        # generate indexes for every antibody
        ids = np.arange(len(Ab))
        # set indexes for each antibody
        for (c_id, c_Ab) in zip(ids, Ab):
            Ab_t[c_id] = np.insert(c_Ab, 0, c_id, axis = 0)
        # indexed antibodies
        return Ab_t
    
    def fitness(self, Ab):
        # store the band gaps of the current photonic crystal
        c_bands = []    
        c_nr_center = (len(Ab) - 1) / (self.dim + 1)  
        tid = int(Ab[0])
        filename = "mpb/PBG" + str(c_nr_center) + "/phc_id_" + str(tid) + ".ctl"     
        center_lines, radius_lines = self.opt_ainet_utils.grep(filename, "center", "radius") 
        center_list, radius_list = self.opt_ainet_utils.split_attr(Ab[1:], (c_nr_center * self.dim), c_nr_center)  
        is_rod = True
            
        for j in range(c_nr_center):
            if (radius_list[j] <= 0.0):
                is_rod = False
         
        if (is_rod):
            # before run MPB, write the corresponding file
            self.opt_ainet_utils.write(filename, center_lines, radius_lines, center_list, radius_list)
            # call MPB
            p_mpb = subprocess.Popen(['mpb', filename], stdout = subprocess.PIPE)
            out_mpb, mpb_err = p_mpb.communicate()
                                
            # search for a 'Gap' word in mpb's output
            if "Gap" in out_mpb:
                v_out = out_mpb.split("Gap")
                #print v_out
                                         
                for j in range(len(v_out) - 1):
                    current_str = v_out[j + 1] 
                    begining = current_str.find(", ") + 2
                    end = current_str.find("%")
                    current_band = float(current_str[begining:end])
                    c_bands.append(current_band)
            else:
                c_bands.append(0.)   
                     
            # get the max band           
            band = max(c_bands)                 
        else:
            band = 0
                
        return band
        
    def clone_mut(self):
        # for each model 
        for i in range(self.nr_models):               
            print "\nPopulation %d: %d centers" % (i, self.nr_centers[i])
            nr_attr = self.nr_attr[i]
                                    
            # for each parent cell
            for j in range(self.nr_Ab):
                # store parent cell that will be evaluated as a clone one
                self.Absc[i][j][0] = self.Abs[i][j]
                # fitness of current cell and its clones
                self.clones_fit[i][j][0] = self.fit[i][j]
                
                print "----------------------------------------------------------------"
                print "cloning parent cell: %d - beta: %0.3f - pm: %0.3f - stb: %d...\n" % (j, self.beta_cell[i][j], self.pm[i], self.stable_ab_counter[i][j])         
                # counter of clones    
                k = 1
                
                while (k <= self.nr_clones):                
                    # all clones must respect the bounds of domain
                    while True:
                        # make sure all genetic variation are zero before defining the attribute to be mutated
                        mut = np.zeros(nr_attr)
                        # outcome which determine if a attribute will be mutated or note
                        r = np.random.uniform(0, 1, nr_attr)
                        # attribute's indexes to be mutated
                        mut_ids = np.where(self.pm[i] > r)
                        # number of attributes to be mutated
                        nr_mut = np.array(mut_ids).shape[1]
                        # genetic variability of each attribute to be mutated
                        _alpha = np.exp(-(self.fit[i][j] / max(self.fit[i]))) / self.beta_cell[i][j]
                        gv = _alpha * np.random.standard_normal(size = nr_mut)
                        mut[mut_ids] = gv 
                        #print "mut: ", mut
                        Ab_mut = self.Abs[i][j] + mut
                        is_inside_bounds = self.opt_ainet_utils.is_inside_bounds(Ab_mut,             \
                                                                                 self.x_bounds[0],   \
                                                                                 self.x_bounds[1],   \
                                                                                 self.y_bounds[0],   \
                                                                                 self.y_bounds[1],   \
                                                                                 self.nr_centers[i], \
                                                                                 self.dim)
                                    
                        if is_inside_bounds:
                            self.Absc[i][j][k] = Ab_mut   
                            break                                   
                    
                    k = k + 1
                                
                Ab_t = self.index_antibodies(self.Absc[i][j][1:], self.nr_centers[i])
               
                if __name__ == '__main__':
                    self.clones_fit[i][j][1:] = parmap(self.fitness, Ab_t)        
            
                self.print_ab_fit(self.Absc[i][j], self.clones_fit[i][j])
                print "----------------------------------------------------------------"
          
    # select best individuals to form the memory cells' set
    def select(self):
        for i in range(self.nr_models):
            for j in range(self.nr_Ab):
                best_id = np.argmax(self.clones_fit[i][j])
                self.best_ids[i][j] = best_id
                # selecting best antibodies along the mutated ones
                self.Abs[i][j] = self.Absc[i][j][best_id]
                self.fit[i][j] = self.clones_fit[i][j][best_id]
     
    def count_stable_ab(self):
        # best indexes with value equal to zero means parents did not reproduce more affinity offsprings
        mask = self.best_ids == 0
        # counting up parents which still did not reproduce more affinity offsprings
        self.stable_ab_counter[mask] += 1
        # set to zero parents which reproduced better offsprings
        self.stable_ab_counter[-mask] = 0
                   
    def replace(self):
        # search for antibodies with lower affinities
        #low_aff = zip(*np.where(self.fit == 0.0))
        d_lowest = np.argpartition(self.fit, self.d)[:, :self.d]
        new_Abs = []
        # antibody indexes
        i = 0
        
        for i_m in range(d_lowest.shape[0]):
            c_nr_centers = self.nr_centers[i_m]
            new_Ab = np.empty([(c_nr_centers * self.dim) + c_nr_centers])
             
            for _ in range(self.d):                
                while True:                    
                    centers = np.random.uniform(self.x_bounds[0], self.x_bounds[1], [c_nr_centers * self.dim])
                    radii = np.random.uniform(0, self.x_bounds[1], [c_nr_centers])
                    new_Ab = np.concatenate((centers, radii))               
                    
                    is_inside_bounds = self.opt_ainet_utils.is_inside_bounds(new_Ab,           \
                                                                             self.x_bounds[0], \
                                                                             self.x_bounds[1], \
                                                                             self.y_bounds[0], \
                                                                             self.y_bounds[1], \
                                                                             c_nr_centers,     \
                                                                             self.dim)
                    if (is_inside_bounds):   
                        new_Ab = np.append(i, new_Ab)    
                        new_Abs.append(new_Ab)     
                        i += 1        
                        break
            
        # obtain the new antibodies' fitness
        fit_new_Abs = np.empty([len(new_Abs)])
        if __name__ == '__main__':
            fit_new_Abs = parmap(self.fitness, new_Abs)  
            
        # introduce the new antibodies into the memory cells and set their fitness correspondingly
        i = 0 # incomers' counter
        i_m = 0 # model's counter
        for m_d_lowest in d_lowest:
            for a_id in m_d_lowest:
                self.Abs[i_m][a_id] = new_Abs[i][1:]
                self.fit[i_m][a_id] = fit_new_Abs[i]
                # reset attribute elements for new antibodies
                self.beta_cell[i_m][a_id] = self.beta
                self.stable_ab_counter[i_m][a_id] = int(0)
                i += 1
            i_m += 1
      
    def define_mut_param(self, i):
        # stable antibodies have their fitness unchanged over generations, respecting a specific threshold
        stable_abs = np.where(self.stable_ab_counter == 3)
        # increases beta's values for antibody cells which have reached a steady state
        self.beta_cell[stable_abs[0], stable_abs[1]] *= 1.0618
        # reset stable antibodies counter
        self.stable_ab_counter[stable_abs[0], stable_abs[1]] = int(0)
        
        #update mutation probability
        self.pm = 1.0 * (self.pm_q ** i) 
        
          
    def search(self):   
        for i in range(self.nr_gen):
            print "----------------------------------------------------------------"
            print "Generation ", i + 1
            print "----------------------------------------------------------------"
            self.clone_mut()
            self.select()
            self.count_stable_ab()
            self.define_mut_param(i + 1)
            
            if ((i + 1) % 20) == 0:
                self.replace()
        
    def print_ab_fit(self, Ab, fit):
        for i in range(len(Ab)):
            rounded_Ab = np.around(Ab[i], decimals=3)
            rounded_fit = np.around(fit[i], decimals=3)
            print "cell " + str(i) + ": " + str(rounded_Ab) + " - fit: " + str(rounded_fit)

 
#r = np.random.uniform(0, 1, 6)
#vra1 = np.random.standard_normal(size=0)
# attribute's indexes to be mutated
#mut_ids = np.where(0.001 > r)
#ua = np.array(mut_ids).shape[1]
# beta_vec = []
# beta = 1
# i = 0
# min_beta = 300
# while (beta < min_beta):    
#     beta_vec.append(beta)
#     beta = beta * 1.0618
#     i += 1
#     
# import matplotlib.pyplot as plt
# plt.plot(beta_vec)
# plt.show()

# m = 300
# n = 300
# a_n = 1 / float(m)
# q = a_n ** (1 / float(n - 1))
# a_1 = 1
# 
# pm_vec = []
# for i in range(300):
#     a_i = a_1 * (q ** i)
#     pm_vec.append(a_i)
#     
# import matplotlib.pyplot as plt
# plt.plot(pm_vec)
# plt.show()

Abs = []
dim = 2
nr_centers = np.array([2, 3])
print "number of centers for each unit cell: ", nr_centers
print "number of populations: ", len(nr_centers)
nr_Ab = 2
print "Number of individuals per population: ", nr_Ab
nr_clones = 1
print "number of clones per individual: ", nr_clones
nr_gen = 22
print "number of generations: ", nr_gen
beta = 1
print "beta value: ", beta
d = 1
print "number of low affinity antibodies to be replaced: ", d
x_bounds = [-0.5, 0.5]
print "bounds in x-axis: ", x_bounds
y_bounds = x_bounds
print "bounds in y-axis: ", y_bounds
print "-----------------------------------------"
print strftime("Started on: %a, %d %b %Y %H:%M:%S", localtime())
print "-----------------------------------------"
start = time()
ais = AISMultiModel(Abs, nr_centers, nr_Ab, nr_clones, nr_gen, beta, d, x_bounds, y_bounds, dim)
ais.search()
print "-----------------------------------------"
print "\nElapsed runtime: %f" % (time() - start)
print "-----------------------------------------"
print strftime("Finished on: %a, %d %b %Y %H:%M:%S", localtime())