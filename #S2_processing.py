## This file extracts information from datasets

print("Step 2: Data extraction from spreadsheets")
print("--------------")
print("--------------")

import pandas as pd
import re
import numpy as np
import spacy
from NLP_pipeline import nlp_pipeline

nlp = spacy.load('en')

publication = pd.read_csv('publication.csv', encoding="ISO-8859-1")
publication_link = pd.read_csv('publication_link.csv', encoding="ISO-8859-1")
project = pd.read_csv('project.csv', encoding="ISO-8859-1")
abstract = pd.read_csv('abstract.csv', encoding="ISO-8859-1")

project['PROJECT_TERMS'] = project['PROJECT_TERMS'].fillna("")

print("Step 2. All data are loaded.")

project['CORE_PROJECT_NUM'] = project['CORE_PROJECT_NUM'].astype("str")
abstract_id = np.unique(project['CORE_PROJECT_NUM'])
replace_text = ['DESCRIPTION \\(provided by applicant\\)\\:', 'DESCRIPTION \\(provide by applicant\\)\\:']

round_number = (len(abstract_id) // 100) + 1
remainder = (len(abstract_id) % 100) - 1
print("Loop begins. There will be " + str(round_number) + " loops and " +
      str(len(abstract_id)) + " projects.")

# round_number_1 = round_number
round_number_1 = round_number

for l in range(round_number):
    # Determine the beginning positon and ending position for each loop
    start_position = 1 + (l * 100)
    if l == round_number - 1:
        end_position = start_position + remainder
    else:
        end_position = start_position + 100
    print("Round " + str(l) + ": from projects #" + str(start_position) + " to #" + str(end_position))

    # Create empty DF or read existing file before each loop
    if l == 0:
        PROJECT_SUM = pd.DataFrame()
        PAPER_SUM = pd.DataFrame()
    else:
        PROJECT_SUM = pd.read_csv('PROJECT_SUM.csv',
                                  encoding="ISO-8859-1")
        PAPER_SUM = pd.read_csv('PAPER_SUM.csv',
                                encoding="ISO-8859-1")
    print("------ " + str(len(PROJECT_SUM.index)) + " projects and " +
          str(len(PAPER_SUM.index)) + " papers in the record")

    # Run the loops
    for i in range(start_position, end_position):

        print("Processing Round #" + str(l) + " Project #" + str(i))
        # Project pipeline
        project_sub = project.loc[project['CORE_PROJECT_NUM'] == abstract_id[i]]
        abstract_sub = abstract.loc[abstract['APPLICATION_ID'].isin(project_sub['APPLICATION_ID'])]
        publication_link_sub = publication_link.loc[
            publication_link['PROJECT_NUMBER'].isin(project_sub['CORE_PROJECT_NUM'])]
        pmids = publication_link_sub['PMID']
        SUB_PROJ_NUM = len(project_sub.index)
        SUB_PROJ_ABS_NUM = len(abstract_sub.index)

        # Get project abstract: if more than one, concatenate everything
        if SUB_PROJ_ABS_NUM > 1:
            project_abstract_text = str(" ".join(abstract_sub['ABSTRACT_TEXT'].values))
        elif SUB_PROJ_ABS_NUM == 1:
            project_abstract_text = str(abstract_sub['ABSTRACT_TEXT'].item())
        else:
            project_abstract_text = None

        # If with any subprojects,
        if SUB_PROJ_NUM > 1:
            project_term_all = ";".join(project_sub['PROJECT_TERMS'])
            core_project_num = project_sub['CORE_PROJECT_NUM'].values[0]
            activity = project_sub['activity_new'].values[0]
            starting_year = int("20" + project_sub['PROJECT_START'].values[0][-2:])
            ending_year = int("20" + project_sub['PROJECT_END'].values[0][-2:])
            org_country = project_sub['ORG_COUNTRY'].values[0]
            total_cost = project_sub['TOTAL_COST'].values[0]
        else:
            project_term_all = project_sub['PROJECT_TERMS'].item()
            core_project_num = project_sub['CORE_PROJECT_NUM'].item()
            activity = project_sub['activity_new'].item()
            starting_year = int("20" + project_sub['PROJECT_START'].item()[-2:])
            ending_year = int("20" + project_sub['PROJECT_END'].item()[-2:])
            org_country = project_sub['ORG_COUNTRY'].item()
            total_cost = project_sub['TOTAL_COST'].item()

        if project_abstract_text is not None:
            project_abstract_text = re.sub('|'.join(replace_text), " ", project_abstract_text)
            project_abstract_text = re.sub('^\[\'|\'\]$', " ", project_abstract_text)
            project_abstract_text = project_abstract_text.strip()

            text_table = nlp_pipeline(project_abstract_text)

            if len(text_table) > 0:
                project_abstract_keyword = text_table
            else:
                project_abstract_keyword = None
        else:
            project_abstract_keyword = None

        if project_abstract_keyword == None:
            term_string = ""
            term_length = 0
        else:
            term_string = ";".join(project_abstract_keyword)
            term_length = len(project_abstract_keyword)

        if str(project_term_all) != 'nan':
            project_term = project_term_all.replace("; ", ";").replace(", ", ";").replace(",", ";").split(";")
            project_term_new = []
            for term in project_term:
                term = re.sub("\/|\-| \- | \/ |\(.*\)| \(.*\)|\(.*\) ", "", term)
                if (len(term.split()) > 1 & len(term.split()) < 4):
                    project_term_new.append(" ".join(token.lemma_ for token in nlp(term)))
            project_term_term = ";".join(list(set(project_term_new)))
            project_term_length = len(project_term_new)
            if project_term_length == 0:
                project_term_term = ""
        else:
            project_term_new = ""
            project_term_length = 0

        # Paper pipeline
        if len(publication_link_sub.index) > 0:
            for pmid in pmids:
                paper_year = publication.loc[publication['PMID'] == int(pmid), 'PUB_YEAR'].item()
                PAPER_SUM_SUB = pd.DataFrame([[str(core_project_num),
                                               pmid,
                                               paper_year]],
                                             columns=['CORE_PROJECT_NUM', 'PMID', 'YEAR'])
                PAPER_SUM = PAPER_SUM.append(PAPER_SUM_SUB)

        project_list = [str(core_project_num),
                        SUB_PROJ_NUM - 1,
                        str(activity),
                        str(starting_year),
                        str(ending_year),
                        str(org_country),
                        str(total_cost),
                        term_string,
                        term_length,
                        project_term_term,
                        project_term_length,
                        len(publication_link_sub['PMID'])]
        PROJECT_SUM_SUB = pd.DataFrame([project_list], columns=['CORE_PROJECT_NUM', 'SUB_PROJ', 'ACTIVITY',
                                                                'YEAR_START', 'YEAR_END', 'COUNTRY', 'COST',
                                                                'KEYWORD', 'KEYWORD_NUM', 'TERM', 'TERM_NUM',
                                                                'PAPER_NUM'])
        PROJECT_SUM_SUB = PROJECT_SUM_SUB.loc[(PROJECT_SUM_SUB['KEYWORD_NUM'] > 0) | (PROJECT_SUM_SUB['TERM_NUM'] > 0)]
        PROJECT_SUM = PROJECT_SUM.append(PROJECT_SUM_SUB)

    PROJECT_SUM.to_csv("PROJECT_SUM.csv", index_label=False, index=False,
                       columns=['CORE_PROJECT_NUM', 'SUB_PROJ', 'ACTIVITY',
                                'YEAR_START', 'YEAR_END', 'COUNTRY', 'COST',
                                'KEYWORD', 'KEYWORD_NUM', 'TERM', 'TERM_NUM',
                                'PAPER_NUM'])
    PAPER_SUM.to_csv("PAPER_SUM.csv", index_label=False, index=False,
                     columns=['CORE_PROJECT_NUM', 'PMID', 'YEAR'])
    print("Round " + str(l) + " finished: " + str(len(PROJECT_SUM.index)) + " projects and " +
          str(len(PAPER_SUM.index)) + " papers saved.")
    print("----------------")
    print("----------------")
