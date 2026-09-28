import torch
from mmengine.config import Config
from mmengine.runner import Runner
from mmdet.utils import register_all_modules
register_all_modules()

cfg = Config.fromfile('configs/val/grounding_dino_swin_t_vifood_val.py')
cfg.work_dir = 'work_dirs/test_eval'
runner = Runner.from_cfg(cfg)
runner.load_checkpoint('work_dirs/vifood_1k/iter_2000.pth')
dataloader = runner.test_dataloader

for data_batch in dataloader:
    with torch.no_grad():
        outputs = runner.model.test_step(data_batch)
    preds = outputs[0].pred_instances
    print(f'Total predicted: {len(preds)}')
    print(f'Labels: {preds.labels.tolist()}')
    print(f'Scores: {preds.scores.tolist()[:10]}')
    print(f'Label names: {getattr(preds, "label_names", None)}')
    print(f'Text: {data_batch["data_samples"][0].text}')
    print(f'Dataset classes: {len(dataloader.dataset.metainfo["classes"])}')
    break
