# -*- coding: utf-8 -*-
"""数据质量诊断脚本"""
import pandas as pd, os

RAW_DIR = 'data/raw'
for f in sorted(os.listdir(RAW_DIR)):
    if not f.endswith('.csv'): continue
    df = pd.read_csv(os.path.join(RAW_DIR, f), parse_dates=['datetime'])
    print(f'=== {f} ===')
    print(f'  Rows: {len(df)} | Range: {df["datetime"].iloc[0]} ~ {df["datetime"].iloc[-1]}')
    print(f'  Columns: {list(df.columns)}')
    ohlcv = ['open','high','low','close','volume']
    for c in ohlcv:
        if c in df.columns:
            print(f'  Nulls({c}): {df[c].isnull().sum()}')
    zero_mask = (df['open']==0)|(df['high']==0)|(df['low']==0)|(df['close']==0)
    print(f'  Zero prices: {zero_mask.sum()}')
    dup = df['datetime'].duplicated().sum()
    print(f'  Duplicate datetimes: {dup}')
    # Check OHLC consistency
    bad_ohlc = ((df['high'] < df['low']) | (df['high'] < df['open']) | (df['high'] < df['close']) | 
                (df['low'] > df['open']) | (df['low'] > df['close'])).sum()
    print(f'  Bad OHLC (high<low etc): {bad_ohlc}')
    # Latest price
    last = df.iloc[-1]
    print(f'  Last: {last["datetime"]} O={last["open"]} H={last["high"]} L={last["low"]} C={last["close"]}')
    print()
