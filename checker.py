import xml.etree.ElementTree as ET
import re
import MeCab
import unicodedata


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
                'hometown','occupation'
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
                'skill', 'habit', 'dream', 'talent', 'motto'
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

    def detect_ng_word(self, xml_text, pool=False):
        # 半角を全角に
        xml_text_2 = unicodedata.normalize('NFKC', xml_text)
        # 記号系が、unicodeだと検出できない場合があるため、念のため両方。
        xml_text = xml_text + xml_text_2
        with open(self.ng_words_file, 'r', encoding='utf-8') as file:
            ng_words = [line.strip() for line in file]

        # 形態素解析でテキストを単語に分割
        node = self.mecab.parseToNode(xml_text)
        words = []
        while node:
            if node.surface:
                words.append(node.surface)
            node = node.next

        for i in range(len(words) - 1):
            first_word = words[i]
            combined_two_word = words[i] + words[i + 1]
            if i >= 1:
                combined_three_word = words[i - 1] + combined_two_word
                if combined_three_word in ng_words:
                    print(f"NG word detected: {combined_three_word}")
                    return False

            if first_word in ng_words:
                print(f"NG word detected: {first_word}")
                return False

            if combined_two_word in ng_words:
                print(f"NG word detected: {combined_two_word}")
                return False

        return True
