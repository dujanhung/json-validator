<h2>
JSON lookup syntax
</h2>

```json
"name":"variant_name"
```

```json
"name|flag_name,...":"variant_name"
```

>[!NOTE]
>`name` shouldn't contains `|` , because it may breaks the script.

example:

the lookup file:

```json
{
 "a":"string",
 "b|external_file(lua)":"string",
 "c|@required,hex(tag,no_alpha)":"string"
}
```

would validate the JSON file likes this:

```json
{
 "a":"aaa",
 "b":"path/to/file.lua",
 "c":"#abcdef"
}
```

or, the minimal one is:

```json
{
 "c":"#abcdef"
}
```

___

<h2>
JSON variants enum
</h2>

```json
"bool"
```

represents a boolean type.

___

```json
"int"
```

represents an integer type.

___

```json
"float"
```

represents a floating-point type.

___

```json
"string"
```

represents a sequence of unicode characters.

___

```json
"array"
```

represents an array type.

___

```json
"json"
```

represents a nested JSON object.

___

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

marks this value as unique to prevent from duplicated values from different JSON objects from the same array.

only available for `int` , `float` and `string` .

example:

the lookup file:

```json
{
 "aa|array_flag(allow_multiple)":[
  {
   "a|@unique":"int"
  }
 ]
}
```

this file is valid:

```json
{
 "aa":[
  {
   "a":1
  },
  {
   "a":2
  }
 ]
}
```

this file is NOT valid (because it violates `@unique` in the lookup file) :

```json
{
 "aa":[
  {
   "a":1
  },
  {
   "a":1
  }
 ]
}
```

___

```txt
array_flag()
```

restricts the array with specified array flags.

only available for `array` .

- `allow_multiple` : allows the array to have multiple elements.
- `strict` : restricts the array to follow as is. if the value is `[]` , blocks all elements. if the value is `"array"` , accepts all elements.

___

```txt
range_flag()
```

restricts `float` and `int` to be within specified range flags.

only available for `float` and `int` .

- `exp` : represents exponental `float` .
- `linear` : represents linear `float` .
- `unsigned` : represents unsigned `int` or `float` .

___

```txt
hex_flag()
```

restricts `string` to be a HEX code with specified HEX flags.

only available for `string` .

- `tag` : include tag symbol ( `#` ).
- `no_alpha` : rejects alpha value.

>[!NOTE]
>HEX codes should be lowercase.
>
>example:
>
>`#abcdef`

___

```txt
external_file()
```

restricts `string` to be a path to external file that relative to the being-validated JSON file.

only available for `string` .

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

example:

the lookup file:

```json
{
 "a|enum(aa,bb)":"string"
}
```

this file is valid:

```json
{
 "a":"bb"
}
```

this file is NOT valid (because the value don't exists in `enum()` in the lookup file):

```json
{
 "a":"zz"
}
```

___

```txt
need()
```

restricts this entry with conditions within the same object level.

- `entry.key` : represents entry key.
- `entry.value` : represents entry value.
- `entry.enum.slot()` : represents entry enum slot in `enum()` . begins with `1` .
- `==` : equal.
- `>=` : more than or equal.
- `<=` : less than or equal.
- `!=` : not equal.
- `(` `)` : brackets for priority.
- `and` : represents "AND" logic.
- `or` : represents "OR" logic.
- `xor` : represents "exclusive OR" logic.
- `!` : represents "NOT" logic.
- `..` : concatenate `string` .

example:

the lookup file:

```json
{
 "a|enum(aa,bb)":"string",
 "b|need(a.value==a.enum.slot(2))":"int"
}
```

this file is valid:

```json
{
 "a":"bb",
 "b":0
}
```

this file is NOT valid (because it violates `need()` in the lookup file):

```json
{
 "a":"aa",
 "b":0
}
```