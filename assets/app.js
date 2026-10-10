/*
 * 团学投稿平台原型 · 共用交互脚本
 * 页面通过 data-* 属性声明按钮行为，本文件统一实现：
 *   data-href            点击跳转（可配合 data-confirm 二次确认）
 *   data-open / data-close  打开 / 关闭弹窗
 *   data-toast           点击后显示提示
 *   data-action          业务动作：submit / pass / reject / save / save-draft / copy /
 *                        export-csv / export-zip / delete-row / crud-edit / crud-save /
 *                        set-status / read-all / sensitive-test / apply-filter / reset-filter /
 *                        add-chip / batch / staff-manual
 *   data-staff-lookup    人员名单弹窗：输入工号回显姓名、学院、职务
 *   data-person          投稿选人：默认只列本单位名单，输入工号可回显人员库后再选定
 *   data-range           日期区间（xxFrom / xxTo 合成为「开始 至 结束」）
 *   data-show-when       条件显示（例如 identity=学生）
 *   data-when-param      根据网址参数显示（用于跨页面回显处理结果）
 */
(function () {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const params = new URLSearchParams(location.search);
  const DATA = window.TG_DATA || {};
  const host = () => $('.phone') || document.body;
  const isMobile = () => !!$('.phone');

  // 稿件状态与标签颜色的对应关系
  const TAG_CLASS = {
    '草稿': 'tag-gray', '待指导老师审核': 'tag-warn', '待副书记审核': 'tag-warn', '待副职领导审核': 'tag-warn', '待一审': 'tag-warn', '待二审': 'tag-warn',
    '待三审': 'tag-warn', '已退回': 'tag-danger', '已终审采用': 'tag-success', '已终审不采用': 'tag-gray',
    '已发布': 'tag-primary', '无需处理': 'tag-gray', '待跟进': 'tag-warn', '已跟进': 'tag-primary',
    '已转为正式新闻': 'tag-success', '计入采用': 'tag-success', '不计入采用': 'tag-gray',
    '启用': 'tag-success', '停用': 'tag-gray', '在任': 'tag-success', '已离任': 'tag-gray'
  };

  const ICON = {
    success: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    warn: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    danger: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    close: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'
  };

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const now = () => { const d = new Date(); return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`; };

  /* ========== 提示 ========== */
  function toast(msg, type = 'success', ms = 2600) {
    let wrap = $('.toast-wrap', host());
    if (!wrap) { wrap = document.createElement('div'); wrap.className = 'toast-wrap'; host().appendChild(wrap); }
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `${ICON[type] || ICON.info}<span>${esc(msg)}</span>`;
    wrap.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transition = 'opacity .3s'; }, ms);
    setTimeout(() => t.remove(), ms + 300);
  }

  /* ========== 弹窗 ========== */
  function openModal(id) {
    const m = document.getElementById(id);
    if (m) { m.classList.add('open'); const f = $('input,textarea,select', m); if (f && !isMobile()) setTimeout(() => f.focus(), 50); }
  }
  function closeModal(m) { if (m) m.classList.remove('open'); }

  // 动态生成的弹窗（确认框、意见框）
  function buildDialog({ title, bodyHtml, okText = '确定', cancelText = '取消', danger = false, sheet }) {
    const m = document.createElement('div');
    const asSheet = sheet ?? isMobile();
    m.className = `modal open${asSheet ? ' sheet' : ''}`;
    m.innerHTML = `
      <div class="modal-box modal-sm">
        <div class="modal-head"><span>${esc(title)}</span><button class="modal-x" data-dlg="cancel" aria-label="关闭">${ICON.close}</button></div>
        <div class="modal-body">${bodyHtml}</div>
        <div class="modal-foot">
          ${cancelText ? `<button class="btn" data-dlg="cancel">${esc(cancelText)}</button>` : ''}
          <button class="btn ${danger ? 'btn-danger' : 'btn-primary'}" data-dlg="ok">${esc(okText)}</button>
        </div>
      </div>`;
    host().appendChild(m);
    return m;
  }

  function confirmBox(opts) {
    return new Promise((resolve) => {
      const m = buildDialog({ ...opts, bodyHtml: `<p class="dlg-text">${esc(opts.text || '')}</p>` });
      m.addEventListener('click', (e) => {
        const b = e.target.closest('[data-dlg]');
        if (!b && e.target !== m) return;
        m.remove();
        resolve(!!b && b.dataset.dlg === 'ok');
      });
    });
  }

  function alertBox(opts) { return confirmBox({ ...opts, cancelText: '' }); }

  // 审核意见框：required 为 true 时意见必填
  function opinionBox({ title, label = '审核意见', required = true, okText = '确认', danger = false, tplKey = 'review', placeholder }) {
    return new Promise((resolve) => {
      const tpls = (DATA.opinionTemplates || {})[tplKey] || [];
      const m = buildDialog({
        title, okText, danger,
        bodyHtml: `
          <div class="field">
            <label class="lbl ${required ? 'req' : ''}">${esc(label)}</label>
            <textarea class="textarea" maxlength="500" placeholder="${esc(placeholder || (required ? '请填写具体意见，意见将永久保存到稿件档案并通知投稿人' : '选填'))}"></textarea>
            <div class="dlg-row"><span class="field-error hidden">${esc(label)}为必填项，请填写后再提交</span><span class="hint dlg-count">0 / 500</span></div>
          </div>
          ${tpls.length ? `<div class="tpl-title">常用意见模板（点击插入）</div><div class="tpl-list">${tpls.map((t) => `<button type="button" class="tpl-chip">${esc(t)}</button>`).join('')}</div>` : ''}`
      });
      const ta = $('textarea', m), err = $('.field-error', m), cnt = $('.dlg-count', m);
      const sync = () => { cnt.textContent = `${ta.value.length} / 500`; if (ta.value.trim()) { err.classList.add('hidden'); ta.closest('.field').classList.remove('is-error'); } };
      ta.addEventListener('input', sync);
      m.addEventListener('click', (e) => {
        const chip = e.target.closest('.tpl-chip');
        if (chip) { ta.value = ta.value ? `${ta.value}\n${chip.textContent}` : chip.textContent; sync(); return; }
        const b = e.target.closest('[data-dlg]');
        if (!b && e.target !== m) return;
        if (b && b.dataset.dlg === 'ok') {
          if (required && !ta.value.trim()) { err.classList.remove('hidden'); ta.closest('.field').classList.add('is-error'); ta.focus(); return; }
          m.remove(); resolve(ta.value.trim() || '无'); return;
        }
        m.remove(); resolve(null);
      });
      if (!isMobile()) setTimeout(() => ta.focus(), 50);
    });
  }

  /* ========== 跳转 ========== */
  // data-next 中的 {字段名} 会被替换为表单中对应字段的值
  function fillTemplate(url, form) {
    return url.replace(/\{(\w+)\}/g, (_, k) => {
      if (!form) return '';
      const checked = $(`[name="${k}"]:checked`, form);
      const el = checked || $(`[name="${k}"]`, form);
      return encodeURIComponent(el ? el.value : '');
    });
  }
  function go(url, delay = 500) { if (url) setTimeout(() => { location.href = url; }, delay); }

  /* ========== 表单校验 ========== */
  const visible = (el) => !!(el.offsetParent || el.getClientRects().length);

  function setError(el, msg) {
    const field = el.closest('.field') || el.parentElement;
    field.classList.add('is-error');
    let e = $(':scope > .field-error', field);
    if (!e) { e = document.createElement('div'); e.className = 'field-error'; field.appendChild(e); }
    e.textContent = msg;
  }
  function clearError(el) {
    const field = el.closest('.field');
    if (!field) return;
    field.classList.remove('is-error');
    const e = $(':scope > .field-error', field);
    if (e) e.remove();
  }

  function validate(form) {
    let first = null;
    const fail = (el, msg) => { setError(el, msg); if (!first) first = el; };
    $$('.field.is-error', form).forEach((f) => { f.classList.remove('is-error'); const e = $(':scope > .field-error', f); if (e) e.remove(); });

    $$('[required], [data-required]', form).forEach((el) => {
      if (!visible(el) && el.type !== 'radio' && el.type !== 'file') return;
      const name = el.dataset.label || (el.closest('.field') && $('.lbl', el.closest('.field')) ? $('.lbl', el.closest('.field')).textContent.trim() : '此项');
      if (el.type === 'radio') {
        if (!$(`[name="${el.name}"]:checked`, form)) fail(el, `请选择${name}`);
      } else if (el.type === 'file' || el.dataset.minFiles) {
        const box = el.closest('.upload-field');
        if (box && !visible(box)) return;
        const n = box ? $$('.file-item', box).length : 0;
        const min = Number(el.dataset.minFiles || 1);
        if (n < min) fail(el, `请至少上传 ${min} 个文件`);
      } else if (el.isContentEditable) {
        if (el.innerText.trim().length < Number(el.dataset.minLength || 1)) fail(el, `请填写${name}${el.dataset.minLength ? `（不少于 ${el.dataset.minLength} 字）` : ''}`);
      } else if (!String(el.value).trim()) {
        fail(el, el.tagName === 'SELECT' ? `请选择${name}` : `请填写${name}`);
      }
    });

    // 格式校验：手机号、名单内选择
    $$('[data-pattern]', form).forEach((el) => {
      if (!visible(el) || !el.value.trim()) return;
      if (!new RegExp(el.dataset.pattern).test(el.value.trim())) fail(el, el.dataset.patternMsg || '格式不正确');
    });
    $$('[data-person]', form).forEach((el) => {
      if (!visible(el) || !el.value.trim()) return;
      if (el.dataset.picked !== el.value.trim()) {
        const name = el.dataset.label || '此项';
        fail(el, `请从列表中选择${name}，或输入工号后点选；不能手动填写姓名`);
      }
    });

    if (first) {
      const target = first.closest('.field') || first;
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      toast('还有必填项未完成，请检查标红的字段', 'danger');
      return false;
    }
    return true;
  }

  // 日期区间：结束不早于开始，并合成为「开始 至 结束」写入隐藏字段
  function checkRanges(form) {
    let ok = true;
    $$('[data-range]', form).forEach((r) => {
      const k = r.dataset.range;
      const from = $(`[name="${k}From"]`, r).value;
      const to = $(`[name="${k}To"]`, r);
      if (from && to.value && to.value < from) { setError(to, '结束日期不能早于开始日期'); ok = false; return; }
      $(`[name="${k}"]`, r).value = `${from} 至 ${to.value}`;
    });
    if (!ok) toast('任期结束日期不能早于开始日期', 'danger');
    return ok;
  }

  /* ========== 名单表格：新增行、行状态、导入、换届 ========== */
  function addTemplateRow(tbl, tpl, vals) {
    const html = tpl.innerHTML.replace(/\{(\w+)\}/g, (_, k) => esc(vals[k] ?? (k === 'now' ? `2026-09-30 ${now()}` : '')));
    const tb = $('tbody', tbl);
    tb.insertAdjacentHTML('afterbegin', html);
    const row = tb.firstElementChild;
    row.classList.add('is-new');
    return row;
  }
  function setRowStatus(row, v) {
    const tagEl = $('.js-tag', row);
    if (tagEl) { tagEl.textContent = v; tagEl.className = `tag js-tag ${TAG_CLASS[v] || ''}`; }
    const sw = $('.switch', row);
    if (sw) sw.classList.toggle('on', v === '启用' || v === '在任');
    if (row.hasAttribute('data-status')) row.dataset.status = v;
  }
  const cellText = (row, k) => { const c = $(`[data-key="${k}"]`, row); return c ? c.textContent.trim() : ''; };
  const liveRows = (tbl) => $$('tbody tr', tbl).filter((r) => !r.classList.contains('empty-row') && !r.classList.contains('removed'));
  const dayBefore = (d) => { const t = new Date(`${d}T00:00:00Z`); t.setUTCDate(t.getUTCDate() - 1); return t.toISOString().slice(0, 10); };

  function parseCsv(text) {
    const rows = [];
    let row = [], cell = '', q = false;
    const s = text.replace(/^\ufeff/, '');
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (q) {
        if (c === '"' && s[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c;
      } else if (c === '"') q = true;
      else if (c === ',') { row.push(cell); cell = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && s[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
      else cell += c;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    return rows.filter((r) => r.some((x) => x.trim()));
  }

  const IMPORT_COLS = { name: ['姓名'], no: ['工号'], college: ['所在学院', '学院', '所属学院', '所属部门', '部门'], duty: ['职务'], from: ['任期开始', '任期开始日期'], to: ['任期结束', '任期结束日期'] };
  const IMPORT_LBL = { name: '姓名', no: '工号', college: '所在学院', duty: '职务', from: '任期开始', to: '任期结束' };
  async function readImport(input) {
    const modal = input.closest('.modal');
    const box = $('[data-import-preview]', modal);
    const file = input.files[0];
    input.value = '';
    modal._import = null;
    if (!file) return;
    $('[data-import-name]', modal).textContent = file.name;
    const bad = (msg) => { box.innerHTML = `<div class="notice notice-danger">${ICON.danger}<div>${msg}</div></div>`; };
    if (!/\.csv$/i.test(file.name)) { bad('仅支持 .csv 文件，请使用导入模板填写后上传'); return; }
    const rows = parseCsv(await file.text());
    const head = (rows.shift() || []).map((h) => h.trim());
    const idx = {};
    Object.entries(IMPORT_COLS).forEach(([k, names]) => { idx[k] = head.findIndex((h) => names.includes(h)); });
    const unit = input.dataset.unitLabel || '所在学院';
    const missCols = Object.keys(idx).filter((k) => idx[k] < 0).map((k) => (k === 'college' ? unit : IMPORT_LBL[k]));
    if (missCols.length) { bad(`表头缺少：${esc(missCols.join('、'))}。请下载导入模板，按模板列填写`); return; }
    if (!rows.length) { bad('文件中没有数据行'); return; }
    const have = new Set(liveRows($(input.dataset.table)).map((r) => cellText(r, 'no')));
    const seen = new Set();
    const date = /^\d{4}-\d{2}-\d{2}$/;
    const items = rows.map((r, i) => {
      const v = {};
      Object.keys(idx).forEach((k) => { v[k] = (r[idx[k]] || '').trim(); });
      const miss = Object.keys(IMPORT_LBL).filter((k) => !v[k]);
      let st = 'ok', msg = '可导入';
      if (miss.length) { st = 'skip'; msg = `缺少${miss.map((k) => (k === 'college' ? unit : IMPORT_LBL[k])).join('、')}`; }
      else if (have.has(v.no)) { st = 'skip'; msg = '工号重复（已在名单中）'; }
      else if (seen.has(v.no)) { st = 'skip'; msg = '工号重复（文件内重复）'; }
      else if (!date.test(v.from) || !date.test(v.to) || v.to <= v.from) { st = 'skip'; msg = '任期日期有误'; }
      if (v.no) seen.add(v.no);
      return { line: i + 2, v, st, msg };
    });
    modal._import = items;
    const okN = items.filter((x) => x.st === 'ok').length;
    const trs = items.map(({ line, v, st, msg }) => `<tr><td>${line}</td><td>${esc(v.name) || '—'}</td><td>${esc(v.no) || '—'}</td><td>${esc(v.college) || '—'}</td><td>${esc(v.duty) || '—'}</td>`
      + `<td class="nowrap">${v.from || v.to ? `${esc(v.from)} 至 ${esc(v.to)}` : '—'}</td><td><span class="tag ${st === 'ok' ? 'tag-success' : 'tag-danger'}">${esc(msg)}</span></td></tr>`).join('');
    box.innerHTML = `<div class="import-sum"><b>预览校验结果</b><span>共 ${items.length} 行</span><span class="c-success">可导入 ${okN} 行</span><span class="c-danger">将跳过 ${items.length - okN} 行</span></div>`
      + `<div class="table-wrap"><table class="tbl"><thead><tr><th>行号</th><th>姓名</th><th>工号</th><th>${esc(unit)}</th><th>职务</th><th>任期</th><th>校验结果</th></tr></thead><tbody>${trs}</tbody></table></div>`;
  }

  function termMark(c) {
    const item = c.closest('.term-item');
    item.classList.toggle('leave', !c.checked);
    const tg = $('[data-term-tag]', item);
    tg.textContent = c.checked ? '续任' : '离任';
    tg.className = `tag ${c.checked ? 'tag-success' : 'tag-gray'}`;
  }
  function termSum(modal) {
    const keeps = $$('[data-term-keep]', modal);
    const k = keeps.filter((c) => c.checked).length;
    $('[data-term-sum]', modal).textContent = keeps.length ? `在任 ${keeps.length} 人 · 续任 ${k} 人 · 离任 ${keeps.length - k} 人` : '';
    const all = $('[data-term-all]', modal);
    if (keeps.length) { all.checked = k === keeps.length; all.indeterminate = k > 0 && k < keeps.length; }
  }

  /* ========== 人员名单：按工号回显 ========== */
  function staffDir() {
    const seen = new Set();
    return [...(DATA.staff || []), ...(DATA.teachers || [])].filter((p) => !seen.has(p.no) && seen.add(p.no));
  }
  function staffShowMore(modal, show) { $$('.js-staff-more', modal).forEach((f) => f.classList.toggle('hidden', !show)); }
  function staffMsg(modal, html, cls = '') {
    const m = $('[data-staff-msg]', modal);
    if (m) { m.innerHTML = html; m.className = cls; }
  }
  function staffReset(modal, edit) {
    modal._echo = null;
    const input = $('[data-staff-lookup]', modal);
    input._last = `${input.value.trim()}!`;
    staffShowMore(modal, edit);
    const m = $('[data-staff-msg]', modal);
    staffMsg(modal, edit ? '修改工号可重新回显人员信息，也可直接修改下方信息' : esc(m.dataset.defaultMsg));
    $$('.staff-picker .picker-list', modal).forEach((l) => l.classList.remove('open'));
  }
  function staffInTable(modal, no) {
    const save = $('[data-action="crud-save"]', modal);
    const tbl = save && $(save.dataset.table);
    return tbl && $$('tbody tr', tbl).some((r) => r !== modal._row && r.style.display !== 'none' && ($('[data-key="no"]', r) || {}).textContent === no);
  }
  function staffFill(modal, p) {
    const set = (name, v) => { const el = $(`[name="${name}"]`, modal); if (el) { el.value = v; clearError(el); } };
    set('no', p.no); set('name', p.name); set('college', p.college); set('duty', p.title); set('title', p.title);
    modal._echo = p.no;
    $('[data-staff-lookup]', modal)._last = `${p.no}!`;
    staffShowMore(modal, true);
    $$('.staff-picker .picker-list', modal).forEach((l) => l.classList.remove('open'));
    if (staffInTable(modal, p.no)) staffMsg(modal, `工号 ${esc(p.no)}（${esc(p.name)}）已在名单中，保存将新增一条重复记录`, 'c-warn');
    else staffMsg(modal, `已按工号回显：<b>${esc(p.name)}</b> · ${esc(p.college)} · ${esc(p.title)}，信息可修改`, 'c-success');
  }
  function staffLookup(input, final) {
    const modal = input.closest('.modal');
    const v = input.value.trim();
    const key = `${v}${final ? '!' : ''}`;
    if (input._last === key || input._last === `${v}!`) return;
    input._last = key;
    const dir = staffDir();
    const hit = dir.find((p) => p.no === v);
    if (hit) { if (modal._echo !== hit.no) staffFill(modal, hit); return; }
    if (modal._echo) {
      ['name', 'college', 'duty', 'title'].forEach((n) => { const el = $(`[name="${n}"]`, modal); if (el) el.value = ''; });
      modal._echo = null;
    }
    if (!v) { staffMsg(modal, esc($('[data-staff-msg]', modal).dataset.defaultMsg)); return; }
    const partial = dir.some((p) => p.no.startsWith(v) || p.name.includes(v));
    if (final || !partial) {
      staffShowMore(modal, true);
      staffMsg(modal, `人员库中未找到工号「${esc(v)}」，请手动填写姓名、学院、职务后保存`, 'c-warn');
    }
  }
  function renderStaffPicker(input) {
    const list = $('.picker-list', input.closest('.staff-picker'));
    const k = input.value.trim();
    const items = k ? staffDir().filter((p) => p.no.includes(k) || p.name.includes(k)).slice(0, 8) : [];
    if (!items.length || (items.length === 1 && items[0].no === k)) { list.classList.remove('open'); return; }
    list.innerHTML = items.map((p) => `<div class="picker-item" data-no="${esc(p.no)}"><b>${esc(p.no)} · ${esc(p.name)}</b><span>${esc(p.college)} · ${esc(p.title)}</span></div>`).join('');
    list.classList.add('open');
  }

  /* ========== 敏感词检测 ========== */
  function detectSensitive(text, mode = 'exact') {
    const s = DATA.sensitive || { high: [], low: [], white: [], variants: {} };
    let src = text;
    s.white.forEach((w) => { src = src.split(w).join('　'.repeat(w.length)); });
    const hits = [];
    const scan = (words, level) => words.forEach((w) => {
      const forms = [w];
      if (mode === 'semantic' && s.variants[w]) forms.push(...s.variants[w]);
      forms.forEach((f) => { if (src.toLowerCase().includes(f.toLowerCase())) hits.push({ word: f, origin: w, level }); });
    });
    scan(s.high, 'high');
    scan(s.low, 'low');
    return hits;
  }
  function highlight(text, hits) {
    let html = esc(text);
    hits.forEach((h) => { html = html.split(esc(h.word)).join(`<mark class="${h.level}">${esc(h.word)}</mark>`); });
    return html;
  }

  /* ========== 表格：筛选 / 搜索 / 排序 / 分页 ========== */
  const tables = {};

  function initTable(tbl) {
    const id = tbl.id;
    const state = { page: 1, size: Number(tbl.dataset.pageSize || 15), tab: null };
    tables[id] = state;
    $$('th[data-sort]', tbl).forEach((th, i) => {
      th.classList.add('sortable');
      th.addEventListener('click', () => sortTable(tbl, th));
    });
    renderTable(tbl);
  }

  function rowMatches(tr, tbl) {
    if (tr.classList.contains('removed') || tr.dataset.hiddenByParam) return false;
    const st = tables[tbl.id];
    if (st.tab && st.tab.key && st.tab.value && !String(tr.dataset[st.tab.key] || '').split(',').includes(st.tab.value)) return false;
    let ok = true;
    $$(`[data-filter][data-for="${tbl.id}"]`).forEach((f) => {
      const v = f.value.trim();
      if (!v) return;
      const key = f.dataset.filter;
      if (key === 'keyword') { if (!tr.textContent.toLowerCase().includes(v.toLowerCase())) ok = false; }
      else if (f.hasAttribute('data-contains')) { if (!String(tr.dataset[key] || '').toLowerCase().includes(v.toLowerCase())) ok = false; }
      else if (key === 'dateFrom') { if ((tr.dataset.date || '') < v) ok = false; }
      else if (key === 'dateTo') { if ((tr.dataset.date || '') > v) ok = false; }
      else if (!String(tr.dataset[key] || '').split(',').includes(v)) ok = false;
    });
    return ok;
  }

  function renderTable(tbl) {
    const st = tables[tbl.id];
    const rows = $$('tbody tr:not(.empty-row)', tbl);
    const matched = rows.filter((r) => rowMatches(r, tbl));
    const pages = Math.max(1, Math.ceil(matched.length / st.size));
    if (st.page > pages) st.page = pages;
    rows.forEach((r) => { r.style.display = 'none'; });
    matched.slice((st.page - 1) * st.size, st.page * st.size).forEach((r) => { r.style.display = ''; });
    matched.forEach((r, i) => { const n = $('td.seq', r); if (n) n.textContent = i + 1; });

    let empty = $('tbody .empty-row', tbl);
    if (!matched.length) {
      if (!empty) {
        empty = document.createElement('tr');
        empty.className = 'empty-row';
        empty.innerHTML = `<td colspan="${$$('thead th', tbl).length}"><div class="empty">暂无符合条件的数据，试试调整筛选条件</div></td>`;
        $('tbody', tbl).appendChild(empty);
      }
      empty.style.display = '';
    } else if (empty) empty.style.display = 'none';

    $$(`[data-total-for="${tbl.id}"]`).forEach((el) => { el.textContent = matched.length; });
    const pager = $(`[data-pager-for="${tbl.id}"]`);
    if (pager) {
      let html = `<span>共 ${matched.length} 条</span><button data-pg="prev" ${st.page === 1 ? 'disabled' : ''}>‹</button>`;
      for (let i = 1; i <= pages; i++) html += `<button data-pg="${i}" class="${i === st.page ? 'on' : ''}">${i}</button>`;
      html += `<button data-pg="next" ${st.page === pages ? 'disabled' : ''}>›</button><select class="select pg-size">${[...new Set([st.size, 15, 30, 50])].sort((a, b) => a - b).map((n) => `<option value="${n}" ${n === st.size ? 'selected' : ''}>${n}条/页</option>`).join('')}</select>`;
      pager.innerHTML = html;
      pager.onclick = (e) => {
        const b = e.target.closest('[data-pg]');
        if (!b || b.disabled) return;
        const v = b.dataset.pg;
        st.page = v === 'prev' ? st.page - 1 : v === 'next' ? st.page + 1 : Number(v);
        renderTable(tbl);
      };
      $('.pg-size', pager).onchange = (e) => { st.size = Number(e.target.value); st.page = 1; renderTable(tbl); };
    }
  }

  function sortTable(tbl, th) {
    const idx = Array.from(th.parentNode.children).indexOf(th);
    const asc = th.dataset.dir !== 'asc';
    $$('th', tbl).forEach((t) => delete t.dataset.dir);
    th.dataset.dir = asc ? 'asc' : 'desc';
    const body = $('tbody', tbl);
    const rows = $$('tr:not(.empty-row)', body);
    const val = (r) => { const c = r.children[idx]; const t = (c && (c.dataset.value || c.textContent) || '').trim(); const n = parseFloat(t.replace(/[^\d.-]/g, '')); return isNaN(n) || /[\u4e00-\u9fa5]{2,}/.test(t) && !c.dataset.value ? t : n; };
    rows.sort((a, b) => { const x = val(a), y = val(b); return (x > y ? 1 : x < y ? -1 : 0) * (asc ? 1 : -1); });
    rows.forEach((r) => body.appendChild(r));
    renderTable(tbl);
    toast(`已按「${th.textContent.trim()}」${asc ? '升序' : '降序'}排列`, 'info', 1500);
  }

  function refreshTableOf(el) {
    const tbl = el.closest('table[data-table]');
    if (tbl) renderTable(tbl);
    updateCounts();
  }

  function updateCounts() {
    $$('[data-count-of]').forEach((el) => {
      const tbl = document.getElementById(el.dataset.countOf);
      if (tbl) el.textContent = $$('tbody tr:not(.empty-row):not(.removed)', tbl).filter((r) => !r.dataset.hiddenByParam).length;
    });
  }

  /* ========== CSV / ZIP 导出 ========== */
  function download(name, blob) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  function tableToCsv(tbl) {
    const cols = $$('thead th', tbl).map((th, i) => ({ i, skip: th.classList.contains('no-export') || th.querySelector('input') }));
    const line = (cells) => cells.filter((_, i) => !cols[i] || !cols[i].skip).map((c) => `"${c.textContent.replace(/\s+/g, ' ').trim().replace(/"/g, '""')}"`).join(',');
    const rows = [line($$('thead th', tbl))];
    $$('tbody tr', tbl).forEach((r) => { if (!r.classList.contains('empty-row') && !r.classList.contains('removed') && !r.dataset.hiddenByParam && (tables[tbl.id] ? rowMatches(r, tbl) : true)) rows.push(line(Array.from(r.children))); });
    return rows.join('\r\n');
  }

  // 极简 ZIP 打包（仅存储、不压缩），用于演示素材包的真实下载
  const CRC_TABLE = (() => { const t = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  const crc32 = (buf) => { let c = 0xFFFFFFFF; for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
  function makeZip(files) {
    const enc = new TextEncoder();
    const parts = [], central = [];
    let offset = 0;
    files.forEach((f) => {
      const name = enc.encode(f.name);
      const data = typeof f.data === 'string' ? enc.encode(f.data) : f.data;
      const crc = crc32(data);
      const head = new DataView(new ArrayBuffer(30));
      head.setUint32(0, 0x04034b50, true); head.setUint16(4, 20, true); head.setUint16(6, 0x0800, true);
      head.setUint32(14, crc, true); head.setUint32(18, data.length, true); head.setUint32(22, data.length, true);
      head.setUint16(26, name.length, true);
      parts.push(new Uint8Array(head.buffer), name, data);
      const cd = new DataView(new ArrayBuffer(46));
      cd.setUint32(0, 0x02014b50, true); cd.setUint16(4, 20, true); cd.setUint16(6, 20, true); cd.setUint16(8, 0x0800, true);
      cd.setUint32(16, crc, true); cd.setUint32(20, data.length, true); cd.setUint32(24, data.length, true);
      cd.setUint16(28, name.length, true); cd.setUint32(42, offset, true);
      central.push(new Uint8Array(cd.buffer), name);
      offset += 30 + name.length + data.length;
    });
    const cdSize = central.reduce((s, p) => s + p.length, 0);
    const end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true);
    end.setUint32(12, cdSize, true); end.setUint32(16, offset, true);
    return new Blob([...parts, ...central, new Uint8Array(end.buffer)], { type: 'application/zip' });
  }

  async function fetchImage(url) {
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 5000);
      const res = await fetch(url, { signal: ctrl.signal });
      clearTimeout(timer);
      if (!res.ok) return null;
      return new Uint8Array(await res.arrayBuffer());
    } catch (e) { return null; }
  }

  /* ========== 业务动作 ========== */
  const actions = {
    // 提交表单：校验 → 敏感词检测 → 二次确认 → 跳转
    async submit(btn) {
      const form = btn.dataset.form ? $(btn.dataset.form) : btn.closest('form');
      if (form && !validate(form)) return;
      if (btn.dataset.sensitive) {
        const text = btn.dataset.sensitive.split(',').map((s) => { const el = $(s); return el ? (el.value ?? '') + (el.isContentEditable ? el.innerText : '') : ''; }).join('\n');
        const hits = detectSensitive(text, 'semantic');
        const high = hits.filter((h) => h.level === 'high'), low = hits.filter((h) => h.level === 'low');
        if (high.length) {
          await alertBox({ title: '检测到高危敏感词，无法提交', text: `稿件中包含高危敏感词：${[...new Set(high.map((h) => h.word))].join('、')}。请修改后再提交。`, okText: '去修改', danger: true });
          return;
        }
        if (low.length && !(await confirmBox({ title: '检测到低危敏感词', text: `稿件中包含低危敏感词：${[...new Set(low.map((h) => h.word))].join('、')}。建议修改后提交，是否仍要继续？`, okText: '仍然提交' }))) return;
      }
      if (btn.dataset.confirm && !(await confirmBox({ title: btn.dataset.confirmTitle || '确认提交', text: btn.dataset.confirm }))) return;
      toast(btn.dataset.msg || '提交成功');
      go(fillTemplate(btn.dataset.next || '', form), 700);
    },

    // 审核通过 / 终审采用：可选填意见
    async pass(btn) {
      const needOpinion = btn.dataset.opinion;
      if (needOpinion) {
        const op = await opinionBox({ title: btn.dataset.title || '审核通过', required: needOpinion === 'required', okText: btn.dataset.ok || '确认通过', tplKey: `${btn.dataset.tpl || 'review'}Pass`, label: btn.dataset.label || '审核意见' });
        if (op === null) return;
      } else if (btn.dataset.confirm && !(await confirmBox({ title: btn.dataset.title || '确认操作', text: btn.dataset.confirm }))) return;
      toast(btn.dataset.msg || '操作成功，稿件已流转至下一环节');
      go(btn.dataset.next, 700);
    },

    // 退回 / 终审不采用：意见必填
    async reject(btn) {
      const op = await opinionBox({ title: btn.dataset.title || '退回稿件', label: btn.dataset.label || '退回意见', required: true, okText: btn.dataset.ok || '确认退回', danger: true, tplKey: btn.dataset.tpl || 'review' });
      if (op === null) return;
      toast(btn.dataset.msg || '已退回，系统已通知投稿人', 'warn');
      go(btn.dataset.next, 800);
    },

    async save(btn) {
      const modalEl = btn.closest('.modal');
      const form = btn.dataset.form ? $(btn.dataset.form) : (btn.closest('form') || (modalEl && $('form', modalEl)));
      if (form && (!validate(form) || !checkRanges(form))) return;
      if (btn.dataset.confirm && !(await confirmBox({ title: '确认保存', text: btn.dataset.confirm }))) return;
      toast(btn.dataset.msg || '保存成功，已记入操作日志');
      const m = btn.closest('.modal');
      if (m && !btn.dataset.keep) closeModal(m);
      if (btn.dataset.next) go(btn.dataset.next, 700);
    },

    'save-draft'(btn) {
      $$('[data-draft-status]').forEach((el) => { el.innerHTML = `<i class="dot-ok"></i>草稿已保存于 ${now()}`; });
      toast('草稿已保存，可在“我的投稿 · 草稿”中继续编辑');
      if (btn.dataset.next) go(btn.dataset.next, 800);
    },

    async copy(btn) {
      const el = btn.dataset.target && $(btn.dataset.target);
      const text = btn.dataset.text || (el ? (el.value ?? el.innerText) : '');
      try { await navigator.clipboard.writeText(text); }
      catch (e) { const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
      toast(btn.dataset.msg || '已复制到剪贴板，复制行为已记入操作日志');
      if (btn.dataset.log) addLog(btn.dataset.log);
    },

    'export-csv'(btn) {
      const tbl = $(btn.dataset.table);
      const fmt = btn.dataset.format || 'CSV';
      const csv = tbl ? tableToCsv(tbl) : (btn.dataset.csv || '').replace(/\\n/g, '\r\n');
      download(`${btn.dataset.filename || '导出数据'}.csv`, new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }));
      toast(`${fmt === 'Excel' ? 'Excel 表格' : 'CSV 文件'}已开始下载，导出行为已记入操作日志`);
      if (btn.dataset.log) addLog(btn.dataset.log);
      if (!btn.dataset.keep) closeModal(btn.closest('.modal[id]'));
    },

    async 'export-zip'(btn) {
      const folder = btn.dataset.folder || '新闻素材包';
      const body = $(btn.dataset.target);
      const images = (btn.dataset.images || '').split('|').filter(Boolean);
      const old = btn.innerHTML;
      btn.disabled = true; btn.innerHTML = '正在打包原图…';
      const files = [{ name: `${folder}/新闻正文.txt`, data: body ? body.innerText : '' }];
      let fail = 0;
      for (let i = 0; i < images.length; i++) {
        const data = await fetchImage(images[i]);
        if (data) files.push({ name: `${folder}/images/图片${i + 1}.jpg`, data });
        else fail++;
      }
      if (fail) files.push({ name: `${folder}/images/原图下载说明.txt`, data: `有 ${fail} 张原图因网络原因未能打包（原型演示环境），正式系统将直接打包服务器上的原始图片文件。\n\n${images.join('\n')}` });
      download(`${folder}.zip`, makeZip(files));
      btn.disabled = false; btn.innerHTML = old;
      toast('素材包已开始下载，导出行为已记入操作日志');
      if (btn.dataset.log) addLog(btn.dataset.log);
    },

    async 'delete-row'(btn) {
      const row = btn.closest('tr, [data-row]');
      if (!(await confirmBox({ title: '确认删除', text: btn.dataset.confirm || '删除后不可恢复，确认删除吗？', okText: '删除', danger: true }))) return;
      row.classList.add('removed');
      row.style.display = 'none';
      refreshTableOf(btn);
      toast(btn.dataset.msg || '已删除，操作已记入日志');
    },

    // 编辑行：把行内 data-key 单元格的内容填入弹窗表单
    'crud-edit'(btn) {
      const row = btn.closest('tr, [data-row]');
      const modal = document.getElementById(btn.dataset.modal);
      if (!modal) return;
      modal._row = row;
      $('.modal-head span', modal).textContent = btn.dataset.title || '编辑';
      $$('[name]', modal).forEach((f) => {
        const cell = row ? $(`[data-key="${f.name}"]`, row) : null;
        const v = cell ? (cell.dataset.value ?? cell.textContent.trim()) : '';
        if (f.type === 'radio') f.checked = f.value === v;
        else f.value = v;
      });
      $$('[data-range]', modal).forEach((r) => {
        const [from, to] = $(`[name="${r.dataset.range}"]`, r).value.split(' 至 ');
        $(`[name="${r.dataset.range}From"]`, r).value = from || '';
        $(`[name="${r.dataset.range}To"]`, r).value = to || '';
      });
      if ($('[data-staff-lookup]', modal)) staffReset(modal, true);
      openModal(btn.dataset.modal);
    },

    // 新增行：清空弹窗表单
    'crud-add'(btn) {
      const modal = document.getElementById(btn.dataset.modal);
      modal._row = null;
      $('.modal-head span', modal).textContent = btn.dataset.title || '新增';
      $$('[name]', modal).forEach((f) => { if (f.type === 'radio') f.checked = f.defaultChecked; else f.value = f.dataset.default || ''; });
      $$('.field.is-error', modal).forEach((el) => { el.classList.remove('is-error'); const e = $(':scope > .field-error', el); if (e) e.remove(); });
      if ($('[data-staff-lookup]', modal)) staffReset(modal, false);
      openModal(btn.dataset.modal);
    },

    // 人员名单导出：按当前筛选结果，任期拆为开始 / 结束两列
    'export-staff'(btn) {
      const tbl = $(btn.dataset.table);
      const rows = liveRows(tbl).filter((r) => rowMatches(r, tbl));
      const q = (x) => `"${String(x).replace(/"/g, '""')}"`;
      const lines = [`姓名,工号,${btn.dataset.unitLabel || '所在学院'},职务,任期开始,任期结束,状态,累计审核`];
      rows.forEach((r) => {
        const [from, to] = cellText(r, 'term').split(' 至 ');
        lines.push([cellText(r, 'name'), cellText(r, 'no'), cellText(r, 'college'), cellText(r, 'duty'), from || '', to || '',
          ($('.js-tag', r) || {}).textContent || '', cellText(r, 'count')].map(q).join(','));
      });
      download(`${btn.dataset.filename || '人员名单'}.csv`, new Blob(['\ufeff' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' }));
      toast(`已导出 ${rows.length} 名人员（按当前筛选条件），导出行为已记入操作日志`);
    },

    // 人员名单导入：打开时清空上次的预览
    'staff-import-open'(btn) {
      const modal = document.getElementById(btn.dataset.modal);
      modal._import = null;
      $('[data-import-preview]', modal).innerHTML = '';
      $('[data-import-name]', modal).textContent = '选择填写好的 CSV 文件';
      openModal(btn.dataset.modal);
    },

    'staff-import'(btn) {
      const modal = btn.closest('.modal');
      const items = modal._import;
      if (!items) { toast('请先选择要导入的 CSV 文件', 'warn'); return; }
      const tbl = $(btn.dataset.table);
      const have = new Set(liveRows(tbl).map((r) => cellText(r, 'no')));
      const ok = items.filter((x) => x.st === 'ok' && !have.has(x.v.no));
      const skip = items.length - ok.length;
      if (!ok.length) { toast(`没有可导入的数据，${skip} 行均已跳过`, 'warn'); return; }
      const tpl = $(btn.dataset.template);
      ok.slice().reverse().forEach(({ v }) => addTemplateRow(tbl, tpl, { name: v.name, no: v.no, college: v.college, duty: v.duty, term: `${v.from} 至 ${v.to}` }));
      closeModal(modal);
      refreshTableOf($('tbody', tbl));
      toast(`导入完成：新增 ${ok.length} 人，跳过 ${skip} 行`);
    },

    // 学年换届：列出在任人员，勾选续任、取消勾选离任
    'term-open'(btn) {
      const modal = document.getElementById(btn.dataset.modal);
      const rows = liveRows($(btn.dataset.table)).filter((r) => r.dataset.status === '在任');
      modal._rows = rows;
      $$('[data-range] input[type=date]', modal).forEach((i) => { i.value = i.dataset.default || ''; });
      $$('.field.is-error', modal).forEach((el) => { el.classList.remove('is-error'); const er = $(':scope > .field-error', el); if (er) er.remove(); });
      $('[data-term-list]', modal).innerHTML = rows.length ? rows.map((r, i) => `<label class="term-item"><input type="checkbox" data-term-keep data-i="${i}" checked>`
        + `<span><b>${esc(cellText(r, 'name'))}</b><div class="t-sub">工号 ${esc(cellText(r, 'no'))}</div></span>`
        + `<span>${esc(cellText(r, 'college'))}<div class="t-sub">${esc(cellText(r, 'duty'))}</div></span>`
        + `<span class="t-sub">现任期<br>${esc(cellText(r, 'term'))}</span><span class="tag tag-success" data-term-tag>续任</span></label>`).join('')
        : '<div class="term-empty">当前名单中没有在任人员，无需换届</div>';
      const all = $('[data-term-all]', modal);
      all.checked = true; all.disabled = !rows.length;
      termSum(modal);
      openModal(btn.dataset.modal);
    },

    async 'term-apply'(btn) {
      const modal = btn.closest('.modal');
      const rows = modal._rows || [];
      if (!rows.length) { toast('当前名单中没有在任人员，无需换届', 'warn'); return; }
      if (!validate($('form', modal))) return;
      const from = $('[name="newTermFrom"]', modal).value;
      const toEl = $('[name="newTermTo"]', modal);
      if (toEl.value <= from) { setError(toEl, '结束日期须晚于开始日期'); toast('新任期结束日期须晚于开始日期', 'danger'); return; }
      const keeps = $$('[data-term-keep]', modal);
      const keepN = keeps.filter((c) => c.checked).length;
      const leaveN = keeps.length - keepN;
      if (!(await confirmBox({ title: '确认换届', text: `新任期 ${from} 至 ${toEl.value}：续任 ${keepN} 人，离任 ${leaveN} 人。离任人员将停用账号并收回审核权限，确认执行吗？`, okText: '确认换届', danger: leaveN > 0 }))) return;
      const prev = dayBefore(from);
      keeps.forEach((c) => {
        const r = rows[Number(c.dataset.i)];
        const cell = $('[data-key="term"]', r);
        if (c.checked) { cell.textContent = `${from} 至 ${toEl.value}`; setRowStatus(r, '在任'); }
        else { const start = cell.textContent.split(' 至 ')[0]; cell.textContent = `${start} 至 ${prev < start ? start : prev}`; setRowStatus(r, '已离任'); }
        r.classList.add('is-new');
        setTimeout(() => r.classList.remove('is-new'), 3000);
      });
      closeModal(modal);
      refreshTableOf($('tbody', $(btn.dataset.table)));
      toast(`换届完成：续任 ${keepN} 人，离任 ${leaveN} 人`);
    },

    // 人员名单：工号库中没有的人员，展开姓名、学院、职务手动填写
    'staff-manual'(btn) {
      const modal = btn.closest('.modal');
      staffShowMore(modal, true);
      staffMsg(modal, '已切换为手动填写，请补充姓名、学院、职务和任期');
      const name = $('[name="name"]', modal);
      if (name) name.focus();
    },

    // 保存弹窗：编辑时更新原行，新增时按 <template> 插入新行
    'crud-save'(btn) {
      const modal = btn.closest('.modal');
      const form = $('form', modal) || modal;
      const lookup = $('[data-staff-lookup]', form);
      if (lookup && lookup.value.trim() && $('.js-staff-more.hidden', form)) staffLookup(lookup, true);
      if (!validate(form)) return;
      if (!checkRanges(form)) return;
      const vals = {};
      $$('[name]', form).forEach((f) => { if (f.type !== 'radio' || f.checked) vals[f.name] = f.value.trim(); });
      let row = modal._row;
      if (!row) {
        row = addTemplateRow($(btn.dataset.table), $(btn.dataset.template), vals);
      } else {
        Object.entries(vals).forEach(([k, v]) => {
          if (row.hasAttribute(`data-${k}`)) row.dataset[k] = v;
          const cell = $(`[data-key="${k}"]`, row);
          if (!cell) return;
          if (cell.classList.contains('tag')) { cell.className = `tag ${TAG_CLASS[v] || 'tag-primary'}`; }
          cell.textContent = v;
          if (cell.dataset.value !== undefined) cell.dataset.value = v;
        });
        row.classList.add('is-new');
        setTimeout(() => row.classList.remove('is-new'), 2000);
      }
      closeModal(modal);
      refreshTableOf(row);
      toast(btn.dataset.msg || '保存成功，已记入操作日志');
    },

    // 修改状态标签（标记已发布、线索跟进等）
    async 'set-status'(btn) {
      if (btn.dataset.confirm && !(await confirmBox({ title: btn.dataset.title || '确认操作', text: btn.dataset.confirm }))) return;
      const v = btn.dataset.value;
      $$(btn.dataset.target).forEach((t) => { t.textContent = v; t.className = `tag ${TAG_CLASS[v] || 'tag-primary'}`; });
      if (btn.dataset.hide) $$(btn.dataset.hide).forEach((e) => e.classList.add('hidden'));
      if (btn.dataset.show) $$(btn.dataset.show).forEach((e) => e.classList.remove('hidden'));
      toast(btn.dataset.msg || `状态已更新为「${v}」，已记入操作日志`);
      const m = btn.closest('.modal');
      if (m) closeModal(m);
      if (btn.dataset.log) addLog(btn.dataset.log);
    },

    reload() { location.reload(); },
    'toggle-nav'(btn) { const open = btn.closest('.nav-sec').classList.toggle('open'); btn.setAttribute('aria-expanded', open); },
    'go-back'(btn) {
      if (history.length > 1) history.back();
      else location.href = btn.dataset.href;
    },
    'read-all'() {
      $$('.msg-item.unread').forEach((m) => m.classList.remove('unread'));
      $$('[data-unread-count]').forEach((b) => { b.textContent = '0'; b.classList.add('hidden'); });
      toast('已将全部消息标记为已读');
    },

    'sensitive-test'(btn) {
      const src = $(btn.dataset.source);
      const out = $(btn.dataset.result);
      const modeEl = $('input[name="mode"]:checked');
      const mode = modeEl ? modeEl.value : 'exact';
      const text = src.value.trim();
      if (!text) { toast('请先输入要检测的文字', 'warn'); return; }
      const hits = detectSensitive(text, mode);
      const high = hits.filter((h) => h.level === 'high').length, low = hits.length - high;
      out.innerHTML = `
        <div class="test-sum">检测模式：<b>${mode === 'semantic' ? '语义匹配' : '精准匹配'}</b>　命中高危词 <b class="c-danger">${high}</b> 个，低危词 <b class="c-warn">${low}</b> 个
        ${high ? '<span class="tag tag-danger">将拦截提交</span>' : low ? '<span class="tag tag-warn">提交时提示</span>' : '<span class="tag tag-success">可以提交</span>'}</div>
        <div class="test-text">${highlight(text, hits)}</div>`;
    },

    'apply-filter'(btn) { const tbl = document.getElementById(btn.dataset.for); tables[tbl.id].page = 1; renderTable(tbl); toast(`查询完成，共 ${$(`[data-total-for="${tbl.id}"]`) ? $(`[data-total-for="${tbl.id}"]`).textContent : ''} 条结果`, 'info', 1500); },

    'reset-filter'(btn) {
      $$(`[data-filter][data-for="${btn.dataset.for}"]`).forEach((f) => { f.value = ''; });
      const tbl = document.getElementById(btn.dataset.for);
      tables[tbl.id].page = 1;
      renderTable(tbl);
      toast('筛选条件已重置', 'info', 1500);
    },

    'add-chip'(btn) {
      const wrap = btn.closest('.chip-input');
      const input = $('input', wrap);
      const v = input.value.trim();
      if (!v) { toast('请先输入内容', 'warn'); return; }
      $('.chips', wrap).insertAdjacentHTML('beforeend', `<span class="chip">${esc(v)}<button type="button" class="chip-x" aria-label="移除">×</button></span>`);
      input.value = '';
      toast(`已添加「${v}」，保存后生效`, 'info', 1500);
    },

    // 批量不通过：意见必填，对勾选的行生效
    async 'batch-reject'(btn) {
      const tbl = $(btn.dataset.table);
      const rows = $$('tbody input.row-check:checked', tbl).map((c) => c.closest('tr'));
      if (!rows.length) { toast('请先勾选需要办理的待办', 'warn'); return; }
      const op = await opinionBox({ title: `批量不通过（${rows.length} 条）`, label: '退回意见', required: true, okText: '确认不通过', danger: true, tplKey: btn.dataset.tpl || 'review' });
      if (op === null) return;
      rows.forEach((r) => { r.classList.add('removed'); r.style.display = 'none'; const c = $('input.row-check', r); if (c) c.checked = false; });
      const all = $('thead input.check-all', tbl); if (all) all.checked = false;
      refreshTableOf(tbl.querySelector('tbody'));
      toast(`已批量退回 ${rows.length} 条稿件，系统已通知投稿人`, 'warn');
    },

    // 批量操作：对勾选的行执行
    async batch(btn) {
      const tbl = $(btn.dataset.table);
      const rows = $$('tbody input.row-check:checked', tbl).map((c) => c.closest('tr'));
      if (!rows.length) { toast('请先勾选需要操作的数据', 'warn'); return; }
      if (!(await confirmBox({ title: btn.dataset.title || '批量操作', text: (btn.dataset.confirm || '确认对选中的 {n} 条数据执行操作？').replace('{n}', rows.length), danger: !!btn.dataset.danger }))) return;
      rows.forEach((r) => {
        if (btn.dataset.value) setRowStatus(r, btn.dataset.value);
        else { r.classList.add('removed'); r.style.display = 'none'; }
        const c = $('input.row-check', r); if (c) c.checked = false;
      });
      const all = $('thead input.check-all', tbl); if (all) all.checked = false;
      refreshTableOf(tbl.querySelector('tbody'));
      toast((btn.dataset.msg || '已完成 {n} 条数据的操作').replace('{n}', rows.length));
    }
  };

  // 在页面的操作日志表中追加一行（用于演示“记入操作日志”）
  function addLog(text) {
    const tb = $('#logTable tbody');
    if (!tb) return;
    tb.insertAdjacentHTML('afterbegin', `<tr class="is-new"><td>2026-09-30 ${now()}</td><td>${esc(document.body.dataset.user || '当前用户')}</td><td>${esc(text)}</td><td>10.12.34.56</td></tr>`);
  }

  /* ========== 富文本编辑器 ========== */
  const SAMPLE_IMG = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5BA6EA"/><stop offset="1" stop-color="#1B71BC"/></linearGradient></defs><rect width="640" height="360" fill="url(#g)"/><circle cx="470" cy="120" r="46" fill="#fff" opacity=".35"/><path d="M0 300 180 170 300 260 420 190 640 330V360H0z" fill="#fff" opacity=".3"/><text x="320" y="200" font-size="30" fill="#fff" text-anchor="middle" font-family="sans-serif">示例图片</text></svg>');
  const BLOCK_LABEL = { h2: '标题', h3: '小标题' };
  const edHost = (el) => { const box = el.closest('.editor-box'); return box && $('[contenteditable]', box); };
  function edFocus(host, range) {
    const sel = getSelection();
    if (!range && sel.rangeCount && host.contains(sel.anchorNode)) return;
    host.focus();
    if (!range) { range = document.createRange(); range.selectNodeContents(host); range.collapse(false); }
    sel.removeAllRanges(); sel.addRange(range);
  }
  function edSync(host) {
    const box = host.closest('.editor-box');
    $$('.editor-bar button[data-cmd]', box).forEach((b) => {
      const c = b.dataset.cmd;
      let on = false;
      try {
        if (c === 'formatBlock') on = !b.closest('.dropdown-menu') && document.queryCommandValue('formatBlock') === b.dataset.arg;
        else if (/^(bold|italic|underline|strikeThrough|justify\w+|insert\w+List)$/.test(c)) on = document.queryCommandState(c);
      } catch (err) { on = false; }
      b.classList.toggle('on', on);
    });
    const lab = $('.ed-dd-label', box);
    if (lab) lab.textContent = BLOCK_LABEL[document.queryCommandValue('formatBlock')] || '正文';
  }
  function edCmd(btn) {
    const host = edHost(btn);
    if (!host) return;
    edFocus(host);
    const c = btn.dataset.cmd;
    let arg = btn.dataset.arg || null;
    if (c === 'formatBlock') { if (document.queryCommandValue('formatBlock') === arg && arg !== 'p') arg = 'p'; arg = `<${arg}>`; }
    document.execCommand(c, false, arg);
    $$('.dropdown.open').forEach((d) => d.classList.remove('open'));
    edSync(host);
  }
  function edInsert(host, html, range) {
    edFocus(host, range);
    document.execCommand('insertHTML', false, html);
    edSync(host);
  }
  function edAction(btn) {
    const box = btn.closest('.editor-box');
    const host = edHost(btn);
    const pop = $('.ed-pop', box);
    const mode = btn.dataset.ed;
    if (mode === 'link' || mode === 'image') {
      const sel = getSelection();
      box.edRange = sel.rangeCount && host.contains(sel.anchorNode) ? sel.getRangeAt(0).cloneRange() : null;
      pop.dataset.mode = mode;
      $('.ed-pop-title', pop).textContent = mode === 'link' ? '插入链接' : '插入图片';
      const url = $('.ed-url', pop);
      url.value = '';
      url.placeholder = mode === 'link' ? '请输入链接地址，如 https://news.csu.edu.cn' : '粘贴图片地址，或选择本地图片 / 示例图片';
      $('.ed-text', pop).value = box.edRange ? box.edRange.toString() : '';
      pop.hidden = false;
      url.focus();
      return;
    }
    if (mode === 'cancel') { pop.hidden = true; edFocus(host, box.edRange); return; }
    if (mode === 'sample') { pop.hidden = true; edInsert(host, `<img src="${SAMPLE_IMG}" alt="示例图片">`, box.edRange); toast('已插入示例图片', 'info', 1500); return; }
    if (mode === 'ok') {
      let url = $('.ed-url', pop).value.trim();
      if (!url) { toast(pop.dataset.mode === 'link' ? '请输入链接地址' : '请输入图片地址或选择本地图片', 'warn'); $('.ed-url', pop).focus(); return; }
      if (!/^(https?:|data:|\/|\.)/i.test(url)) url = `https://${url}`;
      pop.hidden = true;
      if (pop.dataset.mode === 'link') {
        const text = $('.ed-text', pop).value.trim() || url;
        edInsert(host, `<a href="${esc(url)}" target="_blank" rel="noopener">${esc(text)}</a>&nbsp;`, box.edRange);
        toast('已插入链接', 'info', 1500);
      } else {
        edInsert(host, `<img src="${esc(url)}" alt="正文图片">`, box.edRange);
        toast('已插入图片', 'info', 1500);
      }
    }
  }
  document.addEventListener('mousedown', (e) => {
    if (e.target.closest('.editor-bar button') || e.target.closest('.teacher-picker .picker-list')) e.preventDefault();
  });
  document.addEventListener('selectionchange', () => {
    const sel = getSelection();
    const n = sel.rangeCount && sel.anchorNode;
    const host = n && (n.nodeType === 1 ? n : n.parentElement).closest('.editor-box [contenteditable]');
    if (host) edSync(host);
  });

  /* ========== 事件委托 ========== */
  document.addEventListener('click', async (e) => {
    const t = e.target;

    // 下拉菜单
    const ddBtn = t.closest('[data-dropdown]');
    if (ddBtn) { e.preventDefault(); const dd = ddBtn.closest('.dropdown'); const open = dd.classList.contains('open'); $$('.dropdown.open').forEach((d) => d.classList.remove('open')); if (!open) dd.classList.add('open'); return; }
    if (!t.closest('.dropdown-menu')) $$('.dropdown.open').forEach((d) => d.classList.remove('open'));

    // 人员工号检索列表
    const sp = t.closest('.staff-picker .picker-item');
    if (sp) { const p = staffDir().find((x) => x.no === sp.dataset.no); if (p) staffFill(sp.closest('.modal'), p); return; }
    if (!t.closest('.staff-picker')) $$('.staff-picker .picker-list.open').forEach((l) => l.classList.remove('open'));

    // 指导老师 / 负责领导选择列表
    const pick = t.closest('.teacher-picker .picker-item');
    if (pick) {
      const wrap = pick.closest('.teacher-picker');
      const person = (wrap._items || [])[Number(pick.dataset.idx)];
      if (person) choosePerson(wrap, person);
      return;
    }
    if (!t.closest('.teacher-picker')) $$('.teacher-picker .picker-list.open').forEach((l) => l.classList.remove('open'));

    // 静态意见框中的模板插入
    const fill = t.closest('.tpl-chip[data-fill]');
    if (fill) { const ta = $(fill.dataset.fill); ta.value = ta.value ? `${ta.value}\n${fill.textContent}` : fill.textContent; ta.dispatchEvent(new Event('input', { bubbles: true })); return; }

    // 标签移除
    if (t.closest('.chip-x')) { t.closest('.chip').remove(); toast('已移除，保存后生效', 'info', 1500); return; }

    // 上传文件删除
    if (t.closest('.fi-del')) { e.stopPropagation(); e.preventDefault(); const item = t.closest('.file-item'); const box = item.closest('.upload-field'); item.remove(); updateFileCount(box); toast('已移除该文件', 'info', 1500); return; }

    // 弹窗关闭
    const closer = t.closest('[data-close]');
    if (closer) { e.preventDefault(); closeModal(closer.closest('.modal')); return; }
    if (t.classList.contains('modal') && !t.dataset.static && t.id) { closeModal(t); return; }

    const opener = t.closest('[data-open]');
    if (opener) { e.preventDefault(); openModal(opener.dataset.open); return; }

    // 编辑器工具栏
    const cmd = t.closest('[data-cmd]');
    if (cmd) { e.preventDefault(); edCmd(cmd); return; }
    const ed = t.closest('[data-ed]');
    if (ed) { e.preventDefault(); edAction(ed); return; }

    // Tab 切换
    const tab = t.closest('[data-tab]');
    if (tab) {
      e.preventDefault();
      const group = tab.closest('[data-tabs]');
      $$('[data-tab]', group).forEach((x) => x.classList.toggle('on', x === tab));
      if (tab.dataset.filterItems) {
        const v = tab.dataset.filterValue;
        let n = 0;
        $$(`${tab.dataset.filterItems} > [data-${tab.dataset.filterKey}]`).forEach((it) => {
          if (it.dataset.hiddenByParam) return;
          const show = !v || String(it.dataset[tab.dataset.filterKey]).split(',').includes(v);
          it.style.display = show ? '' : 'none';
          if (show) n++;
        });
        const empty = $(`${tab.dataset.filterItems} + .m-empty`);
        if (empty) empty.classList.toggle('hidden', n > 0);
      } else if (tab.dataset.filterList) {
        $$(tab.dataset.filterList).forEach((l) => l.classList.toggle('only-unread', tab.dataset.tab === 'unread'));
      } else if (tab.dataset.filterTable) {
        const tbl = $(tab.dataset.filterTable);
        tables[tbl.id].tab = { key: tab.dataset.filterKey, value: tab.dataset.filterValue };
        tables[tbl.id].page = 1;
        renderTable(tbl);
      } else {
        const scope = group.closest('[data-tabs-scope]') || document;
        $$('[data-panel]', scope).forEach((p) => p.classList.toggle('on', p.dataset.panel === tab.dataset.tab));
      }
      return;
    }

    // 消息点击：标记已读后跳转
    const msg = t.closest('.msg-item');
    if (msg && !t.closest('button')) {
      if (msg.classList.contains('unread')) {
        msg.classList.remove('unread');
        $$('[data-unread-count]').forEach((b) => { const n = Math.max(0, Number(b.textContent) - 1); b.textContent = n; b.classList.toggle('hidden', n === 0); });
      }
      if (msg.dataset.href) go(msg.dataset.href, 300);
      return;
    }

    // 开关
    const sw = t.closest('.switch');
    if (sw && !sw.disabled) {
      const on = !sw.classList.contains('on');
      if (sw.dataset.confirmOff && !on && !(await confirmBox({ title: '确认停用', text: sw.dataset.confirmOff, danger: true, okText: '停用' }))) return;
      sw.classList.toggle('on', on);
      const row = sw.closest('tr, [data-row]');
      const tagEl = row && $('.js-tag', row);
      if (tagEl) { const v = on ? (tagEl.dataset.on || '启用') : (tagEl.dataset.off || '停用'); tagEl.textContent = v; tagEl.className = `tag js-tag ${TAG_CLASS[v] || ''}`; if (row.hasAttribute('data-status')) row.dataset.status = v; }
      toast(on ? (sw.dataset.onMsg || '已启用') : (sw.dataset.offMsg || '已停用'), on ? 'success' : 'info');
      return;
    }

    // 业务动作
    const act = t.closest('[data-action]');
    if (act && actions[act.dataset.action]) { e.preventDefault(); actions[act.dataset.action](act); return; }

    // 提示
    const tt = t.closest('[data-toast]');
    if (tt) { e.preventDefault(); toast(tt.dataset.toast, tt.dataset.toastType || 'info'); if (tt.dataset.href) go(tt.dataset.href, 800); return; }

    // 跳转（可带确认）
    const link = t.closest('[data-href], a[data-confirm]');
    if (link && !t.closest('input, select, textarea, label')) {
      e.preventDefault();
      if (link.dataset.confirm && !(await confirmBox({ title: link.dataset.confirmTitle || '提示', text: link.dataset.confirm }))) return;
      go(link.dataset.href || link.getAttribute('href'), 0);
    }
  });

  /* ========== 输入类事件 ========== */
  function updateFileCount(box) {
    if (!box) return;
    const n = $$('.file-item', box).length;
    $$('[data-file-count]', box).forEach((el) => { el.textContent = n; });
    if (n) clearError($('input[type=file]', box));
  }

  function handleUpload(input) {
    const box = input.closest('.upload-field');
    const list = $('.files', box);
    const max = Number(input.dataset.maxMb || 20);
    const kind = input.dataset.upload || 'img';
    Array.from(input.files).forEach((f) => {
      const isImg = f.type.startsWith('image/');
      if (kind === 'img' && !isImg) { toast(`「${f.name}」不是图片格式，仅支持 JPG / PNG`, 'danger'); return; }
      if (f.size > max * 1024 * 1024) { toast(`「${f.name}」超过 ${max}MB 大小限制`, 'danger'); return; }
      const size = f.size > 1048576 ? `${(f.size / 1048576).toFixed(1)} MB` : `${Math.ceil(f.size / 1024)} KB`;
      const thumb = isImg ? `<img src="${URL.createObjectURL(f)}" alt="${esc(f.name)}">` : `<div class="fi-doc">${esc(f.name.split('.').pop().toUpperCase())}</div>`;
      list.insertAdjacentHTML('beforeend', `
        <div class="file-item">${thumb}
          <button type="button" class="fi-del" aria-label="删除">×</button>
          <div class="fi-meta"><span class="fi-name">${esc(f.name)}</span><span>${size} · ${kind === 'doc' ? '附件' : '原图'}</span></div>
          ${input.dataset.remark !== undefined ? '<input placeholder="单张照片备注（选填）">' : ''}
        </div>`);
    });
    input.value = '';
    updateFileCount(box);
    toast(kind === 'doc' ? '附件上传成功' : '上传成功，原图已保存', 'success', 1500);
  }

  function evalShowWhen(scope = document) {
    $$('[data-show-when]', scope).forEach((el) => {
      const [name, val] = el.dataset.showWhen.split('=');
      const checked = $(`[name="${name}"]:checked`) || $(`select[name="${name}"]`);
      const cur = checked ? checked.value : '';
      el.classList.toggle('hidden', !val.split('|').includes(cur));
    });
  }

  document.addEventListener('change', (e) => {
    const t = e.target;
    if (t.matches('input[type=file][data-upload]')) { handleUpload(t); return; }
    if (t.matches('[data-import-file]')) { readImport(t); return; }
    if (t.matches('[data-term-keep]')) { termMark(t); termSum(t.closest('.modal')); return; }
    if (t.matches('[data-term-all]')) { const m = t.closest('.modal'); $$('[data-term-keep]', m).forEach((c) => { c.checked = t.checked; termMark(c); }); termSum(m); return; }
    if (t.matches('[data-nav-radio]') && t.checked) { location.href = t.value; return; }
    if (t.matches('[data-ed-file]')) {
      const file = t.files[0];
      const box = t.closest('.editor-box');
      t.value = '';
      if (!file) return;
      if (!file.type.startsWith('image/')) { toast('请选择图片文件', 'warn'); return; }
      const rd = new FileReader();
      rd.onload = () => { $('.ed-pop', box).hidden = true; edInsert(edHost(t), `<img src="${rd.result}" alt="${esc(file.name)}">`, box.edRange); toast(`已插入图片：${file.name}`, 'info', 1500); };
      rd.readAsDataURL(file);
      return;
    }
    if (t.name) evalShowWhen();
    if (t.name === 'dept') syncLeaderPicker(t.value);
    if (t.matches('[data-filter][data-for]') && t.tagName === 'SELECT') { const tbl = document.getElementById(t.dataset.for); tables[tbl.id].page = 1; renderTable(tbl); }
    if (t.matches('.check-all')) { const tbl = t.closest('table'); $$('tbody tr', tbl).filter((r) => r.style.display !== 'none').forEach((r) => { const c = $('input.row-check', r); if (c) c.checked = t.checked; }); }
    // 下拉修改行内状态（线索处置等）
    if (t.matches('select[data-set-tag]')) {
      const row = t.closest('tr, [data-row]');
      const tagEl = row && $('.js-tag', row);
      if (tagEl) { tagEl.textContent = t.value; tagEl.className = `tag js-tag ${TAG_CLASS[t.value] || ''}`; }
      const opt = t.selectedOptions[0];
      if (opt && opt.dataset.open) openModal(opt.dataset.open);
      else toast(`已更新为「${t.value}」，已记入操作日志`);
    }
    if (t.matches('[data-toast-change]')) toast(t.dataset.toastChange, 'info', 1500);
    const f = t.closest('.field'); if (f && f.classList.contains('is-error') && String(t.value).trim()) clearError(t);
  });

  document.addEventListener('input', (e) => {
    const t = e.target;
    const f = t.closest && t.closest('.field');
    if (f && f.classList.contains('is-error') && (t.value || t.innerText || '').trim()) clearError(t);
    if (t.closest && t.closest('form[data-autosave]')) t.closest('form').dataset.dirty = '1';
    // 字数统计
    if (t.dataset && t.dataset.counter) { const c = $(t.dataset.counter); if (c) c.textContent = (t.value ?? t.innerText).trim().length; }
    // 关键词实时搜索
    if (t.matches && t.matches('[data-filter][data-live]')) { const tbl = document.getElementById(t.dataset.for); tables[tbl.id].page = 1; renderTable(tbl); }
    // 指导老师 / 负责领导：姓名只在本单位名单里筛，纯数字按工号回显人员库
    if (t.closest && t.closest('.teacher-picker') && t.matches('input')) {
      const wrap = t.closest('.teacher-picker');
      if (t.dataset.picked && t.value.trim() !== t.dataset.picked) {
        delete t.dataset.picked;
        delete t.dataset.pickedNo;
        delete t.dataset.echo;
      }
      wrap._hi = t.value.trim() ? 0 : -1;
      renderPicker(wrap, t.value);
    }
    // 人员工号回显
    if (t.matches && t.matches('[data-staff-lookup]')) {
      renderStaffPicker(t);
      clearTimeout(t._lookup);
      t._lookup = setTimeout(() => staffLookup(t, false), 300);
    }
  });

  document.addEventListener('focusout', (e) => {
    const t = e.target;
    if (t.matches && t.matches('[data-staff-lookup]')) { clearTimeout(t._lookup); t._lookup = setTimeout(() => staffLookup(t, true), 200); }
  });

  document.addEventListener('keydown', (e) => {
    const pickerInput = e.target.closest && e.target.closest('.teacher-picker') && e.target.matches('input') ? e.target : null;
    if (pickerInput && (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Enter' || e.key === 'Escape')) {
      const wrap = pickerInput.closest('.teacher-picker');
      const list = $('.picker-list', wrap);
      if (e.key === 'Escape') {
        if (list.classList.contains('open')) { e.preventDefault(); list.classList.remove('open'); pickerInput.setAttribute('aria-expanded', 'false'); }
        return;
      }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!list.classList.contains('open')) { wrap._hi = -1; renderPicker(wrap, ''); }
        const n = (wrap._items || []).length;
        if (!n) return;
        const cur = Number.isInteger(wrap._hi) ? wrap._hi : -1;
        wrap._hi = e.key === 'ArrowDown' ? (cur + 1) % n : (cur <= 0 ? n - 1 : cur - 1);
        $$('.picker-item', list).forEach((el, i) => el.classList.toggle('on', i === wrap._hi));
        const on = $('.picker-item.on', list);
        if (on) on.scrollIntoView({ block: 'nearest' });
        return;
      }
      if (e.key === 'Enter' && list.classList.contains('open')) {
        e.preventDefault();
        const items = wrap._items || [];
        let i = Number.isInteger(wrap._hi) ? wrap._hi : -1;
        if (!(i >= 0 && items[i]) && items.length === 1) i = 0;
        if (items[i]) choosePerson(wrap, items[i]);
        return;
      }
    }
    if (e.target.matches && e.target.matches('.ed-pop input')) {
      const pop = e.target.closest('.ed-pop');
      if (e.key === 'Enter') { e.preventDefault(); $('[data-ed="ok"]', pop).click(); return; }
      if (e.key === 'Escape') { $('[data-ed="cancel"]', pop).click(); return; }
    }
    if (e.key === 'Enter' && e.target.matches('[data-staff-lookup]')) {
      e.preventDefault();
      const first = $('.picker-list.open .picker-item', e.target.closest('.staff-picker'));
      const p = first && staffDir().find((x) => x.no === first.dataset.no);
      if (p && e.target.value.trim() !== p.no && !staffDir().some((x) => x.no === e.target.value.trim())) staffFill(e.target.closest('.modal'), p);
      else staffLookup(e.target, true);
      $$('.staff-picker .picker-list', e.target.closest('.modal')).forEach((l) => l.classList.remove('open'));
      return;
    }
    if (e.key === 'Escape') $$('.modal.open').forEach((m) => { if (m.id) closeModal(m); });
    if (e.key === 'Enter' && e.target.matches('.chip-input input')) { e.preventDefault(); actions['add-chip']($('button', e.target.closest('.chip-input'))); }
    if (e.key === 'Enter' && e.target.matches('[data-top-search]')) {
      e.preventDefault();
      const v = e.target.value.trim();
      const kw = $('[data-filter="keyword"]');
      if (!v) { toast('请输入稿件标题、编号或投稿人', 'warn'); return; }
      if (kw) { kw.value = v; const tbl = document.getElementById(kw.dataset.for); tables[tbl.id].page = 1; renderTable(tbl); kw.scrollIntoView({ block: 'center', behavior: 'smooth' }); toast(`已在当前列表中搜索“${v}”`, 'info'); }
      else toast(`已搜索“${v}”，请到稿件列表页查看结果`, 'info');
    }
    if (e.key === 'Enter' && e.target.matches('input[data-filter]')) { e.preventDefault(); const tbl = document.getElementById(e.target.dataset.for); tables[tbl.id].page = 1; renderTable(tbl); }
  });

  document.addEventListener('focusin', (e) => {
    const p = e.target.closest && e.target.closest('.teacher-picker');
    if (p && e.target.matches('input')) {
      p._hi = -1;
      renderPicker(p, '');
      e.target.select();
    }
  });

  function personText(p) { return `${p.name}（${p.college}）`; }
  function pickerUnit(wrap) {
    if (wrap.dataset.picker === 'vice') {
      const sel = $('select[name="dept"]');
      return sel ? sel.value : '';
    }
    return wrap.dataset.unit || '';
  }
  function rosterPeople(wrap) {
    const unit = pickerUnit(wrap);
    if (wrap.dataset.picker === 'vice') return (DATA.viceLeaders || []).filter((p) => p.active !== false && p.college === unit);
    return (DATA.teachers || []).filter((p) => p.college === unit);
  }
  function choosePerson(wrap, p) {
    const input = $('input', wrap);
    const text = personText(p);
    input.value = text;
    input.dataset.picked = text;
    input.dataset.pickedNo = p.no;
    input.dataset.echo = rosterPeople(wrap).some((x) => x.no === p.no) ? '0' : '1';
    clearError(input);
    $('.picker-list', wrap).classList.remove('open');
    input.setAttribute('aria-expanded', 'false');
    wrap._hi = -1;
    toast(`已选择${input.dataset.label || '人员'}：${text}`, 'info', 1500);
  }
  function syncLeaderPicker(unit) {
    $$('.teacher-picker[data-picker="vice"]').forEach((wrap) => {
      const input = $('input', wrap);
      const listOpen = $('.picker-list', wrap).classList.contains('open');
      if (input.dataset.echo === '1') { if (listOpen) renderPicker(wrap, ''); return; }
      const hit = (DATA.viceLeaders || []).find((p) => personText(p) === input.dataset.picked && p.college === unit && p.active !== false);
      if (!hit) {
        input.value = '';
        delete input.dataset.picked;
        delete input.dataset.pickedNo;
        delete input.dataset.echo;
      }
      if (listOpen) renderPicker(wrap, '');
    });
  }
  function renderPicker(wrap, kw) {
    const list = $('.picker-list', wrap);
    const input = $('input', wrap);
    const k = (kw || '').trim();
    const digits = /^\d+$/.test(k);
    const roster = rosterPeople(wrap);
    const nameKey = k.replace(/（.*/, '');
    let items;
    if (!k) items = roster;
    else if (digits) items = staffDir().filter((p) => p.no.startsWith(k));
    else items = roster.filter((p) => p.name.includes(nameKey));
    wrap._items = items;
    if (!Number.isInteger(wrap._hi) || wrap._hi < 0 || wrap._hi >= items.length) wrap._hi = -1;
    if (!items.length) {
      const msg = digits
        ? `未找到工号「${esc(k)}」。请核对后重试，不能手动填写姓名。`
        : (k
          ? `当前名单中没有“${esc(nameKey)}”。如需选择其他人员，请输入工号查找。`
          : (wrap.dataset.picker === 'vice' ? '该部门暂无在任副职领导，请输入工号查找。' : '本院暂无已配置的指导老师，请输入工号查找。'));
      list.innerHTML = `<div class="picker-empty">${msg}</div>`;
    } else {
      list.innerHTML = items.map((p, i) => `<div class="picker-item${i === wrap._hi ? ' on' : ''}" role="option" data-idx="${i}"><b>${esc(p.name)}</b><span>${esc(p.college)} · ${esc(p.title || '')} · 工号 ${esc(p.no)}</span></div>`).join('');
    }
    list.classList.add('open');
    if (input) input.setAttribute('aria-expanded', 'true');
  }

  /* ========== 网址参数回显（跨页面闭环） ========== */
  function applyParams() {
    const done = params.get('done');
    if (done) {
      $$(`[data-row-id="${done}"]`).forEach((r) => { r.dataset.hiddenByParam = '1'; r.style.display = 'none'; });
      $$('[data-counter]').forEach((c) => { const n = Number(c.textContent); if (!isNaN(n) && n > 0) c.textContent = n - 1; });
    }
    $$('[data-when-param]').forEach((el) => {
      const [k, v] = el.dataset.whenParam.split('=');
      const match = v === undefined ? params.has(k) : v.split('|').includes(params.get(k));
      el.classList.toggle('hidden', !match);
      if (match && el.dataset.highlight !== undefined) el.classList.add('is-new');
      if (el.tagName === 'TR') { if (match) delete el.dataset.hiddenByParam; else el.dataset.hiddenByParam = '1'; }
    });
    $$('[data-when-param-hide]').forEach((el) => {
      const [k, v] = el.dataset.whenParamHide.split('=');
      if (v === undefined ? params.has(k) : v.split('|').includes(params.get(k))) { el.classList.add('hidden'); if (el.tagName === 'TR') el.dataset.hiddenByParam = '1'; }
    });
    $$('[data-param-text]').forEach((el) => { const v = params.get(el.dataset.paramText); if (v) el.textContent = v; });

    const msg = params.get('msg');
    if (msg) {
      const page = $('.page, .m-body');
      if (page) {
        const link = params.get('link');
        const type = params.get('type') === 'warn' ? 'warn' : 'success';
        page.insertAdjacentHTML('afterbegin', `<div class="result-bar ${type}">${ICON[type]}<span>${esc(msg)}</span>${link ? `<a href="${esc(link)}">${esc(params.get('linkText') || '查看')} ›</a>` : ''}<button class="rb-x" aria-label="关闭">×</button></div>`);
        $('.result-bar .rb-x', page).onclick = (e) => e.target.closest('.result-bar').remove();
      }
      toast(msg, params.get('type') === 'warn' ? 'warn' : 'success');
    }
  }

  /* ========== 初始化 ========== */
  document.addEventListener('DOMContentLoaded', () => {
    // 图片加载失败时显示占位图
    $$('img').forEach((img) => img.addEventListener('error', function onErr() {
      img.removeEventListener('error', onErr);
      img.src = 'data:image/svg+xml;utf8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="100%" height="100%" fill="#E3F1F9"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" fill="#9CBFDA" font-size="18" font-family="sans-serif">图片素材</text></svg>');
    }));

    applyParams();
    evalShowWhen();
    $$('table[data-table]').forEach(initTable);
    updateCounts();

    // 草稿自动保存（每 30 秒，有改动时触发）
    $$('form[data-autosave]').forEach((form) => {
      setInterval(() => {
        if (form.dataset.dirty) {
          form.dataset.dirty = '';
          $$('[data-draft-status]').forEach((el) => { el.innerHTML = `<i class="dot-ok"></i>已自动保存于 ${now()}`; });
        }
      }, 30000);
    });
  });

  // 对外暴露，便于页面内少量自定义脚本调用
  window.TG = { toast, confirmBox, opinionBox, openModal, closeModal, validate, detectSensitive };
})();
