from lunar_python import Solar, Lunar

def calculate_bazi(year, month, day, hour, minute, gender):
    """
    八字排盘核心函数
    :param year: 年 (阳历)
    :param month: 月
    :param day: 日
    :param hour: 时
    :param minute: 分
    :param gender: 性别 (1男, 0女) - 影响大运顺逆
    :return: 包含排盘信息的字典
    """

    # 1. 初始化阳历对象
    solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)

    # 2. 转为农历对象
    lunar = solar.getLunar()

    # 3. 获取八字对象 (核心)
    bazi = lunar.getEightChar()

    # --- A. 基础四柱 (干支) ---
    pillars = {
        "年柱": bazi.getYear(),
        "月柱": bazi.getMonth(),
        "日柱": bazi.getDay(),
        "时柱": bazi.getTime()
    }

    # --- B. 五行分析 (金木水火土) ---
    wuxing_detail = {
        "年柱五行": bazi.getYearWuXing(),
        "月柱五行": bazi.getMonthWuXing(),
        "日柱五行": bazi.getDayWuXing(),
        "时柱五行": bazi.getTimeWuXing()
    }

    wuxing_list = [
        bazi.getYearWuXing(),
        bazi.getMonthWuXing(),
        bazi.getDayWuXing(),
        bazi.getTimeWuXing()
    ]

    # 统计五行个数
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    all_wuxing_str = "".join(wuxing_list)
    for w in wuxing_count:
        wuxing_count[w] = all_wuxing_str.count(w)

    # --- C. 十神 ---
    ten_gods = {
        "年干十神": bazi.getYearShiShenGan(),
        "月干十神": bazi.getMonthShiShenGan(),
        "日干十神": bazi.getDayShiShenGan(),
        "时干十神": bazi.getTimeShiShenGan(),
        "年支十神": bazi.getYearShiShenZhi(),
        "月支十神": bazi.getMonthShiShenZhi(),
        "日支十神": bazi.getDayShiShenZhi(),
        "时支十神": bazi.getTimeShiShenZhi()
    }

    # --- D. 纳音 ---
    nayin = {
        "年柱纳音": bazi.getYearNaYin(),
        "月柱纳音": bazi.getMonthNaYin(),
        "日柱纳音": bazi.getDayNaYin(),
        "时柱纳音": bazi.getTimeNaYin()
    }

    # --- E. 大运 ---
    yun = bazi.getYun(gender)

    qiyun_info = {
        "起运年数": yun.getStartYear(),
        "起运月数": yun.getStartMonth(),
        "起运天数": yun.getStartDay(),
        "起运描述": f"出生{yun.getStartYear()}年{yun.getStartMonth()}个月{yun.getStartDay()}天后起运"
    }

    dayun_list = yun.getDaYun()
    dayun_data = []
    for i, dy in enumerate(dayun_list[:8]):
        try:
            gan_zhi = dy.getGanZhi()
        except:
            gan_zhi = "起运前"

        dayun_data.append({
            "序号": i,
            "大运干支": gan_zhi,
            "起运年份": dy.getStartYear(),
            "起运年龄": dy.getStartAge(),
            "结束年龄": dy.getEndAge()
        })

    # --- F. 流年 ---
    liunian_data = []
    if len(dayun_list) > 1:
        liunian_list = dayun_list[1].getLiuNian()
        for i, ln in enumerate(liunian_list):
            liunian_data.append({
                "序号": i,
                "年份": ln.getYear(),
                "年龄": ln.getAge(),
                "干支": ln.getGanZhi()
            })

    # 组装返回数据
    result = {
        "user_info": {
            "阳历": f"{year}-{month}-{day} {hour}:{minute}",
            "农历": f"{lunar.getYearInChinese()}年 {lunar.getMonthInChinese()}月 {lunar.getDayInChinese()}",
            "生肖": lunar.getYearShengXiao(),
            "性别": "男" if gender == 1 else "女"
        },
        "bazi": pillars,
        "day_master": bazi.getDayGan(),
        "wuxing": {
            "detail": wuxing_detail,
            "list": wuxing_list,
            "counts": wuxing_count
        },
        "nayin": nayin,
        "shi_shen": ten_gods,
        "qi_yun": qiyun_info,
        "da_yun": dayun_data,
        "liu_nian": liunian_data
    }

    return result
