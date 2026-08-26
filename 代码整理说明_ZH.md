# 第一篇论文代码整理说明

## 整理结果

本次没有移动、删除或重命名原始分析代码，也没有覆盖冻结结果。新增的
`code_release/` 是第一篇论文的独立索引层，用于把分散在 `src/`、`scripts/`、
`config/`、`results/` 和 `manuscript/` 中的最终代码串成一条可检查、可运行的流程。

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

## 已修复的问题

`make_figure3_reliability_enriched.py` 曾被图 4 绘图代码误覆盖。本次已从此前保存的
完整代码附件恢复图 3 脚本；误覆盖版本保存在
`manuscript/paper1/scripts/archive/`，因此没有删除历史内容。恢复操作不涉及图 1，
也未重新计算或修改任何统计结果。

## 投稿时建议公开的最小集合

- `src/metabolic_information_mwc/` 中本论文涉及的模块；
- `pipeline.json` 列出的正式分析脚本、配置模板和绘图脚本；
- `code_release/` 全部文件；
- 允许公开的去标识化派生表、ROI 元数据和空间置换索引；
- LaTeX、BibTeX、最终矢量图及补充材料；
- 数据访问说明，而不是受限制的原始影像。

不要公开原始受试者影像、账户信息、本机绝对路径、ADNI 下载内容或与本篇论文
无关的大量探索结果。
