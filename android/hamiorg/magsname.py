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
        '25ans': '雜誌/日文/25ans',
        "CLUTCH Magazine": "雜誌/日文/CLUTCH Magazine",
        "婦人畫報": "雜誌/日文/婦人畫報",
        "日本聰明好生活": "雜誌/日文/日本聰明好生活",

        '世界腕錶雜誌': '雜誌/流行時尚/世界腕錶雜誌',
        '《明潮》': '雜誌/流行時尚/《明潮》',
        '【霸屏女孩】髮型': '雜誌/流行時尚/【霸屏女孩】髮型',
        'vivi': '雜誌/流行時尚/vivi',
        'mina': '雜誌/流行時尚/mina',
        'InStyle 時尚樂': '雜誌/流行時尚/InStyle 時尚樂',
        'Girl愛女生': '雜誌/流行時尚/Girl愛女生',
        'VOGUE': '雜誌/流行時尚/VOGUE',
        '潮人物': '雜誌/流行時尚/潮人物',
        'Marie Claire美麗佳人': '雜誌/流行時尚/Marie Claire美麗佳人',
        'BEAUTY': '雜誌/流行時尚/BEAUTY',

        '小日子享生活誌': '雜誌/家庭生活/小日子享生活誌',
        '時尚家居': '雜誌/家庭生活/時尚家居',
        'SENSE好感': '雜誌/家庭生活/SENSE好感',
        '親子天下': '雜誌/家庭生活/親子天下',
        '康健特刊': '雜誌/家庭生活/康健特刊',
        '媽媽寶寶': '雜誌/家庭生活/媽媽寶寶',

        '經貿透視': '雜誌/商業理財/經貿透視',
        '今周刊': '雜誌/商業理財/今周刊',
        '商業周刊': '雜誌/商業理財/商業周刊',
        '天下雜誌': '雜誌/商業理財/天下雜誌',
        '財訊': '雜誌/商業理財/財訊雙週刊',
        '先探投資週刊': '雜誌/商業理財/先探投資週刊',
        '遠見雜誌': '雜誌/商業理財/遠見雜誌',
        '女人變有錢': '雜誌/商業理財/女人變有錢',
        '理財周刊': '雜誌/商業理財/理財周刊',
        'Money錢': '雜誌/商業理財/Money錢',

        '電玩雙週刊': '雜誌/休閒旅遊/電玩雙週刊',
        'Taipei Walker 特別號': '雜誌/休閒旅遊/Taipei Walker 特別號',
        '單車誌': '雜誌/休閒旅遊/單車誌',
        '食尚玩家': '雜誌/休閒旅遊/食尚玩家',
        'Travel for Fun 旅日趣': '雜誌/休閒旅遊/Travel for Fun 旅日趣',
        '大人的週末精華特輯': '雜誌/休閒旅遊/大人的週末精華特輯',
        'az旅遊生活雜誌': '雜誌/休閒旅遊/az旅遊生活雜誌',

        '新新聞': '雜誌/新聞時事/新新聞',
        '鏡週刊': '雜誌/新聞時事/鏡週刊',
        '周刊王': '雜誌/新聞時事/周刊王',
        '明報周刊': '雜誌/新聞時事/明報周刊',
        '時報周刊': '雜誌/新聞時事/時報周刊',
        '看雜誌': '雜誌/新聞時事/看雜誌',

        '幼獅少年': '雜誌/兒童/幼獅少年',
        'Joy to the world': '雜誌/兒童/Joy to the world',
        '康軒學習雜誌': '雜誌/兒童/康軒學習雜誌',

        'Make：國際中文版': '雜誌/3C科學/Make',
        'iPhone, iPad 玩樂誌': '雜誌/3C科學/iPhone, iPad 玩樂誌',
        'Android 密技王': '雜誌/3C科學/Android 密技王',
        'Stuff Taiwan史塔夫科技': '雜誌/3C科學/Stuff Taiwan史塔夫科技',
        '知識大圖解': '雜誌/3C科學/知識大圖解',
        'BBC知識 Knowledge': '雜誌/3C科學/BBC知識 Knowledge',

        '壹週刊': '雜誌/影視娛樂/壹週刊',
        'iLOOK電影雜誌': '雜誌/影視娛樂/iLOOK電影雜誌',
        '世界電影雜誌': '雜誌/影視娛樂/世界電影雜誌',

        '當代設計雜誌': '雜誌/藝術設計/當代設計雜誌',
        'Shopping Design': '雜誌/藝術設計/Shopping Design設計採買誌',
        'ARCH 雅趣': '雜誌/藝術設計/ARCH 雅趣',
        '城邦國際名表': '雜誌/藝術設計/城邦國際名表',
        '住宅美學': '雜誌/藝術設計/住宅美學',
        'DECO 居家': '雜誌/藝術設計/DECO 居家',
        'La Vie': '雜誌/藝術設計/La Vie',
        '古美術': '雜誌/藝術設計/古美術',
        '小典藏': '雜誌/藝術設計/小典藏',
        '今藝術': '雜誌/藝術設計/今藝術',

        '君子時代雜誌國際中文版': '雜誌/男性時尚/君子雜誌國際中文版',
        "men's uno": "雜誌/男性時尚/mens uno",
        'GQ': '雜誌/男性時尚/GQ',
        'BANG': '雜誌/男性時尚/BANG',

        '阿路巴高爾夫國際中文版': '雜誌/運動競技/阿路巴高爾夫國際中文版',
        '職業棒球': '雜誌/運動競技/職業棒球',

        '動腦雜誌': '雜誌/行銷企管/動腦雜誌',
        '能力雜誌': '雜誌/行銷企管/能力雜誌',

        '車主Auto Driver': '雜誌/汽機車/車主Auto Driver',
        'Option改裝車訊': '雜誌/汽機車/Option改裝車訊',
        'CARNEW一手車訊': '雜誌/汽機車/CARNEW一手車訊',

        '聯合文學': '雜誌/人文社會/聯合文學',

        '漂亮家居': '雜誌/建築攝影/漂亮家居',

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
