import pandas as pd
import re
import numpy as np

print("Step 1: Data Preprocessing")
print("--------------")
print("--------------")
publication = pd.DataFrame()
publication_link = pd.DataFrame()
project = pd.DataFrame()
abstract = pd.DataFrame()

### Beginning year set to 2008 as 06-07 have irregular user-supplied keywords

for i in range(2008, 2018):
    publication_sub = pd.read_csv("RePORTER_PUB_C_" + str(i) + ".csv",
                                  encoding="ISO-8859-1")
    publication_sub['Year'] = i
    publication_sub['PMID'].replace("", np.nan, inplace=True)
    publication_sub.dropna(subset=['PMID'], inplace=True)

    publication_link_sub = pd.read_csv("RePORTER_PUBLNK_C_" + str(i) + ".csv",
                                       encoding="ISO-8859-1")
    publication_link_sub['Year'] = i

    publication = publication.append(publication_sub,
                                     ignore_index=True)
    print("Step 1. Read publication data from the year of " + str(i))

    publication_link = publication_link.append(publication_link_sub,
                                               ignore_index=True)
    print("Step 1. Read publication link data from the year of " + str(i))

for i in range(2008, 2016):
    ### Project
    project_sub = pd.read_csv("RePORTER_PRJ_C_FY" + str(i) + ".csv",
                              encoding="ISO-8859-1")
    project_sub = project_sub.loc[project_sub['APPLICATION_TYPE'] == 1]
    project_sub.dropna(subset=['ACTIVITY'], inplace=True)
    project_sub.dropna(subset=['PROJECT_START'], inplace=True)
    project_sub.dropna(subset=['PROJECT_END'], inplace=True)
    project_sub = project_sub.reset_index()
    for j in range(len(project_sub.index)):
        activity_search = re.search('\A\D{1}', project_sub.loc[j, 'ACTIVITY'], re.IGNORECASE)
        project_sub.loc[j, 'activity_new'] = activity_search.group(0)
        print(str(i) + '--' + str(j))

    project_sub = project_sub.loc[project_sub['activity_new'].isin(['R', 'K', 'T', 'F', 'P'])]
    project_sub = project_sub.loc[project_sub['PROJECT_START'] != "2016"]
    print("Step 1. Read project data from the year of " + str(i))

    project = project.append(project_sub,
                             ignore_index=True)

    ### Abstract
    abstract_sub = pd.read_csv("RePORTER_PRJABS_C_FY" + str(i) + ".csv",
                               encoding="ISO-8859-1")
    abstract_sub['ABSTRACT_TEXT'].replace("", np.nan, inplace=True)
    abstract_sub.dropna(subset=['ABSTRACT_TEXT'], inplace=True)
    print("Step 1. Read abstract data from the year of " + str(i))

    abstract = abstract.append(abstract_sub,
                               ignore_index=True)

# Match everything to project dataset
abstract = abstract.loc[abstract['APPLICATION_ID'].isin(project['APPLICATION_ID'])]
publication_link = publication_link.loc[publication_link['PROJECT_NUMBER'].isin(project['CORE_PROJECT_NUM'])]
publication = publication.loc[publication['PMID'].isin(publication_link['PMID'])]
project = project.loc[project['APPLICATION_ID'].isin(abstract['APPLICATION_ID'])]
print("Step 1. Datasets are matched and screened.")

### Write to file
publication.to_csv('publication.csv', index_label=False, index=False)
publication_link.to_csv('publication_link.csv', index_label=False, index=False)
project.to_csv('project.csv', index_label=False, index=False)
abstract.to_csv('abstract.csv', index_label=False, index=False)

print("Step 1. Datasets are saved.")
print("Step 1. Publication has " + str(len(publication.index)) + " records.")
print("Step 1. Project has " + str(len(project.index)) + " records.")
print("Step 1. Abstract has " + str(len(abstract.index)) + " records.")
print("Step 1. Publication link has " + str(len(publication_link.index)) + " records.")
print("Step 1 is over.")
print("--------------")
print("--------------")


