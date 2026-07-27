#!/usr/bin/env python3
"""
CityWalk 路线地图生成器（纯前端方案，无需地理编码 API Key）
- Agent 先通过网络搜索查到各地点的经纬度坐标
- 将坐标传入本脚本，生成 Leaflet.js 交互式 HTML 地图
- 使用高德地图瓦片（中文标注），无需 Key

用法:
    python generate_route_map.py --city "上海" --output route.html --title "上海法租界 CityWalk" --points "武康大楼|31.2156|121.4312|标志性拍照打卡点,安福路|31.2150|121.4570|咖啡馆和独立小店聚集,愚园路|31.2220|121.4420|文艺气息老马路,静安寺|31.2233|121.4470|古刹地标终点"
"""

import argparse
import json
import time
import os
import html


def generate_html(route_points, city, output_path, title="CityWalk 路线图"):
    """生成 Leaflet.js 交互式 HTML 地图"""
    
    markers_js = []
    coords_list = []
    
    colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c', '#34495e']
    icons = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    for i, point in enumerate(route_points):
        name, lat, lon, info = point
        color = colors[i % len(colors)]
        icon = icons[i % len(icons)]
        popup_html = f"<b>{i+1}. {html.escape(name)}</b>"
        if info:
            popup_html += f"<br><span style='color:#666;font-size:12px'>{html.escape(info)}</span>"
        
        markers_js.append(f"""
    L.circleMarker([{lat}, {lon}], {{
        radius: 16,
        fillColor: '{color}',
        color: '#fff',
        weight: 3,
        opacity: 1,
        fillOpacity: 0.9
    }}).addTo(map).bindPopup(`{popup_html}`).bindTooltip('{i+1}', {{permanent: true, direction: 'center', className: 'waypoint-label'}});
""")
        coords_list.append(f"[{lat}, {lon}]")
    
    route_coords = ", ".join(coords_list)
    
    lats = [p[1] for p in route_points]
    lons = [p[2] for p in route_points]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    padding = 0.005
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - {html.escape(city)}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f5f5; }}
        #header {{
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        #header h1 {{ font-size: 22px; margin-bottom: 6px; }}
        #header .meta {{ font-size: 13px; opacity: 0.85; }}
        #map {{ width: 100%; height: 60vh; min-height: 450px; }}
        .route-list {{
            max-width: 700px;
            margin: 16px auto;
            padding: 20px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .route-list h2 {{ font-size: 16px; color: #333; margin-bottom: 14px; }}
        .route-list .point {{
            display: flex;
            align-items: flex-start;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .route-list .point:last-child {{ border-bottom: none; }}
        .route-list .num {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            color: white;
            font-size: 13px;
            font-weight: bold;
            margin-right: 12px;
            flex-shrink: 0;
        }}
        .route-list .point-info b {{ font-size: 15px; color: #333; }}
        .route-list .point-info .desc {{ font-size: 13px; color: #888; margin-top: 2px; }}
        .waypoint-label {{
            background: transparent !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 12px !important;
            text-shadow: 0 0 3px rgba(0,0,0,0.6) !important;
        }}
        .leaflet-popup-content {{ font-size: 14px; line-height: 1.6; }}
        .footer {{ text-align: center; padding: 16px; font-size: 12px; color: #aaa; }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🚶 {html.escape(title)}</h1>
        <div class="meta">📍 {html.escape(city)} · {len(route_points)} 个路线点 · {time.strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    <div id="map"></div>
    <div class="route-list">
        <h2>📋 路线详情</h2>
"""
    for i, point in enumerate(route_points):
        name, lat, lon, info = point
        color = colors[i % len(colors)]
        html_content += f"""        <div class="point">
            <span class="num" style="background:{color}">{i+1}</span>
            <div class="point-info">
                <b>{html.escape(name)}</b>
                {f'<div class="desc">{html.escape(info)}</div>' if info else ''}
            </div>
        </div>
"""
    
    html_content += f"""    </div>
    <div class="footer">CityWalk 路线图 · 点击标记点查看详情 · 可切换地图图层</div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([{(min_lat+max_lat)/2}, {(min_lon+max_lon)/2}], 15);
        
        // 高德地图瓦片（中文标注，无需Key）
        var amapNormal = L.tileLayer('https://webrd0{{s}}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={{x}}&y={{y}}&z={{z}}', {{
            subdomains: ['1', '2', '3', '4'],
            attribution: '高德地图',
            maxZoom: 20
        }}).addTo(map);
        
        // 高德卫星图
        var amapSatellite = L.tileLayer('https://webst0{{s}}.is.autonavi.com/appmaptile?style=6&x={{x}}&y={{y}}&z={{z}}', {{
            subdomains: ['1', '2', '3', '4'],
            attribution: '高德卫星',
            maxZoom: 20
        }});
        
        // OpenStreetMap
        var osmLayer = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            subdomains: ['a', 'b', 'c'],
            attribution: 'OpenStreetMap',
            maxZoom: 19
        }});
        
        L.control.layers({{
            '🗺️ 高德地图': amapNormal,
            '🛰️ 高德卫星': amapSatellite,
            '🌍 OpenStreetMap': osmLayer
        }}).addTo(map);
        
        // 路线连线（虚线）
        var route = L.polyline([{route_coords}], {{
            color: '#e74c3c',
            weight: 4,
            opacity: 0.75,
            dashArray: '12, 8',
            lineCap: 'round'
        }}).addTo(map);
        
        // 标记点
"""
    
    for marker_js in markers_js:
        html_content += marker_js
    
    html_content += f"""
        // 自动适配视图
        map.fitBounds([[{min_lat - padding}, {min_lon - padding}], [{max_lat + padding}, {max_lon + padding}]], {{
            padding: [40, 40]
        }});
        
        // 路线总距离估算
        var totalDist = 0;
        var coords = [{route_coords}];
        for (var i = 1; i < coords.length; i++) {{
            totalDist += map.distance(coords[i-1], coords[i]);
        }}
        var distStr = totalDist < 1000 ? Math.round(totalDist) + ' 米' : (totalDist/1000).toFixed(1) + ' 公里';
        document.querySelector('.meta').innerHTML += ' · 直线距离约 ' + distStr;
    </script>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='CityWalk 路线地图生成器')
    parser.add_argument('--city', required=True, help='城市名称，如：上海')
    parser.add_argument('--points', required=True, 
                        help='路线点，格式: 名称|纬度|经度|信息(可选)，逗号分隔。例: 武康大楼|31.2156|121.4312|拍照打卡,安福路|31.2150|121.4570|咖啡馆聚集')
    parser.add_argument('--output', default='route.html', help='输出 HTML 文件路径')
    parser.add_argument('--title', default='CityWalk 路线图', help='地图标题')
    
    args = parser.parse_args()
    
    # 解析路线点
    route_points = []
    for item in args.points.split(','):
        parts = item.strip().split('|')
        if len(parts) >= 3:
            name = parts[0].strip()
            lat = float(parts[1])
            lon = float(parts[2])
            info = parts[3].strip() if len(parts) > 3 else ''
            route_points.append((name, lat, lon, info))
    
    if len(route_points) < 2:
        print("错误: 至少需要 2 个路线点")
        return
    
    print(f"城市: {args.city}")
    print(f"路线: {' -> '.join(p[0] for p in route_points)}")
    print(f"地点数: {len(route_points)}")
    print()
    
    output_path = generate_html(route_points, args.city, args.output, args.title)
    print(f"地图已生成: {os.path.abspath(output_path)}")
    print(f"用浏览器打开查看交互式路线图")


if __name__ == '__main__':
    main()
