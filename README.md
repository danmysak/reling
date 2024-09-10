# ReLing: Command-line Tool for Learning Foreign Languages

ReLing allows you to learn or enhance your knowledge of any [major world language](#languages) supported by [GPT models](https://platform.openai.com/docs/models). To use this tool, you must have a paid [OpenAI account](https://platform.openai.com/) with an [API key created](https://platform.openai.com/api-keys).

The program operates as follows:

- [Select a GPT model](#setting-models-and-api-key) to generate a [text](#generating-texts) or [dialogue](#generating-dialogues) on a chosen or random topic.
- View or translate the generated content into any [supported language](#languages).
- Take an  [exam](#taking-exams) to translate the text from one language to another and receive:
  - A score for each sentence on a 10-point scale;
  - Suggestions for improving your translations;
  - The program’s own translation of the sentence.

You can retake exams at your preferred frequency until you achieve perfect scores.

ReLing also enables you to view a [list](#listing-content) of all generated texts and dialogues and their associated [exam histories](#exam-history).

Optionally, the system can vocalize sentences in both the source and target languages and accept your responses via voice.


## Table of Contents<a name="table-of-contents"></a>

- [Installation](#installation)
- [Generating Texts](#generating-texts)
- [Generating Dialogues](#generating-dialogues)
- [Displaying Content](#displaying-content)
- [Taking Exams](#taking-exams)
- [Exam History](#exam-history)
- [Listing Content](#listing-content)
- [Archiving Content](#archiving-content)
- [Unarchiving Content](#unarchiving-content)
- [Renaming Content](#renaming-content)
- [Deleting Content](#deleting-content)
- [Exporting Data](#exporting-data)
- [Languages](#languages)
- [Setting Models and API Key](#setting-models-and-api-key)
- [Specifying Genders](#specifying-genders)


## Installation<a name="installation"></a>

Install [Python](https://www.python.org/downloads/) 3.12 or higher and [pipx](https://pipx.pypa.io/stable/installation/), then proceed based on your audio preference:

### Without Audio Support

```bash
pipx install reling
```

### With Audio Support

On macOS, first install [Homebrew](https://brew.sh/), then:

```bash
brew install portaudio
```

On Ubuntu, run:

```bash
sudo apt install python3-pyaudio
```

Install the package with the `audio` extra:

```bash
pipx install 'reling[audio]'
```

### Auto-completion

To enable completions, run:

```bash
reling --install-completion
```

On a Mac, you may also need to add `compinit -D` at the end of your `~/.zshrc`.


## Generating Texts<a name="generating-texts"></a>
`reling create text`

The command format is:

```bash
reling create text en [--level basic] [--topic food] [--style news] [--size 5] [--include "cook: a person"] [--model <GPT-MODEL>] [--api-key <OPENAI-KEY>]
```

### Language

Specify a [supported language](#languages) as the only positional argument. The text will be in that language but can be translated later.

### `level`

Choose from three complexity levels:

- `basic`;
- `intermediate` (default);
- `advanced`.

### `topic`

You may select a topic for the text. If unspecified, a random topic from [100 predefined options](src/reling/data/topics.csv) will be chosen.

### `style`

You may also choose a style for the text. If unspecified, a random style from [25 predefined options](src/reling/data/styles.csv) will be chosen.

### `size`

This sets the number of sentences in the text. By default, 10 sentences are generated.

### `include`

This parameter allows you to ensure the inclusion of specific vocabulary in the text. You can specify a simple word (`--include cook`), a word with a specific meaning (`--include "cook: a person"`), or several words or phrases (`--include "cook: a person" --include soup --include "mac and cheese"`).

### `model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Generating Dialogues<a name="generating-dialogues"></a>
`reling create dialogue`

The command format is:

```bash
reling create dialogue en [--level advanced] [--speaker waiter] [--topic food] [--size 5] [--include "cook: a person"] [--speaker-gender male] [--user-gender female] [--model <GPT-MODEL>] [--api-key <OPENAI-KEY>]
```

### Language

Specify a [supported language](#languages) as the only positional argument. The dialogue will be generated in this language and can be translated later.

### `level`

Choose from three complexity levels:

- `basic`;
- `intermediate` (default);
- `advanced`.

### `speaker`

Specify an interlocutor or let the system choose randomly from [20 predefined options](src/reling/data/speakers.csv).

### `topic`

Choose a topic for the dialogue or let it be automatically determined.

### `size`

This parameter sets the number of sentence pairs in the dialogue. The default is 10.

### `include`

This parameter allows you to ensure the inclusion of specific vocabulary in the dialogue. You can specify a simple word (`--include cook`), a word with a specific meaning (`--include "cook: a person"`), or several words or phrases (`--include "cook: a person" --include soup --include "mac and cheese"`).

### `speaker-gender` & `user-gender`

Refer to [Specifying Genders](#specifying-genders).

If the interlocutor’s gender is not specified, it will be randomly chosen as either `male` or `female`.

### `model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Displaying Content<a name="displaying-content"></a>
`reling show`

View or listen to a text or dialogue with:

```bash
reling show <CONTENT-ID> [en] [--read] [--model <GPT-MODEL>] [--tts-model <TTS-MODEL>] [--api-key <OPENAI-KEY>]
```

### Content ID

Specify the identifier of the content to view. This ID is provided when content is created and [listed](#listing-content).

### Language

Optionally, specify a language to view the content in that language, translating if necessary.

### `read`

If enabled, the content will be read aloud.

### `model`, `tts-model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Taking Exams<a name="taking-exams"></a>
`reling exam`

To translate a text or dialogue and receive feedback, run:

```bash
reling exam <CONTENT-ID> [--from en] [--to fr] [--read fr] [--listen] [--model <GPT-MODEL>] [--tts-model <TTS-MODEL>] [--asr-model <ASR-MODEL>] [--api-key <OPENAI-KEY>]
```

### Content ID

Specify the content identifier for the exam. This ID is provided when content is created and [listed](#listing-content).

### `from` & `to`

Specify the languages from which and to which you would like to translate the text or dialogue. If one of the languages is not specified, the original language of the selected text or dialogue will be used.

### `read`

Optionally, you can specify one or both of the selected source and target languages to have the text read aloud. For example, use `--read en --read fr` to hear the content in English and French.

### `listen`

When this flag is enabled, ReLing will accept your responses via voice. You also have the option to switch to manual input mode if needed.

### `model`, `tts-model`, `asr-model` & `api-key`

Refer to [Setting Models and API Key](#setting-models-and-api-key).


## Exam History<a name="exam-history"></a>
`reling stats`

To view your exam history and statistics, use the command:

```bash
reling stats <CONTENT-ID> [--from en] [--to fr]
```

### Content ID

Specify the identifier of the text or dialogue whose exam history you wish to review.

### `from` & `to`

Limit the display of exam results to translations between specified source and target languages.


## Listing Content<a name="listing-content"></a>
`reling list`

To view a list of all generated texts and dialogues, execute:

```bash
reling list [--category dialogue] [--level intermediate] [--language en] [--search <REGEX>] [--archive] [--ids-only]
```

### `category`

Choose to display either `text`s or `dialogue`s.

### `level`

Filter content by complexity level: `basic`, `intermediate`, or `advanced`.

### `language`

Display content generated in a specific language.

### `search`

Use a regular expression to search content IDs, text, topics, styles, or interlocutors.

### `archive`

Toggle to view content from the [archive](#archiving-content).

### `ids-only`

Display only the identifiers of texts and dialogues without full details.


## Archiving Content<a name="archiving-content"></a>
`reling archive`

To archive texts and dialogues:

```bash
reling archive <CONTENT-ID>
```

### Content ID

Provide the identifier of the content you wish to archive.


## Unarchiving Content<a name="unarchiving-content"></a>
`reling unarchive`

To restore archived content to the main list:

```bash
reling unarchive <CONTENT-ID>
```

### Content ID

Specify the identifier of the content to be restored from the archive.


## Renaming Content<a name="renaming-content"></a>
`reling rename`

To rename a specific text or dialogue:

```bash
reling rename <CONTENT-ID> <NEW-NAME>
```

### Content ID

Enter the identifier of the content you want to rename.

### New Name

Provide the new name for the content.


## Deleting Content<a name="deleting-content"></a>
`reling delete`

To remove texts or dialogues permanently:

```bash
reling delete <CONTENT-ID> [--force]
```

### Content ID

Specify the identifier of the content you intend to delete.

### `force`

Enable immediate deletion without confirmation.


## Exporting Data<a name="exporting-data"></a>
`reling db`

To access the data storage file for transferring or backing up content and exam results:

```bash
reling db
```


## Languages<a name="languages"></a>

ReLing supports over **180 major languages** [sourced from Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) under the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/deed.en).

To specify a language in a command argument, you can either write its full name (e.g., `English` or `english`) or use the 2-character or 3-character code for that language (e.g., `en` or `eng` for English).


## Setting Models and API Key<a name="setting-models-and-api-key"></a>

To avoid specifying [model names](https://platform.openai.com/docs/models) and entering the [API key](https://platform.openai.com/api-keys) separately for each command, you can set the following environment variables:

- `RELING_API_KEY`: a pre-generated API key for OpenAI’s web API.
- `RELING_MODEL`: the name of the GPT model used for generating text and taking exams (e.g., `gpt-4o`).
- `RELING_TTS_MODEL`: the name of the text-to-speech (TTS) model (e.g., `tts-1`).
- `RELING_ASR_MODEL`: the name of the automatic speech recognition (ASR) model for voice response recognition (e.g., `whisper-1`).

Parameter values specified in individual commands will take precedence over these environment variables.

If a model or key is not specified in either the command or the environment variable, the program will prompt you to enter it directly.


## Specifying Genders<a name="specifying-genders"></a>

The system requires knowledge of your gender and the gender of your interlocutor to accurately generate dialogues in languages with grammatical gender and to provide voice outputs with appropriate voices.

To avoid specifying your gender each time you generate a new dialogue, you can set the environment variable `RELING_USER_GENDER`.

The system accepts one of the following values for gender: `male`, `female`, or `nonbinary`.