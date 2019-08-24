importScripts('speak_generator.js');

onmessage = function(event) {
  postMessage(generateSpeech(event.data.text, event.data.args));
};

