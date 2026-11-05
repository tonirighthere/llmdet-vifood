#!/usr/bin/env python3
"""
scripts/vifood54/strip_lmm.py
=============================
Bỏ phần LLM khỏi checkpoint train có lmm (B5, OV-W, hoặc checkpoint LLMDet công bố) -> detector thuần,
dùng với config không có lmm (vd. ..._b1_od.py) cho mmdet_test.py, eval_grounding.py, eval_ov.py, app.

    python scripts/vifood54/strip_lmm.py IN.pth OUT.pth
"""
from __future__ import annotations

import argparse
import collections

import torch

# Module chỉ tồn tại khi lmm != None (GroundingDINO.__init__, nhánh `if lmm is not None`).
# 'ref_point_head.' cấp cao nhất là MLP của LMM; detector dùng 'decoder.ref_point_head.' nên không bị đụng.
LMM_PREFIXES: tuple[str, ...] = ('lmm.', 'connector.', 'region_connector.', 'image_seperate.', 'img_sep.',
                                 'ref_point_head.')


def strip_lmm(src: str, dst: str) -> None:
    ckpt = torch.load(src, map_location='cpu', weights_only=False)
    state: dict[str, torch.Tensor] = ckpt['state_dict'] if 'state_dict' in ckpt else ckpt
    dropped = collections.Counter(k.split('.')[0] for k in state if k.startswith(LMM_PREFIXES))
    kept = {k: v for k, v in state.items() if not k.startswith(LMM_PREFIXES)}
    if not any(k.startswith('backbone.') for k in kept):
        raise KeyError(f'{src}: không thấy key backbone.* — không phải checkpoint mmdet GroundingDINO')
    out = {'state_dict': kept, 'meta': ckpt.get('meta', {})} if 'state_dict' in ckpt else {'state_dict': kept}
    torch.save(out, dst)
    print(f'{src} -> {dst}: giữ {len(kept)} key, bỏ {sum(dropped.values())} key {dict(dropped)}')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('src')
    p.add_argument('dst')
    a = p.parse_args()
    strip_lmm(a.src, a.dst)
