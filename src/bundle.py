import os, sys
from subprocess import Popen, PIPE, STDOUT

SUPORT_LANGUAGES = ['en_us', 'es', 'fr'] # fr Needed for French

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'espeak')
JS_VOICES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'js', 'voices')
JS_VOICES_DICT_DIR = os.path.join(JS_VOICES_DIR, 'dict')
JS_VOICES_VOICES_DIR = os.path.join(JS_VOICES_DIR, 'voices')

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

def create_directory_if_not_exists(language):
  if LANGUAGES[language][2]:
    if not os.path.exists(os.path.join(JS_VOICES_VOICES_DIR, LANGUAGES[language][2])):
      os.makedirs(os.path.join(JS_VOICES_VOICES_DIR, LANGUAGES[language][2]))

def get_dict_location(language):
  voice_dict = LANGUAGES[language][0]
  if LANGUAGES[language][2]:
    location = os.path.join(LANGUAGES[language][2], LANGUAGES[language][1])
    virtual_location = '/' + LANGUAGES[language][2]
  else:
    location = LANGUAGES[language][1]
    virtual_location = ''
  return (voice_dict, location, virtual_location)

def create_dynamic_voices_files(file2json):
  for language in SUPORT_LANGUAGES:
    voice_dict, location, virtual_location = get_dict_location(language)
    create_directory_if_not_exists(language)

    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', voice_dict)], stdout=PIPE).communicate()
    out = open(os.path.join(JS_VOICES_DICT_DIR, voice_dict) + '.json', 'w')
    out.write(f[0])
    out.close()

    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', 'voices', location)], stdout=PIPE).communicate()
    out = open(os.path.join(JS_VOICES_VOICES_DIR, location) + '.json', 'w')
    out.write(f[0])
    out.close()

def create_static_voices_files(file2json, files):
  create_data_files = ''
  for language in SUPORT_LANGUAGES:
    voice_dict, location, virtual_location = get_dict_location(language)

    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', voice_dict), voice_dict], stdout=PIPE).communicate()
    files += f[0]
    create_data_files += 'FS.createDataFile(\'/espeak/espeak-data\', \'{}\', {}, true, false);\n'.format(voice_dict, voice_dict)

    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', 'voices', location), language], stdout=PIPE).communicate()
    files += f[0]
    create_data_files += 'FS.createDataFile(\'/espeak/espeak-data/voices{}\', \'{}\', {}, true, false);\n'.format(virtual_location, LANGUAGES[language][1], language)
  return (files, create_data_files)

def process(emscripten_directory, filename, load_dynamically=False):
  file2json = os.path.join(emscripten_directory, 'tools', 'file2json.py')

  files = ''
  create_data_files = ''

  if load_dynamically:
    SUPORT_LANGUAGES = list(LANGUAGES.keys())

  for filey in ['config', 'phontab', 'phonindex', 'phondata', 'intonations']:
    f = Popen(['python', file2json, os.path.join(BASE_DIR, 'espeak-data', filey), filey], stdout=PIPE).communicate()
    files += f[0]

  if load_dynamically:
    create_dynamic_voices_files(file2json)
  else:
    files, create_data_files = create_static_voices_files(file2json, files)

  src = open(filename).read()
  pre = open('pre.js').read()
  post = open('post.js').read()

  out = open(filename, 'w')
  out.write(pre.replace('{{{ FILES }}}', files))
  out.write(src)
  out.write(post.replace('{{{ CREATE_DATA_FILES }}}', create_data_files))
  out.close()

if len(sys.argv) < 4:
  process(sys.argv[1], sys.argv[2])
else:
  process(sys.argv[2], sys.argv[3], sys.argv[1] == '-d')

