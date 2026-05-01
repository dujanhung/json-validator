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

represents an integer.

___

```json
"float"
```

represents a floating-point.

___

```json
"string"
```

represents a sequence of unicode characters.

___

```json
"array"
```

represents an array.

___

```json
"json"
```

represents a nested JSON object.

<h2>
JSON flags enum
</h2>

```txt
@required
```

marks this entry as required.

___

```txt
@unique
```

marks this value as unique against similar values within the array.

___

```txt
array_flag()
```

specify array flags.

only available for `array` .

- `allow_multiple` : allows the array to have multiple elements.
- `strict` : restricts the array to follow as is. if the value is `[]` , blocks all elements. if the value is `"array"` , accepts all elements.

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
- `no_alpha` : rejects alpha value.

___

```txt
external_file()
```

represents a path to external file.

only available for `string`

the mandatory is used to specify file extension.

- `png` : represents a PNG file.
- `obj` : represents an OBJ file.
- `lua` : represents a Lua file.

___

```txt
enum()
```

restricts the value with specified enum.

only available for `string` .

___

```txt
need()
```

restricts this entry with required conditions within the same object level.

- `entry.key` : represents entry key.
- `entry.value` : represents entry value.
- `entry.enum.slot()` : represents entry enum slot in `enum()` . begins with `1` .
- `==` : equal.
- `>=` : more than or equal.
- `<=` : less than or equal.
- `!=` : not equal.
- `..` : concatenate `string` .