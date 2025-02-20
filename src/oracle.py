import requests
import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from openai import OpenAI
import google.generativeai as genai
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage

# openai apis
# MODEL_GPT4 = 'gpt-4'                  # out-dated, should not use
# MODEL_GPT3_5 = 'gpt-3.5-turbo-0125'   # out-dated, should not use
MODEL_GPT4_TURBO = 'gpt-4-turbo'
MODEL_GPT4o = 'gpt-4o'
MODEL_GPT4o_MINI = 'gpt-4o-mini'
MODEL_GPT_o1 = 'o1'
MODEL_GPT_o1_MINI = 'o1-mini'
MODEL_GPT_o3_MINI = 'o3-mini'
MODEL_EMBED_SMALL = 'text-embedding-3-small'
MODEL_EMBED_LARGE = 'text-embedding-3-large'
# google models
MODEL_GEMINI_15_PRO = 'gemini-1.5-pro'
MODEL_GEMINI_15_FLASH = 'gemini-1.5-flash'
MODEL_GEMINI_1_PRO = 'gemini-1.0-pro'
MODEL_GEMINI_2_FLASH = 'gemini-2.0-flash'
MODEL_GEMINI_2_FLASH_LITE = 'gemini-2.0-flash-lite-preview-02-05'
MODEL_EMBED_GOOGLE = 'text-embedding-004'
# azure deployments (for phi-family models you need to specify the endpoint url by yourself)
MODEL_PHI_3_MINI = 'phi-3-mini'
MODEL_PHI_3_5_MINI = 'phi-3.5-mini'
MODEL_PHI_3_SMALL = 'phi-3-small'
MODEL_PHI_3_MEDIUM = 'phi-3-medium'
# deepinfra deployments
DEEP_INFRA_BASE_URL = 'https://api.deepinfra.com/v1/openai'
MODEL_LLAMA_3_8B = 'llama-3-8B'     # [02/20] 3 -> 3.1
MODEL_LLAMA_3_70B = 'llama-3-70B'   # [02/20] 3 -> 3.1
MODEL_MIXTRAL_8X7B = 'mixtral-8x7B'
MODEL_DEEP_SEEK_R1 = 'deepseek-r1'
MODEL_DEEP_SEEK_V3 = 'deepseek-v3'
MODEL_PHI_4 = 'phi-4'
MODEL_MISTRAL_SMALL = 'mistral-small'
DEEP_INFRA_MAP = {MODEL_LLAMA_3_8B: 'meta-llama/Meta-Llama-3.1-8B-Instruct',
                  MODEL_LLAMA_3_70B: 'meta-llama/Meta-Llama-3.1-70B-Instruct',
                  MODEL_MIXTRAL_8X7B: 'mistralai/Mixtral-8x7B-Instruct-v0.1',
                  MODEL_DEEP_SEEK_R1: 'deepseek-ai/DeepSeek-R1',
                  MODEL_DEEP_SEEK_V3: 'deepseek-ai/DeepSeek-V3',
                  MODEL_PHI_4: 'microsoft/phi-4',
                  MODEL_MISTRAL_SMALL: 'mistralai/Mistral-Small-24B-Instruct-2501',}

# ollama
OLLAMA_BASE_URL = 'https://u547021-8ded-55e5d1f2.cqa1.seetacloud.com:8443/api/generate/'
MODEL_QWQ_32B = 'qwq_32b' #quant int4
MODEL_QWQ_32B_Q8 = 'qwq_32b_q8'
OLLAMA_MAP = {MODEL_QWQ_32B: 'modelscope.cn/AI-ModelScope/QwQ-32B-Preview-GGUF:latest',
              MODEL_QWQ_32B_Q8: 'modelscope.cn/AI-ModelScope/QwQ-32B-Preview-GGUF:Q8_0',}

openai_model_list = [MODEL_GPT4o_MINI, MODEL_GPT4o, MODEL_GPT4_TURBO, MODEL_GPT_o1, MODEL_GPT_o1_MINI, MODEL_GPT_o3_MINI,
                    MODEL_EMBED_SMALL, MODEL_EMBED_LARGE]
google_model_list = [MODEL_GEMINI_1_PRO, MODEL_GEMINI_15_PRO, MODEL_GEMINI_15_FLASH, 
                     MODEL_GEMINI_2_FLASH, MODEL_GEMINI_2_FLASH_LITE, MODEL_EMBED_GOOGLE]
azure_model_list = [MODEL_PHI_3_MINI, MODEL_PHI_3_5_MINI, MODEL_PHI_3_SMALL, MODEL_PHI_3_MEDIUM]
deepinfra_model_list = [MODEL_LLAMA_3_8B, MODEL_LLAMA_3_70B, MODEL_MIXTRAL_8X7B, MODEL_DEEP_SEEK_R1, MODEL_DEEP_SEEK_V3,
                        MODEL_PHI_4, MODEL_MISTRAL_SMALL]
ollama_model_list = [MODEL_QWQ_32B, MODEL_QWQ_32B_Q8]
all_model_list = []
for l in [openai_model_list, google_model_list, azure_model_list, deepinfra_model_list, ollama_model_list]:
    all_model_list += l

def response_failure(prompt_user, model, e,):
    print(f"err: The following error occurred when querying {prompt_user} through {model}:")
    print(e)
    return {"query": prompt_user, "answer": "QUERY_FAILED"}

def openai_chat_query(
        # single query
        client, # openai client object;
        model,
        prompt_sys,
        prompt_user,
        temp,
        top_p,
    ) -> dict:

        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt_sys},
                    {"role": "user", "content": prompt_user},
                ],
                stream=False,
                temperature=temp,
                top_p=top_p,
            )

            response_result = ""
            # for chunk in stream:
            if completion.choices[0].message:
                response_result += completion.choices[0].message.content

            return {"query": prompt_user, "answer": response_result}

        except Exception as e:  # Consider capturing a specific exception if possible
            return response_failure(prompt_user, model, e)

def openai_embed_query(client, model, list_of_text, dimensions) -> dict:
    # small batch query
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

    # replace newlines, which can negatively affect performance.
    list_of_text = [text.replace("\n", " ") for text in list_of_text]

    data = client.embeddings.create(input=list_of_text, model=model, dimensions=dimensions).data
    
    res = {list_of_text[i]:data[i].embedding for i in range(len(list_of_text))}
    return res

def google_chat_query(client, model, prompt_sys, prompt_user, temp, top_p,) -> dict:
    # here model and prompt_sys are useless, just to align with the openai interface
    # TODO: support top_p
    gen_config = {"temperature": temp,}
    try:
        response = client.generate_content(prompt_user, generation_config=gen_config)
        res =  {"query": prompt_user, "answer": response.text}
        return res
    except Exception as e:
        return response_failure(prompt_user, model, e)

def rest_chat_query(client, model, prompt_sys, prompt_user, temp, top_p,) -> dict:
    try:
        response = requests.post(
            client['url'],
            auth=('apitoken', client['apitoken']),
            json={
                "model": model,
                "prompt": prompt_sys + prompt_user,
                "stream": False,
                "options": {
                    "temperature": temp,
                    "top_p": top_p,
                },
            }
        )
        # res = {"query": prompt_user, "answer": response.json()['response']}
        res = {"query": prompt_user, "answer": response.json()}
        return res
    except Exception as e:
        return response_failure(prompt_user, model, e)
    
def azure_chat_query(client, model, prompt_sys, prompt_user, temp, top_p,) -> dict:
    # TODO: support top_p
    sys_message = SystemMessage(content=prompt_sys)
    usr_message = UserMessage(content=prompt_user)
    try:
        response = client.complete(messages=[sys_message, usr_message,], temperature=temp,)
        response_text = response['choices'][0]['message']['content']
        res = {"query": prompt_user, "answer": response_text}
        return res
    except Exception as e:
        return response_failure(prompt_user, model, e)

class Oracle:
    def __init__(self, model, apikey=None, azure_end_point=''):
        assert model in all_model_list, f'err: model named {model} is not supported'
        self.model = model
        self.apikey = apikey
        # for openai models
        if model in openai_model_list:
            if apikey: openai.api_key = apikey
            self.client = OpenAI()
        elif model in deepinfra_model_list:
            self.client = OpenAI(api_key=apikey, base_url=DEEP_INFRA_BASE_URL)
        elif model in ollama_model_list:
            self.client = {'url': OLLAMA_BASE_URL, 'apitoken': self.apikey}
        elif model in google_model_list:
            genai.configure(api_key=apikey,)
            self.client = genai.GenerativeModel(model)
        elif model in azure_model_list:
            azure_credential = AzureKeyCredential(apikey)
            self.client = ChatCompletionsClient(endpoint=azure_end_point, credential=azure_credential)
    
    def query(self, prompt_sys, prompt_user, temp=1.0, top_p=0.9):
        if self.model in openai_model_list:
            return openai_chat_query(self.client, self.model, prompt_sys, prompt_user, temp, top_p)
        elif self.model in deepinfra_model_list:
            return openai_chat_query(self.client, DEEP_INFRA_MAP[self.model], prompt_sys, prompt_user, temp, top_p)
        elif self.model in ollama_model_list:
            return rest_chat_query(self.client, OLLAMA_MAP[self.model], prompt_sys, prompt_user, temp, top_p)
        elif self.model in google_model_list:
            # prompt_sys not supported
            return google_chat_query(self.client, self.model, prompt_sys, prompt_user, temp, top_p)
        elif self.model in azure_model_list:
            return azure_chat_query(self.client, self.model, prompt_sys, prompt_user, temp, top_p)
    
    def query_all(self, prompt_sys, prompt_user_all, workers=12, temp=1.0, top_p=0.9, **kwargs):
        # prompt_user_all: [str,]

        # collect procedure
        results = []
        print(f"Total queries: {len(prompt_user_all)}, start collecting...")

        model_name = self.model
        if self.model in openai_model_list:
            single_query_fn = openai_chat_query
        elif self.model in deepinfra_model_list:
            single_query_fn = openai_chat_query
            model_name = DEEP_INFRA_MAP[self.model]
        elif self.model in ollama_model_list:
            single_query_fn = rest_chat_query
            model_name = OLLAMA_MAP[self.model]
        elif self.model in google_model_list:
            single_query_fn = google_chat_query
            if prompt_sys: # refresh the system prompt
                self.client = genai.GenerativeModel(model_name=self.model, system_instruction=prompt_sys,)
        elif self.model in azure_model_list:
            single_query_fn = azure_chat_query
        
        with ThreadPoolExecutor(max_workers=workers) as executor: # avg. 0.13s per item
            future_results = [executor.submit(single_query_fn, self.client, model_name, prompt_sys, p, temp, top_p,) for p in prompt_user_all]
        
            for future in tqdm(as_completed(future_results), total=len(prompt_user_all), desc="Processing Items"):
                result = future.result()
                results.append(result)
        return results
    
    def encode(self, text, dim=1024):
        # single
        if self.model in openai_model_list:
            return openai_embed_query(self.client, self.model, [text], dim)

    def encode_all(self, list_of_text, workers=12, dim=1024, chunk_size=100):
        # split the list into small sublists
        sublists = [list_of_text[i:i + chunk_size] for i in range(0, len(list_of_text), chunk_size)]
        
        results = []
        print(f"Total queries: {len(list_of_text)}, start collecting...")
        
        if self.model in openai_model_list:
            single_query_fn = openai_embed_query
        else:
            raise RuntimeError(f'unsupported error for model {self.model}')

        with ThreadPoolExecutor(max_workers=workers) as executor: # avg. 0.13s per item
            future_results = [executor.submit(single_query_fn, self.client, self.model, p, dim) for p in sublists]
        
            for future in tqdm(as_completed(future_results), total=len(sublists), desc="Processing Items"):
                result = future.result()
                results.append(result)
        return results
