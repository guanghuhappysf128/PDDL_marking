team_dict = {
    # 1:{"team_name":"staff_team_basic","team_id":"Azul project group 99","url":"gitlab.eng.unimelb.edu.au/ruihanz/comp90054-2020s1-azul.git"},
    # 2:{"team_name":"staff_team_middle","team_id":"Azul project group 99","url":"gitlab.eng.unimelb.edu.au/guangh1/comp90054-2020s1-azul.git"},
    # 3:{"team_name":"staff_team_hard","team_id":"Azul project group 99","url":"gitlab.eng.unimelb.edu.au/happysf128/comp90054-2020s1-azul.git"},
    # 4:{"team_name":"staff_team_advanced","team_id":"Azul project group 99","url":"gitlab.eng.unimelb.edu.au/ruihanz/comp90054-2020s1-azul1.git"}# fail test
}
PARALLEL_THREADS = 4
import sys
import chardet # read file from other encoding such as "UTF-8 with BOM"
from joblib import Parallel, delayed
import pandas
import json

excel_data_df = pandas.read_excel('assign2.xlsx', sheet_name='Sheet1')

json_str = excel_data_df.to_json(orient='records')
records = json.loads(json_str)

# print('Excel Sheet to JSON:\n', json_str)

for i,record in  enumerate(records):
    '''
    team_id = record["Canvas Team name (e.g. Azul project group xx) -- must be the same as in Canvas: People -> Azul project group"]
    team_name = record["Competition team name. This name is chosen by you and will be the name displayed on the tournament leaderboard. Feel free to use the Canvas group name, or something more creative :)"].replace(" ","_")
    team_url = record["url"].replace("https://","")
    '''
    tlist = list(record.items())
    student_name = tlist[5][1]
    student_email = tlist[6][1]
    student_id = tlist[7][1]
    student_login = tlist[8][1]
    student_url = tlist[9][1].replace("https://","")

    def findID(id,dict):
        return id in dict.values()

    if not True in [findID(student_id,d) for d in team_dict.values()]:
        team_dict.update({i:{"student_name":student_name,"student_email":student_email,"student_id":student_id,"student_login":student_login,"student_url":student_url,}})

# print("\n\n\n",team_dict)




# #main
# from runner import *
import os
from tqdm import tqdm
# import itertools
import datetime

# class run_options():
#     pass

usr_name = "root"
passwrd = "iVIngSHA"
if not os.path.exists("assignments"):
    os.mkdir("assignments")
    
path_name = "assignments/" + datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S-%f")
# path_name = "competitions/" + "test"

if not os.path.exists(path_name):
    os.makedirs(path_name, exist_ok = True)
    
# if not os.path.exists(path_name+"/teams"):
#     os.mkdir(path_name+"/teams")

assignments = {}
# matches = {}

#git clone
print ("git cloneing all repos")

base = "git clone https://{}:{}@".format(usr_name,passwrd)

def git_clone_team(idx,v):
    teams = {}
    teams[idx] = {}
    teams[idx].update(v)
    
    url = v["student_url"]+" "
    folder_name = "{}/{}".format(path_name,v["student_id"])
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    teams[idx]["git_res"] = os.system(base + url + folder_name)
    
    # if len(os.listdir(folder_name)) == 0:
    #     teams[idx]["git_succ"] = False
    # else:
    #     teams[idx]["git_succ"] = True

    # return v

Parallel(n_jobs=PARALLEL_THREADS)(delayed(git_clone_team)(idx,v) for idx,v in tqdm(team_dict.items()))
    
# print ("Combining git result...")
# for team in tres:
#     if team["student_id"] in assignments:
#         pass
#     else:
#         assignments.update(team)


def readFiles(path_name,file_name):

    # adding different encoding support
    try:
        file = open("{}/{}".format(path_name,file_name), 'rb')
        raw = file.read(32) # at most 32 bytes are returned
        encoding = chardet.detect(raw)['encoding']
    except FileNotFoundError:
        encoding = 'utf-8'
        pass


    file_content = ""
    error_info ={}
    try:
        file_content=open("{}/{}".format(path_name,file_name), 'r', encoding=encoding).read()
        
    except UnicodeDecodeError:
        error_msg = "UnicodeDecodeError: 'gbk' codec can't decode byte 0xbf in position 2: illegal multibyte sequence\nResult: cannot read file\n Possible cause: file encoding is not UTF-8\n Please contact ghu1@student.unimelb.edu.au"
        error_info={file_name:error_msg}
        print("[UnicodeDecodeError]: {}/{}".format(path_name,path_name))
    except FileNotFoundError:
        error_msg = "File not found"
        error_info={file_name:error_msg}
        print("[FileNotFoundError]: {}/{}".format(path_name,path_name))
    return (file_content,error_info)


# running the solvers

import requests

import xlsxwriter 
  
workbook = xlsxwriter.Workbook('{}/result.xlsx'.format(path_name)) 
worksheet = workbook.add_worksheet()
row = 0
worksheet.write(row, 0,"student_name")
worksheet.write(row, 1,"student_email")
worksheet.write(row, 2,"student_id")
worksheet.write(row, 3,"student_login")
worksheet.write(row, 4,"student_url")
worksheet.write(row, 5,"part1_result")
worksheet.write(row, 6,"part2_result")
worksheet.write(row, 7,"part3_result")
worksheet.write(row, 8,"part1_mark (3/3)")
worksheet.write(row, 9,"part1_comments")
worksheet.write(row, 10,"part2_mark (2/2)")
worksheet.write(row, 11,"part2_comments")
worksheet.write(row, 12,"part3_mark (2/2)")
worksheet.write(row, 13,"part3_comments")

for idx,v in tqdm(team_dict.items()):
    print("\nStart planning for {}".format(v["student_id"]))
    domain = ""
    problem = ""
    error_info ={}


    # part 1
    part1_result=-1
    domain,error_msg = readFiles("{}/{}".format(path_name,v["student_id"]),"part1_domain.pddl")
    if not error_msg == {}: error_info.update(error_msg)

    problem,error_msg = readFiles("{}/{}".format(path_name,v["student_id"]),"part1_problem.pddl")
    if not error_msg == {}: error_info.update(error_msg)
    
    data = {'domain': domain, 'problem': problem}
    resp = requests.post('http://solver.planning.domains/solve',
                        verify=False, json=data).json()
    resp.update(error_info)
    with open("{}/{}/part1_run.json".format(path_name,v["student_id"]),'w') as f:
        json.dump(resp,f)
    if resp["status"]=="ok":
        with open("{}/{}/part1.plan".format(path_name,v["student_id"]), 'w') as f:
            try:
                f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
            except TypeError:
                f.write("\n".join(resp['result']['plan']))
        with open("{}/{}/part1.plan".format(path_name,v["student_id"]), 'r') as f:
            if f.readline().startswith("(move a1 b1") \
                and f.readline().startswith("(move b1 b2")\
                    and f.readline().startswith("(move b2 b3")\
                        and f.readline().startswith("(move b3 a3")\
                            and f.readline().startswith(''):
                part1_result = 1
            else:
                part1_result = 0

    # part 2
    part2_result = -1
    domain,error_msg = readFiles("{}/{}".format(path_name,v["student_id"]),"part2_domain.pddl")
    if not error_msg == {}: error_info.update(error_msg)

    problem,error_msg = readFiles("{}/{}".format(path_name,v["student_id"]),"part2_problem.pddl")
    if not error_msg == {}: error_info.update(error_msg)
    
    data = {'domain': domain, 'problem': problem}
    resp = requests.post('http://solver.planning.domains/solve',
                        verify=False, json=data).json()

    resp.update(error_info)
    with open("{}/{}/part2_run.json".format(path_name,v["student_id"]),'w') as f:
        json.dump(resp,f)

    if resp["status"]=="ok":
        with open("{}/{}/part2.plan".format(path_name,v["student_id"]), 'w') as f:
            try:
                f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
            except TypeError:
                f.write("\n".join(resp['result']['plan']))
        with open("{}/{}/part2.plan".format(path_name,v["student_id"]), 'r') as f:
            if f.readline().startswith("(move a1 b1")\
                and f.readline().startswith("(move b1 b2")\
                    and f.readline().startswith("(move b2 b3")\
                        and f.readline().startswith("(move b3 b4")\
                            and f.readline().startswith("(move b4 a4")\
                                and f.readline().startswith("(move a4 a5")\
                                    and f.readline()=='':
                part2_result = 1
            else:
                part2_result = 0

    # part 3
    part3_result=-1
    domain,error_msg = readFiles("{}/{}".format(path_name,v["student_id"]),"part3_domain.pddl")
    if not error_msg == {}: error_info.update(error_msg)

    problem,error_msg = readFiles("{}/{}".format(path_name,v["student_id"]),"part3_problem.pddl")
    if not error_msg == {}: error_info.update(error_msg)
    
    data = {'domain': domain, 'problem': problem}
    resp = requests.post('http://solver.planning.domains/solve',
                        verify=False, json=data).json()
    resp.update(error_info)
    with open("{}/{}/part3_run.json".format(path_name,v["student_id"]),'w') as f:
        json.dump(resp,f)

    if resp["status"]=="ok":
        with open("{}/{}/part3.plan".format(path_name,v["student_id"]), 'w') as f:
            try:
                f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
            except TypeError:
                f.write("\n".join(resp['result']['plan']))
        with open("{}/{}/part3.plan".format(path_name,v["student_id"]), 'r') as f:
            if f.readline().startswith("(move a1 b1")\
                and f.readline().startswith("(move b1 b2")\
                    and f.readline().startswith("(move b2 b3")\
                        and f.readline().startswith("(move b3 b4")\
                            and f.readline().startswith("(move b4 b5")\
                                and f.readline().startswith("(move b5 b4)")\
                                    and f.readline().startswith("(move b4 a4)")\
                                        and f.readline().startswith("(move a4 a5)")\
                                            and f.readline()=='':
                part3_result = 1
            else:
                part3_result = 0

        with open("{}/{}/part3.plan".format(path_name,v["student_id"]), 'r') as f:
            if f.readline().startswith("(move a1 b1")\
                and f.readline().startswith("(move b1 a1")\
                    and f.readline().startswith("(move a1 b1")\
                        and f.readline().startswith("(move b1 b2")\
                             and f.readline().startswith("(move b2 b3")\
                                 and f.readline().startswith("(move b3 b4")\
                                     and f.readline().startswith("(move b4 b5")\
                                         and f.readline().startswith("(move b5 b4)")\
                                             and f.readline().startswith("(move b4 a4)")\
                                                 and f.readline().startswith("(move a4 a5)")\
                                                     and f.readline()=='':
                part3_result = 1
            else:
                pass

        with open("{}/{}/part3.plan".format(path_name,v["student_id"]), 'r') as f:
            if f.readline().startswith("(move a1 b1")\
                and f.readline().startswith("(move b1 a1")\
                    and f.readline().startswith("(move a1 a2")\
                        and f.readline().startswith("(move a2 b2")\
                             and f.readline().startswith("(move b2 b3")\
                                 and f.readline().startswith("(move b3 b4")\
                                     and f.readline().startswith("(move b4 b5")\
                                         and f.readline().startswith("(move b5 b4)")\
                                             and f.readline().startswith("(move b4 a4)")\
                                                 and f.readline().startswith("(move a4 a5)")\
                                                     and f.readline()=='':
                part3_result = 1
            else:
                pass
    row = row + 1
    worksheet.write(row, 0,v["student_name"])
    worksheet.write(row, 1,v["student_email"])
    worksheet.write(row, 2,v["student_id"])
    worksheet.write(row, 3,v["student_login"])
    worksheet.write(row, 4,v["student_url"])
    worksheet.write(row, 5,part1_result)
    worksheet.write(row, 6,part2_result)
    worksheet.write(row, 7,part3_result)

workbook.close()





'''
for idx,v in tqdm(team_dict.items()):
    teams[idx] = {}
    teams[idx].update(v)
    
    url = v["url"]+" "
    folder_name = "{}/teams/{}".format(path_name,v["team_name"])
    target_name = "{}/players/{}".format(path_name,v["team_name"])
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    if not os.path.exists(target_name):
        # os.system("cd "+path_name)
        # os.mkdir("players/"+v["team_name"])
        # os.system("cd ../..")
        os.system("mkdir -p "+target_name)
        print("This is target name: "+target_name)

    teams[idx]["git_res"] = os.system(base + url + folder_name)
    
    if len(os.listdir(folder_name)) == 0:
        teams[idx]["git_succ"] = False
    else:
        teams[idx]["git_succ"] = True
        os.system("cp -r "+folder_name+"/players/*"+" "+target_name)
'''

# os.system("cp -r ./*py "+path_name)
# os.system("cp -r ./players/*py "+path_name+"/players")

# #run the competition
# l = list(team_dict.keys())
# competition_list = list(itertools.product(l,l))

# print ("running competitions, totally {} matches".format(len(competition_list)))

# def run_match(match_idx,players):
#     matches = {}
#     t1,t2 = players
#     if t1 == t2:
#         matches[match_idx] = {"succ":False}
#         return matches
#     if not teams[t1]["git_succ"]:
#         matches[match_idx] = {"succ":False}
#         return matches
#     if not teams[t2]["git_succ"]:
#         matches[match_idx] = {"succ":False}
#         return matches

#     options = run_options()
#     options.red = path_name.replace("/",".") + ".players.{}.".format(teams[t1]["team_name"]) + 'myPlayer'
#     options.blue = path_name.replace("/",".") + ".players.{}.".format(teams[t2]["team_name"]) + 'myPlayer'
#     # print("RED TEAM: "+options.red)
#     options.redName = teams[t1]["team_name"]
#     options.blueName = teams[t2]["team_name"]
#     options.textgraphics = False
#     options.quiet = True
#     options.superQuiet = True
#     options.warningTimeLimit = 1
#     options.startRoundWarningTimeLimit= 5
#     options.numOfWarnings = 3
#     options.multipleGames = 2
#     options.setRandomSeed = random.randint(0,1e10)
#     options.saveGameRecord = True
#     options.output = path_name + "/results"
#     options.saveLog = True
#     options.replay = None
#     options.delay = 0

#     matches[match_idx] = run(options)
#     matches[match_idx]["r_idx"] = t1
#     matches[match_idx]["b_idx"] = t2  
#     matches[match_idx]["succ"] = True  

#     return matches


# tres = Parallel(n_jobs=PARALLEL_THREADS)(delayed(run_match)(idx,players) for idx,players in enumerate(tqdm(competition_list)))
# print ("Combining match result...")
# for match in tres:
#     matches.update(match)
    
# '''
# for no,(t1,t2) in enumerate(tqdm(competition_list)):
#     if t1 == t2:
#         continue
        
#     if not teams[t1]["git_succ"]:
#         continue
#     if not teams[t2]["git_succ"]:
#         continue
        
#     match_idx += 1

#     options = run_options()
#     options.red = path_name.replace("/",".") + ".players.{}.".format(teams[t1]["team_name"]) + 'myPlayer'
#     options.blue = path_name.replace("/",".") + ".players.{}.".format(teams[t2]["team_name"]) + 'myPlayer'
#     # print("RED TEAM: "+options.red)
#     options.redName = teams[t1]["team_name"]
#     options.blueName = teams[t2]["team_name"]
#     options.textgraphics = False
#     options.quiet = True
#     options.superQuiet = True
#     options.warningTimeLimit = 1
#     options.startRoundWarningTimeLimit= 1
#     options.numOfWarnings = 3
#     options.multipleGames = 2
#     options.setRandomSeed = random.randint(0,1e10)
#     options.saveGameRecord = True
#     options.output = path_name + "/results"
#     options.saveLog = True
#     options.replay = None
#     options.delay = 0

#     matches[match_idx] = run(options)
#     matches[match_idx]["r_idx"] = t1
#     matches[match_idx]["b_idx"] = t2
# '''





# # import csv
# # with open('result.csv', 'w', newline='') as file:
# #     writer = csv.writer(file)
# #     writer.writerow(["team_id", "team_name","team_url","git_success","myPlayer"])
    
# #statistic
# print ("analysising results")

# for idx,v in teams.items():
#     v["total_score"] = 0
#     v["total_game"] = 0
#     v["total_win"] = 0
#     v["total_lose"] = 0
#     v["total_tie"] = 0
#     v["total_load_err"] = 0
    
# for idx,v in matches.items():
#     if not v["succ"]:
#         continue
#     load_err = False
#     for teamName, err in v["load_errs"].items():
#         load_err = True
#         teamMap = {"teamRed":"r_idx","teamBlue":"b_idx"}
#         teams[v[teamMap[teamName]]]["total_load_err"] +=1
#     if load_err:
#         continue
    
#     rt = teams[v["r_idx"]]
#     bt = teams[v["b_idx"]]
    
#     rt["total_score"] += v["r_avg"] * v["options"].multipleGames
#     rt["total_game"] += v["options"].multipleGames
#     rt["total_win"] += v["r_win"]
#     rt["total_lose"] += v["options"].multipleGames - v["r_win"]
#     rt["total_tie"] += v["tie"]
    
#     bt["total_score"] += v["b_avg"] * v["options"].multipleGames
#     bt["total_game"] += v["options"].multipleGames
#     bt["total_win"] += v["b_win"]
#     bt["total_lose"] += v["options"].multipleGames - v["b_win"]
#     bt["total_tie"] += v["tie"]
    
# for i,v in teams.items():
#     v["final_score"] = v["total_score"] + v["total_win"]*50 + v["total_tie"]*20
#     # with open('result.csv', 'a', newline='') as file:
#     #     writer = csv.writer(file)
#     #     writer.writerow([v["team_id"], v["team_name"], v["url"], v["git_succ"],v["total_load_err"]==0])
#     row = row + 1
#     worksheet.write(row, 0,v["team_id"])
#     worksheet.write(row, 1,v["team_name"])
#     worksheet.write(row, 2,v["url"])
#     worksheet.write(row, 3,v["git_succ"])
#     worksheet.write(row, 4,v["total_load_err"]==0)

# workbook.close()

# tres = sorted(teams.items(), key = lambda x: x[1]["final_score"], reverse=True)
# reses = []
# for rank,(i,res) in enumerate(tres):
#     tdict = res
#     res["id"] = i
#     res["rank"] = rank+1
#     reses.append(res)
# import json

# with open(path_name + "/result.json",'w') as f:
#     json.dump(reses,f)


