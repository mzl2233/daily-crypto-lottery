#!/usr/bin/env python3
"""Send crypto + lottery results to Feishu group via webhook card."""
import json
import os
import requests
from datetime import datetime, timezone, timedelta

WEBHOOK = os.environ.get('FEISHU_WEBHOOK_URL', '')

def send_card(crypto_data, lottery_data):
    """Send Feishu interactive card with crypto + lottery."""
    if not WEBHOOK:
        print("⚠️ No webhook URL")
        return

    tz = timezone(timedelta(hours=8))
    today = datetime.now(tz).strftime('%Y-%m-%d')

    elements = []

    # === Crypto Section ===
    if crypto_data and crypto_data.get('coins'):
        elements.append({
            "tag": "markdown",
            "content": f"## 🪙 加密货币行情"
        })
        elements.append({"tag": "hr"})

        for coin in crypto_data['coins']:
            emoji = "🟢" if coin['change_24h'] > 0 else "🔴"
            price_str = f"${coin['price']:,.2f}"
            change_str = f"{coin['change_24h']:+.2f}%"
            
            elements.append({
                "tag": "markdown",
                "content": (
                    f"**{emoji} {coin['name']} ({coin['symbol']})**\n"
                    f"现价 **{price_str}**　｜　24h: {change_str}\n"
                    f"24h高点 ${coin['high_24h']:,.2f}　低点 ${coin['low_24h']:,.2f}"
                )
            })

    # === Lottery Section ===
    if lottery_data and lottery_data.get('lottery'):
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "markdown",
            "content": f"## 🎰 彩票开奖"
        })
        elements.append({"tag": "hr"})

        for lot in lottery_data['lottery']:
            emoji = "🔴" if lot['name'] == '双色球' else "🟡"
            elements.append({
                "tag": "markdown",
                "content": (
                    f"**{emoji} {lot['name']}** 第 {lot['issue']} 期\n"
                    f"开奖日期: {lot['date']}\n"
                    f"**{lot['numbers']}**"
                )
            })

    # Footer
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "markdown",
        "content": "📊 数据仅供参考 ｜ 不构成投资建议"
    })

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "template": "orange",
                "title": {"tag": "plain_text", "content": f"💰 智投看板 · 币圈 & 彩票 · {today}"}
            },
            "elements": elements
        }
    }

    resp = requests.post(WEBHOOK, json=card)
    if resp.status_code == 200:
        result = resp.json()
        if result.get('code') == 0 or result.get('StatusCode') == 0:
            print("✅ 飞书群卡片已发送")
        else:
            print(f"❌ 发送失败: {result}")
    else:
        print(f"❌ HTTP错误: {resp.status_code}")

def main():
    crypto = None
    lottery = None

    if os.path.exists('crypto_prices.json'):
        with open('crypto_prices.json', 'r', encoding='utf-8') as f:
            crypto = json.load(f)

    if os.path.exists('lottery_results.json'):
        with open('lottery_results.json', 'r', encoding='utf-8') as f:
            lottery = json.load(f)

    send_card(crypto, lottery)

if __name__ == '__main__':
    main()
