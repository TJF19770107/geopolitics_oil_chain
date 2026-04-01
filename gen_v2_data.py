# -*- coding: utf-8 -*-
"""
大道量化系统 v2.0 数据生成脚本
- 读取全量730天1H CSV数据
- 聚合生成4H/日K/周K/月K
- 导出供HTML内嵌的JSON
- 校验数据完整性
"""
import pandas as pd
import json
import os
import math

RAW_DIR = 'data/raw'
OUT_FILE = 'html/chart_data_v2.json'

SYMBOLS = {
    'GC': {'name': '黄金 Gold', 'unit': 'USD/oz', 'color': '#f5c518'},
    'SI': {'name': '白银 Silver', 'unit': 'USD/oz', 'color': '#c0c0c0'},
    'CL': {'name': '原油WTI', 'unit': 'USD/bbl', 'color': '#ff6b35'},
    'NG': {'name': '天然气', 'unit': 'USD/MMBtu', 'color': '#4fc3f7'},
    'W':  {'name': '小麦', 'unit': 'USc/bu', 'color': '#a5d6a7'},
}

def resample_ohlcv(df, rule):
    """聚合K线数据"""
    df2 = df.set_index('datetime')
    agg = df2.resample(rule).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna(subset=['open','close'])
    agg = agg.reset_index()
    return agg

def safe_float(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return round(float(v), 4)

def df_to_bars(df):
    """转换为 [datetime, open, high, low, close, volume] 列表"""
    bars = []
    for _, row in df.iterrows():
        dt = row['datetime']
        if hasattr(dt, 'strftime'):
            dt_str = dt.strftime('%Y-%m-%d %H:%M')
        else:
            dt_str = str(dt)[:16]
        o = safe_float(row['open'])
        h = safe_float(row['high'])
        l = safe_float(row['low'])
        c = safe_float(row['close'])
        v = safe_float(row['volume'])
        if o is None or c is None:
            continue
        bars.append([dt_str, o, h, l, c, v or 0])
    return bars

out_data = {}

for sym, cfg in SYMBOLS.items():
    fpath = os.path.join(RAW_DIR, f'{sym}_1h.csv')
    if not os.path.exists(fpath):
        print(f'WARN: {fpath} not found, skip')
        continue

    df = pd.read_csv(fpath, parse_dates=['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)

    # 数据校验
    null_count = df[['open','high','low','close']].isnull().sum().sum()
    print(f'{sym}: {len(df)} bars | {df["datetime"].iloc[0]} ~ {df["datetime"].iloc[-1]} | nulls={null_count}')

    # 各周期聚合
    periods = {
        '1H': df.copy(),
        '4H': resample_ohlcv(df, '4h'),
        '1D': resample_ohlcv(df, '1D'),
        '1W': resample_ohlcv(df, '1W'),
        '1M': resample_ohlcv(df, 'MS'),
    }

    period_data = {}
    for period, pdf in periods.items():
        bars = df_to_bars(pdf)
        period_data[period] = bars
        print(f'  {period}: {len(bars)} bars')

    # 校验: 1H黄金最新收盘价
    last_bar = period_data['1H'][-1]
    print(f'  Last 1H bar: {last_bar[0]} O={last_bar[1]} H={last_bar[2]} L={last_bar[3]} C={last_bar[4]}')

    out_data[sym] = {
        'name': cfg['name'],
        'unit': cfg['unit'],
        'color': cfg['color'],
        'periods': period_data
    }

os.makedirs('html', exist_ok=True)
with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(out_data, f, ensure_ascii=False, separators=(',', ':'))

size_kb = os.path.getsize(OUT_FILE) / 1024
print(f'\nExported to {OUT_FILE} ({size_kb:.1f} KB)')
print('Data generation complete.')
