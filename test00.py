import re

ans = ['崎岖的','神圣','制裁']
test0 = '崎岖'
test1='神圣的'

# print(re.search('崎岖','可。。崎岖的'))
# print(re.search('神圣的','神圣'))
# print(re.search('神圣','神圣的'))
# if re.search('神圣','神圣的'):
#     print('yes')
# else:
#     print('No')

test3='信誉；学分'
print(test3.replace(',','!').replace('；',','))



import pickle
# saveTest={'a':1,'b':2,'c':3}

# file='list_test.pkl'
# with open(file,'wb' ) as f:
#     pickle.dump(saveTest,f)
data=pickle.load(open('.\\youdao_dict_file.pkl','rb'))
print(data)
print(len(data))