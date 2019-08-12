import os, sys
from subprocess import Popen, PIPE, STDOUT

def process(emscripten_directory, filename):
  file2json = os.path.join(emscripten_directory, 'tools', 'file2json.py')
  base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'espeak')

  files = ''

  for filey in ['config', 'phontab', 'phonindex', 'phondata', 'intonations', 'en_dict']: # fr_dict # Needed for French
    f = Popen(['python', file2json, os.path.join(base_dir, 'espeak-data', filey), filey], stdout=PIPE).communicate()
    files += f[0]

  f = Popen(['python', file2json, os.path.join(base_dir, 'espeak-data', 'voices', 'en', 'en-us'), 'en_us'], stdout=PIPE).communicate()
  files += f[0]

  # Needed for French
  #f = Popen(['python', file2json, os.path.join(base_dir, 'espeak-data', 'voices', 'fr'), 'fr'], stdout=PIPE).communicate()
  #files += f[0]

  src = open(filename).read()
  pre = open('pre.js').read()
  post = open('post.js').read()

  out = open(filename, 'w')
  out.write(pre.replace('{{{ FILES }}}', files))
  out.write(src)
  out.write(post)
  out.close()

process(sys.argv[1], sys.argv[2])

