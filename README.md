# 大道量化系统 · 因子驱动1.0 | 地缘产业链策略库

> 建立时间：2026-03-31  
> 版本：终极版 (Ultimate)  
> 终极修复日期：2026-03-31

## 项目简介

本项目是**大道量化系统**的因子驱动1.0模块，专注于大宗商品（黄金、白银、原油、天然气、小麦）的地缘政治与产业链传导量化研究。

## 目录结构

```
daodao_geopolitics_oil_chain/
├── data/
│   └── raw/              # 原始1H K线数据 (Yahoo Finance)
│       ├── GC_1h.csv     # 黄金 (10521条)
│       ├── SI_1h.csv     # 白银 (10518条)
│       ├── CL_1h.csv     # 原油WTI (10352条)
│       ├── NG_1h.csv     # 天然气 (10314条)
│       └── W_1h.csv      # 小麦CBOT (8524条)
├── docs/
│   └── factor_drive_v1.0_plan.md   # 因子驱动1.0完整方案
├── html/
│   ├── chart_data.json   # v1可视化数据
│   └── chart_data_v2.json # v2全周期数据 (3577KB)
├── kline_viewer.html      # v1交互式K线图
├── kline_viewer_v2.0.html # v2全量数据版 (3.5MB，已弃用)
├── kline_viewer_v2.1.html # v2.1增强版 (47KB，数据外置)
├── kline_viewer_ultimate.html # 终极版 (60KB，自定义周期+均线)
├── kline_viewer_template.html # 通用模板
├── fetch_data.py          # 数据拉取脚本
├── gen_html.py            # v1 HTML生成脚本
├── gen_v2_data.py         # v2数据聚合脚本（CSV→多周期JSON）
├── gen_v2_html.py         # v2 HTML生成脚本
├── gen_v21_html.py        # v2.1 HTML生成脚本
└── gen_ultimate_html.py   # 终极版HTML生成脚本
```

## 核心定位

**从经验交易型 → 因子驱动型（因果驱动）**

| 品种 | 核心驱动因子 | 传导方向 |
|------|------------|---------|
| 黄金GC | 地缘避险 / 美元走弱 / 降息预期 | 涨 |
| 白银SI | 黄金联动 / 工业需求 | 补涨 |
| 原油CL | OPEC减产 / 霍尔木兹 / 地缘冲突 | 涨 |
| 天然气NG | 原油联动 / 季节需求 | 补涨 |
| 小麦W | 天然气→尿素→成本传导 / 黑海供给 | 涨 |

## 产业链传导图谱

```
地缘事件/OPEC → 原油CL (即时) → 天然气NG (+1~3天) → 小麦W (+5~10天)
避险情绪 → 黄金GC (即时) → 白银SI (+0.5~2天)
```

## 快速使用

1. 打开 `kline_viewer_ultimate.html` 即可查看5品种K线+全部功能
   - 需要 `html/chart_data_v2.json` 在同目录下
2. 运行 `python fetch_data.py` 更新最新数据
3. 运行 `python gen_v2_data.py` 重新聚合多周期数据
4. 运行 `python gen_ultimate_html.py` 重新生成终极版K线图

### 终极版功能 (Ultimate)
- **自定义周期**：支持任意周期 (2H/6H/12H/3D等)，前端实时从1H聚合
- **自定义均线系统**：SMA/EMA/WMA切换，参数/颜色/线型/粗细全部可配，配置持久化保存
- **MACD/BOLL 技术指标**：工具栏一键切换，MACD含副图
- **产业链传导面板**：可视化CL→NG→W、GC→SI传导路径
- **键盘快捷键**：←→切换品种、M=MACD、B=BOLL、C=产业链、E=导出CSV
- **CSV导出**：一键导出当前品种/周期数据
- **配置持久化**：周期/均线/最后品种等全部保存到localStorage
- **价格精度自适应**：根据品种价格自动调整小数位
- **42事件因子+14趋势节点**：完整的因子标注体系

### 数据校验标准 (固化规则)
- OHLC严格校验：high≥max(open,close), low≤min(open,close)
- 涨跌幅=(close-open)/open*100%，禁止用历史低点计算
- 聚合周期volume为累计值
- 跨周期一致性：1H最后收盘价=聚合周期收盘价
- 零价格/NaN/重复时间戳全部清除

## 大道心法

> 不预测，只识别；不预判，只跟随。  
> 以K线为相，以量价为证，以结构为凭，以历史为镜。  
> 境由心转，而非心由境转。
