__author__ = 'ivana'


def get_paper_numbers(reference_file):
    result_dict = {}
    f = open(reference_file,"r")
    line = str(f.read()).split("\item")
    for i in range(len(line)):
        if len(line[i])>0:
            splited_line = line[i].split("{")
            name = (splited_line[1].split("}"))[0]
            cite_name = (splited_line[2].split("}"))[0]
            result_dict[cite_name] = {"name":name,"number":i}
    return result_dict


def replace_cite_with_paper_numbers(file_to_replace, file_paper_numbers):
    cite_number_dict = get_paper_numbers(file_paper_numbers)
    f = open(file_to_replace,"r")
    text = f.read()

    # remove `cite{...}'
    while True:
        cite_index = text.find("\\cite{")
        if cite_index == -1:
            break
        aux_text = text[cite_index:len(text)].replace("}","]",1)
        text = text[0:cite_index]+aux_text
        text = text.replace("\\cite{","[",1)

    for key in cite_number_dict:
        if key == "liu2016cascading":
            text = text.replace(str("liu2016cascadinginner")," "+str(cite_number_dict["liu2016cascadinginner"]["number"])+" ")
        text = text.replace(str(key)," "+str(cite_number_dict[key]["number"])+" ")
    print text


replace_cite_with_paper_numbers("taxonomy.txt","papers_order.txt")

