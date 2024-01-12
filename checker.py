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

    def detect_ng_word(self, xml_text):
        with open(self.ng_words_file, 'r') as file:
            ng_words = {line.strip() for line in file}

        for word in ng_words:
            # 単語境界を使用してNGワードを検索
            if re.search(r'\b' + re.escape(word) + r'\b', xml_text):
                print(word)
                return False
        return True




