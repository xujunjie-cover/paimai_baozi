import time
import requests
import re

# 1. 粘贴产品ID
# 2. 输入预期价格  时间剩余2秒时 且  低于预期价格 开始加价
# 3 输入cookie
ID = '121872311'  # 产品id
my_price = 115  # 预期价格
y = 1  # 加价幅度
s = 2  # 等待刷新时间

c = '3AB9D23F7A4B3C9B=BDWVUEAVPW2DXPN5S3LLYLASM4TOKLSGGA43YDBB3U3KO6ENOJCUI7IRVH2VYUPX7MSYP4DHQQ2ZLNKDCPCPS3IAGI; thor=BB160DD12BCDCD98FFD10A8175795F2A068E1042209D78D2070E7A41A721460FA3DD0CA4B64F47F389CC3C2DF0556229C6103D166187A58AE273D890734834AA20DF625C3F9606AFEB4719B5567E2C09ECC5801EA9F8C1815D331AE96662A6BA5E0925821D112E6C581616BF41924F26301ADDCC61C7E5C6938BD602B3E3D08ACC80F4F8FF8543C6E59E6951EDB107D4D5D7C9D572FCC4AAE4C8C44B52F201F6; pin=jd_448c07018f92c; unick=jd_132985kwo; _c_id=qbphdla5nzndiidxkay1575387844085zwmk; _s_id=i7pyn4s45qrjgxwy7kg1575387844085q4yk; __jda=104464258.15753878444541518747713.1575387844.1575387844.1575387844.1; __jdc=104464258; __jdv=104464258|direct|-|none|-|1575387844455; __tak=ba6d4df2e8230ea8b5abb45ce4fe9ddd92da746e4b36b7290f846c5adda2b1002911c29d1f2e8f4d574d0ddf440e4a3c7b97432571b8e9f54ea7e7c37fef381e6f7d904f805af365528ee1b4370cfcc8; i7pyn4s45qrjgxwy7kg1575387844085q4yk=1; __jdb=104464258.12.15753878444541518747713|1.1575387844'
# 设置上面即可


HEADERS = {
    'Referer': 'https://paipai.jd.com/auction-detail/113158389',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Cookie': 'coo'
}
HEADERS['Cookie'] = c
url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'


# 获取当前价格&剩余时间
def get_pricetime():
    r_url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'
    r = requests.get(r_url, headers=HEADERS)
    p_url = 'https://used-api.jd.com/auctionRecord/getCurrentAndOfferNum?auctionId=' + ID + '&callback=__jp17'
    p = requests.get(p_url, headers=HEADERS)
    cur_price = re.findall(r"currentPrice\":(.+?),", p.text)
    c_time = re.findall(r"currentTime\":\"(.+?)\"", r.text)[0]

    e_time = re.findall(r"endTime\":(.+?),", r.text)[0]
    cur_price = ''.join(cur_price)


    o_time = int((int(e_time) - int(c_time)) / 1000)  # 计算剩余时间并换算成秒

    min = int(o_time / 60)
    sec = o_time % 60

    name = re.findall(r"model\":\"(.+?)\",", r.text)
    coloer = re.findall(r"quality\":\"(.+?)\",", r.text)
    print(name + coloer, end='')
    return cur_price, str(min) + ':' + str(sec), o_time


# 下单

def buy(price):
    # price = int(price)
    # buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice?auctionId='+ ID + '&price='+ str(price)  +'&callback=__jp24'
    # bib = requests.get(buy_url,headers=HEADERS)
    # print(bib.text)
    buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
    data = {
        'trackId': '3b154f3a78a78f8b6c2eea5a3cee5674',
        'eid': 'UTT4AVFUIZFVD6KGHHJRAGEEGFJ4MWFSOPDUEF7KBEHDA5ODK3GKDKP5PCVTWIAQ32N2ZT2AR5YBAH3T27354OAI3Q',

    }
    data['price'] = str(int(price))
    data['auctionId'] = str(ID)
    # print(data)
    resp = requests.post(buy_url, headers=HEADERS, data=data)
    print(resp.json())


try:
    while True:
        p = get_pricetime()
        print('编号:' + ID + ',当前的价格是:' + p[0] + '剩余时间' + p[1] + ',预期价格:' + str(my_price))
        x = p[0]
        x = float(x)
        tt = p[2]
        if x <= my_price and tt <= 500000000:
            print('开始加价: 加价金额为' + str(x + y))
            buy(x + y)
        # if tt < 6 and s != 0.0002:
        #     s = 0.0002
        #     print('开始加速 ' + str(s))
        time.sleep(2)  # 等待刷新时间
        if tt < -1:
            print('程序结束')
            break
except KeyboardInterrupt:
    print('已停止')
