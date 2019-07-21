# import openpyxl
import os
import re
import time

import xlrd
import test01
import pickle
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

def check_answer(student_answer,book,youdao_dict):
    # youdao_dict = pickle.load(open('.\\youdao_dict_file.pkl', 'rb'))# youdao_dict={word:[meaning0,m1,...],...,...}

    total=0
    result={}
    '''
    result is a dict result={'word0':{'row_number':#,'student_meaning'=[],'SAT_meanings':[m0,m1,m2],'youdao_meanings':[m00,m01,m02]},
                              'word1':
                              }
    '''
    print('row,      word,    student_answer,   groundTruth')

    for word in student_answer:
        # print('TEST: check word :', word)
        total+=1
        correct_flag=0#if correct correct_flag==1 else 0
        for meaning in student_answer[word] :#in case of student type in more meanings of one word
            #CAUTION! replace '的，得，地'may cause meaning errors! but correct rate may increase!
            if not meaning:
                result[word]={'row_number':total,'student_meaning':None,'SAT_meanings':book[word],'youdao_meanings':youdao_dict[word]}
                break
            if check_match(meaning,book[word]+youdao_dict[word]):
                correct_flag=1
                break
        if not correct_flag and student_answer[word][0]!='':
            result[word]={'row_number':total,'student_meaning':student_answer[word],'SAT_meanings':book[word],'youdao_meanings':youdao_dict[word]}
            # print(total,word,student_answer[word], book[word])


    # print('total#:',total)
    # print('=================test========================')
    # res_wrong_words=[]
    # for word in result['wrong_words']:
    #     # print(word) word is a tuple(#, word)
    #     online_meaning=test01.getAllMeanings(word[1])
    #     for student_meaning in student_answer[word[1]]:
    #         if not check_match(student_meaning,online_meaning):
    #             res_wrong_words.append((word[1],student_answer[word[1]]))
    # print(res_wrong_words)
    # print(len(res_wrong_words))


    return result

def check_match(student,book_list):
    if not student:
        return False
    # print('test',student,book_list)
    student=student.strip('的').strip('得').strip('地')
    for answer in book_list:
        if re.search(student,answer) or re.search(answer,student):
            return True
    return False

def get_online_meanings(word):
    return test01.getAllMeanings(word)


def _create_local_youdao_dict(words_dict):
    youdao_dict={}
    n=0
    for word in words_dict:
        youdao_dict[word]=test01.getAllMeanings(word)
        n+=1
        time.sleep(0.5)
        if not n%10:
            print('{}/853'.format(n))
    _save_data_in_local(youdao_dict,'youdao_dict_file.pkl')

def _save_data_in_local(data,file_path):
    '''
    :param data: youdao_dict={'word':[meanings,....]}
    :param file_path:
    :return: store data in file_path as a file
    '''
    import pickle
    with open(file_path,'wb' ) as f:
        pickle.dump(data,f)

if __name__ == '__main__':
    case_00_path='.\\test_cases\\1-100词测.xlsx'
    ground_truth_folder='.\\ground_truth'


    #===============checking grond_truth_dict================================
    # for i in ground_truth_dict:
    #     if ground_truth_dict[i] == '' or not ground_truth_dict[i] or ground_truth_dict[i]==' ':
    #         print('ERROR!!!',i,ground_truth_dict[i])
    #         break
    #     if not i:
    #         print('EMPTY word!')
    #         break
    #
    # print('FINISH READING ALL GROUND TRUTH!')
    # print(len(ground_truth_dict))
    #================= finish checking ================================
    # create_local_youdao_dict(ground_truth_dict) #this is used for create local youdao dict file
    # =======================================================================
    case_00=read_sheet(case_00_path)

    ground_truth_dict=record_ground_truth(ground_truth_folder)# record all word:meanings in ground truth dict
    youdao_dict = pickle.load(open('.\\youdao_dict_file.pkl', 'rb'))# youdao_dict={word:[meaning0,m1,...],...,...}
    result=check_answer(case_00,ground_truth_dict,youdao_dict)
    print('================test=================')
    # print(result)
    empty_words=[]
    for i in result:
        if result[i]['student_meaning']:
            print(i,result[i])
        else:
            empty_words.append(i)
    print('TEST total wrong words #: ', len(result))
    print('TEST empty words are', empty_words)
    print('TEST total wrong words # except empty words',len(result)-len(empty_words))
    print('TEST total exam word number:',len(case_00))