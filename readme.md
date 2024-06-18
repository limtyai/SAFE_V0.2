执行步骤如下：
1. split_dataset.py 
2. get_spatialdata.py 
3. preprocess.py 
4. main.py

```
│  config.json
│  geohash.py
│  get_spatialdata.py
│  main.py
│  preprocess.py
│  readme.md
│  split_dataset.py
├─data
│  │  2020_balanced_test.csv
│  │  2020_balanced_train.csv
│  │  2020_balanced_valid.csv
│  │  2020_real_test.csv
│  │  2020_real_train.csv
│  │  2020_real_valid.csv
│  │  dataset.py
│  │  feature_sizes_2020.txt
│  │  geohashes.txt
│  │  geohash_to_index.txt
│  │  kzstty2020_result.csv
│  └─ __init__.py
│
├─log
├─model
│  │  Classifier.py
│  │  losses.py
│  │  mobilenet.py
│  │  SAFE.py
│  │  TabTransformer.py
│  │  vig.py
│  │  __init__.py
│  │
│  └─gcn_lib
│    │  pos_embed.py
│    │  torch_edge.py
│    │  torch_nn.py
│    │  torch_vertex.py
│    └─ __init__.py
│
└─result
    │  best_1000.pt
    └─ best_80.pt
```

