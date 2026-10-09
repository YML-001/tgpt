# 审核页通用模板：指导老师、一审、二审、三审共用
from urllib.parse import urlencode, quote
from lib import icon, tag, card, page_head, btn, a_btn, flow_steps, modal, field
from common import sensitive_card, op_log_table
from data import TYPE_NAME
from workflow import node_chart, bd_grid, base_cells, sec
from detail import sub_content


def q(path, **params):
    """拼接带参数的网址，参数值自动编码"""
    return f'{path}?{urlencode(params, quote_via=quote)}'


def review_body(sub, status, node, cur, timer, timeline_html, actions, back_href, identity='学生', extra_right='',
                logs=None, start=None, arrive=None):
    """办理页：对齐统一待办的任务办理布局（任务标题 + 页签：表单信息 / 流程图 / 审批记录 / 操作日志）"""
    t_text, t_level = timer
    t_cls = {'over': 'tag-danger', 'warn': 'tag-warn', 'ok': 'tag-success'}[t_level]
    logs = logs or [('2026-09-28 10:24', f'{sub["author"]}', '提交投稿，生成 v1', '10.12.34.21'),
                    ('2026-09-28 10:02', f'{sub["author"]}', '新建草稿', '10.12.34.21')]
    start = start or sub['time']
    arrive = arrive or sub['time']
    tabs = ''.join(f'<button class="wf-pill{" on" if i == 0 else ""}" data-tab="{k}">{n}</button>'
                   for i, (k, n) in enumerate([('form', '表单信息'), ('chart', '流程图'), ('flow', '审批记录'), ('log', '操作日志')]))
    side = f'''<div class="grid" style="align-content:start">
      <div class="timer {'danger' if t_level == 'over' else ('ok' if t_level == 'ok' else '')}">{icon("clock", 22)}<div><div style="font-size:12px">当前节点：{node} · 时限 3 个工作日</div><b>{t_text}</b></div></div>
      {sensitive_card(sub['type'])}
      <div class="notice notice-info">{icon("info", 15)}<div>退回必须填写审核意见，意见将永久保存到稿件档案并通知投稿人。</div></div>
      {extra_right}
    </div>'''
    form = f'''<div class="grid g-main-wide">
    <div>{sec('基础信息', bd_grid(base_cells(sub, start, arrive)))}{sec('稿件内容', f'<div class="wf-article">{sub_content(sub)}</div>')}</div>
    {side}
  </div>'''
    return f'''<div class="card wf-sheet wf-handle" data-tabs-scope>
  <div class="wf-pills" data-tabs>{tabs}</div>
  <div class="wf-task">
    <div class="wf-task-title"><b>{TYPE_NAME[sub["type"]]}审核：《{sub["title"]}》</b>
      <span class="tag tag-success">当前节点：{node}</span><span class="tag tag-primary">发起人：{sub["author"]}（{sub["college"]} · {sub["identity"]}）</span><span class="tag {t_cls}">{t_text}</span></div>
    <div class="wf-task-actions">{actions}{a_btn('返回待办', back_href, '', 'arrow-l')}</div>
  </div>
  <div class="tab-panel on" data-panel="form">{form}</div>
  <div class="tab-panel" data-panel="chart">{sec('节点流程图', '<div class="wf-flow-panel">' + node_chart(identity, cur) + '</div>')}</div>
  <div class="tab-panel" data-panel="flow">{sec('审批记录', '<div class="wf-flow-panel">' + timeline_html + '</div>')}</div>
  <div class="tab-panel" data-panel="log">{sec('操作日志', op_log_table(logs))}</div>
</div>'''


def reject_modal(mid, title, label, tpls, next_url, ok='确认退回', danger=True, open_=True, cancel='review.html'):
    chips = ''.join(f'<button type="button" class="tpl-chip" data-fill="#{mid}Text">{t}</button>' for t in tpls)
    body = f'''<form id="{mid}Form" novalidate>
<div class="notice notice-warn mb16">{icon("alert", 15)}<div>{label}为必填项，提交后稿件状态将变更，并通过消息通知投稿人。</div></div>
{field(label, f'<textarea class="textarea" id="{mid}Text" name="opinion" required maxlength="500" style="min-height:120px" placeholder="请填写具体、可操作的修改意见"></textarea>', req=True)}
<div class="tpl-title">常用意见模板（点击插入，可在“审核意见模板”中维护）</div><div class="tpl-list">{chips}</div></form>'''
    cls = 'btn-danger' if danger else 'btn-primary'
    foot = (f'<a class="btn" href="{cancel}">取消</a>'
            f'<button type="button" class="btn {cls}" data-action="submit" data-form="#{mid}Form" data-msg="{title}成功，已通知投稿人" data-next="{next_url}">{ok}</button>')
    return modal(mid, title, body, foot, 'modal-sm', open_=open_)


# ---------- 视频 / 照片 / 线索：各审核角色的办理页与已办详情 ----------
SAMPLE_STAGE = {'视频': ('adopted', '已终审采用'), '照片': ('adopted', '已终审采用'), '线索': ('r3', '待三审')}


def row_sub(t, d):
    from detail import sample_for
    if d is None:
        return sample_for(t)
    return sample_for(t, dict(id=d['sid'], title=d['title'], author=d['author'], college=d['col'], identity=d['ident'], time=d['start']))


def type_review_pages(page, rows, node, stage, todo_href, done_href, tpl, pass_label, pass_msg, crumbs_active,
                      reject_title='退回稿件', reject_label='退回意见', reject_text='退回修改', reject_icon='undo', reject_msg=None,
                      handle='review.html', extra_right=''):
    """为每种非新闻类型生成办理页：通过（意见选填）/ 退回（意见必填，可选模板），处理后回到待办并移除该稿"""
    from detail import flow_records, chart_cur, STATUS
    from data import typed
    out = {}
    for t in ('视频', '照片', '线索'):
        d = next((r for r in rows if r['t'] == t), None)
        sub = row_sub(t, d)
        sid = sub['id']
        pass_next = q(todo_href, done=sid, msg=pass_msg, link=q(done_href, new=sid, act='pass'), linkText='查看已办')
        reject_next = q(todo_href, done=sid, type='warn', msg=reject_msg or f'已退回稿件，系统已通知投稿人{sub["author"]}',
                        link=q(done_href, new=sid, act='reject'), linkText='查看已办')
        actions = (btn(pass_label, 'btn-success btn-lg', 'check', f'data-action="pass" data-opinion="optional" data-tpl="{tpl}" data-title="{pass_label}" data-ok="确认" data-msg="{pass_msg}" data-next="{pass_next}"') +
                   btn(reject_text, 'btn-danger-o btn-lg', reject_icon, f'data-action="reject" data-tpl="{tpl}" data-title="{reject_title}" data-label="{reject_label}" data-ok="确认{reject_text}" data-next="{reject_next}"'))
        timer = (d['rem'], d['lv']) if d else ('剩余 3 个工作日', 'ok')
        start = d['start'] if d else sub['time']
        arrive = d['arrive'] if d else sub['time']
        body = review_body(sub, STATUS[stage], node, chart_cur(sub['identity'], stage), timer, flow_records(sub, stage), actions, todo_href,
                           identity=sub['identity'], start=start, arrive=arrive, extra_right=extra_right)
        page(typed(handle, t), '办理', body, [crumbs_active, f'{TYPE_NAME[t]}审核'], '', todo_href)
        out[t] = (sid, sub['title'], t, sub['author'], sub['college'])
    return out


def type_done_pages(page, node, back_href, done_file='done-detail.html'):
    from detail import flow_records, chart_cur, sub_content, sample_for
    from workflow import detail_body
    from data import typed
    for t in ('视频', '照片', '线索'):
        sub = sample_for(t)
        stage, status = SAMPLE_STAGE[t]
        body = detail_body(sub, status, 'tag-solid-ok', node_chart(sub['identity'], chart_cur(sub['identity'], stage)), flow_records(sub, stage),
                           back_href, sub['time'], sub['time'], sub_content(sub))
        page(typed(done_file, t), '已办详情', body, ['已办', f'{TYPE_NAME[t]}审核'], '', back_href)
