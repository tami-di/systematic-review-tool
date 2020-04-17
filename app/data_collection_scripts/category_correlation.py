from app import app, db
#import api.db_api as db_api
import requests

models = ['one to one like','power grid coupled','mapping','Inter network load transfer','multiple dependence',
          'mixed interactions','supply-chain','probability defined model','state dependent','directed support-dependence','Contagion/influence','antagonistic-dependent','geometric/spatial']
metrics = ['breaking-point','amount','cost','path length','probability','rate','time','performance']
studies = ['size of giant component',
           'coupling',
           'percolation',
           'targeted attacks',
           'capacity/load',
           'optimization',
           'cost',
           'avalanche',
           'cascading time',
           'recovery',
           'length',
           'genetic algorithm',
           'laplacian',
           'lifetime',
           'localized attaks',
           'Probability of failure',
           'delay',
           'Markov',
           'single net',
           'small cluster',
           'stability',
           'Probability of stop cascading failure',
           'PMF of the failure size',
           'components',
           'Information for attack',
           'neighbouring distribution',
           'Clustering coefficient',
           'Layer configuration',
           'evenness',
           'difference','Transmissibility','Antagonistic nodes','lattice dimension','size of second component']
networks = ['simulated','both']

tuples = []
categories_id = []

#for i in range(len(models)):
 #   for j in range(len(metrics)):
  #      for k in range(len(studies)):
   #         for l in range(len(networks)):
  #      k = -1
   #     l = -1
               # tuples.append([i,j,k,l])
#for k in range(len(studies)):
 #   for l in range(len(networks)):
  #      tuples.append([-1,-1,k,l])
#for i in range(len(models)):
 #   for j in range(len(metrics)):
        #for k in range(len(studies)):
for l in range(len(studies)):
    tuples.append([-1,-1,l,-1])
results_dictionary = {}


def query(tuples, results_dictionary):
    for index_list in tuples:
        request_dictionary = {'accept-new-data': u'',
                                'search-abstract': u'',
                                'search-authors': u'',
                                'search-code-name': u'',
                                'search-library': u'',
                                'search-metric-description': u'',
                                'search-metric-has-type': u'',
                                'search-metric-name': u'',
                                'search-metric-parameters': u'',
                                'search-model-description': u'',
                                'search-model-has-inter-interaction': u'',
                                'search-model-has-intra-interaction': u'',
                                'search-model-has-model-type': u'',
                                'search-model-name': u'',
                                'search-network-tested-description': u'',
                                'search-network-tested-name': u'',
                                'search-proposes-model-description': u'',
                                'search-proposes-model-name': u'',
                                'search-source': u'',
                                'search-study-description': u'',
                                'search-study-name': u'',
                                'search-summary': u'',
                                'search-title': u'',
                                'search-year': u''}
        key = ""
        if index_list[0] != -1:
            key += "." +str(models[index_list[0]])
            request_dictionary['search-model-has-model-type'] = u''+ str(models[index_list[0]])
        if index_list[1] != -1:
            key += "." + str(metrics[index_list[1]])
            request_dictionary['search-metric-has-type'] = u'' + str(metrics[index_list[1]])
        if index_list[2] != -1:
            key += "." + str(studies[index_list[2]])
            request_dictionary['search-study-name'] = u'' + str(studies[index_list[2]])
        if index_list[3] != -1:
            key += "." + str(networks[index_list[3]])
            request_dictionary['search-network-tested-name'] = u'' + str(networks[index_list[3]])

        r = requests.post("http://localhost:5000/search",data=request_dictionary)
        amount_of_papers = r.content.count("\"abstract\":") - 1

        #key = str(models[index_list[0]])+ "." + str(metrics[index_list[1]]) + "." + str(studies[index_list[2]]) + "." + \
         #     str(networks[index_list[3]])
        results_dictionary[key] = amount_of_papers

query(tuples, results_dictionary)
sum = 0
index = 0
print "\pbox{0.3\\textwidth}{Estudio} & \pbox{0.3\\textwidth}{Tipo de redes de testeo} & \pbox{0.4\\textwidth}{Citas} \\\\ \hline"
for key, value in sorted(results_dictionary.iteritems(), key=lambda (k,v): (v,k),reverse=True):

    if value is not 0:
        index += 1
        sep_key = key.split(".")
        #print "\pbox{0.3\\textwidth}{\\vspace{0.1cm}"+sep_key[1] +"\\vspace{0.1cm}} & \pbox{0.3\\textwidth}{\\vspace{0.1cm}"+sep_key[2]+"\\vspace{0.1cm}} & \pbox{0.4\\textwidth}{\\vspace{0.1cm}\cite{"+str(value)+"}\\vspace{0.1cm}} \\\\ \hline"
        value_2 = str(round(int(value)*100.0/79,2))
        print "%s: %s" % (key, value)
        sum+=int(value)
print sum, index

