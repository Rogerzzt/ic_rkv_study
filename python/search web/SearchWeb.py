import requests  # 重要
import re        # 重要

# 定义获取HTML内容的方法
def getHtmlText(URL):
    try:
        r = requests.get(url=URL, timeout=30)
        
        # 检查响应
        r.raise_for_status()
        print("...网页响应成功 200")

        # 检查是否乱码
        if r.encoding == 'UTF-8':
            print("...网页源码为utf-8 无乱码")
        else:
            print(r.encoding)
            return
        # time.sleep(2)
        print("...获取HTML页面完成")
        return r.text
    except:
        return ""

# 定义解析数据的方法
def fillUnivList(uList, html):
    try:
        names = re.findall(r'\<span class=\"title\" title=.*?\>', html)
        prices = re.findall(r'\<strong\>[\d\.]*<\/strong\>', html)
        print("...页面数据解析完成")
        # time.sleep(2)
        print("...开始数据清洗")
        for i in range(len(names)):
            name = names[i].split('"')[3]  # 以"为切割标识，取第4段
            price = re.split(">|<", prices[i])[2]  # 以>或<为切割标识。取第2段
            uList.append([name, price])
    except:
        print("解析出错")

# 定义格式化输出的方法
def printUnivList(uList, Path):
    # 读写
    with open(Path, 'a', encoding="utf-8") as f:
        f.write("商品\t价格\n")
        for i in range(len(uList)):
            u = uList[i]
            f.write(u[0] + "\t")  # 写入商品名称
            f.write(u[1] + "\n")  # 写入商品价格
        f.close()  # 关闭文件，避免长时间占用系统资源
        print("成功存储到文件")

def main():
    uinfo = []  # 定义用于存储信息的数组
    good = input("请输入需要检索的商品：")  # 定义需要搜索的商品名称
    page = 1  # 设置浏览页面数——因为商品数量众多，这里仅设置浏览1页的所有商品信息
    path = "./" + good + ".txt"  # 设置数据存储路径 
    
    # 遍历要浏览的商品页数
    for i in range(page):
        # 淘宝的商品地址，通过解析URL地址，其内容格式可简化为 【淘宝地址-搜索物品名称-当前页数】
        URL = "https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&q=" + good + "&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ssid=s5-e&tab=all"
        html = getHtmlText(URL)   # 调用方法
        # time.sleep(2)    
        fillUnivList(uinfo, html)  # 调用方法
    # time.sleep(2)
    print("共搜索了", len(uinfo), "条结果")
    # time.sleep(2)
    printUnivList(uinfo, path)  # 调用方法


if __name__ == "__main__":
    main()


