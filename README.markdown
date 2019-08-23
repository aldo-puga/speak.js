speak.js
========

A port of the eSpeak speech synthesizer from C++ to JavaScript using Emscripten.

Enables text-to-speech on the web using only JavaScript and HTML5.

Note
----

This is a changed version of [speak.js](https://github.com/kripken/speak.js) from the commit [9c6f642f7d78bab51d16b2e8b79cdf205643ec35](https://github.com/kripken/speak.js/commit/9c6f642f7d78bab51d16b2e8b79cdf205643ec35) in Dec 4, 2017.

Usage
-----

Very simple! Do this:

 * Include the script in your html header,

```html
<script src="speakClient.js"></script>
```

   (and make sure you have **speak_client.js** available, as well as
   **speak_worker.js** and **speak_generator.js**)

 * Call `speak()` to say stuff in JavaScript

```js
speak('hello world!', {}, function(data, wav) { ... });
```

See **demo.html** for a more detailed example.


Options
-------

You can also specify some options with calling `speak()`, by doing

```js
speak('hello world', { option1: value1, option2: value2 .. }, function(data, wav) { ... });
```

available options are:

 * `amplitude`: How loud the voice will be (default: 100)
 * `pitch`: The voice pitch (default: 50)
 * `speed`: The speed at which to talk (words per minute) (default: 175)
 * `voice`: Which voice to use (for a non-default voice, requires you to
          build speak.js to include the proper data. See Language Support
          below) (default: en/en-us)
 * `wordgap`: Additional gap between words in 10 ms units (default: 0)
 * `noWorker`: Do not use a web worker (see below in 'Architecture')

For example

```js
speak('hello world', { pitch: 100 }, function(data, wav) { ... });
```

will talk in a very high-pitched voice.


Architecture
------------

**speak_client.js** is the file that you interact with. It defines `speak()`, and
will load **speak_worker.js** in a web worker. speakWorker wraps around
**speak_generator.js**, which does the actual work of converting a string into
a WAV file. The WAV data is returned to `speak()`, which then call the `callback`
parameter returning the WAV file and its metadata.

You can also use speak.js without a web worker. In that case, you don't
need **speak_worker.js**, but you do need to load **speak_generator.js** along
with **speak_client.js** in your HTML page. `speak()`, if called with noWorker
set to true in the options object, will directly call the WAV generation
code in **speak_generator.js** instead of forwarding the call to a worker
which would have done the same.


Building
--------

A prebuilt version is already included. But if you want to tinker with the
source code though, you might want to build it yourself. To do so, run
**emscripten.sh** inside src/. Note that you need to change the paths there.


Build dependencies
------------------

* emsdk
* sdk-1.37.23-64bit or sdk-1.37.23-32bit

Language Support
----------------

eSpeak supports multiple languages so speak.js can too. To do this, you
need to build a custom version of speak.js:

 * Bundle the proper language files. For french, you need fr_dict and voices/fr.
   See commented-out code in **emscripten.sh** and **bundle.py**
 * Run **emscripten.sh** to build.

You then need to call `speak()` with the `voice` option that tells it to use the
right voice for your language. For example, for French this should work:

```js
speak('boulanger', { voice: 'fr' }, function(data, wav) { ... });
```

