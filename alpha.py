# import openpyxl
import xlrd
# import xlwt


def read03Excel(path):
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()
    print('test=========',sheets)

    if 'Sheet' in sheets[0]:
        print(sheets[0])
        aim_sheet_name=sheets[0]
    else:
        aim_sheet_name=sheets[1]
    worksheet = workbook.sheet_by_name(aim_sheet_name)
    for i in range(0, worksheet.nrows):
        row = worksheet.row(i)
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")
        print()


def read_sheet(path):
    working_file = xlrd.open_workbook(path)
    sheets = working_file.sheet_names()
    if 'Sheet' in sheets[0]:
        aim_sheet_name=sheets[0]
    else:
        aim_sheet_name=sheets[1]

    working_sheet = working_file.sheet_by_name(aim_sheet_name)
    answer_dict = {}
    for row_index in range(0, working_sheet.nrows):
        answer_dict[working_sheet.cell_value(row_index, 0)] = working_sheet.cell_value(row_index, 1).strip().split('，')
    return answer_dict


if __name__ == '__main__':
    file_path = '.\\141_160_answer.xls'
    case_00_path='.\\test_case_00.xlsx'
    # read03Excel(case_00)

    # ans= '崎岖，神圣，制裁'
    # test= '崎岖的'
    # print(test in ans or ans in test)

    case_00=read_sheet(case_00_path)
    ground_truth=read_sheet(file_path)
    total_number=0
    wrong_answers_number=0
    for key in case_00:
        total_number+=1
        if case_00[key][0] not  in ground_truth[key]:
            print('[ERROR!]row number: {}, word: {}, ground_truth: {}, answer: {}'.format(total_number,key,ground_truth[key],case_00[key]))
            wrong_answers_number+=1
    print('Checking Complete : Total words: {}, error occurs:{} correct rate: {}%'.format(total_number,wrong_answers_number,(total_number-wrong_answers_number)/total_number*100))


