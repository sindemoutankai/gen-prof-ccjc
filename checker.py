import xml.etree.ElementTree as ET
import re
import MeCab


class Checker:
    def __init__(self, ng_words_file='assets/input/ngword_list.csv'):
        #self.xml_text = xml_text
        self.ng_words_file = ng_words_file
        self.mecab = MeCab.Tagger()

    def xml_checker(self, xml_text):
        try:
            root = ET.fromstring(xml_text)

            if root.tag != 'profile':
                return False

            expected_tags = {
                'hashtags', 'big_five_chart', 'character', 'personality',
                'hometown'
            }

            for child in root:
                if child.tag not in expected_tags:
                    return False
                if child.tag == 'big_five_chart':
                    expected_subtags = {'openness', 'conscientiousness',
                                        'extraversion', 'agreeableness', 'neuroticism'}
                    for subchild in child:
                        if subchild.tag not in expected_subtags:
                            return False

            return True
        except ET.ParseError:
            return False

    def xml_checker2(self, xml_text):
        try:
            root = ET.fromstring(xml_text)

            if root.tag != 'profile':
                return False

            expected_tags = {
                'occupation', 'favorite_things', 'hobby',
                'skill', 'habit', 'dream', 'talent', 'motto', 'comment'
            }

            # XML内のタグ集める
            found_tags = {child.tag for child in root}

            # 期待されるすべてのタグが存在するかチェック
            if not expected_tags.issubset(found_tags):
                return False

            for child in root:
                if len(child.text or '') > 30:
                    return False

            return True
        except ET.ParseError:
            return False


#ここから変換処理
    def _full_to_half(self, text):

        full_to_half_map = str.maketrans(
            '０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ　'
            'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッー',
            '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
            'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝｧｨｩｪｫｬｭｮｯｰ')
        text = text.translate(full_to_half_map)

        dakuten_chars = {
            'ガ': 'ｶﾞ', 'ギ': 'ｷﾞ', 'グ': 'ｸﾞ', 'ゲ': 'ｹﾞ', 'ゴ': 'ｺﾞ',
            'ザ': 'ｻﾞ', 'ジ': 'ｼﾞ', 'ズ': 'ｽﾞ', 'ゼ': 'ｾﾞ', 'ゾ': 'ｿﾞ',
            'ダ': 'ﾀﾞ', 'ヂ': 'ﾁﾞ', 'ヅ': 'ﾂﾞ', 'デ': 'ﾃﾞ', 'ド': 'ﾄﾞ',
            'バ': 'ﾊﾞ', 'ビ': 'ﾋﾞ', 'ブ': 'ﾌﾞ', 'ベ': 'ﾍﾞ', 'ボ': 'ﾎﾞ',
            'パ': 'ﾊﾟ', 'ピ': 'ﾋﾟ', 'プ': 'ﾌﾟ', 'ペ': 'ﾍﾟ', 'ポ': 'ﾎﾟ',
            'ヴ': 'ｳﾞ'
        }
        for full, half in dakuten_chars.items():
            text = text.replace(full, half)
        return text

    def _half_to_full(self, text):

        half_to_full_map = str.maketrans(
            '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
            'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝｧｨｩｪｫｬｭｮｯｰ',
            '０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ　'
            'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッー')
        text = text.translate(half_to_full_map)

        # 濁点付き、半濁点付きカタカナの半角を全角に変換
        handakuten_chars = {
            'ｶﾞ': 'ガ', 'ｷﾞ': 'ギ', 'ｸﾞ': 'グ', 'ｹﾞ': 'ゲ', 'ｺﾞ': 'ゴ',
            'ｻﾞ': 'ザ', 'ｼﾞ': 'ジ', 'ｽﾞ': 'ズ', 'ｾﾞ': 'ゼ', 'ｿﾞ': 'ゾ',
            'ﾀﾞ': 'ダ', 'ﾁﾞ': 'ヂ', 'ﾂﾞ': 'ヅ', 'ﾃﾞ': 'デ', 'ﾄﾞ': 'ド',
            'ﾊﾞ': 'バ', 'ﾋﾞ': 'ビ', 'ﾌﾞ': 'ブ', 'ﾍﾞ': 'ベ', 'ﾎﾞ': 'ボ',
            'ﾊﾟ': 'パ', 'ﾋﾟ': 'ピ', 'ﾌﾟ': 'プ', 'ﾍﾟ': 'ペ', 'ﾎﾟ': 'ポ',
            'ｳﾞ': 'ヴ'
        }
        for half, full in handakuten_chars.items():
            text = text.replace(half, full)
        return text

    def detect_ng_word(self, xml_text):
        # 半角カタカナを全角に変換
        xml_text = self._half_to_full(xml_text)

        with open(self.ng_words_file, 'r') as file:
            ng_words = {line.strip() for line in file}

        node = self.mecab.parseToNode(xml_text)
        while node:
            word = node.surface
            if word in ng_words:
                print(word)
                return False
            node = node.next
        return True



