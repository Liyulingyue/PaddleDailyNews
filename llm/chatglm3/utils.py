import os
from typing import Dict, Optional, Union

import torch
from torch.nn import Module
from transformers import AutoModel


def auto_configure_device_map(num_gpus: int) -> Dict[str, int]:
    # transformer.word_embeddings 占用1层
    # transformer.final_layernorm 和 lm_head 占用1层
    # transformer.layers 占用 28 层
    # 总共30层分配到num_gpus张卡上
    num_trans_layers = 28
    per_gpu_layers = 30 / num_gpus

    # bugfix: 在linux中调用torch.embedding传入的weight,input不在同一device上,导致RuntimeError
    # windows下 model.device 会被设置成 transformer.word_embeddings.device
    # linux下 model.device 会被设置成 lm_head.device
    # 在调用chat或者stream_chat时,input_ids会被放到model.device上
    # 如果transformer.word_embeddings.device和model.device不同,则会导致RuntimeError
    # 因此这里将transformer.word_embeddings,transformer.final_layernorm,lm_head都放到第一张卡上
    # 本文件来源于https://github.com/THUDM/ChatGLM-6B/blob/main/utils.py
    # 仅此处做少许修改以支持ChatGLM3
    device_map = {
        "transformer.embedding.word_embeddings": 0,
        "transformer.encoder.final_layernorm": 0,
        "transformer.output_layer": 0,
        "transformer.rotary_pos_emb": 0,
        "lm_head": 0,
    }

    used = 2
    gpu_target = 0
    for i in range(num_trans_layers):
        if used >= per_gpu_layers:
            gpu_target += 1
            used = 0
        assert gpu_target < num_gpus
        device_map[f"transformer.encoder.layers.{i}"] = gpu_target
        used += 1

    return device_map


def load_model_on_gpus(
    checkpoint_path: Union[str, os.PathLike], num_gpus: int = 2, device_map: Optional[Dict[str, int]] = None, **kwargs
) -> Module:
    if num_gpus < 2 and device_map is None:
        model = AutoModel.from_pretrained(checkpoint_path, trust_remote_code=True, **kwargs).half().cuda()
    else:
        from accelerate import dispatch_model

        model = AutoModel.from_pretrained(checkpoint_path, trust_remote_code=True, **kwargs).half()

        if device_map is None:
            device_map = auto_configure_device_map(num_gpus)

        model = dispatch_model(model, device_map=device_map)

    return model


def load_model_cuda(
    model_path,
) -> Module:
    # 获取GPU设备数量
    num_gpu = torch.cuda.device_count()
    # 获取当前使用的GPU索引
    current_gpu_index = torch.cuda.current_device()
    # 获取GPU显存的总量和已使用量
    total_memory = torch.cuda.get_device_properties(current_gpu_index).total_memory / (1024**3)  # 显存总量(GB)
    used_memory = torch.cuda.memory_allocated(current_gpu_index) / (1024**3)  # 已使用显存(GB)
    free_memory = total_memory - used_memory  # 剩余显存(GB)

    isinstance(free_memory, (int, float))
    # TODO: 应该计算每一张卡的显存, 而不是当前卡的显存
    _memory = num_gpu * total_memory

    if num_gpu > 2:
        return load_model_on_gpus(model_path, num_gpu)

    # TODO: 根据显存调节quantize
    if _memory > 13:
        return AutoModel.from_pretrained(model_path, trust_remote_code=True).cuda()

    return AutoModel.from_pretrained(model_path, trust_remote_code=True).quantize(4).cuda()
