import glob
import pandas as pd
import json
config = json.load(open('./config.json', 'r'))


# root = config['data_dir'] + '/zx_kzsttj2019.csv'
root = config['data_dir'] + '/kzstty2020_result.csv'
files = glob.glob(root)
files.sort()
print(files)
sizes = []
for file in files:
    # year = file.split('.')[0][-4:]
    year = file.split('_')[0][-4:]
    print(year)
    data = pd.read_csv(file, encoding='gbk')
    
    geohashes = list(data['geohash'])
    with open(config['data_dir'] + f'/geohashes.txt', 'w') as f:
        f.write('\n'.join(geohashes))


    # 去除这三个变量： 'geohash', 'geohash_ejz', 'sj', 'kzstmj', 以及索引列 'Unnamed: 0'
    # # 2019-2021
    # continous_features = ['gdmj', 'ydmj', 'ldmj', 'cdmj', 'sdmj', 'nyssjsydmj', 'jtysydmj', 'czjsydmj', 'cunzjsydmj', 'sgssydmj', 'ldsy', 'wlyd', 'tchd',
    #                 'gdggmj', 'gdxtzs', 'yn_2017', 'yphx', 'gc', 'pd', 'rksl']
    # categorial_features = ['gdmjdj', 'ydmjdj', 'ldmjdj', 'cdmjdj', 'sdmjdj', 'nyssjsydmjdj', 'jtysydmjdj', 'czjsydmjdj', 'cunzjsydmjdj', 'sgssydmjdj',
    #                  'ldsydj', 'wlyddj', 'trzd', 'trlx', 'nyjgyqyds', 'jzzfwzjl']
    #
    #
    # # 2022
    # continous_features = ['gdmj', 'ydmj', 'ldmj', 'cdmj', 'sdmj', 'nyssjsydmj', 'jtysydmj', 'czjsydmj', 'cunzjsydmj', 'sgssydmj','ldsy', 'wlyd', 'gdbhmb_2022',
    #                         'yn_2022', 'stbhhx_2022', 'czkfbj_2022','yphx', 'gc', 'pd', 'rksl', 'tchd', 'gdggmj', 'gdxtzs']
    # categorial_features = ['gdmjdj', 'ydmjdj', 'ldmjdj', 'cdmjdj', 'sdmjdj', 'nyssjsydmjdj', 'jtysydmjdj', 'czjsydmjdj', 'cunzjsydmjdj', 'sgssydmjdj', 'ldsydj',
    #                         'wlyddj', 'trlx', 'nyjgyqyds', 'jzzfwzjl', 'trzd']

    # new data
    continous_features = 'sgssydmj,gdggmj,lszwmjzb,fjmsjtsydmj,gdmj,gc,gdhb,tchdz,cunzjsydmj,czjsydmj,ckjytydmj,pdhx,nyssjsydmj,lszwmj,cdmj,gbzntmjzb,sdmj,pop2020,jbnt_2022,gdxtzs,pd,ldsy,jtysydmj,wlyd,jbntcbq,jbntzbq,yphx,ydmj,gbzntmj,jbnt_2017,dxqfd,ldmj'.split(',')
    categorial_features = 'jzydljl2020,nyjgyqyds,trlx,TRZD,ztgnq_2023,jhljl,ztgnq_2017,jzzfwzjl'.split(',')



    # 填补缺失值
    # value = {
    #     'tchd':0,
    #     'trzd':1000,
    #     'gdggmj':0,
    #     'gdxtzs':0,
    #     'rksl': 0
    # }

    # data = data.fillna(value=value)
    data = data.fillna(0) # [NEW]

    # [NEW] object类型特征映射
    TRZD_map = {'0': 0, '壤土': 1, '砂土': 2, '黏土': 3}
    ztgnq_2017_map = {'0': 0, '国家农产品主产区': 1, '国家重点开发区域': 2, '国家重点生态功能区': 3,
                      '省级重点开发区域': 4,
                      '省级重点生态功能区': 5}
    data['TRZD'] = data['TRZD'].apply(lambda x: TRZD_map[str(x)])
    data['ztgnq_2017'] = data['ztgnq_2017'].apply(lambda x: ztgnq_2017_map[str(x)])

    total = continous_features + categorial_features
    with open(config['data_dir'] + f'/feature_sizes_{year}.txt', 'w') as f:
        feature_sizes = []
        for i in range(len(total)):
            feature = total[i]
            feature_sizes.append(str(len(list(set(data[feature])))))

        f.write(','.join(feature_sizes))
