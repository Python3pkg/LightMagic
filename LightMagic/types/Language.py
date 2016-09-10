from ._Base import _Base

class Language(_Base):
    """
        Работа с наименованием языка. Поддерживаются следующие стандарты:
        ISO639-1, ISO639-2/T, ISO639-2/B, ISO639-3, ISO639-6
    """

    lang_639_1 = ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu',
                      'be', 'bn', 'bh', 'bi', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'cv', 'kw', 'co', 'cr',
                      'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gl', 'ka',
                      'de', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'ia', 'id', 'ie', 'ga', 'ig', 'ik',
                      'io', 'is', 'it', 'iu', 'ja', 'jv', 'kl', 'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg',
                      'ko', 'ku', 'kj', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'gv', 'mk', 'mg', 'ms', 'ml',
                      'mt', 'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'nd', 'ne', 'ng', 'nb', 'nn', 'no', 'ii', 'nr', 'oc', 'oj',
                      'cu', 'om', 'or', 'os', 'pa', 'pi', 'fa', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'sa', 'sc',
                      'sd', 'se', 'sm', 'sg', 'sr', 'gd', 'sn', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'ss', 'sv',
                      'ta', 'te', 'tg', 'th', 'ti', 'bo', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug',
                      'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'wo', 'fy', 'xh', 'yi', 'yo', 'za', 'zu']

    lang_639_2_t = ['abk', 'aar', 'afr', 'aka', 'sqi', 'amh', 'ara', 'arg', 'hye', 'asm', 'ava', 'ave', 'aym', 'aze', 'bam',
                    'bak', 'eus', 'bel', 'ben', 'bih', 'bis', 'bos', 'bre', 'bul', 'mya', 'cat', 'cha', 'che', 'nya', 'zho',
                    'chv', 'cor', 'cos', 'cre', 'hrv', 'ces', 'dan', 'div', 'nld', 'dzo', 'eng', 'epo', 'est', 'ewe', 'fao',
                    'fij', 'fin', 'fra', 'ful', 'glg', 'kat', 'deu', 'ell', 'grn', 'guj', 'hat', 'hau', 'heb', 'her', 'hin',
                    'hmo', 'hun', 'ina', 'ind', 'ile', 'gle', 'ibo', 'ipk', 'ido', 'isl', 'ita', 'iku', 'jpn', 'jav', 'kal',
                    'kan', 'kau', 'kas', 'kaz', 'khm', 'kik', 'kin', 'kir', 'kom', 'kon', 'kor', 'kur', 'kua', 'lat', 'ltz',
                    'lug', 'lim', 'lin', 'lao', 'lit', 'lub', 'lav', 'glv', 'mkd', 'mlg', 'msa', 'mal', 'mlt', 'mri', 'mar',
                    'mah', 'mon', 'nau', 'nav', 'nde', 'nep', 'ndo', 'nob', 'nno', 'nor', 'iii', 'nbl', 'oci', 'oji', 'chu',
                    'orm', 'ori', 'oss', 'pan', 'pli', 'fas', 'pol', 'pus', 'por', 'que', 'roh', 'run', 'ron', 'rus', 'san',
                    'srd', 'snd', 'sme', 'smo', 'sag', 'srp', 'gla', 'sna', 'sin', 'slk', 'slv', 'som', 'sot', 'spa', 'sun',
                    'swa', 'ssw', 'swe', 'tam', 'tel', 'tgk', 'tha', 'tir', 'bod', 'tuk', 'tgl', 'tsn', 'ton', 'tur', 'tso',
                    'tat', 'twi', 'tah', 'uig', 'ukr', 'urd', 'uzb', 'ven', 'vie', 'vol', 'wln', 'cym', 'wol', 'fry', 'xho',
                    'yid', 'yor', 'zha', 'zul']

    lang_639_2_b = ['abk', 'aar', 'afr', 'aka', 'alb', 'amh', 'ara', 'arg', 'arm', 'asm', 'ava', 'ave', 'aym', 'aze', 'bam',
                    'bak', 'baq', 'bel', 'ben', 'bih', 'bis', 'bos', 'bre', 'bul', 'bur', 'cat', 'cha', 'che', 'nya', 'chi',
                    'chv', 'cor', 'cos', 'cre', 'hrv', 'cze', 'dan', 'div', 'dut', 'dzo', 'eng', 'epo', 'est', 'ewe', 'fao',
                    'fij', 'fin', 'fre', 'ful', 'glg', 'geo', 'ger', 'gre', 'grn', 'guj', 'hat', 'hau', 'heb', 'her', 'hin',
                    'hmo', 'hun', 'ina', 'ind', 'ile', 'gle', 'ibo', 'ipk', 'ido', 'ice', 'ita', 'iku', 'jpn', 'jav', 'kal',
                    'kan', 'kau', 'kas', 'kaz', 'khm', 'kik', 'kin', 'kir', 'kom', 'kon', 'kor', 'kur', 'kua', 'lat', 'ltz',
                    'lug', 'lim', 'lin', 'lao', 'lit', 'lub', 'lav', 'glv', 'mac', 'mlg', 'may', 'mal', 'mlt', 'mao', 'mar',
                    'mah', 'mon', 'nau', 'nav', 'nde', 'nep', 'ndo', 'nob', 'nno', 'nor', 'iii', 'nbl', 'oci', 'oji', 'chu',
                    'orm', 'ori', 'oss', 'pan', 'pli', 'per', 'pol', 'pus', 'por', 'que', 'roh', 'run', 'rum', 'rus', 'san',
                    'srd', 'snd', 'sme', 'smo', 'sag', 'srp', 'gla', 'sna', 'sin', 'slo', 'slv', 'som', 'sot', 'spa', 'sun',
                    'swa', 'ssw', 'swe', 'tam', 'tel', 'tgk', 'tha', 'tir', 'tib', 'tuk', 'tgl', 'tsn', 'ton', 'tur', 'tso',
                    'tat', 'twi', 'tah', 'uig', 'ukr', 'urd', 'uzb', 'ven', 'vie', 'vol', 'wln', 'wel', 'wol', 'fry', 'xho',
                    'yid', 'yor', 'zha', 'zul']

    lang_639_3 = ['abk', 'aar', 'afr', 'aka', 'sqi', 'amh', 'ara', 'arg', 'hye', 'asm', 'ava', 'ave', 'aym', 'aze', 'bam',
                  'bak', 'eus', 'bel', 'ben', '', 'bis', 'bos', 'bre', 'bul', 'mya', 'cat', 'cha', 'che', 'nya', 'zho',
                  'chv', 'cor', 'cos', 'cre', 'hrv', 'ces', 'dan', 'div', 'nld', 'dzo', 'eng', 'epo', 'est', 'ewe', 'fao',
                  'fij', 'fin', 'fra', 'ful', 'glg', 'kat', 'deu', 'ell', 'grn', 'guj', 'hat', 'hau', 'heb', 'her', 'hin',
                  'hmo', 'hun', 'ina', 'ind', 'ile', 'gle', 'ibo', 'ipk', 'ido', 'isl', 'ita', 'iku', 'jpn', 'jav', 'kal',
                  'kan', 'kau', 'kas', 'kaz', 'khm', 'kik', 'kin', 'kir', 'kom', 'kon', 'kor', 'kur', 'kua', 'lat', 'ltz',
                  'lug', 'lim', 'lin', 'lao', 'lit', 'lub', 'lav', 'glv', 'mkd', 'mlg', 'msa', 'mal', 'mlt', 'mri', 'mar',
                  'mah', 'mon', 'nau', 'nav', 'nde', 'nep', 'ndo', 'nob', 'nno', 'nor', 'iii', 'nbl', 'oci', 'oji', 'chu',
                  'orm', 'ori', 'oss', 'pan', 'pli', 'fas', 'pol', 'pus', 'por', 'que', 'roh', 'run', 'ron', 'rus', 'san',
                  'srd', 'snd', 'sme', 'smo', 'sag', 'srp', 'gla', 'sna', 'sin', 'slk', 'slv', 'som', 'sot', 'spa', 'sun',
                  'swa', 'ssw', 'swe', 'tam', 'tel', 'tgk', 'tha', 'tir', 'bod', 'tuk', 'tgl', 'tsn', 'ton', 'tur', 'tso',
                  'tat', 'twi', 'tah', 'uig', 'ukr', 'urd', 'uzb', 'ven', 'vie', 'vol', 'wln', 'cym', 'wol', 'fry', 'xho',
                  'yid', 'yor', 'zha', 'zul']

    lang_639_6 = ['abks', 'aars', 'afrs', 'boss', 'buls', 'engs', 'fras', 'deus', 'ells', 'hins', 'idos', 'itas', 'lats',
                  'pols']

    def __init__(self, lang_type='lang_639_1', *args, **kwargs):
        if lang_type not in ('lang_639_1', 'lang_639_2_t', 'lang_639_2_b', 'lang_639_3', 'lang_639_6'):
            raise ValueError
        self.lang_type = lang_type

        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if str(value) not in getattr(self, self.lang_type):
            raise ValueError('Language abbreviation is not correct')

        return value
