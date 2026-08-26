
项目代码现按用途分为四类：

1. **核心算法**：`src/metabolic_information_mwc/`，包括 PhiID、代谢加权算子、
   DK68 统一分析、认知标注和生物学标注。
2. **第一篇论文正式入口**：列在 `pipeline.json` 中，只包含正文及补充材料实际
   使用的分析。
3. **冻结结果与最终图**：由 `release_inventory.json` 记录相对路径、文件大小和
   SHA-256；图 1 为人工排版图，不由流程重画。
4. **其他项目或探索分析**：ADNI、有向 MwC、动态指标、纵向后果、基因分析和
   指标筛选仍保留在原位置，但不进入第一篇论文发布白名单。

## 统一使用方法

在项目根目录执行：

```bash
export PYTHONPATH="$PWD/src"
python manuscript/paper1/code_release/paper1_pipeline.py check
python manuscript/paper1/code_release/paper1_pipeline.py plan
```

运行某一分析时使用：

```bash
python manuscript/paper1/code_release/paper1_pipeline.py run <阶段名>
```

阶段名包括：

- `auf_high_resolution`
- `harmonized_auf_monash`
- `qnld_replication`
- `metric_specificity`
- `split_half_reliability`
- `metabolic_information_preference`
- `cognitive_complementarity`
- `cognitive_decoding`
- `external_biology`
- `final_figures`

其中耗时分析可先加 `--debug`；若该阶段有轻量模式，统一入口会自动调用其正式
debug 参数。所有日志写入
`results/information_specific_mwc/paper1_release_logs/`，不会覆盖原日志。
