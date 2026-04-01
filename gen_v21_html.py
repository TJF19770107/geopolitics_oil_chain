# -*- coding: utf-8 -*-
"""
大道量化系统 v2.1 HTML生成脚本
改进:
1. 数据从外部JSON加载(不再内嵌)
2. 新增MACD技术指标副图
3. 价格精度自适应
4. 增强因子标注与产业链传导可视化
5. 键盘快捷键
6. 数据导出CSV功能
"""
import json, os

# 读取预生成的全量数据JSON
with open('html/chart_data_v2.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

data_size = os.path.getsize('html/chart_data_v2.json')
print(f'Data JSON size: {data_size/1024:.1f} KB')

# ============================================================
# 事件因子数据库（完整版 - 从v2.0继承）
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

# 趋势节点数据
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

# 产业链传导关系
CHAIN_LINKS = [
    {"from":"CL","to":"NG","label":"能源联动","delay":"滞后1-3天","desc":"原油上涨→能源价格中枢上移→天然气补涨"},
    {"from":"NG","to":"W","label":"成本传导","delay":"滞后5-10天","desc":"天然气上涨→尿素成本→化肥→小麦种植成本"},
    {"from":"GC","to":"SI","label":"金银联动","delay":"滞后0.5-2天","desc":"黄金上涨→避险扩散→白银弹性补涨"},
    {"from":"CL","to":"W","label":"间接传导","delay":"滞后7-14天","desc":"原油→运输成本→全球粮价"},
]

chain_json = json.dumps(CHAIN_LINKS, ensure_ascii=False, separators=(',', ':'))

print('Building v2.1 HTML...')

# ============================================================
# v2.1 HTML - 增强版（数据外置、MACD、产业链、键盘快捷键）
# ============================================================
HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大道量化系统 v2.1 | 因子驱动 · 大宗商品智能K线</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;overflow-x:hidden}
.header{background:linear-gradient(135deg,#161b22 0%,#0d1117 100%);border-bottom:1px solid #30363d;padding:8px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.header-left h1{font-size:15px;color:#f5c518;letter-spacing:1px}
.header-left p{font-size:10px;color:#6e7681;margin-top:1px}
.header-right{font-size:10px;color:#8b949e;text-align:right}
.version-badge{display:inline-block;background:#1f6feb;color:#fff;font-size:9px;padding:2px 8px;border-radius:10px;margin-left:6px}
.version-badge.v21{background:#238636}
/* 工具栏 */
.toolbar{display:flex;padding:4px 16px;gap:6px;background:#0d1117;border-bottom:1px solid #21262d;align-items:center;flex-wrap:wrap}
.toolbar-btn{padding:3px 10px;border-radius:8px;cursor:pointer;font-size:10px;border:1px solid #30363d;background:#21262d;color:#8b949e;transition:all 0.2s}
.toolbar-btn:hover{border-color:#58a6ff;color:#58a6ff}
.toolbar-btn.active{background:#1f6feb;color:#fff;border-color:#1f6feb}
.toolbar-sep{width:1px;height:16px;background:#30363d}
.toolbar-info{font-size:9px;color:#484f58;margin-left:auto}
/* 品种Tab */
.sym-tabs{display:flex;padding:6px 16px;gap:5px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;align-items:center}
.sym-tab{padding:4px 12px;border-radius:14px;cursor:pointer;font-size:11px;font-weight:600;border:1px solid #30363d;background:#21262d;color:#8b949e;transition:all 0.2s;white-space:nowrap}
.sym-tab.active{color:#000;border-color:var(--sym-color)}
.sym-tab:hover:not(.active){border-color:#58a6ff;color:#58a6ff}
/* 周期Tab */
.period-tabs{display:flex;padding:4px 16px;gap:3px;background:#0d1117;border-bottom:1px solid #21262d;align-items:center}
.period-label{font-size:10px;color:#6e7681;margin-right:6px}
.period-tab{padding:2px 10px;border-radius:10px;cursor:pointer;font-size:10px;font-weight:500;border:1px solid #30363d;background:transparent;color:#6e7681;transition:all 0.2s}
.period-tab.active{background:#1f6feb;color:#fff;border-color:#1f6feb}
.period-tab:hover:not(.active){border-color:#58a6ff;color:#58a6ff}
/* 信息栏 */
.info-bar{display:flex;padding:5px 16px;gap:14px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap;align-items:center}
.info-item{font-size:11px;white-space:nowrap}
.info-item .lbl{color:#6e7681}
.info-item .val{font-weight:700;margin-left:3px}
.up{color:#f85149}.dn{color:#3fb950}.neutral{color:#e6edf3}
/* 图表区域 */
#chart{width:100%;height:calc(100vh - 260px);min-height:400px}
/* 底部 */
.footer{padding:4px 16px;background:#0d1117;border-top:1px solid #21262d;font-size:9px;color:#484f58;display:flex;justify-content:space-between;flex-wrap:wrap;gap:3px}
/* 弹窗 */
.popup-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;z-index:2000;background:rgba(0,0,0,0.6)}
.popup{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;z-index:2001;min-width:340px;max-width:500px;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
.popup.show,.popup-overlay.show{display:block}
.popup-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.popup-title{font-size:14px;font-weight:700;color:#e6edf3}
.popup-close{cursor:pointer;color:#6e7681;font-size:18px;line-height:1;padding:0 4px}
.popup-close:hover{color:#e6edf3}
.popup-badge{display:inline-block;padding:2px 8px;border-radius:8px;font-size:10px;font-weight:600;margin-bottom:8px}
.badge-bull{background:rgba(248,81,73,0.15);color:#f85149;border:1px solid rgba(248,81,73,0.3)}
.badge-bear{background:rgba(63,185,80,0.15);color:#3fb950;border:1px solid rgba(63,185,80,0.3)}
.badge-trend{background:rgba(245,197,24,0.15);color:#f5c518;border:1px solid rgba(245,197,24,0.3)}
.popup-row{display:flex;margin-bottom:6px;font-size:11px;line-height:1.5}
.popup-row .key{color:#6e7681;min-width:72px;flex-shrink:0}
.popup-row .vval{color:#e6edf3;flex:1}
.popup-divider{border:none;border-top:1px solid #21262d;margin:8px 0}
.popup-signal{margin-top:8px;padding:8px;background:#0d1117;border-radius:8px;border-left:3px solid #f5c518}
.popup-signal .sig-title{font-size:10px;color:#f5c518;font-weight:600;margin-bottom:3px}
.popup-signal .sig-val{font-size:12px;color:#e6edf3;font-weight:700}
/* 产业链面板 */
.chain-panel{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;z-index:2001;min-width:420px;max-width:600px;max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
.chain-panel.show{display:block}
.chain-title{font-size:14px;font-weight:700;color:#f5c518;margin-bottom:12px}
.chain-row{display:flex;align-items:center;gap:8px;padding:8px;background:#0d1117;border-radius:8px;margin-bottom:6px}
.chain-arrow{color:#58a6ff;font-size:16px}
.chain-sym{font-weight:700;font-size:12px;padding:2px 8px;border-radius:6px;color:#000}
.chain-delay{font-size:10px;color:#f5c518}
.chain-desc{font-size:10px;color:#8b949e}
/* 图例 */
.legend-dots{display:flex;gap:10px;align-items:center;font-size:9px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:2px}
.dot-bull{background:#f85149}.dot-bear{background:#3fb950}.dot-trend{background:#f5c518}
/* 快捷键提示 */
.shortcut-hint{position:fixed;bottom:28px;right:12px;font-size:9px;color:#30363d;z-index:10}
/* 加载动画 */
.loading{display:flex;align-items:center;justify-content:center;height:calc(100vh - 260px);color:#6e7681;font-size:13px}
.loading::after{content:'';width:20px;height:20px;border:2px solid #30363d;border-top-color:#58a6ff;border-radius:50%;animation:spin 0.8s linear infinite;margin-left:10px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <h1>大道量化系统 · 因子驱动1.0 <span class="version-badge v21">v2.1</span></h1>
    <p>大宗商品智能K线 · MACD指标 · 产业链传导 · 因子标注 · 趋势信号</p>
  </div>
  <div class="header-right">
    <div>数据源：Yahoo Finance | 2024-05-28 ~ 2026-03-31</div>
    <div style="margin-top:1px">不预测只识别，不预判只跟随</div>
  </div>
</div>

<div class="toolbar">
  <button class="toolbar-btn" onclick="toggleMACD()" id="btnMACD">MACD</button>
  <button class="toolbar-btn" onclick="toggleBOLL()" id="btnBOLL">BOLL</button>
  <div class="toolbar-sep"></div>
  <button class="toolbar-btn" onclick="showChainPanel()">产业链传导</button>
  <button class="toolbar-btn" onclick="exportCSV()">导出CSV</button>
  <div class="toolbar-sep"></div>
  <button class="toolbar-btn" onclick="zoomToFit()">适应窗口</button>
  <button class="toolbar-btn" onclick="zoomRecent()">最近100根</button>
  <div class="toolbar-info" id="toolbarInfo">加载中...</div>
</div>

<div class="sym-tabs" id="symTabs">
  <div class="sym-tab active" data-sym="GC" style="--sym-color:#f5c518;background:#f5c518" onclick="switchSym('GC',this)">黄金 GC</div>
  <div class="sym-tab" data-sym="SI" style="--sym-color:#c0c0c0" onclick="switchSym('SI',this)">白银 SI</div>
  <div class="sym-tab" data-sym="CL" style="--sym-color:#ff6b35" onclick="switchSym('CL',this)">原油 CL</div>
  <div class="sym-tab" data-sym="NG" style="--sym-color:#4fc3f7" onclick="switchSym('NG',this)">天然气 NG</div>
  <div class="sym-tab" data-sym="W" style="--sym-color:#a5d6a7" onclick="switchSym('W',this)">小麦 W</div>
  <div style="margin-left:auto;font-size:9px;color:#484f58">
    <span class="legend-dots">
      <span><span class="dot dot-bull"></span>利多</span>
      <span><span class="dot dot-bear"></span>利空</span>
      <span><span class="dot dot-trend"></span>趋势</span>
    </span>
  </div>
</div>

<div class="period-tabs">
  <span class="period-label">周期：</span>
  <div class="period-tab active" onclick="switchPeriod('1H',this)">1H</div>
  <div class="period-tab" onclick="switchPeriod('4H',this)">4H</div>
  <div class="period-tab" onclick="switchPeriod('1D',this)">日K</div>
  <div class="period-tab" onclick="switchPeriod('1W',this)">周K</div>
  <div class="period-tab" onclick="switchPeriod('1M',this)">月K</div>
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

<div id="chart"><div class="loading">加载K线数据...</div></div>

<div class="footer">
  <span>大道心法：无动无静，无生无灭 | 不预测只识别，不预判只跟随 | 以K线为相，以量价为证，以结构为凭</span>
  <span>快捷键: ←→切换品种 1-5周期 M=MACD B=BOLL C=产业链 E=导出</span>
</div>

<!-- 事件弹窗 -->
<div class="popup-overlay" id="popupOverlay" onclick="closePopup()"></div>
<div class="popup" id="eventPopup">
  <div class="popup-header">
    <div class="popup-title" id="popupTitle">事件详情</div>
    <div class="popup-close" onclick="closePopup()">&#10005;</div>
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

<!-- 产业链面板 -->
<div class="popup-overlay" id="chainOverlay" onclick="closeChainPanel()"></div>
<div class="chain-panel" id="chainPanel">
  <div class="chain-title">产业链传导图谱</div>
  <div style="font-size:10px;color:#6e7681;margin-bottom:12px">
    地缘事件/OPEC → CL(即时) → NG(+1~3天) → W(+5~10天)<br>
    避险情绪 → GC(即时) → SI(+0.5~2天)
  </div>
  <div id="chainContent"></div>
</div>

<script>
// ============================================================
// 配置
// ============================================================
const DATA_URL = 'html/chart_data_v2.json';
const EVENTS_DB = __EVENTS_JSON__;
const TRENDS_DB = __TRENDS_JSON__;
const CHAIN_LINKS = __CHAIN_JSON__;

const SYM_COLORS = {GC:'#f5c518',SI:'#c0c0c0',CL:'#ff6b35',NG:'#4fc3f7',W:'#a5d6a7'};
const SYM_NAMES = {GC:'黄金GC',SI:'白银SI',CL:'原油CL',NG:'天然气NG',W:'小麦W'};
const PERIOD_NAMES = {'1H':'1小时','4H':'4小时','1D':'日K','1W':'周K','1M':'月K'};
const SYM_LIST = ['GC','SI','CL','NG','W'];

// ============================================================
// 状态
// ============================================================
let ALL_DATA = null;
let curSym = 'GC';
let curPeriod = '1H';
let showMACD = false;
let showBOLL = false;
let chart = null;
let isLoading = true;

// ============================================================
// 初始化
// ============================================================
async function init() {
  try {
    const resp = await fetch(DATA_URL);
    ALL_DATA = await resp.json();
    isLoading = false;
    chart = echarts.init(document.getElementById('chart'), 'dark');
    renderChart();
    updateToolbarInfo();
    window.addEventListener('resize', () => chart.resize());
  } catch(e) {
    document.getElementById('chart').innerHTML = '<div style="padding:40px;color:#f85149">数据加载失败: ' + e.message + '</div>';
  }
}

function updateToolbarInfo() {
  if (!ALL_DATA) return;
  const d = ALL_DATA[curSym];
  const bars = d.periods[curPeriod] || d.periods['1H'];
  document.getElementById('toolbarInfo').textContent = 
    SYM_NAMES[curSym] + ' | ' + PERIOD_NAMES[curPeriod] + ' | ' + bars.length + '条 | 数据已加载';
}

// ============================================================
// MACD计算
// ============================================================
function calcEMA(data, n) {
  const k = 2 / (n + 1);
  const ema = [data[0]];
  for (let i = 1; i < data.length; i++) {
    ema.push(data[i] * k + ema[i-1] * (1-k));
  }
  return ema;
}

function calcMACD(closes, fast=12, slow=26, signal=9) {
  const emaFast = calcEMA(closes, fast);
  const emaSlow = calcEMA(closes, slow);
  const dif = emaFast.map((v,i) => +(v - emaSlow[i]).toFixed(6));
  const dea = calcEMA(dif, signal).map(v => +v.toFixed(6));
  const macd = dif.map((v,i) => +((v - dea[i]) * 2).toFixed(6));
  return {dif, dea, macd};
}

// ============================================================
// BOLL计算
// ============================================================
function calcMA(closes, n) {
  return closes.map((_, i) => {
    if (i < n - 1) return null;
    const s = closes.slice(i - n + 1, i + 1);
    return +(s.reduce((a,b) => a+b, 0) / n).toFixed(6);
  });
}

function calcBOLL(closes, n=20, k=2) {
  const ma = calcMA(closes, n);
  const upper = [], lower = [];
  for (let i = 0; i < closes.length; i++) {
    if (ma[i] === null) { upper.push(null); lower.push(null); continue; }
    const slice = closes.slice(i-n+1, i+1);
    const mean = slice.reduce((a,b)=>a+b,0)/n;
    const std = Math.sqrt(slice.reduce((a,b)=>a+(b-mean)**2,0)/n);
    upper.push(+(mean + k*std).toFixed(6));
    lower.push(+(mean - k*std).toFixed(6));
  }
  return {upper, middle: ma, lower};
}

// ============================================================
// 价格精度自适应
// ============================================================
function getPrecision(price) {
  if (price === 0) return 2;
  const abs = Math.abs(price);
  if (abs >= 1000) return 0;
  if (abs >= 100) return 2;
  if (abs >= 10) return 2;
  if (abs >= 1) return 3;
  return 4;
}

function fmtPrice(v, precision) {
  if (v === null || v === undefined) return '-';
  return Number(v).toFixed(precision);
}

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
  updateToolbarInfo();
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
  updateToolbarInfo();
}

// ============================================================
// 工具栏
// ============================================================
function toggleMACD() {
  showMACD = !showMACD;
  document.getElementById('btnMACD').classList.toggle('active', showMACD);
  renderChart();
}
function toggleBOLL() {
  showBOLL = !showBOLL;
  document.getElementById('btnBOLL').classList.toggle('active', showBOLL);
  renderChart();
}
function zoomToFit() {
  if (chart) chart.dispatchAction({type:'dataZoom', start:0, end:100});
}
function zoomRecent() {
  if (chart) chart.dispatchAction({type:'dataZoom', start:80, end:100});
}

// ============================================================
// 导出CSV
// ============================================================
function exportCSV() {
  if (!ALL_DATA) return;
  const bars = ALL_DATA[curSym].periods[curPeriod] || ALL_DATA[curSym].periods['1H'];
  let csv = 'datetime,open,high,low,close,volume\n';
  bars.forEach(b => { csv += b.join(',') + '\n'; });
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = curSym + '_' + curPeriod + '.csv';
  a.click();
  URL.revokeObjectURL(url);
}

// ============================================================
// 产业链面板
// ============================================================
function showChainPanel() {
  const container = document.getElementById('chainContent');
  let html = '';
  CHAIN_LINKS.forEach(link => {
    html += '<div class="chain-row">' +
      '<span class="chain-sym" style="background:'+SYM_COLORS[link.from]+'">'+SYM_NAMES[link.from]+'</span>' +
      '<span class="chain-arrow">→</span>' +
      '<span class="chain-delay">'+link.delay+'</span>' +
      '<span class="chain-arrow">→</span>' +
      '<span class="chain-sym" style="background:'+SYM_COLORS[link.to]+'">'+SYM_NAMES[link.to]+'</span>' +
      '<span style="margin-left:8px;font-size:10px;color:#58a6ff">'+link.label+'</span>' +
      '<div style="margin-left:auto;font-size:9px;color:#6e7681">'+link.desc+'</div>' +
      '</div>';
  });
  container.innerHTML = html;
  document.getElementById('chainOverlay').classList.add('show');
  document.getElementById('chainPanel').classList.add('show');
}
function closeChainPanel() {
  document.getElementById('chainOverlay').classList.remove('show');
  document.getElementById('chainPanel').classList.remove('show');
}

// ============================================================
// 渲染图表
// ============================================================
function renderChart() {
  if (!ALL_DATA || !chart) return;
  const symData = ALL_DATA[curSym];
  if (!symData) return;
  const bars = symData.periods[curPeriod] || symData.periods['1H'];
  if (!bars || bars.length === 0) return;

  const dates = bars.map(b => b[0]);
  const opens = bars.map(b => b[1]);
  const highs = bars.map(b => b[2]);
  const lows = bars.map(b => b[3]);
  const closes = bars.map(b => b[4]);
  const vols = bars.map(b => b[5] || 0);

  // 精度自适应
  const prec = getPrecision(closes[closes.length-1]);

  // 更新信息栏
  const last = bars[bars.length-1];
  const chg = last[4] - last[1];
  const chgPct = (chg / last[1] * 100).toFixed(2);
  document.getElementById('iName').textContent = symData.name;
  document.getElementById('iLast').textContent = fmtPrice(last[4], prec);
  document.getElementById('iOpen').textContent = fmtPrice(last[1], prec);
  document.getElementById('iHigh').textContent = fmtPrice(last[2], prec);
  document.getElementById('iLow').textContent = fmtPrice(last[3], prec);
  const chgEl = document.getElementById('iChange');
  chgEl.textContent = (chg>=0?'+':'') + fmtPrice(chg, prec) + ' (' + (chg>=0?'+':'') + chgPct + '%)';
  chgEl.className = 'val ' + (chg>=0?'up':'dn');
  document.getElementById('iBars').textContent = bars.length + '条';
  document.getElementById('iUnit').textContent = symData.unit;

  // 事件标注
  const symEvents = EVENTS_DB.filter(e => e.sym === curSym);
  const symTrends = TRENDS_DB.filter(t => t.sym === curSym);
  const markPoints = [];

  function findIdx(dateStr, maxDays) {
    let idx = dates.findIndex(d => d.startsWith(dateStr));
    if (idx < 0) {
      const evTs = new Date(dateStr).getTime();
      let minDiff = Infinity, bestIdx = -1;
      dates.forEach((d, i) => {
        const diff = Math.abs(new Date(d.substring(0,10)).getTime() - evTs);
        if (diff < minDiff) { minDiff = diff; bestIdx = i; }
      });
      if (minDiff <= maxDays * 86400000) idx = bestIdx;
    }
    return idx;
  }

  symEvents.forEach(ev => {
    const idx = findIdx(ev.date, 7);
    if (idx < 0) return;
    const color = ev.type === 'bull' ? '#f85149' : '#3fb950';
    const yVal = ev.type === 'bull' ? lows[idx] * 0.998 : highs[idx] * 1.002;
    markPoints.push({
      name: ev.title, coord: [idx, yVal], _evData: ev,
      symbol: 'circle', symbolSize: 12,
      itemStyle: {color, borderColor:'#fff', borderWidth:1.5}, label:{show:false}
    });
  });

  symTrends.forEach(tr => {
    const idx = findIdx(tr.date, 14);
    if (idx < 0) return;
    const yVal = tr.type === 'up' ? lows[idx] * 0.995 : highs[idx] * 1.005;
    markPoints.push({
      name: tr.label, coord: [idx, yVal], _trData: tr,
      symbol: 'diamond', symbolSize: 14,
      itemStyle: {color:'#f5c518', borderColor:'#fff', borderWidth:1.5}, label:{show:false}
    });
  });

  const ma5 = calcMA(closes, 5);
  const ma20 = calcMA(closes, 20);
  const ma60 = calcMA(closes, 60);
  const c = SYM_COLORS[curSym];

  // MACD
  const macdData = calcMACD(closes);

  // BOLL
  const bollData = calcBOLL(closes);

  // 动态网格：根据是否显示MACD
  const hasMACD = showMACD;
  const gridCount = hasMACD ? 3 : 2;
  const gridH = hasMACD ? ['55%','15%','14%'] : ['62%','18%'];
  const grids = [];
  const xAxes = [];
  const yAxes = [];
  for (let i = 0; i < gridCount; i++) {
    grids.push({left:72, right:16, top: i===0?24:undefined, height:gridH[i]});
    xAxes.push({
      type:'category', data:dates,
      axisLine:{lineStyle:{color:'#30363d'}},
      axisLabel:{color:'#6e7681', fontSize:10,
        show: i===gridCount-1,
        formatter: v => {
          if (curPeriod==='1H'||curPeriod==='4H') return v.substring(5,10);
          if (curPeriod==='1D') return v.substring(0,10);
          return v.substring(0,7);
        }
      },
      gridIndex:i, splitLine:{show:false}, boundaryGap:true
    });
    yAxes.push({
      scale:true, gridIndex:i,
      splitLine:{lineStyle:{color:i===0?'#21262d':'transparent'}},
      axisLabel:{color:'#6e7681', fontSize:10, show:i===0||i===gridCount-1},
      axisLine:{lineStyle:{color:'#30363d'}}
    });
  }

  const dataZoom = [
    {type:'inside', xAxisIndex: Array.from({length:gridCount},(_,i)=>i), start:70, end:100},
    {type:'slider', xAxisIndex: Array.from({length:gridCount},(_,i)=>i), bottom:8, height:22,
      borderColor:'#30363d', fillerColor:'rgba(88,166,255,0.1)',
      handleStyle:{color:c}, textStyle:{color:'#6e7681', fontSize:10}}
  ];

  // 构建series
  const series = [
    {
      name:'K线', type:'candlestick', xAxisIndex:0, yAxisIndex:0,
      data: bars.map(b => [b[1],b[4],b[3],b[2]]),
      itemStyle:{color:'#f85149',color0:'#3fb950',borderColor:'#f85149',borderColor0:'#3fb950'},
      markPoint:{data:markPoints}
    },
    {
      name:'MA5', type:'line', xAxisIndex:0, yAxisIndex:0,
      data:ma5, smooth:true,
      lineStyle:{width:1,color:'#ffa500'}, showSymbol:false, connectNulls:true
    },
    {
      name:'MA20', type:'line', xAxisIndex:0, yAxisIndex:0,
      data:ma20, smooth:true,
      lineStyle:{width:1,color:'#9370db'}, showSymbol:false, connectNulls:true
    },
    {
      name:'MA60', type:'line', xAxisIndex:0, yAxisIndex:0,
      data:ma60, smooth:true,
      lineStyle:{width:1.5,color:'#58a6ff'}, showSymbol:false, connectNulls:true
    },
    {
      name:'成交量', type:'bar',
      xAxisIndex:1, yAxisIndex:1,
      data: bars.map((b,i) => ({
        value:vols[i],
        itemStyle:{color:b[4]>=b[1]?'rgba(248,81,73,0.7)':'rgba(63,185,80,0.7)'}
      }))
    }
  ];

  // BOLL
  if (showBOLL) {
    series.push(
      {name:'BOLL上轨',type:'line',xAxisIndex:0,yAxisIndex:0,data:bollData.upper,
        lineStyle:{width:1,color:'#58a6ff',type:'dashed'},showSymbol:false,connectNulls:true},
      {name:'BOLL中轨',type:'line',xAxisIndex:0,yAxisIndex:0,data:bollData.middle,
        lineStyle:{width:1,color:'#58a6ff',type:'dotted'},showSymbol:false,connectNulls:true},
      {name:'BOLL下轨',type:'line',xAxisIndex:0,yAxisIndex:0,data:bollData.lower,
        lineStyle:{width:1,color:'#58a6ff',type:'dashed'},showSymbol:false,connectNulls:true}
    );
  }

  // MACD副图
  if (hasMACD) {
    const macdBarData = macdData.macd.map((v,i) => ({
      value:v,
      itemStyle:{color:v>=0?'rgba(248,81,73,0.7)':'rgba(63,185,80,0.7)'}
    }));
    series.push(
      {name:'MACD柱',type:'bar',xAxisIndex:2,yAxisIndex:2,data:macdBarData},
      {name:'DIF',type:'line',xAxisIndex:2,yAxisIndex:2,data:macdData.dif,
        lineStyle:{width:1.2,color:'#f5c518'},showSymbol:false},
      {name:'DEA',type:'line',xAxisIndex:2,yAxisIndex:2,data:macdData.dea,
        lineStyle:{width:1.2,color:'#58a6ff'},showSymbol:false}
    );
  }

  const legendData = ['K线','MA5','MA20','MA60'];
  if (showBOLL) legendData.push('BOLL上轨','BOLL中轨','BOLL下轨');
  if (hasMACD) legendData.push('MACD柱','DIF','DEA');

  const option = {
    backgroundColor:'#0d1117',
    animation:false,
    tooltip:{
      trigger:'axis',
      axisPointer:{type:'cross'},
      backgroundColor:'#161b22',
      borderColor:'#30363d',
      textStyle:{color:'#e6edf3',fontSize:11},
      formatter: function(params) {
        const k = params.find(p => p.seriesName === 'K线');
        if (!k || !k.data) return '';
        const [o2,c2,l2,h2] = k.data;
        const kChg = ((c2-o2)/o2*100).toFixed(2);
        let tip = '<b>'+k.axisValue+'</b><br>'+
          '开:<b>'+fmtPrice(o2,prec)+'</b>  收:<b>'+fmtPrice(c2,prec)+'</b><br>'+
          '高:<span style="color:#f85149">'+fmtPrice(h2,prec)+'</span>  低:<span style="color:#3fb950">'+fmtPrice(l2,prec)+'</span><br>'+
          '涨跌:<span style="color:'+(c2>=o2?'#f85149':'#3fb950')+'">'+(c2>=o2?'+':'')+kChg+'%</span>';
        // MACD
        if (hasMACD) {
          const difP = params.find(p=>p.seriesName==='DIF');
          const deaP = params.find(p=>p.seriesName==='DEA');
          const macdP = params.find(p=>p.seriesName==='MACD柱');
          if (difP && deaP) {
            tip += '<br><span style="color:#f5c518">DIF:'+Number(difP.value).toFixed(4)+'</span> '+
              '<span style="color:#58a6ff">DEA:'+Number(deaP.value).toFixed(4)+'</span> '+
              '<span style="color:'+(Number(macdP.value)>=0?'#f85149':'#3fb950')+'">MACD:'+Number(macdP.value).toFixed(4)+'</span>';
          }
        }
        return tip;
      }
    },
    axisPointer:{link:[{xAxisIndex:'all'}]},
    grid:grids,
    xAxis:xAxes,
    yAxis:yAxes,
    dataZoom:dataZoom,
    series:series,
    legend:{
      data:legendData,
      textStyle:{color:'#6e7681',fontSize:9},
      top:2,right:16,
      itemWidth:12,itemHeight:8
    }
  };

  chart.setOption(option, true);

  // 点击事件
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
// 弹窗
// ============================================================
function showEventPopup(ev) {
  const isBull = ev.type === 'bull';
  document.getElementById('popupTitle').textContent = ev.title;
  const badge = document.getElementById('popupBadge');
  badge.className = 'popup-badge ' + (isBull?'badge-bull':'badge-bear');
  badge.textContent = (isBull?'利多':'利空') + '信号';
  document.getElementById('popupDate').textContent = ev.date;
  document.getElementById('popupFactor').textContent = ev.factor;
  document.getElementById('popupDetail').textContent = ev.detail;
  document.getElementById('popupLogic').textContent = ev.logic;
  document.getElementById('popupAvg').textContent = ev.avg_move + ' (历史同类事件均值)';
  document.getElementById('popupSignal').textContent = ev.signal;
  document.getElementById('popupOverlay').classList.add('show');
  document.getElementById('eventPopup').classList.add('show');
}

function showTrendPopup(tr) {
  const isUp = tr.type === 'up';
  document.getElementById('popupTitle').textContent = tr.label;
  document.getElementById('popupBadge').className = 'popup-badge badge-trend';
  document.getElementById('popupBadge').textContent = '趋势节点 · ' + (isUp?'上涨':'下跌');
  document.getElementById('popupDate').textContent = tr.date;
  document.getElementById('popupFactor').textContent = isUp?'上涨趋势确立':'下跌趋势确立';
  document.getElementById('popupDetail').textContent = tr.logic;
  document.getElementById('popupLogic').textContent = isUp
    ? '趋势确立后：等待回调，逢低开多；MA5上穿MA20为加仓信号'
    : '下跌趋势：等待反弹，逢高开空；MA5下穿MA20为加仓信号';
  document.getElementById('popupAvg').textContent = isUp?'趋势确立后平均+8~15%':'趋势确立后平均-6~12%';
  document.getElementById('popupSignal').textContent = isUp?'开多/持多':'开空/持空';
  document.getElementById('popupOverlay').classList.add('show');
  document.getElementById('eventPopup').classList.add('show');
}

function closePopup() {
  document.getElementById('popupOverlay').classList.remove('show');
  document.getElementById('eventPopup').classList.remove('show');
}

// ============================================================
// 键盘快捷键
// ============================================================
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  switch(e.key) {
    case 'ArrowLeft': {
      const idx = SYM_LIST.indexOf(curSym);
      if (idx > 0) {
        const newSym = SYM_LIST[idx-1];
        const tab = document.querySelector('.sym-tab[data-sym="'+newSym+'"]');
        if (tab) switchSym(newSym, tab);
      }
      break;
    }
    case 'ArrowRight': {
      const idx = SYM_LIST.indexOf(curSym);
      if (idx < SYM_LIST.length-1) {
        const newSym = SYM_LIST[idx+1];
        const tab = document.querySelector('.sym-tab[data-sym="'+newSym+'"]');
        if (tab) switchSym(newSym, tab);
      }
      break;
    }
    case '1': clickPeriod('1H'); break;
    case '2': clickPeriod('4H'); break;
    case '3': clickPeriod('1D'); break;
    case '4': clickPeriod('1W'); break;
    case '5': clickPeriod('1M'); break;
    case 'm': case 'M': toggleMACD(); break;
    case 'b': case 'B': toggleBOLL(); break;
    case 'c': case 'C': showChainPanel(); break;
    case 'e': case 'E': exportCSV(); break;
    case 'Escape': closePopup(); closeChainPanel(); break;
  }
});

function clickPeriod(p) {
  const tabs = document.querySelectorAll('.period-tab');
  tabs.forEach(t => { if (t.textContent.trim() === p) switchPeriod(p, t); });
}

// 启动
init();
</script>
</body>
</html>'''

# 注入数据
HTML = HTML.replace('__EVENTS_JSON__', events_json)
HTML = HTML.replace('__TRENDS_JSON__', trends_json)
HTML = HTML.replace('__CHAIN_JSON__', chain_json)

# 写入
out_path = 'kline_viewer_v2.1.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(HTML)

size_kb = os.path.getsize(out_path) / 1024
print(f'Generated {out_path} ({size_kb:.1f} KB)')
print('v2.1 generation complete!')
print('New features: MACD, BOLL, chain panel, keyboard shortcuts, CSV export, precision auto-fit')
