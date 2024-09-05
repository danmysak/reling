# ReLing: command-line tool for learning foreign languages through iterative translation with AI-generated feedback

## Installation<a id="installation"></a>

Install [Python](https://www.python.org/downloads/) 3.12 or higher, then run:

### Without audio support

```bash
pip install reling
```

### With audio support

On macOS, first install [Homebrew](https://brew.sh/), then run:

```bash
brew install portaudio
```

On Linux, run:

```bash
sudo apt install python3-pyaudio
```

Install the package with the `audio` extra:

```bash
pip install reling[audio]
```

### Auto-completion

To enable completions, run:

```bash
reling --install-completion
```

On a Mac, you may also need to add `compinit -D` at the end of your `~/.zshrc`.

## Data Sources

This application uses data for 183 major languages [obtained from Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes). The data is used under the terms of the CC BY-SA 4.0 license. Modifications have been made to adapt the data to the needs of this application. For more details on the license, please visit the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/deed.en).
