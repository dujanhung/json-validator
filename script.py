import json
import os
import re
import sys
class Validator:
 def __init__(self,lookup_path,data_path):
  self.lookup_path=lookup_path
  self.data_path=data_path
  self.unique_tracker={}
 def load_json(self,path):
  with open(path,"r",encoding="utf-8") as f:
   return json.load(f)
 def parse_entry(self,key):
  if "|" not in key:
   return key,[]
  parts=key.split("|",1)
  name=parts[0]
  flags=self.parse_flags(parts[1])
  return name,flags
 def parse_flags(self,raw):
  flags=[]
  current=""
  depth=0
  for char in raw:
   if char=="," and depth==0:
    flags.append(current.strip())
    current=""
    continue
   if char=="(":
    depth+=1
   elif char==")":
    depth-=1
   current+=char
  if current:
   flags.append(current.strip())
  return flags
 def validate(self,lookup,data,path="root"):
  errors=[]
  if isinstance(lookup,dict):
   if not isinstance(data,dict):
    return[f"{path}: expected object"]
   parsed_lookup={}
   for raw_key,variant in lookup.items():
    key,flags=self.parse_entry(raw_key)
    parsed_lookup[key]=(variant,flags)
   for key,(variant,flags) in parsed_lookup.items():
    required="@required" in flags
    if key not in data:
     if required:
      errors.append(f"{path}.{key}: missing required field")
     continue
    value=data[key]
    errors.extend(self.validate_variant(key,value,variant,flags,data,path))
  elif isinstance(lookup,list):
   if not isinstance(data,list):
    return[f"{path}: expected array"]
   if len(lookup)==0:
    return[]
   schema=lookup[0]
   for index,item in enumerate(data):
    errors.extend(self.validate(schema,item,f"{path}[{index}]"))
  return errors
 def validate_variant(self,key,value,variant,flags,obj,path):
  errors=[]
  if isinstance(variant,dict):
   errors.extend(self.validate(variant,value,f"{path}.{key}"))
   return errors
  if isinstance(variant,list):
   if not isinstance(value,list):
    errors.append(f"{path}.{key}: expected array")
    return errors
   array_flags=self.extract_flag(flags,"array_flag")
   if array_flags:
    if "allow_multiple" not in array_flags and len(value)>1:
     errors.append(f"{path}.{key}: multiple elements not allowed")
    if "strict" in array_flags:
     if len(variant)==0 and len(value)>0:
      errors.append(f"{path}.{key}: array must remain empty")
   if len(variant)>0:
    for index,item in enumerate(value):
     errors.extend(self.validate(variant[0],item,f"{path}.{key}[{index}]"))
   return errors
  if variant=="bool":
   if not isinstance(value,bool):
    errors.append(f"{path}.{key}: expected bool")
  elif variant=="int":
   if not isinstance(value,int) or isinstance(value,bool):
    errors.append(f"{path}.{key}: expected int")
  elif variant=="float":
   if not isinstance(value,(int,float)) or isinstance(value,bool):
    errors.append(f"{path}.{key}: expected float")
  elif variant=="string":
   if not isinstance(value,str):
    errors.append(f"{path}.{key}: expected string")
  elif variant=="json":
   if not isinstance(value,dict):
    errors.append(f"{path}.{key}: expected JSON object")
  errors.extend(self.validate_flags(key,value,flags,obj,path))
  return errors
 def extract_flag(self,flags,flag_name):
  for flag in flags:
   if flag.startswith(flag_name+"("):
    content=flag[len(flag_name)+1:-1]
    return[x.strip() for x in content.split(",")]
  return None
 def validate_flags(self,key,value,flags,obj,path):
  errors=[]
  for flag in flags:
   if flag=="@required":
    continue
   if flag=="@unique":
    if key not in self.unique_tracker:
     self.unique_tracker[key]=set()
    if value in self.unique_tracker[key]:
     errors.append(f"{path}.{key}: duplicate value")
    else:
     self.unique_tracker[key].add(value)
   elif flag.startswith("enum("):
    enums=[x.strip() for x in flag[5:-1].split(",")]
    if str(value) not in enums:
     errors.append(f"{path}.{key}: value not in enum")
   elif flag.startswith("hex_flag("):
    options=[x.strip() for x in flag[9:-1].split(",")]
    pattern=r"^[0-9a-f]{6}$"
    if "tag" in options:
     pattern=r"^#[0-9a-f]{6}$"
    if "no_alpha" not in options:
     if "tag" in options:
      pattern=r"^#[0-9a-f]{6,8}$"
     else:
      pattern=r"^[0-9a-f]{6,8}$"
    if not isinstance(value,str) or not re.match(pattern,value):
     errors.append(f"{path}.{key}: invalid hex")
   elif flag.startswith("external_file("):
    ext=flag[14:-1]
    if not isinstance(value,str):
     errors.append(f"{path}.{key}: expected file path string")
     continue
    if not value.endswith("."+ext):
     errors.append(f"{path}.{key}: invalid file extension")
    full_path=os.path.join(os.path.dirname(self.data_path),value)
    if not os.path.isfile(full_path):
     errors.append(f"{path}.{key}: file does not exist")
   elif flag.startswith("range_flag("):
    options=[x.strip() for x in flag[11:-1].split(",")]
    if not isinstance(value,(int,float)) or isinstance(value,bool):
     errors.append(f"{path}.{key}: range_flag() requires numeric value")
     continue
    for option in options:
     if option=="exp":
      if value<=0:
       errors.append(f"{path}.{key}: must satisfy x>0")
     elif option=="linear":
      if not(0<=value<=1):
       errors.append(f"{path}.{key}: must satisfy 0<=x<=1")
     elif option=="unsigned":
      if value<0:
       errors.append(f"{path}.{key}: must satisfy x>=0")
   elif flag.startswith("need("):
    condition=flag[5:-1]
    if not self.evaluate_need(condition,obj):
     errors.append(f"{path}.{key}: need() condition failed")
  return errors
 def evaluate_need(self,condition,obj):
  for key,value in obj.items():
   condition=condition.replace(f"{key}.value",repr(value))
  enum_matches=re.findall(r"(\w+)\.enum\.slot\((\d+)\)",condition)
  for field,slot in enum_matches:
   if field not in obj:
    return False
   condition=condition.replace(f"{field}.enum.slot({slot})",repr(obj[field]))
  try:
   return bool(eval(condition))
  except Exception:
   return False
def main():
 if len(sys.argv)!=3:
  print("usage: python validator.py lookup.json data.json")
  sys.exit(1)
 lookup_path=sys.argv[1]
 data_path=sys.argv[2]
 validator=Validator(lookup_path,data_path)
 lookup=validator.load_json(lookup_path)
 data=validator.load_json(data_path)
 errors=validator.validate(lookup,data)
 if errors:
  print("validation failed:")
  for error in errors:
   print(f"- {error}")
  sys.exit(1)
 print("validation successful")
if __name__=="__main__":
 main()