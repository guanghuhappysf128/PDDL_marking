

import sys
import chardet
import requests
import tqdm
import json


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



def run_single(path_name):

    # running the solvers




    print("\nStart planning for {}".format(path_name))
    domain = ""
    problem = ""
    error_info ={}

    # path_name = "{}/{}".format(path_name,v["student_id"]


    # part 1
    part1_result=-1
    domain,error_msg = readFiles(path_name,"part1_domain.pddl")
    if not error_msg == {}: error_info.update(error_msg)

    problem,error_msg = readFiles(path_name,"part1_problem.pddl")
    if not error_msg == {}: error_info.update(error_msg)
    
    data = {'domain': domain, 'problem': problem}
    resp = requests.post('http://solver.planning.domains/solve',
                        verify=False, json=data).json()
    resp.update(error_info)
    with open("{}/part1_run.json".format(path_name),'w') as f:
        json.dump(resp,f)
    if resp["status"]=="ok":
        with open("{}/part1.plan".format(path_name), 'w') as f:
            try:
                f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
            except TypeError:
                f.write("\n".join(resp['result']['plan']))
        with open("{}/part1.plan".format(path_name), 'r') as f:
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
    domain,error_msg = readFiles(path_name,"part2_domain.pddl")
    if not error_msg == {}: error_info.update(error_msg)

    problem,error_msg = readFiles(path_name,"part2_problem.pddl")
    if not error_msg == {}: error_info.update(error_msg)
    
    data = {'domain': domain, 'problem': problem}
    resp = requests.post('http://solver.planning.domains/solve',
                        verify=False, json=data).json()

    resp.update(error_info)
    with open("{}/part2_run.json".format(path_name),'w') as f:
        json.dump(resp,f)

    if resp["status"]=="ok":
        with open("{}/part2.plan".format(path_name), 'w') as f:
            try:
                f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
            except TypeError:
                f.write("\n".join(resp['result']['plan']))
        with open("{}/part2.plan".format(path_name), 'r') as f:
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
    domain,error_msg = readFiles(path_name,"part3_domain.pddl")
    if not error_msg == {}: error_info.update(error_msg)

    problem,error_msg = readFiles(path_name,"part3_problem.pddl")
    if not error_msg == {}: error_info.update(error_msg)
    
    data = {'domain': domain, 'problem': problem}
    resp = requests.post('http://solver.planning.domains/solve',
                        verify=False, json=data).json()
    resp.update(error_info)
    with open("{}/part3_run.json".format(path_name),'w') as f:
        json.dump(resp,f)

    if resp["status"]=="ok":
        with open("{}/part3.plan".format(path_name), 'w') as f:
            try:
                f.write('\n'.join([act['name'] for act in resp['result']['plan']]))
            except TypeError:
                f.write("\n".join(resp['result']['plan']))
        with open("{}/part3.plan".format(path_name), 'r') as f:
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

        with open("{}/part3.plan".format(path_name), 'r') as f:
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

        with open("{}/part3.plan".format(path_name), 'r') as f:
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


if __name__ == '__main__':
    file_path = "late/1104647/comp90054-2020-a2"
    run_single(file_path)