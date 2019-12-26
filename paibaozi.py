import time
import requests
import re

# 产品id
ID = '123780502'
# 预期价格
EXPECTED_PRICE = 30
# 加价幅度
ADDPRICE = 1
# 刷新时间
REFRESH_TIME = 10
# 设置Cookie
COOKIE = 'mba_muid=157533793904868717476; 3AB9D23F7A4B3C9B=ZJNWCA4MEO3DLBG7PKMB57WALOBZT5HFYNNQFFXYSRF4SEVRRXGE7VOFBB557XLTUIX5G2ZIKX3SCI4XHC5OMS36LI; _c_id=xn02vv50uzn7aq2mz261575339014168nnd9; _s_id=cka7qlcl70puwys3btd1575339014168ui69; __jdc=104464258; __tak=9d863cd763e5851d68a3189e42518b20ff4d7f496196b059335ccd93ae31e1d6d11782f6fbdce18f6a70f27d35627a788637cad41e173b7cf647d0a0c50c5ba314f4ed092109884eb13bde20c4f76d02; __jda=104464258.157533793904868717476.1575337939.1575337939.1577340555.2; __jdv=104464258|direct|-|none|-|1577340555087; cka7qlcl70puwys3btd1575339014168ui69=1; pin=jd_PUkwPPRfEYPP; unick=jd_PUkwPPRfEYPP; thor=B946E0BCF13AAD554306CE37DBB3796F95C1F6FB017E2D4C39A2C2300CA030AA6AE0EC75BC2E35419350760D43E9FBB916680C03C6FD52CE1BB933FC890BBA8BC0E10A6EA5B057D6053CC05B08CBAE57E4CE63FE2BD182D92E07965F3FDC589156A759881325660E3BB686649A8B90D77C34C743CCFE2A469FF699A803B80D66601E8D327797B63A7B30459BF42FB20522CEB3266435B4C841EDA66ECD31747A; __jdb=104464258.5.157533793904868717476|2.1577340555'
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
