# 健康评估模型

在缺乏工况数据的情况下，原始的健康指标的趋势性很差。我们通过对健康指标的曲线做平滑处理来保留其长期的趋势特征，同时提取健康指标曲线的斜率和波动幅度的统计特征来尽可能保留趋势性。但是在此，还是要强调一下，健康模型的方法并不适用于多工况的情况。但是这里健康模型的代码中一些时间序列处理的方法仍然具有通用性，比如，utils.py。所以仍然保留了这一部分代码。  
 <div><img src="https://github.com/ultimatejoe/rul_of_cutter/blob/master/%E5%81%A5%E5%BA%B7%E6%8C%87%E6%A0%87%E6%95%88%E6%9E%9C%E4%B8%8D%E7%90%86%E6%83%B3.PNG"/>                        
</div>  
<center>健康模型的方法并不适用于多工况</center>  

**1.1PCA_T2_train.ipynb**  
使用train的前10%左右的数据来构建健康模型

**1.2train_HA.ipynb**  
生成训练集的健康指标 (PCA_T2)

**2.1PCA_T2_test.ipynb**  
查看测试集的健康指标

**2.2test_HA.ipynb**  
生成测试集的健康指标 (PCA_T2)

**4.1show_train_HA.ipynb**  
查看训练集的健康指标

**4.2show_test_HA.ipynb**  
查看测试集的健康指标

**4.3delta.ipynb**  
健康指标的随时间的变化幅度(delta)

**4.4mean.ipynb**  
对健康指标进行平滑处理并提取曲线的一阶导数特征。

**4.5gen_HA_feature.ipynb**  
生成基于健康指标的统计特征，并输出保存。

**4.6window_HA_feature.ipynb**  
数据压缩，例：
train_01的原始的健康指标时间序列长度在10万左右，对应实际时间的跨度为240min。压缩的过程是每5min的数据平均成一个数据点，即最后结果是长度为48的时间序列。

**utils.py**  
封装了cl_curve_smooth和curve_derivative两个函数。

 - cl_curve_smooth
 函数集成了 numpy.polyfit 多项式拟合，Scipy的curve_fit，稳健的滑动平均以及hamper_filter四种曲线平滑的方法。
 - curve_derivative
 函数的功能是对一个时间序列的函数求导。


