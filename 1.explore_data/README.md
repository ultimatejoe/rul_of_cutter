# 数据探索
关于数据详细描述，见[刀具剩余寿命预测-数据介绍](http://www.industrial-bigdata.com/competition/competitionAction!showDetail34.action?competition.competitionId=3)
## 文件结构
**1.1新旧数据一致性探索.ipynb**
官方一共提供了两次数据，数据源是相同的，查看数据的变化
**1.2explore_sensor_clean_cut.ipynb** 
探索sensor文件的inf分布情况、nans分布情况、naive_outliers(绝对值接近数值溢出阈值的异常值)分布情况，并分别保存：  
*'./train_clean_condition/nans_condition_tuple'*   
*'./train_clean_condition/infs_condition_tuple'*   
*'./train_clean_condition/outliers_condition_tuple'*  
**1.3explore_train_plc_cut.ipynb**
plc文件记录了刀具的工况数据，工况参数包括:  

| 字段名        | 说明   | 
| --------   | -----:  |
| time     | 记录时间 |
| spindle_load     | 主轴负载 | 
| x        |   x轴机械坐标   | 
| y        |    y轴机械坐标  |  
| z        |   z轴机械坐标 |

根据plc文件，我们使用tsfresh包提取特征，然后通过画图的方式来查看提取的特征与工况参数之间的关联性，人工选择合适的参数，最后聚类。  
关于聚类的数量，我们把3台设备的数据拼接，观察得到的种类数是4。  
**2.1explore_test_plc_cut.ipynb**  
对test集的plc数据进行探索  
**3.1explore_final.ipynb**    
对final集的plc数据进行探索



