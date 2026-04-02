#!/usr/bin/env python3
"""Fetch crypto prices from multiple sources."""
import requests
import json
import os
from datetime import datetime, timezone, timedelta

def fetch_from_gateio():
    """Fetch from Gate.io API (accessible from China)."""
    pairs = [
        {"pair": "BTC_USDT", "name": "比特币", "symbol": "BTC"},
        {"pair": "ETH_USDT", "name": "以太坊", "symbol": "ETH"},
        {"pair": "SOL_USDT", "name": "Solana", "symbol": "SOL"},
        {"pair": "BNB_USDT", "name": "BNB", "symbol": "BNB"},
        {"pair": "XRP_USDT", "name": "XRP", "symbol": "XRP"},
    ]
    
    results = []
    for coin in pairs:
        try:
            resp = requests.get(
                f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={coin['pair']}",
                timeout=10
            )
            data = resp.json()
            if data and len(data) > 0:
                d = data[0]
                price = float(d['last'])
                change_24h = float(d.get('change_percentage', 0))
                high_24h = float(d.get('high_24h', 0))
                low_24h = float(d.get('low_24h', 0))
                vol_24h = float(d.get('quote_volume', 0))
                
                results.append({
                    "name": coin['name'],
                    "symbol": coin['symbol'],
                    "price": round(price, 2),
                    "change_24h": round(change_24h, 2),
                    "high_24h": round(high_24h, 2),
                    "low_24h": round(low_24h, 2),
                    "vol_24h": round(vol_24h, 2),
                })
                print(f"✅ {coin['name']}: ${price:,.2f} ({change_24h:+.2f}%)")
        except Exception as e:
            print(f"❌ {coin['name']} fetch failed: {e}")
    
    return results

def main():
    print("🪙 获取加密货币行情...")
    prices = fetch_from_gateio()
    
    tz = timezone(timedelta(hours=8))
    result = {
        "date": datetime.now(tz).strftime('%Y-%m-%d'),
        "generated_at": datetime.now(tz).isoformat(),
        "coins": prices,
        "summary": {
            "total": len(prices),
            "up": sum(1 for p in prices if p['change_24h'] > 0),
            "down": sum(1 for p in prices if p['change_24h'] < 0),
        }
    }
    
    with open('crypto_prices.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存 {len(prices)} 个币种数据")
    return result

if __name__ == '__main__':
    main()
