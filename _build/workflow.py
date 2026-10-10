# 统一待办：对齐智慧学工“我的待办”模块（待办 / 已办 / 催办抄送 / 批量审批 / 办理页 / 详情页）
from datetime import datetime, timedelta
from lib import icon, tag, btn, a_btn, filter_select, filter_bar, table
from data import TYPE_NAME, typed, deputy_of

NAMES = ['陈雨桐', '黄思远', '孙铭泽', '郭晓彤', '林嘉懿', '周子墨', '许若彤', '唐诗涵', '高子轩', '梁思雨', '韩博文', '宋可欣']
TIMING = {'over': '已超时', 'warn': '即将超时', 'ok': '正常'}


def shift(ts, hours):
    return (datetime.strptime(ts, '%Y-%m-%d %H:%M') - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M')


def flow_name(t, title):
    return f'{TYPE_NAME[t]}审核：《{title}》'


def flow_type(flow):
    return next((t for t, n in TYPE_NAME.items() if flow.startswith(n)), '新闻')


def norm(rows, kind):
    """统一待办行：sid, title, t, col, ident, author, start, arrive, rem, lv"""
    out = []
    for i, r in enumerate(rows):
        if kind == 'teacher':
            sid, title, t, author, time, rem, lv = r
            out.append(dict(sid=sid, title=title, t=t, col='计算机学院', ident='学生', author=author, start=time, arrive=time, rem=rem, lv=lv))
        elif kind == 'deputy':
            sid, title, t, author, ident, time, rem, lv = r
            start = shift(time, 3 + 46 / 60) if ident == '学生' else time
            out.append(dict(sid=sid, title=title, t=t, col='计算机学院', ident=ident, author=author, start=start, arrive=time, rem=rem, lv=lv))
        else:
            sid, title, t, col, ident, time, rem, lv = r
            author = '陈雨桐' if sid == 'TG2026092801' else NAMES[(i * 5 + len(title)) % len(NAMES)]
            back = {'r1': 9, 'r2': 29, 'r3': 52}[kind]
            out.append(dict(sid=sid, title=title, t=t, col=col, ident=ident, author=author, start=shift(time, back), arrive=time, rem=rem, lv=lv))
    order = {'over': 0, 'warn': 1, 'ok': 2}
    return sorted(out, key=lambda d: (order[d['lv']], d['arrive']))


def text_filter(tid, key, label, ph):
    return (f'<label class="f-box"><span class="f-lbl">{label}</span><input class="input" data-filter="{key}" data-contains data-live '
            f'data-for="{tid}" placeholder="{ph}"></label>')


def search_block(tid, ctrls):
    return f'<div class="card wf-search">{filter_bar(tid, ctrls)}</div>'


def starter(d):
    return f'{d["author"]}<div class="t-sub">{d["col"]} · {d["ident"]}</div>'


def seq_head():
    return ('序号', 'class="seq-h"')


# ---------- 待办 ----------
def todo_body(tid, rows, node, handle_href):
    trs = ''
    for i, d in enumerate(rows):
        over = ' class="overdue"' if d['lv'] == 'over' else ''
        fn = flow_name(d['t'], d['title'])
        h = typed(handle_href, d['t'])
        trs += (f'<tr{over} data-row-id="{d["sid"]}" data-level="{d["lv"]}" data-timing="{TIMING[d["lv"]]}" data-type="{d["t"]}" data-college="{d["col"]}" '
                f'data-flow="{fn} {d["sid"]}" data-starter="{d["author"]} {d["col"]}">'
                f'<td class="seq">{i + 1}</td><td><a class="t-title" href="{h}">{fn}</a><div class="t-sub">{d["sid"]}</div></td>'
                f'<td>{node}</td><td>{starter(d)}</td><td>{d["start"]}</td><td>{d["arrive"]}</td>'
                f'<td><div class="ops"><a class="link" href="{h}">办理</a></div></td></tr>')
    ctrls = (text_filter(tid, 'flow', '流程名称', '请输入') + text_filter(tid, 'starter', '发起人', '请输入姓名') +
             filter_select(tid, 'timing', '全部时效', ['已超时', '即将超时', '正常']))
    head = [seq_head(), '流程名称', '当前节点', '发起人', ('发起时间', 'data-sort'), ('到达时间', 'data-sort'), ('操作', 'class="no-export"')]
    return f'''{search_block(tid, ctrls)}
<div class="card wf-table">{table(tid, head, [trs], page_size=15)}</div>'''


# ---------- 已办 ----------
def done_body(tid, rows, node, detail_href, statuses, new_row=None, export_name='已办记录'):
    """rows: (sid, title, t, author, col, status, opinion, time, cost, timing)"""
    trs = ''
    for nr in (new_row if isinstance(new_row, list) else [new_row] if new_row else []):
        sid, title, t, author, col, time = nr
        fn = flow_name(t, title)
        trs += (f'<tr class="hidden" data-when-param="new={sid}" data-highlight data-flow="{fn}" data-starter="{author} {col}">'
                f'<td class="seq">1</td><td><a class="t-title" href="{typed(detail_href, t)}">{fn}</a><div class="t-sub">{sid}</div></td><td>{node}</td><td>{author}<div class="t-sub">{col}</div></td>'
                f'<td class="tc"><span data-when-param="act=pass">{tag(statuses[0])}</span><span data-when-param="act=reject">{tag(statuses[1])}</span></td>'
                f'<td class="c-muted">刚刚提交的审核意见</td><td>{time}</td><td>{tag("及时")}</td><td><div class="ops"><a class="link" href="{typed(detail_href, t)}">详情</a></div></td></tr>')
    for i, (sid, title, t, author, col, st, op, time, cost, ok) in enumerate(rows):
        fn = flow_name(t, title)
        h = typed(detail_href, t)
        trs += (f'<tr data-status="{st}" data-ok="{ok}" data-type="{t}" data-flow="{fn} {sid}" data-starter="{author} {col}">'
                f'<td class="seq">{i + 1}</td><td><a class="t-title" href="{h}">{fn}</a><div class="t-sub">{sid}</div></td><td>{node}</td>'
                f'<td>{author}<div class="t-sub">{col}</div></td><td class="tc">{tag(st)}</td><td class="wf-op" title="{op}">{op}</td><td>{time}</td>'
                f'<td>{tag(ok)}<div class="t-sub">用时 {cost}</div></td><td><div class="ops"><a class="link" href="{h}">详情</a></div></td></tr>')
    ctrls = (text_filter(tid, 'flow', '流程名称', '请输入') + text_filter(tid, 'starter', '发起人', '请输入姓名') +
             filter_select(tid, 'status', '全部流程状态', list(statuses)))
    head = [seq_head(), '流程名称', '节点', '发起人', ('流程状态', 'class="tc"'), '意见', ('处理时间', 'data-sort'), '时效', ('操作', 'class="no-export"')]
    exp = btn('导出', '', 'download', f'data-action="export-csv" data-table="#{tid}" data-filename="{export_name}"')
    tools = (f'<div class="wf-tools">{exp}'
             f'<span class="hint">处理时效按到达本节点起 3 个工作日计算，超时记录同步记入超时台账</span></div>')
    return f'''{search_block(tid, ctrls)}
<div class="card wf-table">{tools}{table(tid, head, [trs], page_size=15)}</div>'''


# ---------- 催办 / 抄送 ----------
def cc_body(urges, copies, handle_href, detail_href):
    """urges: (flow, task, who, created, urged)；copies: (flow, task, who, time, read)"""
    hh = lambda f: typed(handle_href, flow_type(f))
    dh = lambda f: typed(detail_href, flow_type(f))
    u = ''.join(f'<tr data-flow="{f}" data-task="{tk}" data-who="{w}"><td class="seq">{i + 1}</td><td><a class="t-title" href="{hh(f)}">{f}</a></td><td>{tk}</td><td>{w}</td><td>{c}</td><td>{ur}</td>'
                f'<td><div class="ops"><a class="link" href="{hh(f)}">办理</a></div></td></tr>' for i, (f, tk, w, c, ur) in enumerate(urges))
    c = ''.join(f'<tr data-flow="{f}" data-task="{tk}" data-who="{w}"><td class="seq">{i + 1}</td><td><a class="t-title" href="{dh(f)}">{f}</a></td><td>{tk}</td><td>{w}</td><td>{t}</td>'
                f'<td class="tc">{tag(rd)}</td><td><div class="ops"><a class="link" href="{dh(f)}">查看</a></div></td></tr>' for i, (f, tk, w, t, rd) in enumerate(copies))
    uc = text_filter('urgeTable', 'flow', '流程名称', '流程名称') + text_filter('urgeTable', 'task', '任务名称', '任务名称') + text_filter('urgeTable', 'who', '催办人', '催办人')
    cc = text_filter('copyTable', 'flow', '流程名称', '流程名称') + text_filter('copyTable', 'task', '任务名称', '任务名称') + text_filter('copyTable', 'who', '抄送人', '抄送人')
    return f'''<div class="card wf-sheet" data-tabs-scope>
<div class="tabs" data-tabs><button class="tab on" data-tab="urge">催办消息<span class="cnt">{len(urges)}</span></button><button class="tab" data-tab="copy">抄送消息<span class="cnt">{len(copies)}</span></button></div>
<div class="tab-panel on" data-panel="urge">{filter_bar('urgeTable', uc)}{table('urgeTable', [seq_head(), '流程名称', '任务名称', '催办人', ('任务创建时间', 'data-sort'), ('催办时间', 'data-sort'), ('操作', 'class="no-export"')], [u], page_size=15)}</div>
<div class="tab-panel" data-panel="copy">{filter_bar('copyTable', cc)}{table('copyTable', [seq_head(), '流程名称', '任务名称', '抄送人', ('抄送时间', 'data-sort'), ('状态', 'class="tc"'), ('操作', 'class="no-export"')], [c], page_size=15)}</div>
</div>'''


# ---------- 批量审批 ----------
def batch_body(rows, node, handle_href, tpl='review'):
    tid = 'batchTable'
    trs = ''
    for i, d in enumerate(rows):
        fn = flow_name(d['t'], d['title'])
        trs += (f'<tr data-row-id="{d["sid"]}" data-type="{d["t"]}" data-flow="{fn} {d["sid"]}" data-college="{d["col"]}" data-starter="{d["author"]}">'
                f'<td><input type="checkbox" class="row-check" aria-label="选择"></td><td class="seq">{i + 1}</td>'
                f'<td><a class="t-title" href="{typed(handle_href, d["t"])}">{fn}</a></td><td>{d["col"]}</td><td>{node}</td><td>{d["author"]}</td><td>{d["start"]}</td>'
                f'<td><div class="ops"><a class="link" href="{typed(handle_href, d["t"])}">办理</a></div></td></tr>')
    cats = [('全部待办', ''), ('新闻投稿审核', '新闻'), ('视频投稿审核', '视频'), ('照片投稿审核', '照片'), ('新闻线索审核', '线索')]
    cat_html = ''.join(f'<button class="wf-cat{" on" if i == 0 else ""}" data-tab="c{i}" data-filter-table="#{tid}" data-filter-key="type" data-filter-value="{v}">'
                       f'<span>{n}</span><em>{sum(1 for d in rows if not v or d["t"] == v)}</em></button>' for i, (n, v) in enumerate(cats))
    ctrls = text_filter(tid, 'flow', '流程名称', '流程名称') + text_filter(tid, 'college', '学院名称', '学院名称') + text_filter(tid, 'starter', '发起人', '发起人')
    ops = (btn('批量通过', 'btn-batch-ok', 'check', f'data-action="batch" data-table="#{tid}" data-title="批量通过" data-confirm="确认将选中的 {{n}} 条待办批量{node}通过吗？批量通过不填写意见，请确认已逐篇核对内容。" data-msg="已批量通过 {{n}} 条稿件，已流转至下一环节"') +
           btn('批量不通过', 'btn-batch-no', 'x-circle', f'data-action="batch-reject" data-table="#{tid}" data-tpl="{tpl}"'))
    head = [('<input type="checkbox" class="check-all" aria-label="全选">', 'class="no-export" style="width:50px"'), seq_head(), '流程名称', '学院名称', '当前任务', '发起人',
            ('发起时间', 'data-sort'), ('操作', 'class="no-export"')]
    return f'''<div class="card wf-sheet">{filter_bar(tid, ctrls)}
<div class="wf-batch">
  <div class="wf-cats" data-tabs><div class="wf-cats-title">流程分类<em>{len(cats) - 1}</em></div>{cat_html}</div>
  <div class="wf-batch-main"><div class="wf-tools">{ops}<span class="ml-auto hint">当前任务</span><span class="tag tag-primary">{node}</span></div>
  {table(tid, head, [trs], page_size=15)}</div>
</div></div>'''


# ---------- 节点流程图 ----------
def node_chart(identity='学生', cur=1, back_at=None, end='采用归档'):
    names = (['开始', '指导老师审核', '副书记审核', '一审', '二审', '三审终审', end] if identity == '学生'
             else ['开始', '副书记审核', '一审', '二审', '三审终审', end])
    out = []
    for i, n in enumerate(names):
        if back_at is not None and i == back_at:
            cls, mark, st = 'back', '!', '退回'
        elif i < cur:
            cls, mark, st = 'done', '✓', '通过'
        elif i == cur:
            cls, mark, st = 'cur', '●', '办理中'
        else:
            cls, mark, st = '', '○', '待处理'
        out.append(f'<div class="wf-node {cls}"><i>{mark}</i><b>{n}</b><span>{st}</span></div>')
    return '<div class="wf-nodes">' + '<span class="wf-arrow">→</span>'.join(out) + '</div>'


def bd_grid(cells):
    return '<div class="bd-grid">' + ''.join(f'<div class="bd-cell"><span>{k}</span><b>{v}</b></div>' for k, v in cells) + '</div>'


def base_cells(sub, start, arrive):
    return [('稿件编号', sub['id']), ('稿件类型', TYPE_NAME[sub['type']]), ('投稿人', f'{sub["author"]}（{sub["identity"]}）'), ('所属学院', sub['college']),
            ('指导老师', sub.get('teacher', '—') if sub['identity'] == '学生' else '—（教师投稿无需指定）'),
            ('副书记', f'{deputy_of(sub["college"])} · 学工系统'), ('流程发起时间', start), ('到达本节点时间', arrive)]


def sec(title, body, extra=''):
    return f'<div class="wf-sec"><div class="flex between"><div class="section-title">{title}</div>{extra}</div>{body}</div>'


def flow_panel(chart, timeline_html):
    return (f'<div class="wf-flow-panel"><div class="wf-sub">节点流程图</div>{chart}'
            f'<div class="wf-sub mt20">操作日志</div>{timeline_html}</div>')


# ---------- 已办详情 ----------
def detail_body(sub, status, status_cls, chart, timeline_html, back_href, start, arrive, article_html):
    top = (f'<div class="card wf-sheet wf-top"><div class="flex gap12"><div class="section-title">{TYPE_NAME[sub["type"]]}审核</div>'
           f'<span class="tag tag-solid {status_cls}">{status}</span><span class="hint">《{sub["title"]}》</span></div>'
           f'{a_btn("返回已办", back_href, "", "arrow-l")}</div>')
    body = (sec('基础信息', bd_grid(base_cells(sub, start, arrive))) + sec('稿件内容', f'<div class="wf-article">{article_html}</div>') +
            sec('审批流程', flow_panel(chart, timeline_html)))
    return f'{top}<div class="card wf-sheet-body">{body}</div>'
