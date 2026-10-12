"""Compile documented guidance into diagrams, never claim a running automation."""
from __future__ import annotations

from .models import WorkflowDefinition

MODEL_PATH = 'knowledge/system/workflow-purpose-model.json'


def _meta(title: str, output: str, repository: dict[str, str]) -> dict:
    return {'title': title, 'locale': 'zh-CN', 'output': output,
            'animation': 'none', 'quality_profile': 'showcase',
            'repository': {**repository, 'provider': 'github', 'link_mode': 'web'}}


def _model_source(workflow: WorkflowDefinition, step_id: str | None = None) -> list[dict]:
    # Lines are attached by the builder from the actual authored model, not guessed.
    return [{'path': MODEL_PATH, 'label': '指导流程定义', 'line': 1}]


def build_archify_candidate(workflow: WorkflowDefinition, repository: dict[str, str]) -> dict:
    positions = {
        'purpose': ('intent', 0), 'trigger': ('intent', 1),
        'input': ('evidence', 1), 'logic': ('evidence', 2),
        'execute': ('execution', 2), 'authorize': ('governance', 2),
        'output': ('governance', 3), 'validate': ('governance', 4),
        'state': ('governance', 5), 'failure': ('execution', 4),
    }
    hints = {'purpose': '目标与停止条件', 'trigger': '当前任务与范围',
             'input': '真实来源与日期', 'logic': '证据决定下一步',
             'execute': '本地准备与草稿', 'authorize': '外部动作须批准',
             'output': '按授权范围执行', 'validate': '核对实际结果',
             'failure': '保留阻塞与原因', 'state': '证据与下一步'}
    nodes = []
    for step in workflow.steps:
        lane, col = positions[step.id]
        nodes.append({'id': f'{workflow.id}-{step.id}', 'lane': lane, 'col': col,
                      'type': 'security' if step.id in {'authorize', 'failure'} else 'database' if step.id == 'state' else 'backend',
                      'label': step.label, 'sublabel': hints[step.id], 'width': 160,
                      'sources': _model_source(workflow, step.id)})
    order = ['purpose', 'trigger', 'input', 'logic', 'execute', 'authorize', 'output', 'validate', 'state']
    edges = []
    for left, right in zip(order, order[1:]):
        edge = {'id': f'{left}-{right}', 'from': f'{workflow.id}-{left}', 'to': f'{workflow.id}-{right}', 'role': 'main'}
        if left == 'authorize':
            edge.update(label='获准或仅草稿', variant='security')
        elif left == 'validate':
            edge.update(label='通过', variant='emphasis')
        edges.append(edge)
    edges.extend([
        {'id': 'approval-blocked', 'from': f'{workflow.id}-authorize', 'to': f'{workflow.id}-failure', 'label': '未获准', 'role': 'error', 'variant': 'security'},
        {'id': 'validation-failed', 'from': f'{workflow.id}-validate', 'to': f'{workflow.id}-failure', 'label': '未通过', 'role': 'error', 'variant': 'security'},
        {'id': 'repair-recheck', 'from': f'{workflow.id}-failure', 'to': f'{workflow.id}-logic', 'label': '补证后重检', 'role': 'return', 'variant': 'dashed'},
    ])
    return {'schema_version': 2, 'diagram_type': 'workflow',
            'meta': _meta(f'{workflow.label} · 指导流程', f'docs/workflows/diagrams/{workflow.id}.html', repository),
            'lanes': [{'id': 'intent', 'label': '目的与触发'}, {'id': 'evidence', 'label': '输入与判断'},
                      {'id': 'execution', 'label': '准备与恢复'}, {'id': 'governance', 'label': '授权、验收与沉淀'}],
            'mainPath': [f'{workflow.id}-{key}' for key in order], 'nodes': nodes, 'edges': edges,
            'cards': [
                {'dot': 'cyan', 'title': '工作目的与底层逻辑', 'items': [workflow.purpose, *workflow.logic]},
                {'dot': 'amber', 'title': '执行与授权', 'items': [step.detail for step in workflow.steps if step.id in {'execute', 'authorize', 'output'}]},
                {'dot': 'emerald', 'title': '输出与验收', 'items': [*workflow.outputs, *workflow.validation]},
                {'dot': 'rose', 'title': '失败与恢复', 'items': list(workflow.failure_modes)},
                {'dot': 'slate', 'title': '完整阶段说明', 'items': [f'{step.label}：{step.detail}' for step in workflow.steps if step.id not in {'execute', 'authorize', 'output'}]},
            ]}


def build_overview_candidate(workflows: tuple[WorkflowDefinition, ...], repository: dict[str, str]) -> dict:
    # Purpose nodes are alternatives chosen by the user, not dependent job stages.
    nodes = []
    edges = []
    lanes = []
    for index, workflow in enumerate(workflows):
        lane = f'purpose-row-{index}'
        lanes.append({'id': lane, 'label': f'{index + 1:02d}'})
        nodes.append({'id': f'purpose-{workflow.id}', 'lane': lane, 'col': 0,
                      'type': 'frontend', 'label': workflow.label, 'sublabel': '按目标选择', 'width': 180,
                      'sources': _model_source(workflow)})
        nodes.append({'id': f'logic-{workflow.id}', 'lane': lane, 'col': 1,
                      'type': 'backend', 'label': '证据与判断', 'sublabel': '输入 / 逻辑 / 草稿', 'width': 160,
                      'sources': _model_source(workflow)})
        nodes.append({'id': f'gate-{workflow.id}', 'lane': lane, 'col': 2,
                      'type': 'security', 'label': '人工授权门', 'sublabel': '外部动作须批准', 'width': 160,
                      'sources': _model_source(workflow)})
        nodes.append({'id': f'result-{workflow.id}', 'lane': lane, 'col': 3,
                      'type': 'database', 'label': '验收与状态', 'sublabel': '失败保留并恢复', 'width': 160,
                      'sources': _model_source(workflow)})
        for left, right in [('purpose','logic'),('logic','gate'),('gate','result')]:
            edge = {'id': f'{workflow.id}-{left}-{right}', 'from': f'{left}-{workflow.id}', 'to': f'{right}-{workflow.id}'}
            if left == 'gate': edge.update(label='获准或仅草稿', variant='security')
            edges.append(edge)
    return {'schema_version': 2, 'diagram_type': 'workflow',
            'meta': _meta('知识库 · 13 类工作目的', 'docs/workflows/diagrams/archify-overview.html', repository),
            'lanes': lanes, 'nodes': nodes, 'edges': edges,
            'semanticChecks': {'allowedRoots': [f'purpose-{w.id}' for w in workflows], 'allowedTerminals': [f'result-{w.id}' for w in workflows]},
            'cards': [{'dot': 'cyan', 'title': '阅读方式', 'items': ['每一行是一种可独立选择的工作目的，不表示上下行之间存在执行依赖。', '交互目录 index.html 提供完整步骤、技能筛选和原文入口。', '这是文档化指导流程，不代表已经运行、发送、发布或部署。']}]}


def attach_model_lines(candidate: dict, model_text: str) -> dict:
    """Bind every diagram node to its exact authored definition in committed JSON."""
    import json
    lines = model_text.splitlines()
    models = json.loads(model_text)
    for node in candidate['nodes']:
        workflow = next(w for w in models if node['id'].startswith(w['id'] + '-') or node['id'].endswith('-' + w['id']))
        start = next(i for i, line in enumerate(lines, 1) if f'"id": "{workflow["id"]}"' in line)
        step_id = node['id'][len(workflow['id'])+1:] if node['id'].startswith(workflow['id'] + '-') else None
        if step_id:
            line = next(i for i in range(start, len(lines)+1) if f'"id":"{step_id}"' in lines[i-1])
        else:
            line = start
        node['sources'] = [{'path': MODEL_PATH, 'line': line, 'end_line': line, 'label': '指导流程定义'}]
    return candidate
