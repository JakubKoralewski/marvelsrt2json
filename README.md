# marvelsrt2json.py

Given the folder of subtitles (.srt SubRip UTF-8 encoded) with each having a name
that is easily recognizable to belonging to a certain Marvel movie (title and year)
this script generates another directory recognisable by the 
[mcuverse](https://github.com/seanlennaerts/mcuverse) project.

## Example

### Given something like this:

```srt
1
00:00:19,602 --> 00:00:20,603
Stark.

2
00:00:21,396 --> 00:00:23,898
- Nie wygląda na zadowolonego.
- Witaj, Hank.

...
```

### Generates something like this:

```json

[
  {
    "index": 0,
    "sub": [
      "Stark."
    ],
    "time": "0:19"
  },
  {
    "index": 1,
    "sub": [
      "Nie wygląda na zadowolonego.",
      "Witaj, Hank."
    ],
    "time": "0:21"
  },

...
```

# LICENSE
MIT