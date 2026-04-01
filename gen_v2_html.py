# -*- coding: utf-8 -*-
"""
大道量化系统 v2.0 HTML生成脚本
生成 kline_viewer_v2.0.html（含全量数据）
和 kline_viewer_template.html（通用模板）
"""
import json, os

# 读取预生成的全量数据JSON
with open('html/chart_data_v2.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 精简数据：每个周期只保留关键字段
# bar格式: [dateStr, open, high, low, close, volume]
# 为了控制HTML大小，1H数据取全量，其他周期也全量
data_json = json.dumps(raw_data, ensure_ascii=False, separators=(',', ':'))
data_size = len(data_json.encode('utf-8'))
print(f'Data JSON size: {data_size/1024:.1f} KB')

# ============================================================
# 事件因子数据库（完整版）
# ============================================================
EVENTS = [
    # 黄金 GC
    {"sym":"GC","date":"2024-06-12","type":"bull","title":"美联储暂停加息","factor":"降息预期因子","detail":"美联储6月会议暂停加息，暗示年内降息，黄金避险需求+降息预期双驱动","logic":"美元走弱→黄金上涨；降息预期上升→黄金配置需求增加","avg_move":"+2.1%","signal":"开多","trend":"上涨趋势确立"},
    {"sym":"GC","date":"2024-07-19","type":"bear","title":"特朗普支持比特币","factor":"避险因子减弱","detail":"特朗普共和党大会发表亲加密货币演讲，风险资产上涨，黄金获利回吐","logic":"风险偏好上升→黄金资金外流→短期回调","avg_move":"-1.5%","signal":"平多"},
    {"sym":"GC","date":"2024-09-18","type":"bull","title":"美联储降息50bp","factor":"降息因子触发","detail":"美联储超预期降息50bp，历史性节点。美元指数快速下跌，黄金突破历史高位","logic":"大幅降息→实际利率下降→黄金持仓成本降低→机构买入","avg_move":"+3.8%","signal":"开多","trend":"强势上涨趋势"},
    {"sym":"GC","date":"2024-11-05","type":"bear","title":"特朗普当选美国总统","factor":"特朗普因子","detail":"特朗普当选后美元指数暴涨，黄金短期承压下跌，但中期地缘风险依然利多","logic":"特朗普当选→美元走强→黄金短期承压；但贸易战预期→长期利多","avg_move":"-2.3%","signal":"减仓观望"},
    {"sym":"GC","date":"2025-01-20","type":"bull","title":"特朗普就职+关税威胁","factor":"地缘避险+关税因子","detail":"特朗普就职首日签署一系列行政令，对加、墨加征25%关税，全球贸易战担忧升温","logic":"贸易战→全球经济不确定性→避险需求→黄金上涨","avg_move":"+4.2%","signal":"开多","trend":"上涨趋势确立"},
    {"sym":"GC","date":"2025-04-02","type":"bull","title":"关税战全面升级","factor":"贸易战避险因子","detail":"特朗普宣布对所有进口商品加征基础关税10%+对中国商品加征50%，全球市场恐慌","logic":"关税战→全球衰退预期→大规模避险买入黄金→金价暴涨","avg_move":"+6.5%","signal":"开多","trend":"强势突破上涨"},
    {"sym":"GC","date":"2025-06-15","type":"bear","title":"美联储暂停降息","factor":"降息预期收缩","detail":"美联储6月会议暂停降息，表态鹰派，美元反弹，黄金获利回吐","logic":"暂停降息→实际利率预期上升→黄金持仓成本增加→回调","avg_move":"-3.1%","signal":"平多/减仓"},
    {"sym":"GC","date":"2025-08-05","type":"bull","title":"中东冲突再升级","factor":"地缘避险因子","detail":"以色列-伊朗冲突再升级，中东局势高度紧张，全球避险情绪暴涨","logic":"中东冲突→原油供给风险→全面避险→黄金白银同步暴涨","avg_move":"+5.2%","signal":"开多","trend":"上涨趋势确立"},
    {"sym":"GC","date":"2025-11-20","type":"bull","title":"美联储再次降息25bp","factor":"降息因子","detail":"美联储连续第三次降息，累计降息125bp，黄金创历史新高","logic":"持续降息→美元持续走弱→黄金系统性上涨","avg_move":"+2.8%","signal":"加仓"},
    {"sym":"GC","date":"2026-02-10","type":"bull","title":"地缘风险全面升温","factor":"全球避险因子","detail":"多地地缘冲突同时爆发，全球央行持续购金，黄金需求创历史记录","logic":"多因子共振：地缘+降息+央行购金→黄金突破新高","avg_move":"+4.1%","signal":"开多","trend":"历史性牛市确立"},
    {"sym":"GC","date":"2026-03-10","type":"bull","title":"黄金突破4600美元","factor":"技术突破+多因子共振","detail":"黄金突破4600关键阻力，MACD金叉，成交量放大，多因子完全共振","logic":"技术面突破+基本面支撑→趋势加速上涨","avg_move":"+3.5%","signal":"开多加仓","trend":"加速上涨趋势"},

    # 白银 SI
    {"sym":"SI","date":"2024-09-19","type":"bull","title":"黄金联动带动白银","factor":"黄金联动因子+工业需求","detail":"Fed降息后黄金大涨，白银跟随上涨，工业需求（光伏/新能源）同步驱动","logic":"黄金上涨→金银比值修复→白银补涨，滞后0.5-2天","avg_move":"+4.5%","signal":"开多","trend":"补涨趋势"},
    {"sym":"SI","date":"2025-01-22","type":"bull","title":"白银滞后补涨启动","factor":"黄金联动+工业需求","detail":"特朗普关税战后黄金先涨，白银补涨启动，光伏装机量创新高推动工业需求","logic":"白银兼具避险+工业属性，弹性更大，补涨幅度通常超过黄金","avg_move":"+6.8%","signal":"开多","trend":"补涨加速"},
    {"sym":"SI","date":"2025-08-07","type":"bull","title":"中东危机 金银同步暴涨","factor":"避险+工业共振","detail":"中东冲突带动全面避险，白银同步暴涨，一天内涨幅超黄金","logic":"地缘危机→避险因子触发→白银弹性大于黄金→超额收益","avg_move":"+7.2%","signal":"开多"},
    {"sym":"SI","date":"2025-10-15","type":"bear","title":"工业需求担忧","factor":"工业需求因子减弱","detail":"全球PMI数据走弱，工业需求预期下降，白银相对黄金跑输","logic":"工业需求下降→白银工业属性拖累→金银比扩大→白银相对弱势","avg_move":"-2.8%","signal":"减仓"},
    {"sym":"SI","date":"2026-01-15","type":"bull","title":"白银再次补涨","factor":"黄金联动+绿能需求","detail":"黄金创新高，白银再次启动补涨，绿色能源转型推动工业需求长期利多","logic":"长期：绿色能源→光伏用银增加→白银工业需求增长；短期：黄金联动","avg_move":"+5.5%","signal":"开多","trend":"上涨趋势确立"},

    # 原油 CL
    {"sym":"CL","date":"2024-06-02","type":"bull","title":"OPEC+维持减产至2025年底","factor":"供给收缩因子","detail":"OPEC+会议决定将减产协议延至2025年底，市场预期供给持续收紧","logic":"减产→供给减少→原油价格支撑；沙特额外减产100万桶/天","avg_move":"+3.2%","signal":"开多","trend":"供给支撑趋势"},
    {"sym":"CL","date":"2024-08-05","type":"bear","title":"全球衰退担忧压制原油","factor":"需求收缩因子","detail":"美国就业数据弱于预期，全球经济衰退担忧升温，原油需求预期下降","logic":"经济衰退预期→需求下降→原油下跌；OPEC减产对冲部分压力","avg_move":"-4.1%","signal":"减仓/平多"},
    {"sym":"CL","date":"2025-01-21","type":"bull","title":"特朗普对伊朗极限施压","factor":"霍尔木兹地缘因子","detail":"特朗普签署重新制裁伊朗行政令，伊朗原油出口受威胁，霍尔木兹海峡风险升温","logic":"伊朗制裁→供给减少→原油价格上涨；霍尔木兹封锁风险溢价","avg_move":"+4.8%","signal":"开多","trend":"地缘溢价确立"},
    {"sym":"CL","date":"2025-02-01","type":"bull","title":"OPEC+维持减产","factor":"供给收缩因子","detail":"OPEC+2月会议维持减产不变，沙特坚持守价策略","logic":"供给收缩持续→价格支撑→趋势延续","avg_move":"+2.1%","signal":"加仓"},
    {"sym":"CL","date":"2025-04-05","type":"bull","title":"关税战推动能源需求重构","factor":"贸易战能源因子","detail":"特朗普关税战后，能源供应链重构，美国页岩油出口需求增加","logic":"关税战→供应链重构→美国能源出口需求增加→WTI走强","avg_move":"+3.7%","signal":"开多"},
    {"sym":"CL","date":"2025-06-10","type":"bull","title":"霍尔木兹海峡紧张","factor":"霍尔木兹因子","detail":"美伊对峙升级，霍尔木兹海峡紧张，全球油轮保险费暴涨","logic":"霍尔木兹→全球20%原油过境→封锁风险→价格暴涨；历史案例+40%","avg_move":"+5.8%","signal":"开多","trend":"地缘溢价大幅扩张"},
    {"sym":"CL","date":"2025-09-15","type":"bear","title":"OPEC+讨论增产","factor":"供给扩张因子","detail":"OPEC+内部出现增产分歧，部分成员国讨论逐步增产","logic":"增产预期→供给扩大→价格承压；但地缘风险对冲部分压力","avg_move":"-3.5%","signal":"减仓"},
    {"sym":"CL","date":"2025-11-01","type":"bull","title":"OPEC+延长减产至2026","factor":"供给收缩因子强化","detail":"OPEC+11月会议决定将减产延至2026年底，超预期利多","logic":"长期减产确定性增强→价格中枢上移→趋势性上涨","avg_move":"+4.2%","signal":"开多","trend":"趋势确立"},
    {"sym":"CL","date":"2026-03-05","type":"bull","title":"原油突破100美元","factor":"多因子共振","detail":"OPEC+减产+地缘+美元走弱三因子共振，原油突破100美元关键位","logic":"技术面突破100整数关口+基本面多因子支撑→趋势加速","avg_move":"+5.0%","signal":"开多加仓","trend":"突破百元上涨趋势"},

    # 天然气 NG
    {"sym":"NG","date":"2024-07-15","type":"bear","title":"夏季需求不及预期","factor":"季节性需求因子","detail":"美国夏季气温低于历史均值，空调需求下降，天然气价格承压","logic":"季节性→需求下降→价格回落；夏季是天然气淡季","avg_move":"-5.2%","signal":"开空"},
    {"sym":"NG","date":"2024-10-01","type":"bull","title":"冬季需求预期启动","factor":"季节性因子+原油联动","detail":"进入10月，冬季供暖需求预期升温，叠加原油上涨联动效应","logic":"原油上涨→能源价格整体上移→天然气联动；冬季需求→价格上涨","avg_move":"+8.3%","signal":"开多","trend":"季节性上涨确立"},
    {"sym":"NG","date":"2025-01-15","type":"bull","title":"极寒天气+原油联动","factor":"天气因子+原油联动","detail":"美国东部极寒天气，天然气需求暴增，同时原油上涨带动","logic":"极端天气→需求暴增→价格急涨；历史同类事件平均+15%","avg_move":"+12.5%","signal":"开多","trend":"急涨行情"},
    {"sym":"NG","date":"2025-04-08","type":"bear","title":"春季需求回落","factor":"季节性因子","detail":"冬季结束，供暖需求回落，天然气价格季节性下跌","logic":"季节性规律→春季是天然气熊市→价格回落","avg_move":"-6.8%","signal":"开空/平多"},
    {"sym":"NG","date":"2025-10-20","type":"bull","title":"冬季需求+LNG出口增加","factor":"需求因子+出口因子","detail":"美国LNG出口能力提升，叠加冬季需求，天然气需求显著增加","logic":"LNG出口→国内供给减少→价格上涨；欧洲需求旺盛→美国LNG溢价","avg_move":"+9.2%","signal":"开多","trend":"上涨趋势"},
    {"sym":"NG","date":"2026-02-20","type":"bull","title":"欧洲天然气短缺危机","factor":"地缘供给因子","detail":"欧洲天然气库存骤降，美国LNG出口订单暴涨，价格联动上涨","logic":"欧洲需求→美国LNG出口→国内供给减少→价格上涨；传导滞后1-3天","avg_move":"+7.5%","signal":"开多","trend":"供给紧张趋势"},

    # 小麦 W
    {"sym":"W","date":"2024-06-20","type":"bear","title":"北半球小麦丰收预期","factor":"供给增加因子","detail":"美国/欧洲/澳洲小麦产量均高于预期，全球供给充裕","logic":"丰收→供给增加→价格下跌；USDA报告上调产量预估","avg_move":"-4.5%","signal":"开空"},
    {"sym":"W","date":"2024-09-10","type":"bull","title":"黑海小麦出口受阻","factor":"地缘供给因子","detail":"黑海地区局势紧张，乌克兰出口受阻，全球小麦供应链担忧","logic":"黑海→全球28%小麦出口→供给减少→价格上涨","avg_move":"+5.8%","signal":"开多","trend":"供给风险溢价"},
    {"sym":"W","date":"2025-01-10","type":"bull","title":"天然气→尿素→小麦成本传导","factor":"成本传导因子","detail":"天然气上涨→尿素化肥成本大涨→小麦种植成本上升→价格支撑","logic":"NG↑→尿素成本↑→小麦成本↑→价格支撑；传导滞后5-10天","avg_move":"+3.2%","signal":"开多"},
    {"sym":"W","date":"2025-03-05","type":"bull","title":"俄罗斯小麦出口限制","factor":"供给收缩因子","detail":"俄罗斯宣布限制小麦出口配额，全球最大出口国供给收缩","logic":"俄罗斯→全球18%小麦出口→限额→供给减少→价格急涨","avg_move":"+6.1%","signal":"开多","trend":"供给冲击上涨"},
    {"sym":"W","date":"2025-07-01","type":"bear","title":"欧洲小麦丰收","factor":"供给增加因子","detail":"欧洲小麦产量超预期，俄罗斯出口限制放松，全球供给压力缓解","logic":"供给增加→价格回落；南半球丰收预期也压制价格","avg_move":"-3.8%","signal":"平多/减仓"},
    {"sym":"W","date":"2025-10-08","type":"bull","title":"拉尼娜天气影响","factor":"天气因子","detail":"拉尼娜现象导致澳洲干旱，南半球小麦减产预警","logic":"天气异常→关键产区减产→全球供给预期收紧→价格上涨","avg_move":"+4.2%","signal":"开多"},
    {"sym":"W","date":"2026-01-15","type":"bull","title":"黑海风险+天然气联动","factor":"地缘+成本双因子","detail":"黑海紧张局势+天然气上涨带动化肥成本，小麦价格双因子共振上涨","logic":"地缘供给+成本传导双驱动→小麦突破关键阻力位","avg_move":"+5.5%","signal":"开多","trend":"上涨趋势确立"},
]

events_json = json.dumps(EVENTS, ensure_ascii=False, separators=(',', ':'))

# 趋势节点数据（用于趋势标注）
TRENDS = [
    {"sym":"GC","date":"2024-09-18","type":"up","label":"上涨趋势确立","logic":"Fed降息50bp，实际利率下降，机构配置需求爆发，黄金突破历史高位"},
    {"sym":"GC","date":"2025-01-20","type":"up","label":"强势上涨趋势","logic":"特朗普关税战+地缘风险双驱动，多因子共振，黄金进入加速上涨阶段"},
    {"sym":"GC","date":"2025-06-15","type":"down","label":"短期调整","logic":"暂停降息+技术面超买，黄金进入震荡调整，非趋势性反转"},
    {"sym":"GC","date":"2025-08-05","type":"up","label":"恢复上涨趋势","logic":"中东地缘危机触发避险需求，多因子再次共振，黄金恢复强势上涨"},
    {"sym":"GC","date":"2026-03-10","type":"up","label":"加速上涨趋势","logic":"黄金突破4600，多因子完全共振，进入历史性牛市加速阶段"},
    {"sym":"CL","date":"2025-01-21","type":"up","label":"上涨趋势确立","logic":"伊朗制裁+OPEC减产，供给端双重收缩，原油进入上升通道"},
    {"sym":"CL","date":"2025-06-10","type":"up","label":"急涨行情","logic":"霍尔木兹紧张触发地缘溢价，原油短期急涨"},
    {"sym":"CL","date":"2025-09-15","type":"down","label":"调整趋势","logic":"增产预期压制，原油进入震荡调整"},
    {"sym":"CL","date":"2025-11-01","type":"up","label":"恢复上涨趋势","logic":"OPEC+延长减产确认，供给端确定性增强，原油恢复上升趋势"},
    {"sym":"SI","date":"2024-09-19","type":"up","label":"补涨启动","logic":"黄金先涨，白银补涨，金银比值修复+工业需求双驱动"},
    {"sym":"NG","date":"2024-10-01","type":"up","label":"季节性上涨确立","logic":"冬季需求预期+原油联动，天然气进入季节性上涨阶段"},
    {"sym":"NG","date":"2025-04-08","type":"down","label":"季节性回落","logic":"冬季结束，供暖需求消失，天然气进入季节性熊市"},
    {"sym":"W","date":"2024-09-10","type":"up","label":"供给风险溢价","logic":"黑海风险+天然气成本传导，小麦价格启动上涨"},
    {"sym":"W","date":"2025-03-05","type":"up","label":"供给冲击上涨","logic":"俄罗斯限制出口，全球供给收缩，小麦进入急涨行情"},
]

trends_json = json.dumps(TRENDS, ensure_ascii=False, separators=(',', ':'))

print('Building HTML...')

HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大道量化系统 v2.0 | 因子驱动 · 大宗商品智能K线</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;overflow-x:hidden}
.header{background:linear-gradient(135deg,#161b22 0%,#0d1117 100%);border-bottom:1px solid #30363d;padding:10px 20px;display:flex;align-items:center;justify-content:space-between}
.header-left h1{font-size:16px;color:#f5c518;letter-spacing:1px}
.header-left p{font-size:11px;color:#6e7681;margin-top:2px}
.header-right{font-size:11px;color:#8b949e;text-align:right}
.version-badge{display:inline-block;background:#1f6feb;color:#fff;font-size:10px;padding:2px 8px;border-radius:10px;margin-left:8px}
/* 品种Tab */
.sym-tabs{display:flex;padding:8px 16px;gap:6px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;align-items:center}
.sym-tab{padding:5px 14px;border-radius:16px;cursor:pointer;font-size:12px;font-weight:600;border:1px solid #30363d;background:#21262d;color:#8b949e;transition:all 0.2s;white-space:nowrap}
.sym-tab.active{color:#000;border-color:var(--sym-color)}
.sym-tab:hover:not(.active){border-color:#58a6ff;color:#58a6ff}
/* 周期Tab */
.period-tabs{display:flex;padding:6px 16px;gap:4px;background:#0d1117;border-bottom:1px solid #21262d;align-items:center}
.period-label{font-size:11px;color:#6e7681;margin-right:8px}
.period-tab{padding:3px 12px;border-radius:12px;cursor:pointer;font-size:11px;font-weight:500;border:1px solid #30363d;background:transparent;color:#6e7681;transition:all 0.2s}
.period-tab.active{background:#1f6feb;color:#fff;border-color:#1f6feb}
.period-tab:hover:not(.active){border-color:#58a6ff;color:#58a6ff}
/* 信息栏 */
.info-bar{display:flex;padding:6px 16px;gap:16px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;align-items:center}
.info-item{font-size:12px;white-space:nowrap}
.info-item .lbl{color:#6e7681}
.info-item .val{font-weight:700;margin-left:4px}
.up{color:#f85149}.dn{color:#3fb950}.neutral{color:#e6edf3}
/* 图表区域 */
#chart{width:100%;height:calc(100vh - 230px);min-height:480px}
/* 底部说明 */
.footer{padding:5px 16px;background:#0d1117;border-top:1px solid #21262d;font-size:10px;color:#484f58;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px}
/* 弹窗 */
.popup-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;z-index:2000;background:rgba(0,0,0,0.6)}
.popup{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;z-index:2001;min-width:320px;max-width:480px;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
.popup.show,.popup-overlay.show{display:block}
.popup-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.popup-title{font-size:15px;font-weight:700;color:#e6edf3}
.popup-close{cursor:pointer;color:#6e7681;font-size:18px;line-height:1;padding:0 4px}
.popup-close:hover{color:#e6edf3}
.popup-badge{display:inline-block;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;margin-bottom:10px}
.badge-bull{background:rgba(248,81,73,0.15);color:#f85149;border:1px solid rgba(248,81,73,0.3)}
.badge-bear{background:rgba(63,185,80,0.15);color:#3fb950;border:1px solid rgba(63,185,80,0.3)}
.badge-trend{background:rgba(245,197,24,0.15);color:#f5c518;border:1px solid rgba(245,197,24,0.3)}
.popup-row{display:flex;margin-bottom:8px;font-size:12px;line-height:1.5}
.popup-row .key{color:#6e7681;min-width:80px;flex-shrink:0}
.popup-row .vval{color:#e6edf3;flex:1}
.popup-divider{border:none;border-top:1px solid #21262d;margin:10px 0}
.popup-signal{margin-top:10px;padding:10px;background:#0d1117;border-radius:8px;border-left:3px solid #f5c518}
.popup-signal .sig-title{font-size:11px;color:#f5c518;font-weight:600;margin-bottom:4px}
.popup-signal .sig-val{font-size:13px;color:#e6edf3;font-weight:700}
/* 标注图例 */
.legend-dots{display:flex;gap:12px;align-items:center;font-size:10px}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:3px}
.dot-bull{background:#f85149}.dot-bear{background:#3fb950}.dot-trend{background:#f5c518}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <h1>大道量化系统 · 因子驱动1.0 <span class="version-badge">v2.0</span></h1>
    <p>大宗商品智能K线 · 全量730天数据 · 多周期切换 · 因子标注 · 趋势信号</p>
  </div>
  <div class="header-right">
    <div>数据源：Yahoo Finance | 2024-05-28 ~ 2026-03-31</div>
    <div style="margin-top:2px">不预测只识别，不预判只跟随</div>
  </div>
</div>

<div class="sym-tabs" id="symTabs">
  <div class="sym-tab active" data-sym="GC" style="--sym-color:#f5c518;background:#f5c518" onclick="switchSym('GC',this)">黄金 GC</div>
  <div class="sym-tab" data-sym="SI" style="--sym-color:#c0c0c0" onclick="switchSym('SI',this)">白银 SI</div>
  <div class="sym-tab" data-sym="CL" style="--sym-color:#ff6b35" onclick="switchSym('CL',this)">原油 CL</div>
  <div class="sym-tab" data-sym="NG" style="--sym-color:#4fc3f7" onclick="switchSym('NG',this)">天然气 NG</div>
  <div class="sym-tab" data-sym="W" style="--sym-color:#a5d6a7" onclick="switchSym('W',this)">小麦 W</div>
  <div style="margin-left:auto;font-size:10px;color:#484f58">
    <span class="legend-dots">
      <span><span class="dot dot-bull"></span>利多/开多</span>
      <span><span class="dot dot-bear"></span>利空/开空</span>
      <span><span class="dot dot-trend"></span>趋势节点</span>
    </span>
  </div>
</div>

<div class="period-tabs">
  <span class="period-label">周期：</span>
  <div class="period-tab active" data-period="1H" onclick="switchPeriod('1H',this)">1小时</div>
  <div class="period-tab" data-period="4H" onclick="switchPeriod('4H',this)">4小时</div>
  <div class="period-tab" data-period="1D" onclick="switchPeriod('1D',this)">日K</div>
  <div class="period-tab" data-period="1W" onclick="switchPeriod('1W',this)">周K</div>
  <div class="period-tab" data-period="1M" onclick="switchPeriod('1M',this)">月K</div>
</div>

<div class="info-bar" id="infoBar">
  <div class="info-item"><span class="lbl">品种</span><span class="val neutral" id="iName">-</span></div>
  <div class="info-item"><span class="lbl">最新</span><span class="val neutral" id="iLast">-</span></div>
  <div class="info-item"><span class="lbl">开</span><span class="val neutral" id="iOpen">-</span></div>
  <div class="info-item"><span class="lbl">高</span><span class="val up" id="iHigh">-</span></div>
  <div class="info-item"><span class="lbl">低</span><span class="val dn" id="iLow">-</span></div>
  <div class="info-item"><span class="lbl">涨跌幅</span><span class="val" id="iChange">-</span></div>
  <div class="info-item"><span class="lbl">周期</span><span class="val neutral" id="iPeriod">1H</span></div>
  <div class="info-item"><span class="lbl">数据量</span><span class="val neutral" id="iBars">-</span></div>
  <div class="info-item"><span class="lbl">单位</span><span class="val neutral" id="iUnit">-</span></div>
</div>

<div id="chart"></div>

<div class="footer">
  <span>大道心法：无动无静，无生无灭 | 不预测只识别，不预判只跟随 | 以K线为相，以量价为证，以结构为凭</span>
  <span>MA5(橙) MA20(紫) MA60(蓝) | 标注: 🔴利多 🟢利空 🟡趋势节点 | 点击标注查看因子详情</span>
</div>

<!-- 事件详情弹窗 -->
<div class="popup-overlay" id="popupOverlay" onclick="closePopup()"></div>
<div class="popup" id="eventPopup">
  <div class="popup-header">
    <div class="popup-title" id="popupTitle">事件详情</div>
    <div class="popup-close" onclick="closePopup()">✕</div>
  </div>
  <div id="popupBadge" class="popup-badge badge-bull">利多信号</div>
  <div class="popup-row"><span class="key">时间</span><span class="vval" id="popupDate">-</span></div>
  <div class="popup-row"><span class="key">驱动因子</span><span class="vval" id="popupFactor">-</span></div>
  <div class="popup-row"><span class="key">事件详情</span><span class="vval" id="popupDetail">-</span></div>
  <hr class="popup-divider">
  <div class="popup-row"><span class="key">影响逻辑</span><span class="vval" id="popupLogic">-</span></div>
  <div class="popup-row"><span class="key">历史涨跌</span><span class="vval" id="popupAvg">-</span></div>
  <hr class="popup-divider">
  <div class="popup-signal">
    <div class="sig-title">📋 操作建议</div>
    <div class="sig-val" id="popupSignal">-</div>
  </div>
</div>

<script>
// ============================================================
// 完整数据（由Python脚本注入）
// ============================================================
const ALL_DATA = __DATA_JSON__;

const EVENTS_DB = __EVENTS_JSON__;

const TRENDS_DB = __TRENDS_JSON__;

// ============================================================
// 状态
// ============================================================
let curSym = 'GC';
let curPeriod = '1H';
const chart = echarts.init(document.getElementById('chart'), 'dark');
const SYM_COLORS = {GC:'#f5c518',SI:'#c0c0c0',CL:'#ff6b35',NG:'#4fc3f7',W:'#a5d6a7'};
const PERIOD_NAMES = {'1H':'1小时','4H':'4小时','1D':'日K','1W':'周K','1M':'月K'};

// ============================================================
// 切换品种
// ============================================================
function switchSym(sym, el) {
  curSym = sym;
  document.querySelectorAll('.sym-tab').forEach(t => {
    t.classList.remove('active');
    t.style.background = '';
    t.style.color = '';
  });
  el.classList.add('active');
  el.style.background = SYM_COLORS[sym];
  el.style.color = '#000';
  renderChart();
}

// ============================================================
// 切换周期
// ============================================================
function switchPeriod(period, el) {
  curPeriod = period;
  document.querySelectorAll('.period-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('iPeriod').textContent = PERIOD_NAMES[period];
  renderChart();
}

// ============================================================
// 计算MA
// ============================================================
function calcMA(closes, n) {
  return closes.map((_, i) => {
    if (i < n - 1) return null;
    const slice = closes.slice(i - n + 1, i + 1);
    return parseFloat((slice.reduce((a, b) => a + b, 0) / n).toFixed(4));
  });
}

// ============================================================
// 渲染图表
// ============================================================
function renderChart() {
  const symData = ALL_DATA[curSym];
  if (!symData) return;
  const bars = symData.periods[curPeriod] || symData.periods['1H'];

  if (!bars || bars.length === 0) return;

  // bars[i] = [dateStr, open, high, low, close, volume]
  const dates = bars.map(b => b[0]);
  const opens = bars.map(b => b[1]);
  const highs = bars.map(b => b[2]);
  const lows = bars.map(b => b[3]);
  const closes = bars.map(b => b[4]);
  const vols = bars.map(b => b[5] || 0);

  // 更新信息栏
  const last = bars[bars.length - 1];
  const prev = bars[bars.length - 2] || last;
  const chg = last[4] - last[1]; // close - open（单根K线涨跌）
  const chgPct = (chg / last[1] * 100).toFixed(2);
  document.getElementById('iName').textContent = symData.name;
  document.getElementById('iLast').textContent = last[4].toFixed(last[4] > 100 ? 2 : 4);
  document.getElementById('iOpen').textContent = last[1].toFixed(last[1] > 100 ? 2 : 4);
  document.getElementById('iHigh').textContent = last[2].toFixed(last[2] > 100 ? 2 : 4);
  document.getElementById('iLow').textContent = last[3].toFixed(last[3] > 100 ? 2 : 4);
  const chgEl = document.getElementById('iChange');
  chgEl.textContent = (chg >= 0 ? '+' : '') + chg.toFixed(2) + ' (' + (chg >= 0 ? '+' : '') + chgPct + '%)';
  chgEl.className = 'val ' + (chg >= 0 ? 'up' : 'dn');
  document.getElementById('iBars').textContent = bars.length + '条';
  document.getElementById('iUnit').textContent = symData.unit;

  // 事件标注：匹配当前品种+日期
  const symEvents = EVENTS_DB.filter(e => e.sym === curSym);
  const symTrends = TRENDS_DB.filter(t => t.sym === curSym);

  // 找最近匹配的K线索引（按日期前缀匹配）
  const markPoints = [];

  symEvents.forEach(ev => {
    let idx = dates.findIndex(d => d.startsWith(ev.date));
    if (idx < 0) {
      // 找最近日期
      const evTs = new Date(ev.date).getTime();
      let minDiff = Infinity, bestIdx = -1;
      dates.forEach((d, i) => {
        const diff = Math.abs(new Date(d.substring(0,10)).getTime() - evTs);
        if (diff < minDiff) { minDiff = diff; bestIdx = i; }
      });
      if (minDiff <= 7 * 86400000) idx = bestIdx;
    }
    if (idx < 0) return;

    const color = ev.type === 'bull' ? '#f85149' : '#3fb950';
    const symbol = ev.type === 'bull' ? 'circle' : 'circle';
    const yVal = ev.type === 'bull' ? lows[idx] * 0.998 : highs[idx] * 1.002;

    markPoints.push({
      name: ev.title,
      coord: [idx, yVal],
      _evData: ev,
      symbol: 'circle',
      symbolSize: 12,
      itemStyle: { color: color, borderColor: '#fff', borderWidth: 1.5 },
      label: { show: false }
    });
  });

  // 趋势标注
  symTrends.forEach(tr => {
    let idx = dates.findIndex(d => d.startsWith(tr.date));
    if (idx < 0) {
      const evTs = new Date(tr.date).getTime();
      let minDiff = Infinity, bestIdx = -1;
      dates.forEach((d, i) => {
        const diff = Math.abs(new Date(d.substring(0,10)).getTime() - evTs);
        if (diff < minDiff) { minDiff = diff; bestIdx = i; }
      });
      if (minDiff <= 14 * 86400000) idx = bestIdx;
    }
    if (idx < 0) return;

    const color = '#f5c518';
    const yVal = tr.type === 'up' ? lows[idx] * 0.995 : highs[idx] * 1.005;

    markPoints.push({
      name: tr.label,
      coord: [idx, yVal],
      _trData: tr,
      symbol: 'diamond',
      symbolSize: 14,
      itemStyle: { color: color, borderColor: '#fff', borderWidth: 1.5 },
      label: { show: false }
    });
  });

  const ma5 = calcMA(closes, 5);
  const ma20 = calcMA(closes, 20);
  const ma60 = calcMA(closes, 60);
  const c = SYM_COLORS[curSym];

  const option = {
    backgroundColor: '#0d1117',
    animation: false,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      backgroundColor: '#161b22',
      borderColor: '#30363d',
      textStyle: { color: '#e6edf3', fontSize: 11 },
      formatter: function(params) {
        const k = params.find(p => p.seriesName === 'K线');
        if (!k || !k.data) return '';
        const [o2, c2, l2, h2] = k.data;
        const kChg = ((c2 - o2) / o2 * 100).toFixed(2);
        const volP = params.find(p => p.seriesName === '成交量');
        const vol = volP ? Number(volP.value).toLocaleString() : '-';
        return '<b>' + k.axisValue + '</b><br>' +
          '开:<b>' + o2 + '</b>  收:<b>' + c2 + '</b><br>' +
          '高:<span style="color:#f85149">' + h2 + '</span>  低:<span style="color:#3fb950">' + l2 + '</span><br>' +
          '涨跌:<span style="color:' + (c2>=o2?'#f85149':'#3fb950') + '">' + (c2>=o2?'+':'') + kChg + '%</span><br>' +
          '成交量:' + vol;
      }
    },
    axisPointer: { link: [{ xAxisIndex: 'all' }] },
    grid: [
      { left: 72, right: 16, top: 24, height: '62%' },
      { left: 72, right: 16, bottom: 44, height: '18%' }
    ],
    xAxis: [
      {
        type: 'category', data: dates,
        axisLine: { lineStyle: { color: '#30363d' } },
        axisLabel: { color: '#6e7681', fontSize: 10, formatter: v => {
          if (curPeriod === '1H' || curPeriod === '4H') return v.substring(5,10);
          if (curPeriod === '1D') return v.substring(0,10);
          return v.substring(0,7);
        }},
        gridIndex: 0, splitLine: { show: false }, boundaryGap: true
      },
      {
        type: 'category', data: dates,
        axisLine: { lineStyle: { color: '#30363d' } },
        axisLabel: { show: false },
        gridIndex: 1, splitLine: { show: false }, boundaryGap: true
      }
    ],
    yAxis: [
      {
        scale: true, gridIndex: 0,
        splitLine: { lineStyle: { color: '#21262d' } },
        axisLabel: { color: '#6e7681', fontSize: 10 },
        axisLine: { lineStyle: { color: '#30363d' } }
      },
      {
        scale: true, gridIndex: 1,
        splitNumber: 2, axisLabel: { show: false },
        splitLine: { show: false }
      }
    ],
    dataZoom: [
      { type: 'inside', xAxisIndex: [0,1], start: 70, end: 100 },
      { type: 'slider', xAxisIndex: [0,1], bottom: 8, height: 22,
        borderColor: '#30363d', fillerColor: 'rgba(88,166,255,0.1)',
        handleStyle: { color: c },
        textStyle: { color: '#6e7681', fontSize: 10 } }
    ],
    series: [
      {
        name: 'K线', type: 'candlestick',
        xAxisIndex: 0, yAxisIndex: 0,
        data: bars.map(b => [b[1], b[4], b[3], b[2]]),
        itemStyle: {
          color: '#f85149', color0: '#3fb950',
          borderColor: '#f85149', borderColor0: '#3fb950'
        },
        markPoint: {
          data: markPoints,
          symbolSize: function(val, params) {
            return params.data._trData ? 16 : 12;
          }
        }
      },
      {
        name: 'MA5', type: 'line',
        xAxisIndex: 0, yAxisIndex: 0,
        data: ma5, smooth: true,
        lineStyle: { width: 1, color: '#ffa500' },
        showSymbol: false, connectNulls: true
      },
      {
        name: 'MA20', type: 'line',
        xAxisIndex: 0, yAxisIndex: 0,
        data: ma20, smooth: true,
        lineStyle: { width: 1, color: '#9370db' },
        showSymbol: false, connectNulls: true
      },
      {
        name: 'MA60', type: 'line',
        xAxisIndex: 0, yAxisIndex: 0,
        data: ma60, smooth: true,
        lineStyle: { width: 1.5, color: '#58a6ff' },
        showSymbol: false, connectNulls: true
      },
      {
        name: '成交量', type: 'bar',
        xAxisIndex: 1, yAxisIndex: 1,
        data: bars.map((b, i) => ({
          value: vols[i],
          itemStyle: { color: b[4] >= b[1] ? 'rgba(248,81,73,0.7)' : 'rgba(63,185,80,0.7)' }
        }))
      }
    ],
    legend: {
      data: ['K线','MA5','MA20','MA60'],
      textStyle: { color: '#6e7681', fontSize: 10 },
      top: 2, right: 16,
      itemWidth: 12, itemHeight: 8
    }
  };

  chart.setOption(option, true);

  // 绑定点击事件（弹出因子详情）
  chart.off('click');
  chart.on('click', function(params) {
    if (params.componentType === 'markPoint') {
      const data = params.data;
      if (data._evData) showEventPopup(data._evData);
      else if (data._trData) showTrendPopup(data._trData);
    }
  });
}

// ============================================================
// 事件弹窗
// ============================================================
function showEventPopup(ev) {
  const isBull = ev.type === 'bull';
  document.getElementById('popupTitle').textContent = ev.title;
  const badge = document.getElementById('popupBadge');
  badge.className = 'popup-badge ' + (isBull ? 'badge-bull' : 'badge-bear');
  badge.textContent = isBull ? '🔴 利多信号' : '🟢 利空信号';
  document.getElementById('popupDate').textContent = ev.date;
  document.getElementById('popupFactor').textContent = ev.factor;
  document.getElementById('popupDetail').textContent = ev.detail;
  document.getElementById('popupLogic').textContent = ev.logic;
  document.getElementById('popupAvg').textContent = ev.avg_move + '（历史同类事件均值）';
  document.getElementById('popupSignal').textContent = ev.signal;
  document.getElementById('popupOverlay').classList.add('show');
  document.getElementById('eventPopup').classList.add('show');
}

function showTrendPopup(tr) {
  const isUp = tr.type === 'up';
  document.getElementById('popupTitle').textContent = tr.label;
  const badge = document.getElementById('popupBadge');
  badge.className = 'popup-badge badge-trend';
  badge.textContent = '🟡 趋势节点 · ' + (isUp ? '上涨' : '下跌');
  document.getElementById('popupDate').textContent = tr.date;
  document.getElementById('popupFactor').textContent = isUp ? '趋势上涨确立' : '趋势下跌确立';
  document.getElementById('popupDetail').textContent = tr.logic;
  document.getElementById('popupLogic').textContent = isUp
    ? '趋势确立后：等待回调，逢低开多；MA5上穿MA20为加仓信号'
    : '下跌趋势：等待反弹，逢高开空；MA5下穿MA20为加仓信号';
  document.getElementById('popupAvg').textContent = isUp ? '趋势确立后平均涨幅 +8~15%' : '趋势确立后平均跌幅 -6~12%';
  document.getElementById('popupSignal').textContent = isUp ? '开多 / 持多' : '开空 / 持空';
  document.getElementById('popupOverlay').classList.add('show');
  document.getElementById('eventPopup').classList.add('show');
}

function closePopup() {
  document.getElementById('popupOverlay').classList.remove('show');
  document.getElementById('eventPopup').classList.remove('show');
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closePopup(); });
window.addEventListener('resize', () => chart.resize());

// 初始渲染
renderChart();
</script>
</body>
</html>'''

# 将数据注入HTML
HTML = HTML.replace('__DATA_JSON__', data_json)
HTML = HTML.replace('__EVENTS_JSON__', events_json)
HTML = HTML.replace('__TRENDS_JSON__', trends_json)

# 写入文件
out_path = 'kline_viewer_v2.0.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(HTML)

size_kb = os.path.getsize(out_path) / 1024
print(f'Generated {out_path} ({size_kb:.1f} KB)')

# ============================================================
# 生成通用模板文件（数据层分离）
# ============================================================
TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大道量化系统 K线模板 v2.0</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<!-- 
=================================================================
大道量化系统 - 通用K线模板 v2.0
=================================================================

使用说明：
1. 替换下方 DATA_SOURCE 对象中的数据（支持大宗商品/加密货币/股票）
2. 数据格式：
   {
     "SYMBOL_NAME": {
       "name": "显示名称",
       "unit": "计价单位",
       "color": "#颜色代码",
       "periods": {
         "1H": [[日期字符串, open, high, low, close, volume], ...],
         "4H": [...],
         "1D": [...],
         "1W": [...],
         "1M": [...]
       }
     }
   }

3. 替换 EVENTS_SOURCE 数组（因子标注，可选）
4. 替换 TRENDS_SOURCE 数组（趋势节点，可选）

适用场景：
- 大宗商品K线（当前：黄金/白银/原油/天然气/小麦）
- 币安永续合约（BTC/ETH/SOL等）
- A股/港股行情分析

注意：若数据量超过5MB，建议改为fetch外部JSON文件而非内嵌。
=================================================================
-->
<style>
/* 完整样式与 kline_viewer_v2.0.html 相同 */
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
.header{background:linear-gradient(135deg,#161b22 0%,#0d1117 100%);border-bottom:1px solid #30363d;padding:10px 20px;display:flex;align-items:center;justify-content:space-between}
.header-left h1{font-size:16px;color:#f5c518;letter-spacing:1px}
.header-left p{font-size:11px;color:#6e7681;margin-top:2px}
.header-right{font-size:11px;color:#8b949e;text-align:right}
.version-badge{display:inline-block;background:#1f6feb;color:#fff;font-size:10px;padding:2px 8px;border-radius:10px;margin-left:8px}
.sym-tabs{display:flex;padding:8px 16px;gap:6px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;align-items:center}
.sym-tab{padding:5px 14px;border-radius:16px;cursor:pointer;font-size:12px;font-weight:600;border:1px solid #30363d;background:#21262d;color:#8b949e;transition:all 0.2s}
.sym-tab.active{color:#000}
.period-tabs{display:flex;padding:6px 16px;gap:4px;background:#0d1117;border-bottom:1px solid #21262d;align-items:center}
.period-label{font-size:11px;color:#6e7681;margin-right:8px}
.period-tab{padding:3px 12px;border-radius:12px;cursor:pointer;font-size:11px;font-weight:500;border:1px solid #30363d;background:transparent;color:#6e7681;transition:all 0.2s}
.period-tab.active{background:#1f6feb;color:#fff;border-color:#1f6feb}
.info-bar{display:flex;padding:6px 16px;gap:16px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;align-items:center}
.info-item{font-size:12px;white-space:nowrap}
.info-item .lbl{color:#6e7681}
.info-item .val{font-weight:700;margin-left:4px}
.up{color:#f85149}.dn{color:#3fb950}.neutral{color:#e6edf3}
#chart{width:100%;height:calc(100vh - 230px);min-height:480px}
.footer{padding:5px 16px;background:#0d1117;border-top:1px solid #21262d;font-size:10px;color:#484f58}
.popup-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;z-index:2000;background:rgba(0,0,0,0.6)}
.popup{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;z-index:2001;min-width:320px;max-width:480px;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
.popup.show,.popup-overlay.show{display:block}
.popup-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.popup-title{font-size:15px;font-weight:700;color:#e6edf3}
.popup-close{cursor:pointer;color:#6e7681;font-size:18px;line-height:1;padding:0 4px}
.popup-badge{display:inline-block;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;margin-bottom:10px}
.badge-bull{background:rgba(248,81,73,0.15);color:#f85149;border:1px solid rgba(248,81,73,0.3)}
.badge-bear{background:rgba(63,185,80,0.15);color:#3fb950;border:1px solid rgba(63,185,80,0.3)}
.badge-trend{background:rgba(245,197,24,0.15);color:#f5c518;border:1px solid rgba(245,197,24,0.3)}
.popup-row{display:flex;margin-bottom:8px;font-size:12px;line-height:1.5}
.popup-row .key{color:#6e7681;min-width:80px;flex-shrink:0}
.popup-row .vval{color:#e6edf3;flex:1}
.popup-divider{border:none;border-top:1px solid #21262d;margin:10px 0}
.popup-signal{margin-top:10px;padding:10px;background:#0d1117;border-radius:8px;border-left:3px solid #f5c518}
.popup-signal .sig-title{font-size:11px;color:#f5c518;font-weight:600;margin-bottom:4px}
.popup-signal .sig-val{font-size:13px;color:#e6edf3;font-weight:700}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <h1 id="chartTitle">大道量化系统 <span class="version-badge">v2.0 模板</span></h1>
    <p>通用K线图 · 多周期切换 · 因子标注 · 趋势信号 | 替换 DATA_SOURCE 即可复用</p>
  </div>
  <div class="header-right">
    <div id="chartSubTitle">数据源：请配置 DATA_SOURCE</div>
    <div style="margin-top:2px">不预测只识别，不预判只跟随</div>
  </div>
</div>

<div class="sym-tabs" id="symTabs"></div>

<div class="period-tabs">
  <span class="period-label">周期：</span>
  <div class="period-tab active" data-period="1H" onclick="switchPeriod('1H',this)">1小时</div>
  <div class="period-tab" data-period="4H" onclick="switchPeriod('4H',this)">4小时</div>
  <div class="period-tab" data-period="1D" onclick="switchPeriod('1D',this)">日K</div>
  <div class="period-tab" data-period="1W" onclick="switchPeriod('1W',this)">周K</div>
  <div class="period-tab" data-period="1M" onclick="switchPeriod('1M',this)">月K</div>
</div>

<div class="info-bar" id="infoBar">
  <div class="info-item"><span class="lbl">品种</span><span class="val neutral" id="iName">-</span></div>
  <div class="info-item"><span class="lbl">最新</span><span class="val neutral" id="iLast">-</span></div>
  <div class="info-item"><span class="lbl">开</span><span class="val neutral" id="iOpen">-</span></div>
  <div class="info-item"><span class="lbl">高</span><span class="val up" id="iHigh">-</span></div>
  <div class="info-item"><span class="lbl">低</span><span class="val dn" id="iLow">-</span></div>
  <div class="info-item"><span class="lbl">涨跌幅</span><span class="val" id="iChange">-</span></div>
  <div class="info-item"><span class="lbl">周期</span><span class="val neutral" id="iPeriod">1H</span></div>
  <div class="info-item"><span class="lbl">数据量</span><span class="val neutral" id="iBars">-</span></div>
  <div class="info-item"><span class="lbl">单位</span><span class="val neutral" id="iUnit">-</span></div>
</div>

<div id="chart"></div>

<div class="footer">大道心法：无动无静，无生无灭 | 以K线为相，以量价为证，以结构为凭 | MA5(橙) MA20(紫) MA60(蓝)</div>

<div class="popup-overlay" id="popupOverlay" onclick="closePopup()"></div>
<div class="popup" id="eventPopup">
  <div class="popup-header">
    <div class="popup-title" id="popupTitle">事件详情</div>
    <div class="popup-close" onclick="closePopup()">✕</div>
  </div>
  <div id="popupBadge" class="popup-badge badge-bull">利多信号</div>
  <div class="popup-row"><span class="key">时间</span><span class="vval" id="popupDate">-</span></div>
  <div class="popup-row"><span class="key">驱动因子</span><span class="vval" id="popupFactor">-</span></div>
  <div class="popup-row"><span class="key">事件详情</span><span class="vval" id="popupDetail">-</span></div>
  <hr class="popup-divider">
  <div class="popup-row"><span class="key">影响逻辑</span><span class="vval" id="popupLogic">-</span></div>
  <div class="popup-row"><span class="key">历史涨跌</span><span class="vval" id="popupAvg">-</span></div>
  <hr class="popup-divider">
  <div class="popup-signal">
    <div class="sig-title">操作建议</div>
    <div class="sig-val" id="popupSignal">-</div>
  </div>
</div>

<script>
// =================================================================
// ⚠️ 数据配置区域 - 仅需修改此处即可复用整个K线系统
// =================================================================

// 【必填】替换为你的数据
// 支持：大宗商品 / 加密货币（BTC/ETH/SOL等）/ 股票
// bar格式: [日期字符串, open, high, low, close, volume]
const DATA_SOURCE = {
  "DEMO": {
    name: "示例品种",
    unit: "USDT",
    color: "#f5c518",
    periods: {
      "1H": [
        // 填入你的数据，格式：["2024-01-01 00:00", 100, 105, 98, 103, 1000],
        // 推荐使用 gen_v2_data.py 脚本生成并注入
      ],
      "4H": [],
      "1D": [],
      "1W": [],
      "1M": []
    }
  }
  // 可添加更多品种...
};

// 【可选】事件标注
const EVENTS_SOURCE = [
  // {sym:"DEMO", date:"2024-01-15", type:"bull", title:"事件名称",
  //  factor:"驱动因子", detail:"详情", logic:"影响逻辑",
  //  avg_move:"+3%", signal:"开多"},
];

// 【可选】趋势节点
const TRENDS_SOURCE = [
  // {sym:"DEMO", date:"2024-02-01", type:"up", label:"上涨趋势确立",
  //  logic:"驱动逻辑说明"},
];

// =================================================================
// 以下代码通用，无需修改
// =================================================================

let curSym = Object.keys(DATA_SOURCE)[0];
let curPeriod = '1H';
const chart = echarts.init(document.getElementById('chart'), 'dark');
const PERIOD_NAMES = {'1H':'1小时','4H':'4小时','1D':'日K','1W':'周K','1M':'月K'};

// 动态生成品种Tab
function initSymTabs() {
  const container = document.getElementById('symTabs');
  Object.entries(DATA_SOURCE).forEach(([sym, d], i) => {
    const tab = document.createElement('div');
    tab.className = 'sym-tab' + (i === 0 ? ' active' : '');
    tab.textContent = d.name;
    tab.style.cssText = i === 0 ? 'background:' + d.color + ';color:#000;border-color:' + d.color : '';
    tab.onclick = function() { switchSym(sym, this); };
    container.appendChild(tab);
  });
}

function switchSym(sym, el) {
  curSym = sym;
  document.querySelectorAll('.sym-tab').forEach(t => { t.classList.remove('active'); t.style.cssText = ''; });
  el.classList.add('active');
  const c = DATA_SOURCE[sym].color;
  el.style.cssText = 'background:' + c + ';color:#000;border-color:' + c;
  renderChart();
}

function switchPeriod(period, el) {
  curPeriod = period;
  document.querySelectorAll('.period-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('iPeriod').textContent = PERIOD_NAMES[period];
  renderChart();
}

function calcMA(closes, n) {
  return closes.map((_, i) => {
    if (i < n - 1) return null;
    const slice = closes.slice(i - n + 1, i + 1);
    return parseFloat((slice.reduce((a, b) => a + b, 0) / n).toFixed(4));
  });
}

function renderChart() {
  const symData = DATA_SOURCE[curSym];
  if (!symData) return;
  const bars = symData.periods[curPeriod] || symData.periods['1H'];
  if (!bars || bars.length === 0) {
    chart.setOption({ title: { text: '暂无' + PERIOD_NAMES[curPeriod] + '数据', textStyle: { color: '#6e7681' }, left: 'center', top: 'center' } }, true);
    return;
  }

  const closes = bars.map(b => b[4]);
  const vols = bars.map(b => b[5] || 0);
  const last = bars[bars.length - 1];
  const chg = last[4] - last[1];
  const chgPct = (chg / last[1] * 100).toFixed(2);
  document.getElementById('iName').textContent = symData.name;
  document.getElementById('iLast').textContent = last[4];
  document.getElementById('iOpen').textContent = last[1];
  document.getElementById('iHigh').textContent = last[2];
  document.getElementById('iLow').textContent = last[3];
  const chgEl = document.getElementById('iChange');
  chgEl.textContent = (chg >= 0 ? '+' : '') + chg.toFixed(4) + ' (' + (chg >= 0 ? '+' : '') + chgPct + '%)';
  chgEl.className = 'val ' + (chg >= 0 ? 'up' : 'dn');
  document.getElementById('iBars').textContent = bars.length + '条';
  document.getElementById('iUnit').textContent = symData.unit;

  const dates = bars.map(b => b[0]);
  const markPoints = [];
  const symEvents = EVENTS_SOURCE.filter(e => e.sym === curSym);
  const symTrends = TRENDS_SOURCE.filter(t => t.sym === curSym);

  function findIdx(dateStr) {
    let idx = dates.findIndex(d => d.startsWith(dateStr));
    if (idx < 0) {
      const evTs = new Date(dateStr).getTime();
      let minDiff = Infinity, bestIdx = -1;
      dates.forEach((d, i) => { const diff = Math.abs(new Date(d.substring(0,10)).getTime() - evTs); if (diff < minDiff) { minDiff = diff; bestIdx = i; } });
      if (minDiff <= 7 * 86400000) idx = bestIdx;
    }
    return idx;
  }

  symEvents.forEach(ev => {
    const idx = findIdx(ev.date);
    if (idx < 0) return;
    const lows2 = bars.map(b => b[3]);
    const highs2 = bars.map(b => b[2]);
    const yVal = ev.type === 'bull' ? lows2[idx] * 0.998 : highs2[idx] * 1.002;
    markPoints.push({ name: ev.title, coord: [idx, yVal], _evData: ev, symbol: 'circle', symbolSize: 12, itemStyle: { color: ev.type === 'bull' ? '#f85149' : '#3fb950', borderColor: '#fff', borderWidth: 1.5 }, label: { show: false } });
  });

  symTrends.forEach(tr => {
    const idx = findIdx(tr.date);
    if (idx < 0) return;
    const lows2 = bars.map(b => b[3]);
    const highs2 = bars.map(b => b[2]);
    const yVal = tr.type === 'up' ? lows2[idx] * 0.995 : highs2[idx] * 1.005;
    markPoints.push({ name: tr.label, coord: [idx, yVal], _trData: tr, symbol: 'diamond', symbolSize: 16, itemStyle: { color: '#f5c518', borderColor: '#fff', borderWidth: 1.5 }, label: { show: false } });
  });

  const c = symData.color;
  chart.setOption({
    backgroundColor: '#0d1117', animation: false,
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' }, backgroundColor: '#161b22', borderColor: '#30363d', textStyle: { color: '#e6edf3', fontSize: 11 },
      formatter: function(params) {
        const k = params.find(p => p.seriesName === 'K线');
        if (!k || !k.data) return '';
        const [o2, c2, l2, h2] = k.data;
        const kChg = ((c2 - o2) / o2 * 100).toFixed(2);
        return '<b>' + k.axisValue + '</b><br>开:<b>' + o2 + '</b> 收:<b>' + c2 + '</b><br>高:<span style="color:#f85149">' + h2 + '</span> 低:<span style="color:#3fb950">' + l2 + '</span><br>涨跌:<span style="color:' + (c2>=o2?'#f85149':'#3fb950') + '">' + (c2>=o2?'+':'') + kChg + '%</span>';
      }
    },
    axisPointer: { link: [{ xAxisIndex: 'all' }] },
    grid: [{ left: 72, right: 16, top: 24, height: '62%' }, { left: 72, right: 16, bottom: 44, height: '18%' }],
    xAxis: [
      { type: 'category', data: dates, axisLine: { lineStyle: { color: '#30363d' } }, axisLabel: { color: '#6e7681', fontSize: 10, formatter: v => curPeriod === '1H' || curPeriod === '4H' ? v.substring(5,10) : v.substring(0,10) }, gridIndex: 0, splitLine: { show: false }, boundaryGap: true },
      { type: 'category', data: dates, axisLabel: { show: false }, gridIndex: 1, splitLine: { show: false }, boundaryGap: true }
    ],
    yAxis: [
      { scale: true, gridIndex: 0, splitLine: { lineStyle: { color: '#21262d' } }, axisLabel: { color: '#6e7681', fontSize: 10 } },
      { scale: true, gridIndex: 1, splitNumber: 2, axisLabel: { show: false }, splitLine: { show: false } }
    ],
    dataZoom: [
      { type: 'inside', xAxisIndex: [0,1], start: 70, end: 100 },
      { type: 'slider', xAxisIndex: [0,1], bottom: 8, height: 22, borderColor: '#30363d', fillerColor: 'rgba(88,166,255,0.1)', handleStyle: { color: c }, textStyle: { color: '#6e7681', fontSize: 10 } }
    ],
    series: [
      { name: 'K线', type: 'candlestick', xAxisIndex: 0, yAxisIndex: 0, data: bars.map(b => [b[1], b[4], b[3], b[2]]), itemStyle: { color: '#f85149', color0: '#3fb950', borderColor: '#f85149', borderColor0: '#3fb950' }, markPoint: { data: markPoints } },
      { name: 'MA5', type: 'line', xAxisIndex: 0, yAxisIndex: 0, data: calcMA(closes, 5), smooth: true, lineStyle: { width: 1, color: '#ffa500' }, showSymbol: false, connectNulls: true },
      { name: 'MA20', type: 'line', xAxisIndex: 0, yAxisIndex: 0, data: calcMA(closes, 20), smooth: true, lineStyle: { width: 1, color: '#9370db' }, showSymbol: false, connectNulls: true },
      { name: 'MA60', type: 'line', xAxisIndex: 0, yAxisIndex: 0, data: calcMA(closes, 60), smooth: true, lineStyle: { width: 1.5, color: '#58a6ff' }, showSymbol: false, connectNulls: true },
      { name: '成交量', type: 'bar', xAxisIndex: 1, yAxisIndex: 1, data: bars.map((b, i) => ({ value: vols[i], itemStyle: { color: b[4] >= b[1] ? 'rgba(248,81,73,0.7)' : 'rgba(63,185,80,0.7)' } })) }
    ],
    legend: { data: ['K线','MA5','MA20','MA60'], textStyle: { color: '#6e7681', fontSize: 10 }, top: 2, right: 16, itemWidth: 12, itemHeight: 8 }
  }, true);

  chart.off('click');
  chart.on('click', function(params) {
    if (params.componentType === 'markPoint') {
      const d = params.data;
      if (d._evData) showEventPopup(d._evData);
      else if (d._trData) showTrendPopup(d._trData);
    }
  });
}

function showEventPopup(ev) {
  document.getElementById('popupTitle').textContent = ev.title;
  const badge = document.getElementById('popupBadge');
  badge.className = 'popup-badge ' + (ev.type === 'bull' ? 'badge-bull' : 'badge-bear');
  badge.textContent = ev.type === 'bull' ? '利多信号' : '利空信号';
  document.getElementById('popupDate').textContent = ev.date;
  document.getElementById('popupFactor').textContent = ev.factor;
  document.getElementById('popupDetail').textContent = ev.detail;
  document.getElementById('popupLogic').textContent = ev.logic;
  document.getElementById('popupAvg').textContent = ev.avg_move + '（历史同类事件均值）';
  document.getElementById('popupSignal').textContent = ev.signal;
  document.getElementById('popupOverlay').classList.add('show');
  document.getElementById('eventPopup').classList.add('show');
}

function showTrendPopup(tr) {
  document.getElementById('popupTitle').textContent = tr.label;
  document.getElementById('popupBadge').className = 'popup-badge badge-trend';
  document.getElementById('popupBadge').textContent = '趋势节点 · ' + (tr.type === 'up' ? '上涨' : '下跌');
  document.getElementById('popupDate').textContent = tr.date;
  document.getElementById('popupFactor').textContent = tr.type === 'up' ? '上涨趋势确立' : '下跌趋势确立';
  document.getElementById('popupDetail').textContent = tr.logic;
  document.getElementById('popupLogic').textContent = tr.type === 'up' ? '等待回调逢低开多' : '等待反弹逢高开空';
  document.getElementById('popupAvg').textContent = tr.type === 'up' ? '趋势确立后平均+8~15%' : '趋势确立后平均-6~12%';
  document.getElementById('popupSignal').textContent = tr.type === 'up' ? '开多/持多' : '开空/持空';
  document.getElementById('popupOverlay').classList.add('show');
  document.getElementById('eventPopup').classList.add('show');
}

function closePopup() {
  document.getElementById('popupOverlay').classList.remove('show');
  document.getElementById('eventPopup').classList.remove('show');
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closePopup(); });
window.addEventListener('resize', () => chart.resize());

initSymTabs();
renderChart();
</script>
</body>
</html>'''

with open('kline_viewer_template.html', 'w', encoding='utf-8') as f:
    f.write(TEMPLATE)

tmpl_size = os.path.getsize('kline_viewer_template.html') / 1024
print(f'Generated kline_viewer_template.html ({tmpl_size:.1f} KB)')
print('All done!')
