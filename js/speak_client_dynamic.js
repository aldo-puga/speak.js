window.speak_js = {
  'voices': {},
  'dicts': {}
};

var speakWorker;
var suportServiceWork;

// https://github.com/yoshi6jp/speak.js/commit/b85d385024f1e20818aa9e3b272c86aa9fc2ebe6
function getSamePathOfSpeakScript(scriptFile) {
  var scripts = document.getElementsByTagName('script');
  for (var i = 0, length = scripts.length; i < length; i++) {
    var script = scripts[i];
    if (script.hasAttribute('src') && script.getAttribute('src').endsWith('speak_client.js')) {
      return script.getAttribute('src').replace('speak_client.js', scriptFile);
    }
  }
  return scriptFile;
}

function importJavaScriptSpeak(filename) {
  var script = document.createElement('script');
  script.setAttribute('type', 'text/javascript');
  script.setAttribute('src', getSamePathOfSpeakScript(filename));
  document.getElementsByTagName('head')[0].appendChild(script);
}

try {
  speakWorker = new Worker(getSamePathOfSpeakScript('speak_worker.js'));
  suportServiceWork = true;
} catch(e) {
  console.warn('speak.js warning: no worker support');
  suportServiceWork = false;
  importJavaScriptSpeak('speak_generator.js');
}

function speak(text, args, callback) {
  var LANGUAGES = {
    'af': 'af_dict',
    'ca': 'ca_dict',
    'cs': 'cs_dict',
    'cy': 'cy_dict',
    'da': 'da_dict',
    'de': 'de_dict',
    'el': 'el_dict',
    'en/en': 'en_dict',
    'en/en-n': 'en_dict',
    'en/en-rp': 'en_dict',
    'en/en-sc': 'en_dict',
    'en/en-us': 'en_dict',
    'en/en-wi': 'en_dict',
    'en/en-wm': 'en_dict',
    'eo': 'eo_dict',
    'es': 'es_dict',
    'es-la': 'es_dict',
    'fi': 'fi_dict',
    'fr': 'fr_dict',
    'fr-be': 'fr_dict',
    'hi': 'hi_dict',
    'hu': 'hu_dict',
    'hy': 'hy_dict',
    'hy-west': 'hy_dict',
    'id': 'id_dict',
    'is': 'is_dict',
    'it': 'it_dict',
    'ka': 'ka_dict',
    'kn': 'kn_dict',
    'ku': 'ku_dict',
    'la': 'la_dict',
    'lv': 'lv_dict',
    'mk': 'mk_dict',
    'ml': 'ml_dict',
    'nl': 'nl_dict',
    'no': 'no_dict',
    'pl': 'pl_dict',
    'pt': 'pt_dict',
    'pt-pt': 'pt_dict',
    'ro': 'ro_dict',
    'ru': 'ru_dict',
    'sk': 'sk_dict',
    'sq': 'sq_dict',
    'sv': 'sv_dict',
    'sw': 'sw_dict',
    'ta': 'ta_dict',
    'tr': 'tr_dict',
    'vi': 'vi_dict',
    'zh': 'zh_dict',
    'zh-yue': 'zhy_dict'
  };
  if (args['voice'] === undefined) {
    args['voice'] = 'en/en-us';
  }
  var executed = false;

  function parseWav(wav) {
    function readInt(i, bytes) {
      var ret = 0;
      var shft = 0;
      while (bytes) {
        ret += wav[i] << shft;
        shft += 8;
        i++;
        bytes--;
      }
      return ret;
    }
    if (readInt(20, 2) != 1) throw 'Invalid compression code, not PCM';
    if (readInt(22, 2) != 1) throw 'Invalid number of channels, not 1';
    return {
      sampleRate: readInt(24, 4),
      bitsPerSample: readInt(34, 2),
      samples: wav.subarray(44)
    };
  }

  function handleWav(wav) {
    var data = parseWav(wav); // validate the data and parse it
    callback(data, wav);
  }

  function execute() {
    if (args && (args.noWorker || !suportServiceWork)) {
      // Do everything right now. speakGenerator.js must have been loaded.
      var wav = generateSpeech(text, args);
      handleWav(wav);
    } else {
      // Call the worker, which will return a wav that we then play
      var startTime = Date.now();
      speakWorker.onmessage = function(event) {
        handleWav(event.data);
      };
      speakWorker.postMessage({ text: text, args: args });
    }
  }

  function executeDynamically(voice) {
    var dict = LANGUAGES[voice];
    if (speak_js.dicts[dict] !== undefined && speak_js.voices[voice] !== undefined && !executed) {
      executed = true;
      execute();
    }
  }

  function loadVoice() {
    var voice = args['voice'];
    var dict = LANGUAGES[voice];

    if ((speak_js.dicts[dict] === undefined) || (speak_js.voices[voice] === undefined)) {
      if (speak_js.dicts[dict] === undefined) {
        var dictPath = getSamePathOfSpeakScript('voices/dict/' + dict + '.json');
        var dictRequest = new XMLHttpRequest();
        dictRequest.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            speak_js.dicts[dict] = JSON.parse(this.responseText);
            args['dict'] = dict;
            args['dict_file'] = speak_js.dicts[dict];
            executeDynamically(voice);
          }
        };
        dictRequest.open('GET', dictPath, true);
        dictRequest.send();
      }

      if (speak_js.voices[voice] === undefined) {
        var voicePath = getSamePathOfSpeakScript('voices/voices/' + voice + '.json');
        var voiceRequest = new XMLHttpRequest();
        voiceRequest.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            speak_js.voices[voice] = JSON.parse(this.responseText);
            args['voice_file'] = speak_js.voices[voice];
            executeDynamically(voice);
          }
        };
        voiceRequest.open('GET', voicePath, true);
        voiceRequest.send();
      }
    } else {
      args['dict'] = dict;
      args['dict_file'] = speak_js.dicts[dict];
      args['voice_file'] = speak_js.voices[voice];
      executeDynamically(voice);
    }
  }

  loadVoice();
}

