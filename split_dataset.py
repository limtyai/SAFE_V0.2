import pandas as pd
import glob
import random
import json
config = json.load(open('./config.json', 'r'))

# file = config['data_dir'] + '/zx_kzsttj2019.csv'
file = config['data_dir'] + '/kzstty2020_result.csv'
print(file)
 
dataset_modes = ['real', 'balanced']
for dataset_mode in dataset_modes:
    # df = pd.read_csv(file)
    df = pd.read_csv(file,encoding='gbk')
    print(df.shape)
    geohashes = list(df['geohash'])

    # 新数据的Label有大量空值
    df['kzstmj'].fillna(0,inplace=True)
    is_kzst = df[df['kzstmj']>7266]
    not_kzst = df[df['kzstmj']<=7266]
    # print(is_kzst.shape, not_kzst.shape)
    is_kzst = is_kzst.sample(frac=1).reset_index(drop=True)
    not_kzst = not_kzst.sample(frac=1).reset_index(drop=True)
    print(is_kzst.shape,not_kzst.shape)

    if dataset_mode == 'real':
        valid_length_is_kzst = len(is_kzst) // 10
        valid_length_not_kzst = len(not_kzst) // 10  ###hugh
        test_length_is_kzst = len(is_kzst) * 2 // 10   ###hugh
        test_length_not_kzst = len(not_kzst) * 2 // 10
        valid_pd = pd.concat([is_kzst[:valid_length_is_kzst], not_kzst[:valid_length_not_kzst]])
        test_pd = pd.concat([is_kzst[valid_length_is_kzst: valid_length_is_kzst+test_length_is_kzst], not_kzst[valid_length_not_kzst: valid_length_not_kzst+test_length_not_kzst]])
        train_pd = pd.concat([is_kzst[valid_length_is_kzst+test_length_is_kzst:], not_kzst[valid_length_not_kzst+test_length_not_kzst:]])
    else:
        valid_length = 62
        test_length = 124
        valid_pd = pd.concat([is_kzst[:valid_length], not_kzst[:valid_length]])
        test_pd = pd.concat([is_kzst[valid_length: valid_length+test_length], not_kzst[valid_length: valid_length+test_length]])
        train_pd = pd.concat([is_kzst[valid_length+test_length:], not_kzst[valid_length+test_length:]])

    valid_pd = valid_pd.sample(frac=1).reset_index(drop=True)
    test_pd = test_pd.sample(frac=1).reset_index(drop=True)
    train_pd = train_pd.sample(frac=1).reset_index(drop=True)
    print(train_pd.shape,test_pd.shape,valid_pd.shape)

    # year = file.split('/')[-1].split('.')[0]
    year = file.split('/')[-1].split('_')[0][-4:]
    train_name = config['data_dir'] + f'/{year}_{dataset_mode}_train.csv'
    valid_name = config['data_dir'] + f'/{year}_{dataset_mode}_valid.csv'
    test_name = config['data_dir'] + f'/{year}_{dataset_mode}_test.csv'
    valid_pd.to_csv(valid_name)
    train_pd.to_csv(train_name)
    test_pd.to_csv(test_name)

    print('-'*20)



