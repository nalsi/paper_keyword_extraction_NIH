import pandas as pd


# Project summary

# project = pd.read_csv("PROJECT_SUM.csv")
# paper = pd.read_csv("PAPER_SUM_NEW.csv")
#
# for i in range(2008, 2016):
#     project_sub = project.loc[project['YEAR_START'] == i]
#     paper_sub = paper.loc[paper['CORE_PROJECT_NUM'].isin(project_sub['CORE_PROJECT_NUM'])]
#     paper_sub_1 = paper_sub.loc[paper_sub['TERM_LENGTH'] > 0]
#     project_no = len(project_sub.index)
#     term_project_len = sum(project_sub['KEYWORD_NUM']) / project_no
#     term_author_len = sum(project_sub['TERM_NUM']) / project_no
#     paper_no = len(paper_sub_1.index) / project_no
#     paper_no_ratio = len(paper_sub_1.index) / len(paper_sub.index)
#     paper_term_len = sum(paper_sub_1['TERM_LENGTH']) / len(paper_sub_1.index)
#     print(i)
#     print("Project no: ", str(project_no))
#     print("Term project no: ", str(term_project_len))
#     print("Term author no: ", str(term_author_len))
#     print("Paper no: ", str(paper_no))
#     print("Paper term no: ", str(paper_term_len))

paper = pd.read_csv("paper_analysis.csv")
project = pd.read_csv("project.csv")
acceptance = pd.read_csv("acceptance_rate.csv")

paper = paper[paper['pyear_1'] > 2007]
paper = paper[paper['pyear_1'] < 2016]
paper = paper.reset_index()

for i in range(len(paper.index)):
	project_number = paper.loc[i, 'CORE_PROJECT_NUM']
	project_year = paper.loc[i, 'pyear_1']
	activity = list(set(project.loc[project['CORE_PROJECT_NUM'] == project_number, 'ACTIVITY']))[0]
	paper.loc[i, 'activity'] = activity
	# funding_rate = acceptance.loc[(acceptance['activity'] == activity) & (acceptance['year'] == project_year), 'rate'].item()
	# paper.loc[i, "funding_rate"] = funding_rate
	print(i)

paper.to_csv("paper_analysis_new.csv", index_label=False, index=False)
