# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai


def _get_mags_cat(name):
    mags = {
        # 雜誌
        'MEN’S CLUB': '雜誌/日文/MEN’S CLUB',
        '2nd': '雜誌/日文/2nd',
        'CLUB HARLEY': '雜誌/日文/CLUB HARLEY',
        'Discover Japan': '雜誌/日文/Discover Japan',
        'flick!': '雜誌/日文/flick!',
        'SALT WORLD': '雜誌/日文/SALT WORLD',
        '美麗的KIMONO': '雜誌/日文/美麗的KIMONO',
        "Harper's BAZAAR": "雜誌/日文/Harpers BAZAAR",
        "25ans Wedding 大人婚": "雜誌/日文/25ans Wedding 大人婚",

        '世界腕錶雜誌': '雜誌/流行時尚/世界腕錶雜誌',
        '《明潮》': '雜誌/流行時尚/《明潮》',
        '【霸屏女孩】髮型': '雜誌/流行時尚/【霸屏女孩】髮型',
        'vivi': '雜誌/流行時尚/vivi',
        'mina': '雜誌/流行時尚/mina',
        'InStyle 時尚樂': '雜誌/流行時尚/InStyle 時尚樂',
        'Girl愛女生': '雜誌/流行時尚/Girl愛女生',

        '小日子享生活誌': '雜誌/家庭生活/小日子享生活誌',
        '時尚家居': '雜誌/家庭生活/時尚家居',

        '經貿透視': '雜誌/商業理財/經貿透視',
        '今周刊': '雜誌/商業理財/今周刊',
        '商業周刊': '雜誌/商業理財/商業周刊',
        '天下雜誌': '雜誌/商業理財/天下雜誌',
        '財訊': '雜誌/商業理財/財訊雙週刊',
        '先探投資週刊': '雜誌/商業理財/先探投資週刊',
        '遠見雜誌': '雜誌/商業理財/遠見雜誌',
        '女人變有錢': '雜誌/商業理財/女人變有錢',
        '理財周刊': '雜誌/商業理財/理財周刊',

        '電玩雙週刊': '雜誌/休閒旅遊/電玩雙週刊',
        'Taipei Walker 特別號': '雜誌/休閒旅遊/Taipei Walker 特別號',
        '單車誌': '雜誌/休閒旅遊/單車誌',
        '食尚玩家': '雜誌/休閒旅遊/食尚玩家',

        '新新聞': '雜誌/新聞時事/新新聞',
        '鏡週刊': '雜誌/新聞時事/鏡週刊',
        '周刊王': '雜誌/新聞時事/周刊王',
        '明報周刊': '雜誌/新聞時事/明報周刊',
        '時報周刊': '雜誌/新聞時事/時報周刊',

        '幼獅少年': '雜誌/兒童/幼獅少年',
        'Joy to the world': '雜誌/兒童/Joy to the world',
        '康軒學習雜誌': '雜誌/兒童/康軒學習雜誌',

        'Make：國際中文版': '雜誌/3C科學/Make',
        'iPhone, iPad 玩樂誌': '雜誌/3C科學/iPhone, iPad 玩樂誌',

        '壹週刊': '雜誌/影視娛樂/壹週刊',

        '當代設計雜誌': '雜誌/藝術設計/當代設計雜誌',
        'Shopping Design': '雜誌/藝術設計/Shopping Design設計採買誌',
        'ARCH 雅趣': '雜誌/藝術設計/ARCH 雅趣',
        '城邦國際名表': '雜誌/藝術設計/城邦國際名表',
        '住宅美學': '雜誌/藝術設計/住宅美學',

        '君子時代雜誌國際中文版': '雜誌/男性時尚/君子雜誌國際中文版',

        # 報紙
        '蘋果日報': '報紙/蘋果日報',
        '工商時報': '報紙/工商時報',
        '中國時報': '報紙/中國時報',
        '自由時報': '報紙/自由時報',
        '聯合晚報': '報紙/聯合晚報',
        '聯合報': '報紙/聯合報',
        '贏家日報': '報紙/贏家日報'
    }

    keys = [k for k, v in mags.items()]
    cats = list(filter(lambda k: k in name, keys))
    if len(cats) > 1:
        raise ValueError('Multiple keyword matched')

    if len(cats) == 0:
        # print("Not matched [{}]".format(name))
        return None

    return mags[cats[0]]


def get_mags_cat(b):
    # print("----")
    # print("[{}] - [{}][{}]".format(b['book_name'], b['book_category_name'], b['book_isbn_name']))

    # if it's a book, just return without '.'
    if b['book_category_name'].startswith('書籍-'):
        cat = "書籍"
    else:
        cat = _get_mags_cat(b['book_name'])

    if cat is None:
        print("[{}] - [{}][{}]".format(b['book_name'], b['book_category_name'], b['book_isbn_name']))
    return cat


def main():
    parser = argparse.ArgumentParser(description='magsname')
    parser.add_argument('-v', '--verbose', help='show more debug information', action='count')
    parser.add_argument('-V', '--version', action='version', version=VERSION, help='show version infomation')
    args = parser.parse_args()


if __name__ == "__main__":
    main()
