price_up_da = \
f"""

select 
user_status,
new_postlevel,
active_tag,
user_aging,
case 
when active_tag = '非活跃用户'  then 'A1.非活跃用户'
when non_white_ind = 'N' or non_black_ind = 'N' then 'B1.黑名单和白名单'
when is_black_list = 'Y' then 'B2.黑名单拒绝'
when credit_relative_days < 90 then 'B3.授信小于90天'
when age <= 22 then 'B4.年龄<=22岁'
when non_overdue_ind = 'N' then 'C.当前逾期'
when new_postlevel in ('A','B') then 'C1.非B卡尾部'
when user_rate*3.6 >= 23.8 then 'D.当前定价高于23.8'
else 'Z.负向准入' end as new_admit_flag,
case when user_rate*3.6 < 14 then '<14'
when user_rate*3.6 < 16 then '[14~16)'
when user_rate*3.6 < 18 then '[16-18)'
when user_rate*3.6 <20 then '[18-20)'
else '[20~24]'
end rate_cut,
count(1) cnt,
sum(user_rate) user_rate,
sum(new_rate) new_rate,
sum(cash_balance) cash_balance,
sum(temp_line+basic_line) xm_line,
sum(income_score) income_score
from xmid_base 
where date =  {{date2}}
group by 1,2,3,4,5,6
"""
#get data
price_up_da = qry.getSpark2(price_up_da)
#check strategy data
price_up_da.groupby('new_admit_flag').agg(cnt=('cnt', 'sum')).sort_values('new_admit_flag')

#output user list 
price_up_list = \
f"""
SELECT 
user_id,
new_postlevel,
active_tag,
case when dhrandom > 25 then '实验组' else '对照组' end exp_control,
user_rate,
new_rate,
cash_balance,
xm_line,
income_score
from (
select 
user_id,
new_postlevel,
active_tag,
case 
when active_tag = '非活跃用户'  then 'A1.非活跃用户'
when non_white_ind = 'N' or non_black_ind = 'N' then 'B1.黑名单和白名单'
when is_black_list = 'Y' then 'B2.黑名单拒绝'
when credit_relative_days < 90 then 'B3.授信小于90天'
when age <= 22 then 'B4.年龄<=22岁'
when non_overdue_ind = 'N' then 'C.当前逾期'
when new_postlevel in ('A','B') then 'C1.非B卡尾部'
when user_rate*3.6 >= 23.8 then 'D.当前定价高于23.8'
when is_zhongan = 'Y' then 'E.众安用户'
else 'Z.负向准入' end as new_admit_flag,
cast( floor(rand()*100) as int) dhrandom,
user_rate*100 user_rate,
round(new_rate,1)*100 new_rate,
cash_balance,
temp_line+basic_line xm_line,
income_score income_score
from xmid_base
where date =  {{date2}}
) t1  
where new_admit_flag = 'Z.负向准入'
"""
#get user list
price_up_list = qry.getSpark2(price_up_list)
price_up_list.head(10)

#check user is unique
print("Count of distinct user_id:", price_up_list['user_id'].nunique())
print("Total count:", len(price_up_list))

#check before rate and new rate is correct
result = price_up_list.groupby('exp_control').agg(
    cnt=('exp_control', 'size'),
    user_rate=('user_rate', 'sum'),
    new_rate=('new_rate', 'sum')
)
result['user_rate'] = (result['user_rate'] / 100 / result['cnt'] * 3.6)
result['new_rate'] = (result['new_rate'] / 100 / result['cnt'] * 3.6)
result

#save data to excel
import datetime as dt
exp_date ='20'+ dt.datetime.now().strftime('%y%m%d')
print(exp_date)

#add new colume before save
price_up_list['date'] = exp_date
price_up_list['policy_name'] = "贷中活跃尾部提价"
price_up_list['policy_type'] = "提价"
price_up_list['sub_test_control'] = "NA"
price_up_list['new_amount'] = price_up_list['xm_line']
price_up_list['is_active'] = 1
price_up_list_upload = price_up_list[['date','user_id','policy_name','policy_type','exp_control','sub_test_control','is_active','new_amount','xm_line','user_rate','new_rate']]
price_up_list_upload.head(10)
price_up_list_upload.to_excel(f"price_up_list_upload_{exp_date}.xlsx", index=False)
