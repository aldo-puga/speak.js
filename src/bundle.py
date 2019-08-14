import os, sys
from subprocess import Popen, PIPE, STDOUT

SUPORT_LANGUAGES = ['en_us'] # fr Needed for French

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'espeak')

LANGUAGES = {
  'af': ['af_dict', 'af', None],
  #'bs': ['', '', None],
  'ca': ['ca_dict', 'ca', None],
  'cs': ['cs_dict', 'cs', None],
  'cy': ['cy_dict', 'cy', None],
  'da': ['da_dict', 'da', None],
  'de': ['de_dict', 'de', None],
  'el': ['el_dict', 'el', None],
  'en': ['en_dict', 'en', 'en'],
  'en_n': ['en_dict', 'en-n', 'en'],
  'en_rp': ['en_dict', 'en-rp', 'en'],
  'en_sc': ['en_dict', 'en-sc', 'en'],
  'en_us': ['en_dict', 'en-us', 'en'],
  'en_wi': ['en_dict', 'en-wi', 'en'],
  'en_wm': ['en_dict', 'en-wm', 'en'],
  'eo': ['eo_dict', 'eo', None],
  'es': ['es_dict', 'es', None],
  'es_la': ['es_dict', 'es-la', None],
  'fi': ['fi_dict', 'fi', None],
  'fr': ['fr_dict', 'fr', None],
  'fr_be': ['fr_dict', 'fr-be', None],
  'hi': ['hi_dict', 'hi', None],
  #'hr': ['', '', None],
  'hu': ['hu_dict', 'hu', None],
  'hy': ['hy_dict', 'hy', None],
  'hy_west': ['hy_dict', 'hy-west', None],
  'id': ['id_dict', 'id', None],
  'is': ['is_dict', 'is', None],
  'it': ['it_dict', 'it', None],
  'ka': ['ka_dict', 'ka', None],
  'kn': ['kn_dict', 'kn', None],
  'ku': ['ku_dict', 'ku', None],
  'la': ['la_dict', 'la', None],
  'lv': ['lv_dict', 'lv', None],
  'mk': ['mk_dict', 'mk', None],
  'ml': ['ml_dict', 'ml', None],
  'nl': ['nl_dict', 'nl', None],
  'no': ['no_dict', 'no', None],
  'pl': ['pl_dict', 'pl', None],
  'pt': ['pt_dict', 'pt', None],
  'pt_pt': ['pt_dict', 'pt-pt', None],
  'ro': ['ro_dict', 'ro', None],
  'ru': ['ru_dict', 'ru', None],
  'sk': ['sk_dict', 'sk', None],
  'sq': ['sq_dict', 'sq', None],
  #'sr': ['', '', None],
  'sv': ['sv_dict', 'sv', None],
  'sw': ['sw_dict', 'sw', None],
  'ta': ['ta_dict', 'ta', None],
  'tr': ['tr_dict', 'tr', None],
  'vi': ['vi_dict', 'vi', None],
  'zh': ['zh_dict', 'zh', None],
  'zh_yue': ['zhy_dict', 'zh-yue', None],
}

def process(emscripten_directory, filename):
  file2json = os.path.join(emscripten_directory, 'tools', 'file2json.py')

  files = ''
  create_data_files = ''

  for filey in ['config', 'phontab', 'phonindex', 'phondata', 'intonations']:
    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', filey), filey], stdout=PIPE).communicate()
    files += f[0]

  for language in SUPORT_LANGUAGES:
    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', LANGUAGES[language][0]), LANGUAGES[language][0]], stdout=PIPE).communicate()
    files += f[0]

    create_data_files += 'FS.createDataFile(\'/espeak/espeak-data\', \'{}\', {}, true, false);\n'.format(LANGUAGES[language][0], LANGUAGES[language][0])

    if LANGUAGES[language][2]:
        location = os.path.join(LANGUAGES[language][2], LANGUAGES[language][1])
    else:
        location = LANGUAGES[language][1]

    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', 'voices', location), language], stdout=PIPE).communicate()
    files += f[0]

    if LANGUAGES[language][2]:
        virtual_location = '/' + LANGUAGES[language][2]
    else:
        virtual_location = ''

    create_data_files += 'FS.createDataFile(\'/espeak/espeak-data/voices{}\', \'{}\', {}, true, false);\n'.format(virtual_location, LANGUAGES[language][1], language)

  src = open(filename).read()
  pre = open('pre.js').read()
  post = open('post.js').read()

  out = open(filename, 'w')
  out.write(pre.replace('{{{ FILES }}}', files))
  out.write(src)
  out.write(post.replace('{{{ CREATE_DATA_FILES }}}', create_data_files))
  out.close()

process(sys.argv[1], sys.argv[2])

