<h2>
JSON entry syntax
</h2>

```json
"name|flag_name,...":"variant_name"
```

<h2>
JSON variants enum
</h2>

```json
"int"
```

represents an integer value.

___

```json
"float"
```

represents a floating-point value.

___

```json
"string"
```

represents a string value.

<h2>
JSON flags enum
</h2>

```txt
@required
```

marks this JSON entry as required.

>[!CAUTION]
>if you remove such entries, the script would reject.

___

```txt
@unique
```

marks this JSON entry as unique against similar values within the array.

>[!CAUTION]
>if you duplicate such entries, the script would reject.

___

```txt
array_flag()
```

specify array flags.

only available for `array` .

- `allow_multiple` : allows the array to have multiple elements.
- `strict` : restricts the array to follow as is.

___

```txt
range_flag()
```

specify range flags.

only available for `float` and `int` .

- `exp` : represents exponental `float` .
- `linear` : represents linear `float` .
- `unsigned` : represents unsigned `int` or `float` .
- `binary` : represents binary `int` .

___

```txt
hex_flag()
```

specify HEX flags.

only available for `string` .

- `tag` : include tag symbol ( `#` ).
- `rgb` : represents RGB color.
- `rgba` : represents RGBA color.