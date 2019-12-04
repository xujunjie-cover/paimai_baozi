import time
import requests
import re

# 产品id
ID = '121911700'
# 预期价格
EXPECTED_PRICE = 30
# 加价幅度
ADDPRICE = 1
# 刷新时间
REFRESH_TIME = 10
# 设置Cookie
COOKIE = '3AB9D23F7A4B3C9B=BDWVUEAVPW2DXPN5S3LLYLASM4TOKLSGGA43YDBB3U3KO6ENOJCUI7IRVH2VYUPX7MSYP4DHQQ2ZLNKDCPCPS3IAGI; thor=BB160DD12BCDCD98FFD10A8175795F2A068E1042209D78D2070E7A41A721460FA3DD0CA4B64F47F389CC3C2DF0556229C6103D166187A58AE273D890734834AA20DF625C3F9606AFEB4719B5567E2C09ECC5801EA9F8C1815D331AE96662A6BA5E0925821D112E6C581616BF41924F26301ADDCC61C7E5C6938BD602B3E3D08ACC80F4F8FF8543C6E59E6951EDB107D4D5D7C9D572FCC4AAE4C8C44B52F201F6; pin=jd_448c07018f92c; unick=jd_132985kwo; _c_id=qbphdla5nzndiidxkay1575387844085zwmk; _s_id=i7pyn4s45qrjgxwy7kg1575387844085q4yk; __jda=104464258.15753878444541518747713.1575387844.1575387844.1575387844.1; __jdc=104464258; __jdv=104464258|direct|-|none|-|1575387844455; __tak=ba6d4df2e8230ea8b5abb45ce4fe9ddd92da746e4b36b7290f846c5adda2b1002911c29d1f2e8f4d574d0ddf440e4a3c7b97432571b8e9f54ea7e7c37fef381e6f7d904f805af365528ee1b4370cfcc8; i7pyn4s45qrjgxwy7kg1575387844085q4yk=1; __jdb=104464258.12.15753878444541518747713|1.1575387844'
# 初始化变量
MY_PRICE = 0

HEADERS = {
    'Referer': 'https://paipai.jd.com/auction-detail/' + ID,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}
HEADERS['Cookie'] = COOKIE
url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'


# 获取返回当前价格和剩余时间
def get_pricetime():
    r_url = 'https://used-api.jd.com/auctionRecord/batchCurrentInfo?auctionId=' + ID + '&callback=__jp17'
    r = requests.get(r_url, headers=HEADERS)
    # 备用
    # p_url = 'https://used-api.jd.com/auctionRecord/getCurrentAndOfferNum?auctionId=' \
    #         + ID + '&callback=__jp17'
    # p = requests.get(p_url, headers=HEADERS)
    # 当前价格
    cur_price = re.findall(r"currentPrice\":(.+?),", r.text)[0]
    # 当前时间
    # c_time = re.findall(r"currentTime\":\"(.+?)\"", r.text)[0]
    c_time = time.time() * 1000
    # 结束时间
    e_time = re.findall(r"actualEndTime\":(.+?),", r.text)[0]

    # 计算剩余时间并换算成秒，取整
    o_time = (int(e_time) - int(c_time)) // 1000
    # 分钟数
    min = o_time // 60
    # 秒数
    sec = o_time % 60

    # 商品名暂时有误
    name = re.findall(r"model\":\"(.+?)\",", r.text)
    coloer = re.findall(r"quality\":\"(.+?)\",", r.text)
    print(name + coloer, end='')
    return cur_price, str(min) + ':' + str(sec), o_time


# 竞拍
def buy(price):
    buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
    data = {
        'trackId': 'f6131bdd68d41dcc356979c01a76e784',
        'eid': '3LSXWBJTSCL3QYX53SUKYF3WCJ27WHKJ73U4EYRLMKGWNJAR5RSCM3EMYI7AWKWAC7UQDROMD4ANPJXL2EBOWL4MPI',
    }
    data['price'] = str(int(price))
    data['auctionId'] = str(ID)
    resp = requests.post(buy_url, headers=HEADERS, data=data)
    print(resp.json())


try:
    while True:
        p = get_pricetime()
        print('编号:' + ID + ',当前的价格是:' + p[0] + '剩余时间' + p[1] + ',预期价格:' +
              str(EXPECTED_PRICE))
        currentPrice = int(float(p[0]))
        remain_time = p[2]
        if remain_time < 0:
            print('拍卖结束')
            break
        if MY_PRICE != currentPrice:
            if currentPrice <= EXPECTED_PRICE:
                newPrice = int(currentPrice + ADDPRICE) if \
                    currentPrice + ADDPRICE <= EXPECTED_PRICE else EXPECTED_PRICE
                print('开始加价: 加价金额为' + str(newPrice))
                buy(newPrice)
                MY_PRICE = newPrice
                # 等待刷新时间
                time.sleep(REFRESH_TIME)
            else:
                print('当前价格大于预期价格，拍卖结束')
                break
        else:
            time.sleep(REFRESH_TIME)

except KeyboardInterrupt:
    print('已停止')
