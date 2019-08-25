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

  execute();
}

