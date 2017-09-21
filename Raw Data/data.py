
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib import style


# In[2]:


im1 = pd.read_csv('IM1.csv', encoding='latin1')[1:27]
im1["Email Address"] = im1["Email Address"].apply(lambda str: str.lower())
im1.sort_values("Name")


# In[3]:


modulesData= {"Module": ["Research", "Analysis", "Ideate", "Build", "Communicate"],
             "Module #": [1, 2, 3, 4, 5]}
modules = pd.DataFrame(modulesData)
modules.index = ["MOD_%i" % i for i in range(modules.shape[0])]
modules


# In[4]:


consolidatedIndResponses = pd.read_csv('Consolidated Student Responses - Individual.csv', encoding='latin1')[:26]
consolidatedIndResponses.head()


# In[5]:


# Building Student Database
students = im1.sort_values("Name")[["Name", "Email Address"]]
students.index = ["S_%i" % i for i in range(students.shape[0])]
students = students[["Name", "Email Address"]]
students["SID"] = ["S_%i" % i for i in range(students.shape[0])]
students["Email Address"] = students["Email Address"].apply(lambda str: str.lower())
students


# In[6]:


# Methods:
# Note: additional methods not asked explicitly about were removed: 
# Affinity Diagram (M3), Dot Voting(M3), Live Prototyping (M4), 3-D Printing (M4)
methods = pd.read_csv('methods.csv', encoding='latin1')
methods.index = ["M_%i" % i for i in range(methods.shape[0])]
methods["MID"] = ["M_%i" % i for i in range(methods.shape[0])]
methods.head()


# In[7]:


# Aggregated Responses by Student
# [SID, Module, Selected Methods (list), Reasons for Selection (list), 
# Unselected Methods (list), Reasons for Unselection (list)]
students['key'] = 1
methods['key'] = 1
indAggResponses = pd.merge(students, methods, on='key')
indAggResponses["Selected"] = 0
indAggResponses["Reason"] = ""
indAggResponses["Familiar"] = 0


# In[8]:


# Adding ISurvey1 into studentResponses
im1s = pd.merge(students, im1, how='inner', on=['Email Address', 'Name'])

mod1Methods = methods[methods["Module #"] == 1]
for method in mod1Methods.Method:
    for SID in im1s["SID"]:
        row = (indAggResponses["SID"] == SID) & (indAggResponses["Method"] == method)
        indAggResponses.loc[row, "Selected"] = (im1s.loc[im1s["SID"] == SID, method + ".1"] == "Yes").values[0]
        indAggResponses.loc[row, "Familiar"] = (im1s.loc[im1s["SID"] == SID, method] == "Yes").values[0]
        indAggResponses.loc[row, "Reason"] = (im1s.loc[im1s["SID"] == SID, method + ".2"]).values[0]


# In[9]:


# Adding All ISurveys into indAggResponses

im2 = pd.read_csv('IM2.csv', encoding='latin1')[1:27]
im3 = pd.read_csv('IM3.csv', encoding='latin1')[1:27]
im4 = pd.read_csv('IM4.csv', encoding='latin1')[1:27]
im5 = pd.read_csv('IM5.csv', encoding='latin1')[1:27]
iSurveys = [im2, im3, im4, im5]

for survey in iSurveys:
    survey.rename(columns={"Unnamed: 1": "Email Address"}, inplace=True)
    survey["Email Address"] = survey["Email Address"].apply(lambda str: str.lower())
    
#im2["Email Address"] = im2["Email Address"].apply(lambda str: str.lower())
#im3["Email Address"] = im3["Email Address"].apply(lambda str: str.lower())
#im4["Email Address"] = im4["Email Address"].apply(lambda str: str.lower())
#im5["Email Address"] = im5["Email Address"].apply(lambda str: str.lower())
iSurveysS = [pd.merge(students, survey, how='inner', on=['Email Address']) for survey in iSurveys]


im1s = pd.merge(students, im1, how='inner', on=['Email Address', 'Name'])
im1s.head()
for i in range(0, 4):
    survey = iSurveysS[i]
    mod1Methods = methods[methods["Module #"] == i + 2]
    for method in mod1Methods.Method:
        for SID in survey["SID"]:
            row = (indAggResponses["SID"] == SID) & (indAggResponses["Method"] == method)
            indAggResponses.loc[row, "Selected"] = (survey.loc[survey["SID"] == SID, method + ".1"] == "Yes").values[0]
            indAggResponses.loc[row, "Familiar"] = (survey.loc[survey["SID"] == SID, method] == "Yes").values[0]
            indAggResponses.loc[row, "Reason"] = (survey.loc[survey["SID"] == SID, method + ".2"]).values[0]


# In[10]:


indAggResponses


# In[11]:


indAggResponses[(indAggResponses["Reason"] == "")].groupby(["Module #", "Name"]).size()


# In[12]:


# Team Roster
teamRoster = pd.read_csv('Team Roster.csv', encoding='latin1')[1:28]
teamRoster = pd.merge(teamRoster, students, on = ["Email Address"])
#teams = teams.groupby("Team")
teams = pd.DataFrame(columns = ["Team", "SID"])
for row in teamRoster[["Team", "SID", "Name"]].groupby("Team"):
    print(type(row[1]))
    print(row[1].SID.values)
    teams.loc[teams.shape[0]] = [row[0], row[1].SID.values]


# In[13]:


teams.loc[[False, True, True, True, True]]


# In[14]:


# Team Aggregate Responses
# Team, Module, Chosen Method (3 rows per team), Reason, Decision Process

teamAggResponses = pd.DataFrame(columns = ["Team", "Module", "Chosen Method", "Reason", "Decision Process"])


# In[15]:


teamAggResponses = pd.DataFrame(columns = ["Team", "Module", "Chosen Method", "Reason", "Decision Process"])

# Note: deleted extra responses from team 1
tm1 = pd.read_csv('TM1.csv', encoding='latin1')
tm1

teamData = [pd.read_csv('TM%d.csv' % i, encoding='latin1') for i in range(1,5 + 1)]

for i in range(1, 5+1):
    team = teamData[i-1]
    for r in range(tm1.shape[0]):
        for q in range(0, 3):
            ri = teamAggResponses.shape[0] # + 1, + 2
            teamAggResponses.loc[ri, "Module"] = i
            teamAggResponses.loc[ri, "Team"] = team[team.columns[1]][r]
            teamAggResponses.loc[ri, "Chosen Method"] = team[team.columns[q*3 + 2]][r]
            teamAggResponses.loc[ri, "Reason"] = team[team.columns[q*3 + 4]][r]
            teamAggResponses.loc[ri, "Decision Process"] = team[team.columns[q*3 + 3]][r]


# In[16]:


teamAggResponses


# In[ ]:




