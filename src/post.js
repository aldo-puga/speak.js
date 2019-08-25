
function run_main(args) {
  args = args || Module['arguments'];

  if (preloadStartTime === null) preloadStartTime = Date.now();

  if (runDependencies > 0) {
    return;
  }

  //writeStackCookie();

  preRun();

  if (runDependencies > 0) return; // a preRun added a dependency, run will be called later

  function doRun() {
    if (ABORT) return;

    ensureInitRuntime();

    preMain();

    if (ENVIRONMENT_IS_WEB && preloadStartTime !== null) {
      Module.printErr('pre-main prep time: ' + (Date.now() - preloadStartTime) + ' ms');
    }

    if (Module['onRuntimeInitialized']) Module['onRuntimeInitialized']();

    if (Module['_main'] && args.length > 0)  Module['callMain'](args);

    postRun();
  }

  if (Module['setStatus']) {
    Module['setStatus']('Running...');
    setTimeout(function() {
      setTimeout(function() {
        Module['setStatus']('');
      }, 1);
      doRun();
    }, 1);
  } else {
    doRun();
  }
  //checkStackCookie();
}

  FS.ignorePermissions = true;

  FS.createPath('/', 'espeak/espeak-data', true, false);
  [['config', config], ['phontab', phontab], ['phonindex', phonindex], ['phondata', phondata], ['intonations', intonations]].forEach(function(pair) {
    var id = pair[0];
    var data = pair[1];
    FS.createDataFile('/espeak/espeak-data', id, data, true, false);
  });

  FS.createPath('/', 'espeak/espeak-data/voices', true, false);
  FS.createPath('/', 'espeak/espeak-data/voices/en', true, false);

  {{{ CREATE_DATA_FILES }}}

  var args = this['args'] || {};

  if (args['voice_file'] !== undefined && args['dict_file'] !== undefined) {
    FS.createDataFile('/espeak/espeak-data' , args['dict'], args['dict_file'], true, false);
    
    var voice = args['voice'].split('/');
    var voicePath;
    if (voice.length < 2) {
      voicePath = '/espeak/espeak-data/voices';
      voice = voice[0];
    } else {
      voicePath = '/espeak/espeak-data/voices/' + voice[0];
      voice = voice[1];
    }
    FS.createDataFile(voicePath, voice, args['voice_file'], true, false);
  }

  FS.root.write = true;

  FS.ignorePermissions = false;

  Module.arguments = [
    '-w', 'wav.wav',
    // options
    '-a', args['amplitude'] ? String(args['amplitude']) : '100',
    '-g', args['wordgap'] ? String(args['wordgap']) : '0', // XXX
    '-p', args['pitch'] ? String(args['pitch']) : '50',
    '-s', args['speed'] ? String(args['speed']) : '175',
    '-v', args['voice'] ? String(args['voice']) : 'en/en-us',
    // end options
    '--path=/espeak',
    this['text']
  ];

  run_main();

  this['ret'] = new Uint8Array(FS.root.contents['wav.wav'].contents);

