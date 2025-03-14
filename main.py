import json
from tqdm import trange
import argparse
import asyncio
from pypdf import PdfReader
from olmocr.pipeline import build_page_query, PageResult
from olmocr.prompts import PageResponse
from openai import OpenAI
import os

class Config:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.api_key = os.getenv("API_KEY")
        self.model_name = os.getenv("MODEL_NAME")
        self.timeout = 60

def get_client(cfg: Config) -> OpenAI:
    return OpenAI(base_url=cfg.base_url, api_key=cfg.api_key, timeout=cfg.timeout)

async def process_page(cfg: Config, filename: str, page_num: int, client: OpenAI) -> PageResult:
    query = await build_page_query(
        filename, page=1, target_longest_image_dim=1024, target_anchor_text_len=6000
    )
    query["model"] = cfg.model_name
    response = client.chat.completions.create(**query)
    model_obj = json.loads(response.choices[0].message.content)
    page_response = PageResponse(**model_obj)

    return PageResult(
        filename,
        page_num,
        page_response,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        is_fallback=False,
    )


async def main(filename: str):
    cfg = Config()
    client = get_client(cfg)
    reader = PdfReader(filename)
    num_pages = reader.get_num_pages()
    results = []

    for page_num in trange(1, num_pages + 1):
        result = await process_page(cfg, filename, page_num, client)
        results.append(result)

    text = "\n".join([result.response.natural_text for result in results])
    print(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="path to file for reading", type=str)
    args = parser.parse_args()
    asyncio.run(main(args.filename))
