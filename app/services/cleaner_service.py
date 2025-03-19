import re

class CleanerService:
    def clean_text(self, text: str) -> str:
        text = text.replace('\t', ' ')
        text = re.sub(' +', ' ', text)

        text = text.replace('’', "'")
        text = text.replace('‘', "'")

        text = text.replace('“', '"')
        text = text.replace('”', '"')

        text = text.replace('«', '"')
        text = text.replace('»', '"')

        text = re.sub(' \.', '.', text)
        text = text.replace(' ,', ',')
        text = text.replace(' ;', ';')
        text = text.replace(' :', ':')
        text = text.replace('…', '...')

        text = re.sub('\( ', '(', text)
        text = re.sub(' \)', ')', text)

        text = text.replace('A\'', 'À')
        text = text.replace('E\'', 'É')
        text = text.replace('I\'', 'Í')
        text = text.replace('O\'', 'Ó')
        text = text.replace('U\'', 'Ú')

        text = text.replace('a\'', 'à')
        text = text.replace('e\'', 'é')
        text = text.replace('i\'', 'í')
        text = text.replace('o\'', 'ó')
        text = text.replace('u\'', 'ú')

        lines = text.split('\n')

        for i in range(len(lines)):
            lines[i] = lines[i].strip()

        return '\n'.join(lines)