import pandas as pd
import spacy
import numpy as np
nlp = spacy.load('en')

paper_result = pd.read_csv("PAPER_SUM_NEW.csv")
project_sum = pd.read_csv("PROJECT_SUM.csv")

project_sum = project_sum.loc[project_sum['ACTIVITY'] == "R"]
paper_result = paper_result.loc[paper_result['TERM_LENGTH'] > 0]
paper_result = paper_result[paper_result['CORE_PROJECT_NUM'].isin(project_sum['CORE_PROJECT_NUM'])]
paper_result.reset_index(drop=True, inplace=True)
project_sum = project_sum[project_sum['CORE_PROJECT_NUM'].isin(paper_result['CORE_PROJECT_NUM'])]

print("Step 4: Keyword matching.")
print("There are " + str(len(paper_result.index)) + " papers to be matched to project keywords.")


####### Needs to be revised
#######

# len(paper_result.index)

for i in range(len(paper_result.index)):
    
    paper_terms = paper_result.loc[i, 'TERM']
    project_num = paper_result.loc[i, 'CORE_PROJECT_NUM']
    project_terms_1 = str(project_sum.loc[project_sum['CORE_PROJECT_NUM'] == project_num,
                                      'KEYWORD'].item()).strip()
    project_terms_2 = str(project_sum.loc[project_sum['CORE_PROJECT_NUM'] == project_num,
                                      'TERM'].item()).strip()
    project_terms = ";".join([project_terms_1, project_terms_2])
    project_term_list = []
    paper_term_list = []
    for term in project_terms.split(";"):
        if (len(term.split()) == 2):
            project_term_list.append(term)
        if (len(term.split()) == 3):
            project_term_list.append(" ".join(term.split()[0:2]))
            project_term_list.append(" ".join(term.split()[1:3]))
    
    paper_term_list = paper_terms.split(";")
    project_term_list = list(set(project_term_list))

    ### Compare terms
    score = 0
    for term in paper_term_list:
        if len(term.split()) == 2:
            if term in project_term_list:
                score = score + 1
        if len(term.split()) == 3:
            if term in project_term_list:
                score = score + 1
            elif " ".join(term.split()[0:2]) in project_term_list:
                score = score + 1
            elif " ".join(term.split()[1:3]) in project_term_list:
                score = score + 1

    project_year_start = project_sum.loc[project_sum['CORE_PROJECT_NUM'] == project_num,
                                      'YEAR_START'].item()
    project_year_end = project_sum.loc[project_sum['CORE_PROJECT_NUM'] == project_num,
                                         'YEAR_END'].item()
    paper_term_length = len(paper_term_list)
    project_term_length = len(project_term_list)
    paper_result.loc[i, 'matched_no'] = score
    paper_result.loc[i, 'final_score'] = score / (paper_term_length + project_term_length)
    paper_result.loc[i, 'paper_term_length'] = paper_term_length
    paper_result.loc[i, 'project_term_length'] = project_term_length
    paper_result.loc[i, 'pyear_1'] = project_year_start
    paper_result.loc[i, 'pyear_2'] = project_year_end
    paper_result.loc[i, 'year_gap'] = paper_result.loc[i, 'YEAR'] - project_year_start
    paper_result.loc[i, 'cost'] = project_sum.loc[project_sum['CORE_PROJECT_NUM'] == project_num,
                                         'COST'].item()
    paper_result.loc[i, 'over_project_end'] = np.where(paper_result.loc[i, 'YEAR'] > project_year_end,
                                                    1, 0)

    print(str(i), " / ", str(len(paper_result.index)))


paper_result.to_csv("paper_analysis.csv", index_label=False, index=False,
                 columns = ['CORE_PROJECT_NUM', 'PMID', 'YEAR', "match", "TERM", 
                            'matched_no', 'final_score',"paper_term_length", 'project_term_length',
                            'pyear_1', 'pyear_2', 'year_gap', 'cost', 'over_project_end'])
