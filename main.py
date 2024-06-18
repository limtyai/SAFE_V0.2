import numpy as np
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.utils.data import sampler
import random
from data.dataset import CriteoDataset
from torch.optim.lr_scheduler import CosineAnnealingLR, MultiStepLR
from model.SAFE import SAFE
import json

# 
# seeds = [20, 178, 1637, 34, 590, 1000, 80,168, 367, 491]
seeds = [80,168, 367, 491]

for seed in seeds:

     print()
     print('------------------------------------------------')
     print(f'random seed: {seed}')
     config = json.load(open('./config.json', 'r'))
     print(config)

     def data_collator(data_list):
          input_id = data_list[0]
          print(len(input_id))
          return data_list


     def setup_seed(seed):
          torch.manual_seed(seed)
          torch.cuda.manual_seed_all(seed)
          np.random.seed(seed)
          random.seed(seed)
          torch.backends.cudnn.deterministic = True

     setup_seed(seed)

     # 900000 items for training, 10000 items for valid, of all 1000000 items
     batch_size = 1000
     year = 2020
     print(year)

     feature_sizes = np.loadtxt(config['data_dir'] + f'/feature_sizes_{year}.txt', delimiter=',')
     feature_sizes = [int(x) for x in feature_sizes]
     print(feature_sizes)
     num_cate = 0
     num_cont = 0
     for num in feature_sizes:
          if num > 100:
               num_cont += 1
          else:
               num_cate += 1
     print(num_cate, num_cont)

     # continous_features = ['gdmj', 'ydmj', 'ldmj', 'cdmj', 'sdmj', 'nyssjsydmj', 'jtysydmj',
     # 'czjsydmj', 'cunzjsydmj', 'sgssydmj', 'ldsy', 'wlyd', 'tchd',
     #                     'gdggmj', 'gdxtzs', 'yn_2017', 'yphx', 'gc', 'pd', 'rksl']
     # categorial_features = ['gdmjdj', 'ydmjdj', 'ldmjdj', 'cdmjdj', 'sdmjdj', 'nyssjsydmjdj',
     # 'jtysydmjdj', 'czjsydmjdj', 'cunzjsydmjdj', 'sgssydmjdj',
     #                      'ldsydj', 'wlyddj', 'trzd', 'trlx', 'nyjgyqyds', 'jzzfwzjl']

     continous_features = ('sgssydmj,gdggmj,lszwmjzb,fjmsjtsydmj,gdmj,gc,gdhb,tchdz,cunzjsydmj,czjsydmj,'
                           'ckjytydmj,pdhx,nyssjsydmj,lszwmj,cdmj,gbzntmjzb,sdmj,pop2020,jbnt_2022,gdxtzs,'
                           'pd,ldsy,jtysydmj,wlyd,jbntcbq,jbntzbq,yphx,ydmj,gbzntmj,jbnt_2017,dxqfd,ldmj').split(',')
     categorial_features = 'jzydljl2020,nyjgyqyds,trlx,TRZD,ztgnq_2023,jhljl,ztgnq_2017,jzzfwzjl'.split(',')

     print(len(categorial_features), len(continous_features))


     # load data
     val_data = CriteoDataset(config['data_dir'], train=True, mode='valid', year=year)
     loader_val = DataLoader(val_data, batch_size=batch_size, shuffle=False)
     test_data = CriteoDataset(config['data_dir'], train=False, mode='test', year=year)
     loader_test = DataLoader(test_data, batch_size=batch_size, shuffle=False)
     train_data = CriteoDataset(config['data_dir'], train=True, year=year)
     loader_train = DataLoader(train_data, batch_size=batch_size, shuffle=True)
     train_data_test = CriteoDataset(config['data_dir'], train=True, mode='train_test', year=2019)
     loader_train_test = DataLoader(train_data_test, batch_size=batch_size, shuffle=False)

     model = SAFE(feature_sizes, seed=seed, num_categories=num_cate, num_continuous=num_cont, config=config, batch_size=batch_size, use_cuda=True)
     optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=0.0)
     model.fit(loader_train, loader_val, loader_test, optimizer, config, year, epochs=10, verbose=True)

     del batch_size, train_data, loader_train, val_data, loader_val, test_data, loader_test, feature_sizes, model, optimizer, num_cate, num_cont
