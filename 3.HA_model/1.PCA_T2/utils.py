import numpy as np
import pandas as pd
import joblib
import warnings
import collections
from itertools import zip_longest
from scipy.optimize import curve_fit
from scipy.misc import derivative

def cl_curve_smooth(var_list, seg_cl, up_thred=30, down_thred=0, confidence=0.5, fit_type='numpy_poly_fit', correct_cl=[], return_cureve_func=False):
    '''
    描述：
        对输入的曲线，根据var_list和seg_cl进行平滑
        
    '''
    var_list_copy = var_list.copy()
    my_fit_func_dict = None

    
    # 使用正常数据拟合粗趋势,适用于'numpy_poly_fit'和'scipy_curve_fit'
    
    # 标记超出阈值的样本为-1
    for i in range(len(var_list)):
        idx_var = var_list[i]
        if (idx_var>up_thred) or (idx_var<down_thred):
            var_list[i] = -1
            
    ser = pd.Series(var_list)
    ser.index = seg_cl #index
    ser[correct_cl] = -1
    # 使用正常数据
    if sum(ser != -1)<=1:
        print('超出阈值的样本数量过多！')
    x_train = ser.index[ser != -1].values
    y_train = ser[ser != -1].values

    if fit_type == 'numpy_poly_fit':
        # 使用numpy.polyfit 多项式拟合
        f1 = np.polyfit(x_train, y_train, 2)
        p1 = np.poly1d(f1)
        tmp = p1(seg_cl)
        var_list = list(tmp)

        if return_cureve_func:
        	my_fit_func_dict = {'numpy_poly_fit':p1}

    elif fit_type == 'scipy_curve_fit':
        # 使用Scipy的curve_fit　
        def func(x_train, a, b):
            return a*pow(x_train,b)

        popt, pcov = curve_fit(func, x_train, y_train)
        tmp = func(seg_cl, *popt)
        var_list = list(tmp)
        if return_cureve_func:
        	def fit_func(x):
        		return popt[0]*pow(x,popt[1])

        	my_fit_func_dict = {'scipy_curve_fit':fit_func}

    elif fit_type == 'moving_robust_avg':

        # 稳健的滑动平均,注意：这里假设没有重复的极值，所以使用var_list_copy
        
        def robust_mean(series):
            the_min = series.min()
            the_max = series.max()
            left_series = series[(series > the_min) & (series < the_max)]
            tmp = np.mean(left_series)
            result = tmp
            if tmp > up_thred:
                result = up_thred
            if tmp <= down_thred:
                result = down_thred

            return result
        
        var_ser = pd.Series(var_list_copy).rolling(window=5, center=True, min_periods=1).agg(robust_mean) 
        var_list = list(var_ser)
    elif fit_type == 'hamper_filter':
        # 
        def hampel_filter(iterable_like, k ,t0):
            y = np.array(iterable_like)
            n = len(y)
            L = 1.4826
            for i in np.arange(k,n-k):
                y0 = np.median(y[(i-k):(i+k)]) # 中值
                S0 = L * np.median(np.abs(y[(i-k):(i+k)]) - y0)  # 距离“第一次中值”的残差
                if np.abs(y[i]-y0) > t0*S0:
                    y[i] = y0
            
            # min max scale
            y_minmax = y.copy()
            # y_minmax = (y-y.min())/(y.max()-y.min())
            out = y_minmax.reset_index(drop=True)
            return out

    else:
        raise ValueError('wrong fit_type')
    
    # 纠正
    for i in range(len(var_list)):
        idx_var = var_list_copy[i]
        cmp_var = var_list[i]
        if np.abs(idx_var - cmp_var) >= confidence:
            pass
        else:
            var_list[i] = idx_var 
     
    return seg_cl, var_list, my_fit_func_dict 

def curve_derivative(fun_dict, x, order=1):
	'''
	描述：
		函数关于x（1维）的导数
	'''
	if 'numpy_poly_fit' in fun_dict.keys():
		fun = fun_dict['scipy_curve_fit']
		return np.polyder(fun, order)(x) # 求order阶导数

	if 'scipy_curve_fit' in fun_dict.keys():
		fun = fun_dict['scipy_curve_fit']
		diff_list = []
		for i in x:
			diff_list.append(derivative(fun, i, dx=1e-6, n=order))
		return np.array(diff_list)

