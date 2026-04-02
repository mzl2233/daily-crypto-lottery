#!/usr/bin/env python3
"""Fetch lottery results from web."""
import requests
import re
import json
from datetime import datetime, timezone, timedelta

def fetch_shuangseqiu():
    """Fetch 双色球 (Double Color Ball) latest results."""
    try:
        # Try 500.com API
        resp = requests.get(
            "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice",
            params={"name": "ssq", "issueCount": "1", "issueStart": "", "issueEnd": "", "dayStart": "", "dayEnd": "", "pageNo": "1", "pageSize": "1", "systemType": "PC"},
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.cwl.gov.cn/"},
            timeout=15
        )
        data = resp.json()
        if data.get('result') and len(data['result']) > 0:
            r = data['result'][0]
            red = r.get('red', '').split(',')
            blue = r.get('blue', '')
            return {
                "name": "双色球",
                "issue": r.get('code', ''),
                "date": r.get('date', '')[:10],
                "red": red,
                "blue": blue,
                "numbers": f"红球 {' '.join(red)} | 蓝球 {blue}"
            }
    except Exception as e:
        print(f"❌ 双色球获取失败: {e}")
    
    return None

def fetch_daletou():
    """Fetch 大乐透 (Super Lotto) latest results."""
    try:
        resp = requests.get(
            "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice",
            params={"name": "dlt", "issueCount": "1", "issueStart": "", "issueEnd": "", "dayStart": "", "dayEnd": "", "pageNo": "1", "pageSize": "1", "systemType": "PC"},
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.cwl.gov.cn/"},
            timeout=15
        )
        data = resp.json()
        if data.get('result') and len(data['result']) > 0:
            r = data['result'][0]
            red = r.get('red', '').split(',')
            blue = r.get('blue', '').split(',')
            return {
                "name": "大乐透",
                "issue": r.get('code', ''),
                "date": r.get('date', '')[:10],
                "red": red,
                "blue": blue,
                "numbers": f"前区 {' '.join(red)} | 后区 {' '.join(blue)}"
            }
    except Exception as e:
        print(f"❌ 大乐透获取失败: {e}")
    
    return None

def main():
    tz = timezone(timedelta(hours=8))
    print("🎰 获取彩票开奖信息...")
    
    ssq = fetch_shuangseqiu()
    if ssq:
        print(f"✅ 双色球 {ssq['issue']}: {ssq['numbers']}")
    
    dlt = fetch_daletou()
    if dlt:
        print(f"✅ 大乐透 {dlt['issue']}: {dlt['numbers']}")
    
    result = {
        "date": datetime.now(tz).strftime('%Y-%m-%d'),
        "generated_at": datetime.now(tz).isoformat(),
        "lottery": []
    }
    
    if ssq:
        result['lottery'].append(ssq)
    if dlt:
        result['lottery'].append(dlt)
    
    with open('lottery_results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 彩票数据已保存")
    return result

if __name__ == '__main__':
    main()
