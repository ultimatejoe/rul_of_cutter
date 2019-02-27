# 数据预处理
# 文件结构
**1.1sensor_integrated.ipynb**   
sensor文件整合,只使用新的数据集(train_add),旧的数据集(train_qLua)存在着电流和振动信号名称混淆的问题  

**1.2train_plc_RULR.ipynb**   
根据plc文件为训练集添加训练标签, 即剩余寿命占比RULR

**1.3sensor_id_sort.ipynb**   
给train_plc添加id和sort_col,因为tsfresh提取特征需要使用id和sort_col

**3.1sensor_clean.ipynb**   
填充nans、infs和简单的过于异常值（比如数值大小接近float64的上下界）处理naive_outlier

**3.2sensor_ad_mean_avg.ipynb**   
使用滑动标准差作为置信边带，找到并填充异常值为滑动均值

**4.1sensor_tsfresh_comprehensive.ipynb**   
使用tsfresh提取特征

 - 使用tsfresh提取时间序列的特征
 使用的条件：我们需要给特征提取器设置id和sort_col,其中id指示片段编号，sort_col指示段内编号
下表给出了一个例子，把时间序列分割成长度为3的片段：  

| feature      | id   |  sort_col  |
| -  | -----:  | :----:  |
|      |     0 |   0     |
|      |     0 |   1     |
|      |     0 |   2     |
|      |     1 |   0     |
|      |     1 |   1     |
|      |     1 |   2     |
|      |     2 |   0     |
|      |     2 |   1     |
|      |   ... |   ...   |

**6.1concat_plc_sensors.ipynb**   
只保留plc的['RULR', 'csv_no', 'CL', 'CLI', 'spindle_load']与sensor进行拼接。

 - 拼接的方法
 在数据采样频率方面，PLC信号采样频率为33Hz，震动传感器采样频率25600Hz。
因此一条plc数据对应上百条的sensor数据，因此在上一步使用tsfresh提取特征的时候，我们就采取“分段平均”的方法来确定时间片段。具体做法如下：
$$片段长度 = sensor文件长度 / plc文件长度$$

需要说明的是：这里未使用刀具的走刀数据（即x，y，z）的原因是它们被单独分离出来做工况模式的聚类。  

**7.1more_feature.ipynb**  
由于tsfresh提取的是用户自定义的时间片段内的统计特征，在这里连续的时间片段之间可能存在数据点的数量不一致的问题，因此需要对像'abs_energy'的特征求段内平均。
例：
    $$AbsEnergyScale = AbsEnergy / 这一段总的样本数$$
    
**8.1cut_concats.ipynb**   
删除存在“停机”状态的片段，停机状态下刀具未发生磨损。

**9.select_features**  

 - 1.explore_feature.ipynb
使用特征的信息熵（entropy）和排列熵（permutation entropy） 作为特征选择指标。
本项目选用的是2阶排列熵，2阶排列熵可以很好地指示特征序列的单调性，排列熵越小，序列单调性越好。刀具磨损指标是具有单调性的，我们期望筛选出排列熵较小的特征来进行下一步的训练。

 - 2.select_feature.ipynb
基于上一步的探索得到的参数进行特征选择。







