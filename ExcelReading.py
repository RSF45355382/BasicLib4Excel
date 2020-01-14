import pandas,os

def read_Csv(filename):
    '''
    读取csv文件
    :param filename:文件路径
    :return:
    '''
    try:
        DataFrame = pandas.read_csv(filename)
    except Exception as e:
        print('Error occured when opening excel file: {}'.format(e))
        return pandas.DataFrame(columns=['Empty'])
    return DataFrame

'''
标准pandas读取Excel函数, 从filename路径读取sheetname_list中的任意一个sheet, 只要发现任意一个就返回
打开文件失败或者没有sheetname,则返回空的DataFrame
'''
def read_Excel(filename,sheetname_list):
    # 标准读取Excel ,如果没有对应的sheet名, 返回一个空的DataFrame
    try:
        DataFrame = pandas.ExcelFile(filename)
    except Exception as e:
        print('Error occured when opening excel file: {}'.format(e))
        return pandas.DataFrame(columns=['Empty'])

    DataFrame_sheetnames = DataFrame.sheet_names
    # print(DataFrame_sheetnames)
    if sheetname_list:
        for each in sheetname_list:
            if each in DataFrame_sheetnames:
                return DataFrame.parse(each)
        print('No one sheet named {} Detected in file {}'.format(str(sheetname_list), filename))
    else:
        print('No sheetname provided.')
    return pandas.DataFrame(columns=['Empty'])

'''
检验DataFrame中是否包含所需的所有column(按照colname来索引)
'''
def validate_DataFrameCol(DataFrame,colname_list):
    # 检查DataFrame是否含有必要的列
    col_names = DataFrame.columns
    for each in colname_list:
        if each not in col_names:
            print('Column {} Not Detected in DataFrame'.format(each))
            return False
    return True

'''
检验DataFrame中是否包含所需的所有column(按照colname来索引)
'''
def validate_DataFrameColType(DataFrame,coltype_dict):
    for each_col,each_type in coltype_dict.items():
        try:
            DataFrame[each_col] = DataFrame[each_col].astype(each_type)
        except ValueError:
            print('There are ValueError in "{}" Column. Data Type Should Be "{}". Please check.\n'.format(each_col, each_type))
            return 'There are ValueError in "{}" Column. Data Type Should Be "{}". Please check.'.format(each_col,each_type)
    return 'Data Validated, All columns type correct.'


def read_valid_Excel(filename,sheetname_list,coltype_dict,colname_list):
    DataFrame = read_Excel(filename,sheetname_list)
    if not DataFrame.empty and validate_DataFrameCol(DataFrame,colname_list):
        check_result = validate_DataFrameColType(DataFrame, coltype_dict)
        # print(check_result)
        if check_result == 'Data Validated, All columns type correct.':
            return DataFrame[colname_list]
    return pandas.DataFrame(columns=['Empty'])

def read_valid_csv(filename,coltype_dict,colname_list):
    DataFrame = read_Csv(filename)
    if not DataFrame.empty and validate_DataFrameCol(DataFrame,colname_list):
        check_result = validate_DataFrameColType(DataFrame, coltype_dict)
        # print(check_result)
        if check_result == 'Data Validated, All columns type correct.':
            return DataFrame[colname_list]
    return pandas.DataFrame(columns=['Empty'])

def read_valid_dataframe(filename,coltype_dict,colname_list,sheetname_list = None):
    '''
    读取文件,csv或者Excel文件
    :param filename: 文件路径
    :param coltype_dict: 需要的列的类型 - 字典格式
    :param colname_list: 需要的列-列表格式
    :param sheetname_list: 如果读取的是Excel需要提供需要读取的sheet名
    :return:读取到的DataFrame或者空的DataFrame
    '''
    file_suf = os.path.splitext(filename)[filename][-1]
    if file_suf in ['.xlsx','.xls','.xlsm']:
        return read_valid_Excel(filename,sheetname_list,coltype_dict,colname_list)
    elif file_suf in ['.csv']:
        return read_valid_csv(filename,coltype_dict,colname_list)
    else:
        print('File [{}] suffix - [{}] nor right.'.format(filename, file_suf))
        return pandas.DataFrame(columns=['Empty'])

def add_DataFrame2sheet(sheet,dataframe):
    '''
    向一个openpyxl的sheet对象中写入pandas.DataFrame
    :param sheet:openpyxl的sheet对象
    :param dataframe:需要写入的pandas.DataFrame
    :return:
    '''
    index_list = dataframe.index.tolist()
    for i in index_list:
        value = dataframe.loc[i].tolist()
        sheet.append(value)




