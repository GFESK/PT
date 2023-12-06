import time
import json
from io import StringIO

import pandas as pd
import numpy as np

import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import BertTokenizer

from flask import Flask, request

from utils import cleaning, tokenize, config_reader, ip_valid

import warnings
warnings.filterwarnings("ignore")

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
model = torch.load('model/bert_model', map_location=torch.device(device))

app = Flask(__name__)
config = config_reader()

host = config['host']
port = config['port']

@app.route('/predict', methods= ['POST'])
def predict():
    result_list = []
    try:
        files = request.json
        json_data = [json.loads(item['data']) for item in files]
        data = pd.DataFrame(json_data).fillna('')
    except:
        files = request.data
        s = str(files, 'utf-8')
        data = StringIO(s)
        data = pd.read_csv(data).fillna('')
    for i, v in data.iterrows():
        start_time = time.time()
        id = str(v['EVENT_ID'])
        if not ip_valid(v['CLIENT_IP']):
            end_time = time.time()
            result_list.append({"EVENT_ID": id, "LABEL_PRED": '1', "Elapsed time": str(end_time - start_time)})
            continue

        data['text'] = data['CLIENT_USERAGENT'].apply(lambda x: cleaning(x)) + ' ' + data['MATCHED_VARIABLE_VALUE'].apply(
            lambda x: cleaning(x))

        req_text = data['text'].values
        tokens = tokenize(req_text, tokenizer)

        input_ids = torch.cat(tokens[0], dim=0)
        attention_masks = torch.cat(tokens[1], dim=0)

        dataset = TensorDataset(input_ids, attention_masks)
        dataloader = DataLoader(dataset, sampler = SequentialSampler(dataset), batch_size = 32)

        predictions = []
        for batch in dataloader:
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            with torch.no_grad():
                output = model(b_input_ids,
                               token_type_ids=None,
                               attention_mask=b_input_mask)
                logits = output.logits
                logits = logits.detach().cpu().numpy()
                pred_flat = np.argmax(logits, axis=1).flatten()

                predictions.extend(list(pred_flat))
        end_time = time.time()
        result_list.append({"EVENT_ID": id, "LABEL_PRED": str(predictions[0]), "Elapsed time": str(end_time - start_time)})

    result = json.dumps(result_list)
    return result

if __name__ == '__main__':
    app.run(host=host, port=port)