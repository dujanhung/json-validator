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
>if you remove such entries, the script would throw an error.

___

```txt
@unique
```

marks this JSON entry as unique against similar values.

>[!CAUTION]
>if you duplicate such entries, the script would throw an error.