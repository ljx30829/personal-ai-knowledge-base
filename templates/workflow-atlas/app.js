(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('atlas-data').textContent);
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const workflowById = new Map(data.workflows.map(w => [w.id, w]));
  const skillById = new Map(data.skills.map(s => [s.id, s]));
  const duplicateIds = new Set(Object.values(data.coverage.duplicate_name_groups).flat());
  const names = {purpose:'目的',logic:'底层判断逻辑',inputs:'输入',outputs:'输出',dependencies:'依赖',validation:'验收',failure_modes:'失败处理',routing_fallback:'分类待复核'};
  let view = 'overview', selectedWorkflow = null, selectedStep = 'purpose';
  let closeTarget = '#overview';
  const field = (title, values) => `<section class="field"><h3>${esc(title)}</h3>${values?.length ? `<ul>${values.map(v => `<li>${esc(v)}</li>`).join('')}</ul>` : '<p class="missing">原文未提取到明确内容，请打开完整原文核对。UNVERIFIED</p>'}</section>`;
  const sourceLink = source => {
    const path = source.path;
    // Only repository-relative file paths are allowed; never interpolate executable URLs.
    if (!path || /^(?:[a-z]+:|\/|\\)/i.test(path) || path.split(/[\\/]/).includes('..')) return '<span>来源路径无效</span>';
    const href = '../../' + path.split('/').map(encodeURIComponent).join('/');
    return `<a class="source-link" href="${href}" target="_blank" rel="noopener">${esc(path)} · L${source.line || 1}${source.end_line ? '–' + source.end_line : ''} ↗</a>`;
  };
  const badge = status => `<span class="badge ${status === 'PASS' ? '' : 'watch'}">${esc(status)}</span>`;
  const matches = skill => {
    const q = $('search').value.trim().toLocaleLowerCase();
    return (!q || [skill.name,skill.purpose,...skill.logic,...skill.workflow_ids.map(id => workflowById.get(id)?.label || '')].join(' ').toLocaleLowerCase().includes(q)) && (!$('status').value || skill.completeness === $('status').value) && (!$('source').value || skill.source === $('source').value) && (!$('duplicates').checked || duplicateIds.has(skill.id));
  };
  const skillCards = skills => skills.length ? `<div class="skill-grid">${skills.map(s => `<button type="button" class="skill-card" data-skill="${esc(s.id)}"><h3>${esc(s.name)}</h3>${badge(s.completeness)}${duplicateIds.has(s.id) ? '<span class="badge">同名多来源</span>' : ''}<p>${esc(s.purpose)}</p><small>${esc(s.source)} · ${esc(s.source_paths[0]?.path || '')}</small></button>`).join('')}</div>` : '<div class="empty">没有匹配的技能。试试清空搜索或重置筛选。</div>';
  function render() {
    $('overview').hidden = view !== 'overview'; $('workflow').hidden = view !== 'workflow'; $('skill-list').hidden = view !== 'skills';
    document.querySelectorAll('[data-view]').forEach(b => b.setAttribute('aria-current', b.dataset.view === (view === 'workflow' ? 'overview' : view) ? 'page' : 'false'));
    const skills = data.skills.filter(matches);
    if (view === 'overview') {
      const workflows = data.workflows.filter(w => skills.some(s => s.workflow_ids.includes(w.id)) || (!$('status').value && !$('source').value && !$('duplicates').checked && [w.label,w.purpose,...w.logic].join(' ').toLocaleLowerCase().includes($('search').value.trim().toLocaleLowerCase())));
      $('result-count').textContent = `${workflows.length} 个工作目的 · ${skills.length} 个匹配技能来源实例`;
      $('overview').innerHTML = workflows.length ? `<div class="grid">${workflows.map(w => `<button type="button" class="purpose-card" data-workflow="${w.id}"><span class="number">${String(data.workflows.indexOf(w)+1).padStart(2,'0')} / 工作目的</span><h3>${esc(w.label)}</h3><p>${esc(w.purpose)}</p><span class="card-foot"><span>${skills.filter(s => s.workflow_ids.includes(w.id)).length} 个匹配技能 · 10 个阶段</span><span>查看流程 →</span></span></button>`).join('')}</div>` : '<div class="empty">没有匹配的工作目的。</div>';
    } else if (view === 'skills') {
      $('result-count').textContent = `${skills.length} / ${data.skills.length} 个技能来源实例。同名不同来源分别保留。`;
      $('skill-list').innerHTML = skillCards(skills);
    } else {
      const w = workflowById.get(selectedWorkflow); if (!w) return;
      const routed = skills.filter(s => s.workflow_ids.includes(w.id));
      $('result-count').textContent = `${w.label} · ${routed.length} 个匹配技能`;
      $('workflow').innerHTML = `<div class="workflow-head"><div><button data-view="overview" type="button">← 返回工作目的</button><h2>${esc(w.label)}</h2></div><a href="diagrams/${w.id}.html">打开 Archify 流程图 ↗</a></div><p class="workflow-purpose">${esc(w.purpose)}</p><div class="fields">${field('触发条件',w.trigger)}${field('输入与证据',w.inputs)}${field('底层判断逻辑',w.logic)}${field('人工授权门',w.approval_gate)}</div><h3>完整工作流程</h3><p class="muted">先准备证据与本地草稿；外部执行经过授权门。验收失败进入恢复，再重新检查。</p><div class="steps">${w.steps.map((s,i) => `<button class="step" type="button" data-step="${s.id}" aria-pressed="${s.id === selectedStep}"><small>${String(i+1).padStart(2,'0')} · ${esc(names[s.id] || ({trigger:'触发',execute:'执行',authorize:'授权',output:'输出',validate:'验收',failure:'失败处理',state:'状态沉淀',input:'输入与证据'})[s.id] || s.id)}</small><strong>${esc(s.label)}</strong></button>`).join('')}</div><div id="step-detail"></div><div class="fields">${field('输出',w.outputs)}${field('验收标准',w.validation)}${field('失败与恢复',w.failure_modes)}${field('状态沉淀',['记录实际完成、证据日期、产物路径、阻塞和下一步；保留 PASS / WATCH / FAIL / BLOCKED / UNVERIFIED 区别。'])}</div><h3>对应技能</h3><p class="muted">按技能名称和简介进行规则路由，可跨多个流程；分类仅作导航，执行前读取原文。</p>${skillCards(routed)}`;
      renderStep();
    }
  }
  function renderStep() {
    const w = workflowById.get(selectedWorkflow); const s = w?.steps.find(s => s.id === selectedStep) || w?.steps[0]; if (!s) return;
    $('step-detail').innerHTML = `<h3>${esc(s.label)}</h3><p>${esc(s.detail)}</p><p>${s.sources.map(sourceLink).join('<br>')}</p>`;
    document.querySelectorAll('[data-step]').forEach(b => b.setAttribute('aria-pressed',b.dataset.step === s.id ? 'true' : 'false'));
  }
  function showSkill(id) {
    const s = skillById.get(id); if (!s) return;
    $('skill-detail').innerHTML = `<h2 id="skill-title">${esc(s.name)}</h2>${badge(s.completeness)}<span class="muted">${esc(s.source)}</span><p>${esc(s.purpose)}</p><p class="muted">此状态只衡量说明字段的提取完整度，未验证该技能在本机或其他电脑的运行结果。</p>${s.missing_fields.length ? `<p class="missing">待核对字段：${s.missing_fields.map(f => esc(names[f] || f)).join('、')}</p>` : ''}<div class="fields">${field('适用时机',s.when_to_use)}${field('输入',s.inputs)}${field('底层逻辑与步骤',s.logic)}${field('输出',s.outputs)}${field('依赖',s.dependencies)}${field('人工授权门',[s.approval_gate])}${field('验收',s.validation)}${field('失败处理',s.failure_modes)}</div><h3>所属工作流程</h3><div class="route-links">${s.workflow_ids.map(w => `<button type="button" data-workflow="${w}">${esc(workflowById.get(w)?.label || w)}</button>`).join('')}</div><h3>来源与完整原文</h3>${s.source_paths.map(sourceLink).join('<br>')}<p class="muted source-link">SHA-256：${esc(s.content_sha256)}</p>`;
    if (!$('skill-dialog').open) $('skill-dialog').showModal();
  }
  function fromHash() {
    const [kind,id] = location.hash.slice(1).split('/');
    if (kind !== 'skill' && $('skill-dialog').open) $('skill-dialog').close();
    if (kind === 'skill' && skillById.has(id)) {render();showSkill(id);return;}
    if (kind === 'workflow' && workflowById.has(id)) {view='workflow';selectedWorkflow=id;selectedStep='purpose';}
    else {view=kind === 'skills' ? 'skills' : 'overview';}
    render();
  }
  document.addEventListener('click', event => {
    const b = event.target.closest('button'); if (!b) return;
    if (b.dataset.view) location.hash=b.dataset.view;
    if (b.dataset.workflow) {location.hash='workflow/'+b.dataset.workflow;}
    if (b.dataset.skill) {closeTarget=location.hash || '#overview';location.hash='skill/'+b.dataset.skill;}
    if (b.dataset.step) {selectedStep=b.dataset.step;renderStep();}
  });
  $('close-dialog').addEventListener('click',() => $('skill-dialog').close());
  $('skill-dialog').addEventListener('close',() => {if (location.hash.startsWith('#skill/')) location.hash=closeTarget;});
  ['search','status','source','duplicates'].forEach(id => $(id).addEventListener(id === 'search' ? 'input' : 'change',render));
  $('reset').addEventListener('click',() => {$('search').value='';$('status').value='';$('source').value='';$('duplicates').checked=false;render();});
  $('source').insertAdjacentHTML('beforeend',[...new Set(data.skills.map(s=>s.source))].sort().map(s=>`<option value="${esc(s)}">${esc(s)}</option>`).join(''));
  $('metrics').innerHTML=`<div class="metric"><strong>${data.workflows.length}</strong><span>工作目的</span></div><div class="metric"><strong>${data.skills.length}</strong><span>技能来源实例</span></div><div class="metric"><strong>${data.coverage.inventory.unique_skill_names}</strong><span>不同名称</span></div>`;
  try {document.documentElement.dataset.theme=localStorage.getItem('atlas-theme') || (matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light');} catch {document.documentElement.dataset.theme='light';}
  $('theme').addEventListener('click',() => {const t=document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';document.documentElement.dataset.theme=t;try {localStorage.setItem('atlas-theme',t);} catch {}});
  window.addEventListener('hashchange',fromHash);fromHash();
})();
