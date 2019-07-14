# import openpyxl
import os
import re

import xlrd
# import xlwt


# def read03Excel(path):
#     workbook = xlrd.open_workbook(path)
#     sheets = workbook.sheet_names()
#     print('test=========',sheets)
#
#     if 'Sheet' in sheets[0]:
#         print(sheets[0])
#         aim_sheet_name=sheets[0]
#     else:
#         aim_sheet_name=sheets[1]
#     worksheet = workbook.sheet_by_name(aim_sheet_name)
#     for i in range(0, worksheet.nrows):
#         row = worksheet.row(i)
#         for j in range(0, worksheet.ncols):
#             print(worksheet.cell_value(i, j), "\t", end="")
#         print()


def read_sheet(path):#for *.xls files
    working_file = xlrd.open_workbook(path)
    sheets = working_file.sheet_names()
    if 'Sheet' in sheets[0]:
        aim_sheet_name=sheets[0]
    else:
        aim_sheet_name=sheets[1]

    working_sheet = working_file.sheet_by_name(aim_sheet_name)
    sheet_dict = {}
    for row_index in range(0, working_sheet.nrows):
        try:
            sheet_dict[working_sheet.cell_value(row_index, 0)] = working_sheet.cell_value(row_index, 1).strip().replace('；','，').split('，')
        except IndexError:
            pass
    return sheet_dict

def record_ground_truth(path):
    ground_truth={}
    for excel_dir in os.listdir(path):
        # print('reading files: ',excel_dir)
        ground_truth.update(read_sheet('.\\ground_truth\\'+excel_dir))
    return ground_truth

def check_answer(student_answer,book):
    total=0
    wrong=0
    print('row,      word,    student_answer,   groundTruth')

    # for word in student_answer:
    #     total+=1
    #     # if student_answer[word][0] not in book[word]:
    #     if not check_match(student_answer[word][0],book[word]):
    #         wrong+=1
    #         print(total,word,student_answer[word], book[word],wrong)
    for word in student_answer:
        total+=1
        correct_flag=0#if correct correct_flag==1 else 0
        for meaning in student_answer[word] :
            if check_match(meaning,book[word]):
                correct_flag=1
                break
        if not correct_flag:
            wrong+=1
            print(total,word,student_answer[word], book[word])

    print('wrong#:',wrong)
    print('total#:',total)

def check_match(student,book_list):
    if not student:
        return False
    for answer in book_list:
        if re.search(student,answer) or re.search(answer,student):
            return True
    return False

if __name__ == '__main__':
    case_00_path='.\\101-200词测(3).xlsx'
    ground_truth_folder='.\\ground_truth'
    ground_truth_dict=record_ground_truth(ground_truth_folder)
    for i in ground_truth_dict:
        if ground_truth_dict[i] == '':
            print('ERROR!!!',i,ground_truth_dict[i])
            break
    case_00=read_sheet(case_00_path)

    check_answer(case_00,ground_truth_dict)
    print('================test=================')
    print(case_00)
    # print("TEST==============================")
    # print(case_00['ensconce'])
    # print(check_match('ensconce',ground_truth_dict['ensconce']))
    # print(ground_truth_dict['ensconce'])



