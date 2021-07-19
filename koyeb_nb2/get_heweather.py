"""Fetch heweather info."""
# pylint: disable=too-many-locals, pointless-string-statement

import logging
# import asyncio
import requests

# from force_async import force_async
from jsonpath_match import jp

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

APIKEY = '1cd16d5de7d248e0b90130c85f2252a9'
URL = 'https://free-api.heweather.net/s6/weather'


# @force_async
async def get_heweather(city: str = '深圳')-> str:
# def get_heweather(city: str = '深圳')-> str:
    ''' get he weather '''
    payload = dict(
        location=city,
        lang="cn",
        unit="m",
        key=APIKEY,
    )
    try:
        resp = requests.post(URL, data=payload, verify=False, timeout=(60, 90))
        resp.raise_for_status()
    except Exception as exc:
        LOGGER.error(exc)
        return str(exc)

    try:
        jdata = resp.json()
    except Exception as exc:
        LOGGER.error(exc)
        return str(exc)

    status = jp.match('$..status', jdata)
    # if status != ['ok']:
    if 'ok' not in status:
        return str(status)

    # jp.match('$..', jdata):
    # In [211]: jdata['HeWeather6'][0].keys()
    # Out[211]: dict_keys(['basic', 'update', 'status', 'now', 'daily_forecast', 'lifestyle'])

    # In [198]: jp.match('$..date', jdata)
    # Out[198]: ['2019-02-07', '2019-02-08', '2019-02-09']
    # In [199]: jp.match('$..tmp_min', jdata)
    # Out[199]: ['20', '20', '18']
    # In [200]: jp.match('$..tmp_max', jdata)
    # Out[200]: ['27', '27', '25']
    # In [201]: jp.match('$..cond_txt_d', jdata)
    # Out[201]: ['多云', '多云', '小雨']
    # In [203]: jp.match('$..cond_txt_n', jdata)
    # Out[203]: ['多云', '小雨', '小雨']
    ''' {city}天气：{cond_txt_now}，气温：{tmp_now}℃，体感温度：{fl_now}℃。当前湿度：{hum_now}%，风力：{wind_sc_now}。

    未来三天天气预测：
    {date_0}
    温度：{tmp_min_0}℃ ~ {tmp_max_0}℃ 白天天气{cond_txt_d_0}，晚间天气{cond_txt_n_0}
    湿度：{hum_0}%，紫外线强度指数：{uv_index_0}，风力：{wind_sc_0}

    {date_1}\n温度：{tmp_min_1}℃ ~ {tmp_max_1}℃\n白天天气{cond_txt_d_1}，晚间天气{cond_txt_n_1}
    湿度：{hum_1}%，紫外线强度指数：{uv_index_1}，风力：{wind_sc_1}

    {date_2}
    温度：{tmp_min_2}℃ ~ {tmp_max_2}℃
    白天天气{cond_txt_d_2}，晚间天气{cond_txt_n_2}
    湿度：{hum_2}%，紫外线强度指数：{uv_index_2}，风力：{wind_sc_2}\n\nPowered by 和风天气'
    '''

    # https://www.heweather.com/blog/wind-speed-vs-wind-scale
    wind_cat = [
        '无风', '软风', '轻风', '微风', '和风',
        '清风', '强风', '劲风', '大风', '烈风',
        '狂风', '暴风', '台风']
    now_items = [
        'cond_txt', 'tmp', 'fl', 'hum',
        'wind_dir', 'wind_spd', 'wind_sc']
    now_data = [jp.match(f'$..now..{elm}', jdata)[0] for elm in now_items]

    # convert wind_sc to wind_cat
    try:
        w_c = int(now_data[-1])
        now_data[-1] = wind_cat[w_c]
    except Exception as exc:
        LOGGER.error(exc)
        # not converted to specical cases

    # {city}天气：{cond_txt_now}，气温：{tmp_now}℃，体感温度：{fl_now}℃。当前湿度：{hum_now}%，风力：{wind_sc_now}。
    now_str = '{}天气：{}，气温：{}℃，体感温度：{}℃，当前湿度：{}%，{}, 风速：{}千米/小时， {}。'.format(city, *now_data)

    fc_items = [
        "date", "cond_txt_d", "cond_txt_n",
        "tmp_min", "tmp_max", "uv_index",
        "hum", "wind_sc"
    ]
    fc_data = [jp.match(f'$..daily_forecast..{elm}', jdata) for elm in fc_items]

    # fc_templ = '{}：日间{}，晚间{}，气温{}-{}℃，{}，相对湿度{}%，风力{}级\n'

    # fc_templ = '{:11}{:>5}{:>5}{:^7}{:^7}{:^3}{:^6}{:5}\n'
    fc_templ = '{:11}{:>6}{:>6}{:>6}{:>6}{:>3}{:>6}{:>6}\n'
    fc_header_data = [
        '',
        '日间', '晚间',
        '最低(度)', '最高(度)',
        '紫指',
        '湿度(%)', '风力(级)'
    ]
    fc_header = fc_templ.format(*fc_header_data)

    # fc_str = '未来3日天气预报\n'
    fc_str = ''
    fc_str += fc_header
    for idx in range(3):
        # data = [elm[idx] for elm in fc_data]
        data = []
        for elm in fc_data:
            if len(elm) > idx:
                data += [elm[idx]]
            else:
                data += ['[]']

        fc_str += fc_templ.format(*data)

    # print(fc_str)

    return now_str + '\n' + fc_str + '\n(数据来源：和风天气 https://www.heweather.com/)'
