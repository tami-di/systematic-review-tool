__author__ = 'ivana'

from app import app, db
import app.api.db_api as db_api

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


cat_id = db_api.get_category_id_from_name(db,"study")
cat_data = db_api.get_data_from_category_by_cat_id(db,cat_id)
cat_names = []
for data in cat_data:
    cat_names.append(data["name"])

cites = {}
result = {}


all_citations = get_all_citations()
depreca3 = db_api.get_paper_id_by_year_less_than(db,2010)


for name in cat_names:
    papers_ids = db_api.search_papers_id(db,[],"",[{'cat_id':str(cat_id),'values':[{'id_name': 'name', 'is_subcat': False, 'value': name}]}])
    p_ids_aux = []
    for p_id in papers_ids:
        if p_id not in depreca3:
            p_ids_aux.append(p_id)
    papers_ids = p_ids_aux
    result[name] = len(papers_ids)
    cites[name] = []
    for p_id in papers_ids:
        if p_id == 515:
            cites[name].append("liu2016cascading")
        #elif p_id in [489]:#,523
         #   continue
        else:
            cites[name].append(all_citations[p_id])

oredered_names = sorted(result, key=result.__getitem__, reverse=True)
for name in oredered_names:
    if result[name]>0:
        cite_str = ""
        for cite in cites[name]:
            cite_str+=cite+","
        print "\'"+name+"\',",result[name],cite_str