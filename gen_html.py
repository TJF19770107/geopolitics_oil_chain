# -*- coding: utf-8 -*-
"""生成 kline_viewer.html - 无f-string嵌套版"""
import json, os

base = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base, 'html/chart_data.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

events = [
    {"date": "2025-01-20", "text": "特朗普就职 关税威胁", "type": "bull", "sym": "GC"},
    {"date": "2025-02-01", "text": "OPEC+维持减产", "type": "bull", "sym": "CL"},
    {"date": "2025-03-15", "text": "美联储暂停降息", "type": "bear", "sym": "GC"},
    {"date": "2025-04-03", "text": "特朗普关税升级 避险大涨", "type": "bull", "sym": "GC"},
    {"date": "2025-06-10", "text": "霍尔木兹紧张 油价冲高", "type": "bull", "sym": "CL"},
    {"date": "2025-08-05", "text": "中东冲突 金银暴涨", "type": "bull", "sym": "GC"},
    {"date": "2025-09-18", "text": "Fed降息25bp 黄金ATH", "type": "bull", "sym": "GC"},
    {"date": "2025-11-01", "text": "OPEC+延长减产", "type": "bull", "sym": "CL"},
    {"date": "2026-01-15", "text": "黑海风险 小麦大涨", "type": "bull", "sym": "W"},
    {"date": "2026-02-20", "text": "天然气短缺 能源联动", "type": "bull", "sym": "NG"},
    {"date": "2026-03-10", "text": "地缘升温 黄金破新高", "type": "bull", "sym": "GC"},
]
events_json = json.dumps(events, ensure_ascii=False)

# 分段构建HTML，避免f-string嵌套
PART1 = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>大道量化系统 · 因子驱动1.0 - 大宗商品K线</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
.hdr{background:linear-gradient(135deg,#161b22,#0d1117);border-bottom:1px solid #30363d;padding:12px 20px}
.hdr h1{font-size:17px;color:#f5c518;letter-spacing:1px}
.hdr p{font-size:11px;color:#8b949e;margin-top:3px}
.tabs{display:flex;padding:8px 18px;gap:8px;background:#161b22;border-bottom:1px solid #30363d;flex-wrap:wrap}
.tab{padding:5px 14px;border-radius:18px;cursor:pointer;font-size:13px;font-weight:500;border:1px solid #30363d;background:#21262d;color:#8b949e;transition:all .2s}
.tab.active{border-color:#f5c518;color:#000}
.tab:hover:not(.active){border-color:#58a6ff;color:#58a6ff}
.info{padding:7px 18px;background:#161b22;display:flex;gap:18px;flex-wrap:wrap;border-bottom:1px solid #30363d}
.ii{font-size:12px}.ii .lbl{color:#8b949e}.ii .v{font-weight:700;margin-left:5px}
.up{color:#f85149}.dn{color:#3fb950}
#chart{width:100%;height:calc(100vh - 190px);min-height:480px}
.chain{padding:5px 18px 8px;background:#0d1117;font-size:11px;color:#8b949e}
.chain span{color:#f5c518}
.foot{padding:4px 18px;background:#0d1117;font-size:10px;color:#6e7681;border-top:1px solid #21262d}
</style>
</head>
<body>
<div class="hdr">
  <h1>大道量化系统 · 因子驱动1.0 | 大宗商品 1H K线 · 地缘事件标注</h1>
  <p>黄金GC · 白银SI · 原油CL · 天然气NG · 小麦W &nbsp;|&nbsp; 近60天1H数据(Yahoo Finance 2025-12~2026-03) &nbsp;|&nbsp; 不预测只识别 不预判只跟随</p>
</div>
<div class="tabs">
  <div class="tab active" onclick="switchSym('GC',this)">黄金 GC</div>
  <div class="tab" onclick="switchSym('SI',this)">白银 SI</div>
  <div class="tab" onclick="switchSym('CL',this)">原油 CL</div>
  <div class="tab" onclick="switchSym('NG',this)">天然气 NG</div>
  <div class="tab" onclick="switchSym('W',this)">小麦 W</div>
</div>
<div class="info">
  <div class="ii"><span class="lbl">品种</span><span class="v" id="iN">-</span></div>
  <div class="ii"><span class="lbl">最新</span><span class="v" id="iL">-</span></div>
  <div class="ii"><span class="lbl">开盘</span><span class="v" id="iO">-</span></div>
  <div class="ii"><span class="lbl">最高</span><span class="v up" id="iH">-</span></div>
  <div class="ii"><span class="lbl">最低</span><span class="v dn" id="iLo">-</span></div>
  <div class="ii"><span class="lbl">涨跌</span><span class="v" id="iC">-</span></div>
  <div class="ii"><span class="lbl">单位</span><span class="v" id="iU">-</span></div>
</div>
<div id="chart"></div>
<div class="chain">
  产业链传导路径：<span>地缘/OPEC</span> → 原油CL (即时) → <span>天然气NG</span> (+1~3天) → 尿素/化肥 → <span>小麦W</span> (+5~10天) &nbsp;|&nbsp;
  避险情绪 → <span>黄金GC</span> (即时) → <span>白银SI</span> (+0.5~2天)
</div>
<div class="foot">红色=阳线(涨) &nbsp; 绿色=阴线(跌) &nbsp; 旗帜=地缘/政策/产业链驱动事件 &nbsp; MA5橙 MA20紫 MA60蓝 &nbsp; 大道心法：以K线为相，以量价为证，以结构为凭，以历史为镜</div>
<script>
"""

PART2 = "const RAW=" + data_json + ";\n"
PART2 += "const EVENTS=" + events_json + ";\n"

PART3 = """
const COLORS={GC:'#f5c518',SI:'#c0c0c0',CL:'#ff6b35',NG:'#4fc3f7',W:'#a5d6a7'};
const chart=echarts.init(document.getElementById('chart'),'dark');

function calcMA(ohlc,n){
  return ohlc.map(function(_,i){
    if(i<n-1) return null;
    var sum=0;
    for(var j=i-n+1;j<=i;j++) sum+=ohlc[j][1];
    return parseFloat((sum/n).toFixed(3));
  });
}

function switchSym(sym,el){
  document.querySelectorAll('.tab').forEach(function(t){
    t.classList.remove('active');
    t.style.background='';t.style.color='';t.style.borderColor='';
  });
  el.classList.add('active');
  el.style.background=COLORS[sym];el.style.color='#000';el.style.borderColor=COLORS[sym];
  renderChart(sym);
}

function renderChart(sym){
  var d=RAW[sym];
  if(!d) return;
  var all_dates=d.dates,all_ohlc=d.ohlc,all_vols=d.vols;
  var N=300,si=Math.max(0,all_dates.length-N);
  var dates=all_dates.slice(si),ohlc=all_ohlc.slice(si),vols=all_vols.slice(si);

  var last=ohlc[ohlc.length-1],prev=ohlc[ohlc.length-2];
  var chg=last[1]-prev[1],pct=(chg/prev[1]*100).toFixed(2);
  document.getElementById('iN').textContent=d.name;
  document.getElementById('iL').textContent=last[1].toFixed(2);
  document.getElementById('iO').textContent=last[0].toFixed(2);
  document.getElementById('iH').textContent=last[3].toFixed(2);
  document.getElementById('iLo').textContent=last[2].toFixed(2);
  var cel=document.getElementById('iC');
  cel.textContent=(chg>=0?'+':'')+chg.toFixed(2)+' ('+(chg>=0?'+':'')+pct+'%)';
  cel.className='v '+(chg>=0?'up':'dn');
  document.getElementById('iU').textContent=d.unit;

  var symEvts=EVENTS.filter(function(e){return e.sym===sym;});
  var mpts=[];
  symEvts.forEach(function(ev){
    var idx=dates.findIndex(function(dt){return dt.indexOf(ev.date)===0;});
    if(idx>=0){
      mpts.push({
        name:ev.text,coord:[idx,ohlc[idx][3]],
        value:ev.type==='bull'?'多':'空',
        itemStyle:{color:ev.type==='bull'?'#f85149':'#3fb950'},
        symbol:'pin',symbolSize:30,
        label:{color:'#fff',fontSize:9,fontWeight:'bold'}
      });
    }
  });

  var c=COLORS[sym];
  chart.setOption({
    backgroundColor:'#0d1117',animation:false,
    tooltip:{
      trigger:'axis',
      axisPointer:{type:'cross'},
      backgroundColor:'#161b22',borderColor:'#30363d',
      textStyle:{color:'#e6edf3',fontSize:12},
      formatter:function(params){
        var k=params.find(function(p){return p.seriesName==='K线';});
        if(!k) return '';
        var v=k.data,o=v[0],cl=v[1],lo=v[2],hi=v[3];
        var p2=((cl-o)/o*100).toFixed(2);
        return '<b>'+k.axisValue+'</b><br>开:'+o.toFixed(2)+'  收:<b>'+cl.toFixed(2)+'</b><br>高:'+hi.toFixed(2)+'  低:'+lo.toFixed(2)+'<br>涨跌:<span style="color:'+(cl>=o?'#f85149':'#3fb950')+'">'+(cl>=o?'+':'')+p2+'%</span>';
      }
    },
    axisPointer:{link:[{xAxisIndex:'all'}]},
    grid:[
      {left:75,right:15,top:28,height:'60%'},
      {left:75,right:15,bottom:50,height:'17%'}
    ],
    xAxis:[
      {type:'category',data:dates,gridIndex:0,boundaryGap:true,
        axisLine:{lineStyle:{color:'#30363d'}},
        axisLabel:{color:'#8b949e',fontSize:10,interval:'auto',
          formatter:function(v){return v.slice(5,10);}},
        splitLine:{show:false}},
      {type:'category',data:dates,gridIndex:1,boundaryGap:true,
        axisLine:{lineStyle:{color:'#30363d'}},
        axisLabel:{show:false},splitLine:{show:false}}
    ],
    yAxis:[
      {scale:true,gridIndex:0,
        splitLine:{lineStyle:{color:'#21262d'}},
        axisLabel:{color:'#8b949e',fontSize:11},
        axisLine:{lineStyle:{color:'#30363d'}}},
      {scale:true,gridIndex:1,splitNumber:2,
        axisLabel:{show:false},splitLine:{show:false}}
    ],
    dataZoom:[
      {type:'inside',xAxisIndex:[0,1],start:70,end:100},
      {type:'slider',xAxisIndex:[0,1],bottom:6,height:22,
        borderColor:'#30363d',fillerColor:'rgba(88,166,255,0.08)',
        handleStyle:{color:c},textStyle:{color:'#8b949e',fontSize:10}}
    ],
    legend:{
      data:['K线','MA5','MA20','MA60'],
      textStyle:{color:'#8b949e',fontSize:11},top:4,right:16
    },
    series:[
      {name:'K线',type:'candlestick',xAxisIndex:0,yAxisIndex:0,
        data:ohlc.map(function(v){return [v[0],v[1],v[2],v[3]];}),
        itemStyle:{color:'#f85149',color0:'#3fb950',borderColor:'#f85149',borderColor0:'#3fb950'},
        markPoint:{data:mpts},
        markLine:{
          symbol:'none',
          data:[{type:'average',name:'均价'}],
          lineStyle:{color:'rgba(88,166,255,0.5)',type:'dashed',width:1},
          label:{color:'#58a6ff',fontSize:10,
            formatter:function(p){return p.name+':'+parseFloat(p.value).toFixed(2);}}
        }
      },
      {name:'MA5',type:'line',xAxisIndex:0,yAxisIndex:0,
        data:calcMA(ohlc,5),smooth:true,showSymbol:false,
        lineStyle:{width:1.2,color:'#ffa500'}},
      {name:'MA20',type:'line',xAxisIndex:0,yAxisIndex:0,
        data:calcMA(ohlc,20),smooth:true,showSymbol:false,
        lineStyle:{width:1.2,color:'#9370db'}},
      {name:'MA60',type:'line',xAxisIndex:0,yAxisIndex:0,
        data:calcMA(ohlc,60),smooth:true,showSymbol:false,
        lineStyle:{width:1.8,color:'#58a6ff'}},
      {name:'成交量',type:'bar',xAxisIndex:1,yAxisIndex:1,
        data:ohlc.map(function(v,i){
          return {value:vols[i],
            itemStyle:{color:v[1]>=v[0]?'rgba(248,81,73,0.65)':'rgba(63,185,80,0.65)'}};
        })}
    ]
  },true);
}

window.addEventListener('resize',function(){chart.resize();});
// 初始化 激活第一个tab的颜色
document.querySelector('.tab.active').style.background=COLORS['GC'];
document.querySelector('.tab.active').style.color='#000';
document.querySelector('.tab.active').style.borderColor=COLORS['GC'];
renderChart('GC');
</script>
</body>
</html>"""

html = PART1 + PART2 + PART3

out_path = os.path.join(base, 'kline_viewer.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize(out_path)
print("Generated:", out_path)
print("File size:", sz // 1024, "KB")
