import xml.etree.ElementTree as ET
import re
class Checker:
    def __init__(self, ng_words_file='assets/input/ngword_list.csv'):
        #self.xml_text = xml_text
        self.ng_words_file = ng_words_file

    def xml_checker(self, xml_text):
        try:
            root = ET.fromstring(xml_text)

            if root.tag != 'profile':
                return False

            expected_tags = {
                'hashtags', 'big_five_chart', 'character', 'personality',
                'hometown', 'occupation', 'favorite_things', 'hobby',
                'skill', 'habit', 'dream', 'talent', 'motto', 'comment'
            }

            # XML内のタグを集める
            found_tags = {child.tag for child in root}

            # 期待されるすべてのタグが存在するかチェック
            if not expected_tags.issubset(found_tags):
                return False

            # 'big_five_chart' タグのサブタグをチェック
            big_five_chart = root.find('big_five_chart')
            if big_five_chart is not None:
                expected_subtags = {'openness', 'conscientiousness',
                                    'extraversion', 'agreeableness', 'neuroticism'}
                found_subtags = {child.tag for child in big_five_chart}
                if not expected_subtags.issubset(found_subtags):
                    return False

            return True
        except ET.ParseError:
            return False

    def detect_ng_word(self, xml_text):
        with open(self.ng_words_file, 'r') as file:
            ng_words = {line.strip() for line in file}

        for word in ng_words:
            # 単語境界を使用してNGワードを検索
            if re.search(r'\b' + re.escape(word) + r'\b', xml_text):
                print(word)
                return False
        return True




