# JSON lookup syntax

a lookup schema defines the expected structure and validation rules for a JSON file.

___

## basic syntax

```json
"name":"variant_name"
```

defines a field with a specific type.

___

## syntax with flags

```json
"name|flag_name,...":"variant_name"
```

defines a field with one or more validation flags.

> [!NOTE]
> `name` must **not** contain `|`, because it is used as the separator for flags.

___

## example

lookup schema:

```json
{
 "a":"string",
 "b|external_file(lua)":"string",
 "c|@required,hex_flag(tag,no_alpha)":"string"
}
```

valid JSON:

```json
{
 "a":"aaa",
 "b":"path/to/file.lua",
 "c":"#abcdef"
}
```

minimal valid JSON:

```json
{
 "c":"#abcdef"
}
```

___
---

# JSON variant types

these are the available built-in value types.

___

## <code>bool</code>

```json
"bool"
```

represents a boolean value.

example:

```json
true
```

---

## <code>int</code>

```json
"int"
```

represents an integer value.

example:

```json
123
```

---

## <code>float</code>

```json
"float"
```

represents a floating-point value.

example:

```json
3.14
```

---

## <code>string</code>

```json
"string"
```

represents a unicode string.

example:

```json
"🐑"
```

---

## <code>array</code>

```json
"array"
```

represents an array.

example:

```json
[1,2,3]
```

---

## <code>json</code>

```json
"json"
```

represents a nested JSON object.

example:

```json
{
 "🐑":0
}
```

___
---

# JSON flags

flags add validation rules to a field.

---

## <code>@required</code>

```txt
@required
```

marks the field as required.

example:

```json
{
 "name|@required":"string"
}
```

the `name` field must exist.

---

## <code>@unique</code>

```txt
@unique
```

ensures values are unique across objects in the same array.

available for:

- `int`
- `float`
- `string`

### example

lookup schema:

```json
{
 "aa|array_flag(allow_multiple)":[
  {
   "a|@unique":"int"
  }
 ]
}
```

valid JSON:

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

invalid JSON:

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

reason: duplicate value violates `@unique`.

---

## <code>array_flag()</code>

```txt
array_flag()
```

applies restrictions to arrays.

available for:

- `array`

### options

- `allow_multiple` → allows multiple elements
- `strict` → enforces the exact schema structure

behavior of `strict`:

- `[]` → rejects all elements
- `"array"` → accepts any element

---

## <code>range_flag()</code>

```txt
range_flag()
```

applies numeric constraints.

available for:

- `int`
- `float`

### options

- `exp` → exponential float ( `x>0` ).
- `linear` → linear float ( `0<=x<=1` ).
- `unsigned` → unsigned int or float ( `x>=0` ).

---

## <code>hex_flag()</code>

```txt
hex_flag()
```

restricts a string to a hex color code.

available for:

- `string`

### options

- `tag` → requires `#` prefix
- `no_alpha` → disallows alpha channel

> [!NOTE]
> hex values must be lowercase.
>
> ### example
>
> ```json
> "#abcdef"
> ```

---

## <code>external_file()</code>

```txt
external_file(extension)
```

restricts a string to a relative file path.

available for:

- `string`

the parameter specifies the required file extension.

supported extensions:

- `png`
- `obj`
- `lua`

### example

```json
{
 "script|external_file(lua)":"string"
}
```

valid:

```json
{
 "script":"scripts/test.lua"
}
```

---

## <code>enum()</code>

```txt
enum()
```

restricts a value to a predefined list.

available for:

- `int`
- `float`
- `string`

### example

lookup schema:

```json
{
 "a|enum(aa,bb)":"string"
}
```

valid JSON:

```json
{
 "a":"bb"
}
```

invalid JSON:

```json
{
 "a":"zz"
}
```

reason: value is not listed in `enum()`.

---

## <code>need()</code>

```txt
need()
```

adds conditional validation based on other fields in the same object.

### supported expressions

- `entry.key` → field name
- `entry.value` → field value
- `entry.enum.slot(n)` → enum position (starts at `1`)

### supported operators

- `==` → equal
- `!=` → not equal
- `>=` → greater than or equal
- `<=` → less than or equal

### example

lookup schema:

```json
{
 "a|enum(aa,bb)":"string",
 "b|need(a.value==a.enum.slot(2))":"int"
}
```

valid JSON:

```json
{
 "a":"bb",
 "b":0
}
```

invalid JSON:

```json
{
 "a":"aa",
 "b":0
}
```

reason: `b` is only allowed when `a` matches enum slot `2`.