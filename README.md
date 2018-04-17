# myXMLTV
Script to search the channel which match with keyword

# Usage
```channel.py keywords channels```

- **keywords** is a list of word used in the title, sub-title or description of the movie, separated by comma

AND

- **channels** is a list of channel where search the keyword, separated by comma

and a html file will be created where the script is executed.

The **keywords** and **channels** _are not case sensitive_.

The comma separator for **keywords** and **channels** is _OR operator_.

# Example
```channel.py hitler```

```channel.py hitler "paris première"```

```channel.py hitler "   rmc découverte,    paris première  "```

```channel.py hitler,allemagne "rmc découverte,paris première"```

```channel.py évêque,religion```

```channel.py turbo m6 ```

# Comptability

[Latin-1 characters](https://fr.wikipedia.org/wiki/ISO/CEI_8859-1)
