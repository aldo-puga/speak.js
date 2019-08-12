import os, sys
from subprocess import Popen, PIPE, STDOUT

SUPORT_LANGUAGES = ['en_us'] # fr Needed for French

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'espeak')

LANGUAGES = {
  'af': ['af_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'af')],
  #'bs': ['', os.path.join(BASE_DIR, 'espeak-data', 'voices', '')],
  'ca': ['ca_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ca')],
  'cs': ['cs_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'cs')],
  'cy': ['cy_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'cy')],
  'da': ['da_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'da')],
  'de': ['de_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'de')],
  'el': ['el_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'el')],
  'en': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en')],
  'en_n': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en-n')],
  'en_rp': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en-rp')],
  'en_sc': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en-sc')],
  'en_us': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en-us')],
  'en_wi': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en-wi')],
  'en_wm': ['en_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'en', 'en-wm')],
  'eo': ['eo_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'eo')],
  'es': ['es_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'es')],
  'es_la': ['es_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'es-la')],
  'fi': ['fi_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'fi')],
  'fr': ['fr_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'fr')],
  'fr_be': ['fr_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'fr-be')],
  'hi': ['hi_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'hi')],
  #'hr': ['', os.path.join(BASE_DIR, 'espeak-data', 'voices', '')],
  'hu': ['hu_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'hu')],
  'hy': ['hy_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'hy')],
  'hy_west': ['hy_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'hy-west')],
  'id': ['id_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'id')],
  'is': ['is_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'is')],
  'it': ['it_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'it')],
  'ka': ['ka_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ka')],
  'kn': ['kn_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'kn')],
  'ku': ['ku_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ku')],
  'la': ['la_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'la')],
  'lv': ['lv_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'lv')],
  'mk': ['mk_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'mk')],
  'ml': ['ml_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ml')],
  'nl': ['nl_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'nl')],
  'no': ['no_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'no')],
  'pl': ['pl_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'pl')],
  'pt': ['pt_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'pt')],
  'pt_pt': ['pt_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'pt-pt')],
  'ro': ['ro_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ro')],
  'ru': ['ru_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ru')],
  'sk': ['sk_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'sk')],
  'sq': ['sq_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'sq')],
  #'sr': ['', os.path.join(BASE_DIR, 'espeak-data', 'voices', '')],
  'sv': ['sv_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'sv')],
  'sw': ['sw_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'sw')],
  'ta': ['ta_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'ta')],
  'tr': ['tr_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'tr')],
  'vi': ['vi_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'vi')],
  'zh': ['zh_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'zh')],
  'zh_yue': ['zhy_dict', os.path.join(BASE_DIR, 'espeak-data', 'voices', 'zh-yue')],
}

def process(emscripten_directory, filename):
  file2json = os.path.join(emscripten_directory, 'tools', 'file2json.py')

  files = ''

  for filey in ['config', 'phontab', 'phonindex', 'phondata', 'intonations']:
    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', filey), filey], stdout=PIPE).communicate()
    files += f[0]

  for language in SUPORT_LANGUAGES:
    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', LANGUAGES[language][0]), LANGUAGES[language][0]], stdout=PIPE).communicate()
    files += f[0]

    f = Popen(['python', file2json, LANGUAGES[language][1], language], stdout=PIPE).communicate()
    files += f[0]

  src = open(filename).read()
  pre = open('pre.js').read()
  post = open('post.js').read()

  out = open(filename, 'w')
  out.write(pre.replace('{{{ FILES }}}', files))
  out.write(src)
  out.write(post)
  out.close()

process(sys.argv[1], sys.argv[2])

