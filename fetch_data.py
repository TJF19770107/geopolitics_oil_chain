# -*- coding: utf-8 -*-
"""
大道量化系统 - 因子驱动1.0
商品期货1小时K线数据拉取脚本
数据源: Yahoo Finance
品种: 黄金GC、白银SI、原油CL、天然气NG、小麦W
"""
import sys
import io
# 修复Windows GBK编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import time
import datetime
import pandas as pd

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'

try:
    import yfinance as yf
except ImportError:
    print("安装 yfinance...")
    os.system(f"{sys.executable} -m pip install yfinance -q")
    import yfinance as yf

# 品种配置
# Yahoo Finance 1h 数据限制: 最多730天，但实际只能拿到约60天内的精确1h数据
# 解决方案: 分段拉取1h数据 (每次最多60天窗口，累计覆盖730天)
SYMBOLS = {
    "GC": {"ticker": "GC=F", "name": "黄金", "unit": "USD/oz"},
    "SI": {"ticker": "SI=F", "name": "白银", "unit": "USD/oz"},
    "CL": {"ticker": "CL=F", "name": "原油WTI", "unit": "USD/bbl"},
    "NG": {"ticker": "NG=F", "name": "天然气", "unit": "USD/MMBtu"},
    "W":  {"ticker": "ZW=F", "name": "小麦CBOT", "unit": "USc/bu"},
}

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

end_dt = datetime.datetime.now()
start_dt = end_dt - datetime.timedelta(days=730)

def fetch_chunked(ticker_code, start, end, chunk_days=58):
    """分段拉取1h数据，每段最多58天"""
    all_frames = []
    current_start = start
    
    while current_start < end:
        current_end = min(current_start + datetime.timedelta(days=chunk_days), end)
        
        # Yahoo Finance 1h 数据要求：起始时间不能超过730天前
        # 如果current_start距今超过729天，跳过
        days_ago = (datetime.datetime.now() - current_start).days
        if days_ago > 729:
            current_start = current_end
            continue
        
        try:
            ticker = yf.Ticker(ticker_code)
            df_chunk = ticker.history(
                start=current_start.strftime("%Y-%m-%d"),
                end=current_end.strftime("%Y-%m-%d"),
                interval="1h",
                auto_adjust=True,
                prepost=False,
            )
            if df_chunk is not None and not df_chunk.empty:
                all_frames.append(df_chunk)
                print(f"  段 {current_start.strftime('%Y-%m-%d')} ~ {current_end.strftime('%Y-%m-%d')}: {len(df_chunk)} 条")
            else:
                print(f"  段 {current_start.strftime('%Y-%m-%d')} ~ {current_end.strftime('%Y-%m-%d')}: 空")
        except Exception as e:
            err_msg = str(e)
            if "1h data not available" in err_msg or "startTime" in err_msg:
                print(f"  段 {current_start.strftime('%Y-%m-%d')}: 超出1h可用范围，跳过")
            else:
                print(f"  段 {current_start.strftime('%Y-%m-%d')}: 错误 {err_msg[:80]}")
        
        current_start = current_end
        time.sleep(0.5)
    
    if not all_frames:
        return None
    
    combined = pd.concat(all_frames)
    combined.index = pd.to_datetime(combined.index)
    return combined


def fetch_and_save(symbol, config):
    ticker_code = config["ticker"]
    name = config["name"]
    print(f"\n[拉取] {name}({symbol}) => {ticker_code}")
    
    try:
        df = fetch_chunked(ticker_code, start_dt, end_dt)
        
        if df is None or df.empty:
            print(f"  无数据返回，跳过")
            return None
        
        # 标准化
        df.index.name = "datetime"
        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.columns = ["open", "high", "low", "close", "volume"]
        
        # 去重、排序
        df = df[~df.index.duplicated(keep="last")]
        df = df.sort_index()
        
        # 时间戳转UTC naive
        if df.index.tzinfo is not None:
            df.index = df.index.tz_convert("UTC").tz_localize(None)
        
        save_path = os.path.join(RAW_DIR, f"{symbol}_1h.csv")
        df.to_csv(save_path, encoding='utf-8')
        
        print(f"  保存: {save_path}")
        print(f"  范围: {df.index[0]} => {df.index[-1]}")
        print(f"  条数: {len(df)}")
        return df
        
    except Exception as e:
        print(f"  拉取失败: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("大道量化系统 - 因子驱动1.0 数据拉取")
    print(f"目标范围: {start_dt.strftime('%Y-%m-%d')} => {end_dt.strftime('%Y-%m-%d')}")
    print(f"注: Yahoo Finance 1h数据限制730天内(实际约60天/批)")
    print(f"保存目录: {RAW_DIR}")
    print("=" * 60)
    
    results = {}
    for symbol, config in SYMBOLS.items():
        df = fetch_and_save(symbol, config)
        results[symbol] = df
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("拉取汇总：")
    success_count = 0
    for symbol, df in results.items():
        name = SYMBOLS[symbol]["name"]
        if df is not None:
            print(f"  OK {name}({symbol}): {len(df)} 条")
            success_count += 1
        else:
            print(f"  FAIL {name}({symbol}): 失败")
    print(f"\n成功: {success_count}/{len(SYMBOLS)} 个品种")
    print("=" * 60)
