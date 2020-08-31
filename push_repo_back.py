import os
import time

path = "20-May-2020-18-35-15-505489"
results_dict = {}




for i,d in enumerate(sorted(os.listdir(path))):
    print(d)
    if os.path.isdir(os.path.join(path,d)):
        os.chdir(os.path.join(path,d))
        succ_add = os.system("git add .") == 0
        succ_commit = os.system('git commit -m "online planner running result feedback"') == 0
        succ_push = os.system('git push') == 0
        print("add ok: {}".format(succ_add))
        print("commit ok: {}".format(succ_commit))
        print("push ok: {}".format(succ_push))
        results_dict.update({i:{"student_id":d,"succ_add":succ_add,"succ_commit":succ_commit,"succ_push":succ_push}})
        os.chdir("../..")

import xlsxwriter 
  
workbook = xlsxwriter.Workbook('{}.xlsx'.format(path)) 
worksheet = workbook.add_worksheet()
row = 0
worksheet.write(row, 0,"student_id")
worksheet.write(row, 1,"succ_add")
worksheet.write(row, 2,"succ_commit")
worksheet.write(row, 3,"succ_push")


for item in results_dict.values():
    row = row +1
    worksheet.write(row, 0,item["student_id"])
    worksheet.write(row, 1,item["succ_add"])
    worksheet.write(row, 2,item["succ_commit"])
    worksheet.write(row, 3,item["succ_push"])


workbook.close()