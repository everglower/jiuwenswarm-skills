#!/usr/bin/env python3
"""
汽车对比卡片生成器
- 生成 3 车（或多车）并排对比的 HTML 卡片
- 包含车型图片（从汽车之家/懂车帝图片搜索获取 URL）、关键参数、评分雷达
- 纯前端渲染，无需 API Key

用法:
    python generate_compare_card.py --output compare.html --cars "车型A|img_url|12.5万|1.5T|177PS|2670mm|6.5L|4.6分|低|85%,车型B|img_url2|14.8万|2.0L|171PS|2700mm|6.2L|4.5分|中|78%,车型C|img_url3|10.9万|1.4T|150PS|2680mm|5.9L|4.3分|低|82%"
"""

import argparse
import json
import time
import os
import html


def generate_html(cars_data, output_path, title="车型对比"):
    """生成并排对比 HTML 卡片"""
    
    car_cards = []
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    badges = ['🏆', '💰', '⭐', '📌', '🔥']
    
    for i, car in enumerate(cars_data):
        name, img_url, price, power, horsepower, wheelbase, fuel, rating, risk, residual = car
        color = colors[i % len(colors)]
        badge = badges[i % len(badges)]
        
        # 评分转百分比
        rating_num = float(rating.replace('分', '')) if '分' in rating else float(rating)
        rating_pct = (rating_num / 5.0) * 100
        
        # 风险等级颜色
        risk_color = {'低': '#27ae60', '中': '#f39c12', '高': '#e74c3c'}.get(risk, '#888')
        
        car_cards.append(f"""
    <div class="car-card" style="border-top-color: {color}">
        <div class="car-badge" style="background: {color}">{badge}</div>
        <div class="car-img-wrap">
            <img src="{html.escape(img_url)}" alt="{html.escape(name)}" onerror="this.style.display='none';this.parentElement.innerHTML='<div class=\\'no-img\\'>🚗<br>图片加载失败</div>'" />
        </div>
        <h2 style="color: {color}">{html.escape(name)}</h2>
        <div class="price-tag" style="color: {color}">{html.escape(price)}</div>
        <div class="rating-bar">
            <div class="rating-fill" style="width: {rating_pct}%; background: {color}"></div>
            <span class="rating-text">口碑 {rating}</span>
        </div>
        <table class="spec-table">
            <tr><td class="spec-label">动力</td><td>{html.escape(power)}</td></tr>
            <tr><td class="spec-label">马力</td><td>{html.escape(horsepower)}</td></tr>
            <tr><td class="spec-label">轴距</td><td>{html.escape(wheelbase)}</td></tr>
            <tr><td class="spec-label">油耗/续航</td><td>{html.escape(fuel)}</td></tr>
            <tr><td class="spec-label">可靠性</td><td><span class="risk-tag" style="background: {risk_color}">{html.escape(risk)}</span></td></tr>
            <tr><td class="spec-label">3年保值率</td><td>{html.escape(residual)}</td></tr>
        </table>
    </div>""")
    
    cards_html = "\n".join(car_cards)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #f0f2f5;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            font-size: 24px;
            color: #1a1a2e;
            margin-bottom: 6px;
        }}
        .subtitle {{
            text-align: center;
            font-size: 13px;
            color: #888;
            margin-bottom: 24px;
        }}
        .compare-container {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .car-card {{
            background: #fff;
            border-radius: 16px;
            padding: 0 0 20px 0;
            width: 340px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            border-top: 5px solid;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .car-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        .car-badge {{
            position: absolute;
            top: 0;
            right: 0;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            border-radius: 0 0 0 16px;
        }}
        .car-img-wrap {{
            width: 100%;
            height: 200px;
            overflow: hidden;
            background: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .car-img-wrap img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .no-img {{
            font-size: 40px;
            color: #ccc;
            text-align: center;
        }}
        .car-card h2 {{
            font-size: 18px;
            text-align: center;
            padding: 14px 16px 4px;
        }}
        .price-tag {{
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            padding: 4px 0 12px;
        }}
        .rating-bar {{
            position: relative;
            background: #eee;
            height: 28px;
            margin: 0 16px 16px;
            border-radius: 14px;
            overflow: hidden;
        }}
        .rating-fill {{
            height: 100%;
            border-radius: 14px;
            opacity: 0.85;
        }}
        .rating-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 13px;
            font-weight: bold;
            color: #333;
            text-shadow: 0 0 4px rgba(255,255,255,0.8);
        }}
        .spec-table {{
            width: calc(100% - 32px);
            margin: 0 16px;
            border-collapse: collapse;
        }}
        .spec-table td {{
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }}
        .spec-label {{
            color: #888;
            width: 40%;
        }}
        .spec-table td:not(.spec-label) {{
            font-weight: 500;
            color: #333;
            text-align: right;
        }}
        .risk-tag {{
            display: inline-block;
            padding: 2px 10px;
            border-radius: 10px;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            padding: 24px;
            font-size: 12px;
            color: #aaa;
        }}
        @media (max-width: 768px) {{
            .compare-container {{ flex-direction: column; align-items: center; }}
            .car-card {{ width: 90%; }}
        }}
    </style>
</head>
<body>
    <h1>🚗 {html.escape(title)}</h1>
    <div class="subtitle">生成时间：{time.strftime('%Y-%m-%d %H:%M')} · 数据来源：汽车之家 · 懂车帝 · 车质网</div>
    <div class="compare-container">
{cards_html}
    </div>
    <div class="footer">点击卡片可查看详情 · 数据仅供参考，实际以经销商报价为准</div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='汽车对比卡片生成器')
    parser.add_argument('--cars', required=True,
                        help='车型数据，格式: 车型名|图片URL|落地价|动力|马力|轴距|油耗|口碑分|可靠性(低/中/高)|3年保值率，逗号分隔')
    parser.add_argument('--output', default='compare.html', help='输出 HTML 文件路径')
    parser.add_argument('--title', default='车型对比', help='对比卡片标题')
    
    args = parser.parse_args()
    
    cars_data = []
    for item in args.cars.split(','):
        parts = [p.strip() for p in item.split('|')]
        if len(parts) >= 10:
            cars_data.append(tuple(parts))
    
    if len(cars_data) < 2:
        print("错误: 至少需要 2 款车型进行对比")
        return
    
    print(f"对比车型: {', '.join(c[0] for c in cars_data)}")
    print(f"车型数量: {len(cars_data)}")
    
    output_path = generate_html(cars_data, args.output, args.title)
    print(f"对比卡片已生成: {os.path.abspath(output_path)}")
    print(f"用浏览器打开查看")


if __name__ == '__main__':
    main()
