import re
import json
import ipaddress

def config_reader():
    with open('config.json') as js_file:
        config = json.load(js_file)
    return config
def cleaning(x):
  if isinstance(x, str):
    x = re.sub('[0-9]+', '', x)
    x = re.sub(r'[|;|:|.|,|/|_|\\]', ' ', x)
    x = re.sub(r'[-]', ' ', x)
    x = re.sub(' +', ' ', x).lower()
    x = x[:500]
  return x

def tokenize(data, tokenizer):
    input_ids = []
    attention_masks = []
    for sent in data:
        encoded_dict = tokenizer.encode_plus(
            sent,
            add_special_tokens=True,
            max_length=474,
            truncation=True,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    return (input_ids, attention_masks)

def ip_valid(ip):
    try:
      if ip.count('.') == 3:
        try:
          ipaddress.IPv4Address(ip)
          return True
        except ipaddress.AddressValueError:
          return False
      else:
        try:
          ipaddress.IPv6Address(ip)
          return True
        except ipaddress.AddressValueError:
          return False
    except:
        return False