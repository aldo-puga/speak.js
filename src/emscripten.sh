# Note: emmaken.py and other scripts mentioned here are part of Emscripten,
# available at https://github.com/kripken/emscripten
# (change the paths here to match where you set that up in your system).

set -e

# Emscripten directory
export EMSCRIPTEN=
# Espeak source code directory
export ESPEAK_SOURCE=../espeak/src
# Load voices dynamically
export LOAD_VOICES_DYNAMICALLY=-d

echo "make"
make --directory=$ESPEAK_SOURCE distclean
make --directory=$ESPEAK_SOURCE clean
CXXFLAGS="-DNEED_WCHAR_FUNCTIONS" $EMSCRIPTEN/emmake make --directory=$ESPEAK_SOURCE -j 2 speak
mv $ESPEAK_SOURCE/speak $ESPEAK_SOURCE/speak.bc

#echo "dis"
#~/Dev/llvm/cbuild/bin/llvm-dis -show-annotations speak -o=speak.ll
#echo "autodebug"
#mv speak.ll speak.orig.ll
#python ~/Dev/emscripten/tools/autodebugger.py speak.orig.ll speak.ll

echo "emscripten"
$EMSCRIPTEN/emcc -O2 --memory-init-file 0 --js-transform "python bundle.py $LOAD_VOICES_DYNAMICALLY $EMSCRIPTEN" $ESPEAK_SOURCE/speak.bc -o speak.raw.js
cat shell_pre.js > ../js/speak_generator.js
cat speak.raw.js >> ../js/speak_generator.js
cat shell_post.js >> ../js/speak_generator.js

if [ "$LOAD_VOICES_DYNAMICALLY" = "-d" ]; then
  cat ../js/speak_client_dynamic.js > ../js/speak_client.js
else
  cat ../js/speak_client_static.js > ../js/speak_client.js 
fi

make --directory=$ESPEAK_SOURCE distclean
make --directory=$ESPEAK_SOURCE clean
rm $ESPEAK_SOURCE/speak.bc
rm speak.raw.js







#~/Dev/mozilla-central/js/src/js -m speak.full.js -w wav.wav --path="/home/alon/Dev/espeak-1.45.04-source" "hello world"
#~/Dev/v8/d8 header.js speak.full.js footer.js
#gnome-sound-recorder wav.wav
#java -jar /home/alon/Dev/closure-compiler-read-only/build/compiler.jar --compilation_level SIMPLE_OPTIMIZATIONS --variable_map_output_file speak.vars --js speak.full.js --js_output_file speak.js
# Test:
#
# ./speak-native --path=/home/alon/Dev/speak.js -v 'en/en-us' -w wav.wav "4 world"
# OR
# ~/Dev/llvm/cbuild/bin/lli speak.bc -v 'en/en-us' -w wav.wav --path="/home/alon/Dev/speak.js" "4 world"
#
# gnome-sound-recorder wav.wav
#
#                                       # --path="/home/alon/Dev/speak.js" ?
# ~/Dev/mozilla-central/js/src/fast/js -m -n speak.full.js -w wav.wav --path="/espeak" "4 world" | grep -vi "bad voice" > wav.new.js
# python ~/Dev/emscripten/tools/make_file.py wav.new.js wav
# gnome-sound-recorder wav.new.js.wav



# Test:
#
# ./speak-native --path=/home/alon/Dev/speak.js -v 'en/en-us' -w wav.wav "4 test"
# OR
# ~/Dev/llvm/cbuild/bin/lli speak.bc -v 'en/en-us' -w wav.wav --path="/home/alon/Dev/speak.js" "4 test"
#
# gnome-sound-recorder wav.wav
#
#                                       # --path="/home/alon/Dev/speak.js" ?
# ~/Dev/mozilla-central/js/src/fast/js -m -n speak.full.js > wav.new.js
# python ~/Dev/emscripten/tools/make_file.py wav.new.js wav
# gnome-sound-recorder wav.new.js.wav

