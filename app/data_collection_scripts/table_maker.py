__author__ = 'ivana'
from app import db
from test_file import *
import app.api.db_api as db_api

models = ["One to one like",
          "Geometric or spatially embedded",
          "Multiple dependencies",
          "Coupled power grid",
          "Load transfer among networks",
          "Mixed interactions",
          "Directed support-dependency",
          "Mapping",
          "Contagion or influence",
          "Supply-chain",
          "Defined by probabilities"]


metrics = ["Counting elements",
           "Breaking point",
           "Time",
           "Probability",
           "Rate",
           "Cost",
           "Path length",
           "Performance"]



studies = ['Size of the giant connected component',
'Coupling',
'Percolation',
'Targeted attacks',
'Load and capacity',
'Cascading time',
'Length',
'Cost',
'Avalanche',
'Localized attacks',
'Optimization',
'Recovery',
'Contagion',
'Size of second largest component',
'Fraction of added intra-links',
'Laplacian',
'Small cluster',
'Single network contrast',
'Markov-chains',
'Efficient paths',
'Core percolation',
'Genetic algorithm',
'Lifetime',
'Interdependent k-core percolation ',
'Clustering coefficient',
'Balance coefficient',
'Delay',
'Information to attack',
'Evenness',
'Antagonistic nodes',
'Intra-network topology',
'Link addition strategy',
'Contagion or alerting rates',
'Redundancy degree',
'Node degree correlation',
'Localized attack stability',
'Lattice dimension',
'System size',
'Resources provided per node',
'Node protection strategy',
'Probability of stabilization',
'Layer configuration',
'Probability of failure',
'Fraction of infected nodes',
'Assortativity',
'Average local threshold',
'Transmissibility',
'Redundant ratio',
'Difference index',
'System intersimilarity',
'Failure distribution',
'Initially infected nodes',
'Amount of components',
'Failure size PMF',
'Components size',
'Mean degree',
'K-core rule']

networks = ['simulated','both']

networks_names = {'simulated':"Simulated",'both':"Real and simulated"}



numer_dict = get_paper_numbers("papers_order.txt")


def get_paper_ids():

        # values maintains the previous field values on the search form
        paper_properties = db_api.get_paper_properties(db)
        values = {}
        paper_values = []
        authors_value = ""
        categories_values = []
        for prop in paper_properties:
            if not prop['type'] == 'category':
                if prop['name'] == 'authors':
                    #authors_value = '' ##### MIRAR ESTA PARTE
                    values[prop['name']] = '' ##### MIRAR ESTA PARTE

                else:
                    paper_values.append({'id_name':(prop['name']).replace(" ","_"),
                                         'value':''})##### MIRAR ESTA PARTE
                    values[prop['name']] = ''##### MIRAR ESTA PARTE
            else:
                category_values = []
                full_data = db_api.get_data_from_category_as_headers_and_column_data(db, prop['id'])
                cat_prop = full_data['headers']

                for c_prop in cat_prop:

                    if c_prop['name'] == 'id':
                        continue
                    if c_prop['type'] == 'subcat':
                        value = ''##### MIRAR ESTA PARTE


                        category_values.append({'subcat_id':c_prop['id'],
                                                'rel_with_cat':c_prop['rel_with_cat'],
                                                'name_value':value,
                                                'is_subcat':True})

                        values[prop['name']+c_prop['name']] = value
                    else:
                        value = ''
                        category_values.append({'id_name':(c_prop['name']).replace(" ","_"),
                                                'value':value,
                                                'is_subcat':False})
                        values[prop['name']+c_prop['name']] = value

                categories_values.append({'cat_id':prop['id'],'values':category_values})
        paper_ids = db_api.search_papers_id(db, paper_values, authors_value, categories_values)
        return paper_ids


def get_reference_from_file_with_title(title,file):
    f = open(file, 'r')
    prev_line = ""
    for file_line in f:

        if file_line.find("title=")>-1:
            title_split_str = file_line.split("{")
            title_split_str = title_split_str[1].split("}")
            found_title = title_split_str[0]
            if found_title == title:
                prev_line_split_str = prev_line.split("{")
                prev_line_split_str = prev_line_split_str[1].split(",")
                cite_name = prev_line_split_str[0]
                return cite_name
        else:
            prev_line = file_line


def get_all_citations():
    cat_id = db_api.get_category_id_from_name(db,"citation")
    cat_data = db_api.get_data_from_category_by_cat_id(db,cat_id)
    cat_names = []

    for data in cat_data:
        cat_names.append(data["name"])
    results = {}
    for name in cat_names:
        results [db_api.search_papers_id(db,[],"",[{'cat_id':str(cat_id),'values':[{'id_name': 'name', 'is_subcat': False, 'value': name}]}])[0]] = name
    return results

all_citations = get_all_citations()

#get_reference_from_file_with_title('Complexity and fragility in ecological networks','cites.txt')

wanted_elements = ['title','metric','model','study','network tested','year']


paper_ids = get_paper_ids()

################################
# dividir los papers en grupos de N elementos partiendo en el i-esimo elemento
tabla = 7

if tabla == 1 :
    i=0
else:
    i = 15*(tabla-1)+1
N = (15)
if i+N > 103:
    N = 103-i
################################
# organized properties
properties_dict = {}
for paper_id in paper_ids[i:i+N]:
    paper_properties = db_api.get_paper_properties_and_values(db,paper_id)

    properties_dict[paper_id] = {}
    for element in paper_properties:
        if element['name'] in wanted_elements:
            if element['name'] == 'model':
                models_types_list = []
                for model_name in element['value']:
                    model_type_name = db_api.get_model_type(db,model_name)
                    models_types_list.append(model_type_name)
                properties_dict[paper_id][element['name']] = models_types_list
            elif element['name'] == 'metric':
                metrics_types_list = []
                for metric_name in element['value']:
                    metric_type_name = db_api.get_metric_type(db,metric_name)
                    metrics_types_list.append(metric_type_name)
                properties_dict[paper_id][element['name']] = metrics_types_list
            else:
                properties_dict[paper_id][element['name']] = element['value']

# pasar un for por los elementos de cada categoria y ver quienes del set lo cumplen
header_line = "\multicolumn{2}{|l|}{Papers}"



for paper_id in paper_ids[i:i+N]:
    if paper_id==515:
        cite_name  = "liu2016cascading"
    else:
        #cite_name = get_reference_from_file_with_title(title,"cites.txt")
        cite_name = all_citations[paper_id]
    if cite_name == None:
        header_line += "& \cite{ERROR p_id"+paper_id+"}"
    else:
        header_line += "& [" + str(numer_dict[cite_name]["number"]) + "] "
header_line += "\\"+"\\"+" \hline"
print header_line

print "\multirow{"+str(len(models))+"}{*}{\\rot{Models}}"
last_model = models[len(models)-1]
for model in models:
    table_line = "& \multicolumn{1}{|l|}{\pbox{0.5\\textwidth}{\\vspace{0.05cm}"+model+"}}"
    for paper_id in paper_ids[i:i+N]:
        # armar la linea
        # print model," IS IN ",properties_dict[paper_id]['model'],"?"
        if model in properties_dict[paper_id]['model']:
            table_line += "& \OK"
        else:
            table_line += "& "
    if not model == last_model:
        table_line += "\\"+"\\"+" \cline{2-"+str(N+2)+"}"
    else:
        table_line += "\\"+"\\"+" \hline"
    print table_line

print "\multirow{"+str(len(metrics))+"}{*}{\\rot{Metrics}} "
last_metric = metrics[len(metrics)-1]
for metric in metrics:
    table_line = "& \multicolumn{1}{|l|}{\pbox{0.5\\textwidth}{\\vspace{0.05cm}"+metric+"}}"
    for paper_id in paper_ids[i:i+N]:
        # armar la linea
        if metric in properties_dict[paper_id]['metric']:
            table_line += "& \OK"
        else:
            table_line += "& "

    if not metric == last_metric:
        table_line += "\\"+"\\"+" \cline{2-"+str(N+2)+"}"
    else:
        table_line += "\\"+"\\"+" \hline"
    print table_line


studies_str_buffer = []
number_of_study_lines = 0
last_study = studies[len(studies)-1]
for study in studies:
    is_this_study_used = 0
    table_line = "& \multicolumn{1}{|l|}{\pbox{0.5\\textwidth}{\\vspace{0.05cm}"+study+"}}"
    for paper_id in paper_ids[i:i+N]:
        # armar la linea
        if study in properties_dict[paper_id]['study']:
            is_this_study_used = 1
            table_line += "& \OK"
        else:
            table_line += "& "

    table_line += "\\"+"\\"+" \cline{2-"+str(N+2)+"}"
    number_of_study_lines += is_this_study_used
    if is_this_study_used > 0:
        studies_str_buffer.append(table_line)

print "\multirow{"+str(len(studies_str_buffer))+"}{*}{\\rot{Studies}}"
last_line = studies_str_buffer[len(studies_str_buffer)-1]
for line in studies_str_buffer:
    if not line == last_line:
        print line
    else:
        print line.replace("\cline{2-"+str(N+2)+"}","\hline")

print "\multirow{2}{*}{\\rot{Networks}}"
for network in networks:
    table_line = "& \multicolumn{1}{|l|}{\pbox{0.5\\textwidth}{\\vspace{0.3cm}"+networks_names[network]+"\\vspace{0.4cm}}}"
    for paper_id in paper_ids[i:i+N]:
        # armar la linea
        if network in properties_dict[paper_id]['network tested']:
            table_line += "& \OK"
        else:
            table_line += "& "
    if not network == "both":
        table_line += "\\"+"\\"+" \cline{2-"+str(N+2)+"}"
    else:
        table_line += "\\"+"\\"+" \hline"

    print table_line


## Hacer una funcion que transforme los nombres de los papers en citas