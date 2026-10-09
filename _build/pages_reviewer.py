# PC 端 · 一审员 / 二审员（结构相同，节点与数据不同）
from lib import icon, tag, type_tag, card, page_head, btn, a_btn, filter_select, search_box, \
    date_range, filter_bar, table, pc_page, write
from data import R1_TODO, R2_TODO, FEATURED, ADOPTED, ARCHIVE, COLLEGES, typed, TYPE_NAME
from common import featured_flow_timeline, adopted_timeline, messages_page_body, info_kv, op_log_table
from review import review_body, reject_modal, q, type_review_pages, type_done_pages, SAMPLE_STAGE
from detail import sub_content, full_detail, default_logs, sample_for
from workflow import norm, todo_body, done_body, cc_body, batch_body, detail_body, node_chart, flow_name, NAMES
from publish import publish_panel, export_buttons

SID = FEATURED['id']
TPL_REVIEW = ['标题过长，请控制在 30 字以内并突出新闻点。', '正文存在错别字和标点不规范问题，请仔细校对。',
              '图片涉及人物肖像，请确认已取得本人同意。', '内容与团学工作关联度不高，建议调整报道角度。']

CONF = {
    'reviewer1': dict(kind='r1', node='一审', status='待一审', cur=3, upto='r1', todo=R1_TODO, next_node='二审', arrive='2026-09-28 16:35',
                      user='刘子涵', peers='一审员共 6 人（学生干部，按学期轮换）'),
    'reviewer2': dict(kind='r2', node='二审', status='待二审', cur=4, upto='r2', todo=R2_TODO, next_node='三审终审', arrive='2026-09-29 11:20',
                      user='周明轩', peers='二审员共 3 人（高年级学生干部，按学年换届）'),
}


def todo_rows(c):
    rows = [(SID, FEATURED['title'], '新闻', '计算机学院', '学生', c['arrive'], '剩余 2.5 个工作日', 'ok')] + c['todo']
    order = {'over': 0, 'warn': 1, 'ok': 2}
    rows.sort(key=lambda r: (order[r[7]], r[5]))
    return rows


def build_for(role):
    c = CONF[role]
    P = f'pc/{role}/'
    node = c['node']
    rows = todo_rows(c)
    n_todo = len(rows)
    n_over = sum(1 for r in rows if r[7] == 'over')
    n_warn = sum(1 for r in rows if r[7] == 'warn')
    pass_next = q('todo.html', done=SID, msg=f'{node}通过，稿件已流转至{c["next_node"]}', link=q('my-ledger.html', new=SID, act='pass'), linkText='查看已办')
    reject_next = q('todo.html', done=SID, type='warn', msg='已退回稿件，系统已通知投稿人陈雨桐', link=q('my-ledger.html', new=SID, act='reject'), linkText='查看已办')

    def page(file, title, body, crumbs=None, modals='', active=None):
        write(P + file, pc_page(role, active or file, title, body, crumbs=crumbs, modals=modals, todo_count=n_todo))

    # ---------- 待办 ----------
    wrows = norm(rows, c['kind'])
    page('todo.html', '待办', todo_body('todoTable', wrows, node, 'review.html'), ['待办'])

    # ---------- 审核页 ----------
    actions = (btn(f'{node}通过，提交{c["next_node"]}', 'btn-success btn-lg', 'check', f'data-action="pass" data-opinion="optional" data-title="{node}通过" data-ok="确认通过" data-msg="{node}通过，已提交{c["next_node"]}" data-next="{pass_next}"') +
               a_btn('退回修改', 'review-reject.html', 'btn-danger-o btn-lg', 'undo'))
    for rej in (False, True):
        body = review_body(FEATURED, c['status'], node, c['cur'], ('剩余 2.5 个工作日', 'ok'), featured_flow_timeline(c['upto']), actions, 'todo.html',
                           start=FEATURED['time'], arrive=c['arrive'])
        modals = reject_modal('rejectBox', '退回稿件', '退回意见', TPL_REVIEW, reject_next) if rej else ''
        page('review-reject.html' if rej else 'review.html', '办理', body, ['待办', '新闻投稿审核'], modals, active='todo.html')

    made = type_review_pages(page, wrows, node, c['kind'], 'todo.html', 'my-ledger.html', 'review', f'{node}通过，提交{c["next_node"]}',
                             f'{node}通过，稿件已流转至{c["next_node"]}', '待办')
    new_rows = [(sid, title, t, author, col, '2026-09-30 16:40') for sid, title, t, author, col in made.values()]
    type_done_pages(page, node, 'my-ledger.html')

    # ---------- 稿件查询 ----------
    trs = ''
    for sid, title, t, col, author, ident, d, st in ARCHIVE:
        can = t == '新闻' and st in ('已终审采用', '已发布')
        pub = f'<span class="tag tag-success">可导出</span>' if can else '<span class="c-muted">—</span>'
        h = typed('submission-detail.html', t)
        trs += (f'<tr data-college="{col}" data-type="{t}" data-status="{st}" data-date="{d}"><td><a class="t-title" href="{h}">{title}</a><div class="t-sub">{sid}</div></td>'
                f'<td>{type_tag(t)}</td><td>{col}</td><td>{author}（{ident}）</td><td>{d}</td><td>{tag(st)}</td><td>{pub}</td>'
                f'<td><a class="link" href="{h}">查看档案</a></td></tr>')
    ctrls = filter_select('subTable', 'college', '全部学院', COLLEGES) + filter_select('subTable', 'type', '全部类型', ['新闻', '视频', '照片', '线索']) + \
        filter_select('subTable', 'status', '全部状态', ['待指导老师审核', '待副书记审核', '待一审', '待二审', '待三审', '已退回', '已终审采用', '已终审不采用', '已发布']) + date_range('subTable') + search_box('subTable')
    body = f'''{page_head('稿件查询', '可浏览全校全部稿件档案，按学院、类型、时间范围、状态组合筛选', btn('导出查询结果', '', 'download', 'data-action="export-csv" data-table="#subTable" data-filename="稿件查询结果"'))}
<div class="card">{filter_bar('subTable', ctrls)}{table('subTable', ['稿件', '类型', '投稿学院', '投稿人', ('投稿日期', 'data-sort'), '流转状态', '升华网素材', ('操作', 'class="no-export"')], [trs])}</div>'''
    page('submissions.html', '稿件查询', body)

    # ---------- 稿件档案（已终审采用的新闻稿） ----------
    logs = op_log_table(default_logs(ADOPTED, 'adopted'))
    body = f'''{page_head(f'{ADOPTED["title"]} {tag("已终审采用")}', f'稿件编号 {ADOPTED["id"]} · 新闻投稿 · 商学院 · 计入采用统计', a_btn('返回查询', 'submissions.html', '', 'arrow-l') + export_buttons())}
<div class="grid g-main-wide">
  <div class="card" data-tabs-scope>
    <div class="tabs" data-tabs><button class="tab on" data-tab="content">稿件内容</button><button class="tab" data-tab="pub">升华网发布素材</button><button class="tab" data-tab="flow">流转记录</button><button class="tab" data-tab="log">操作日志</button></div>
    <div class="tab-panel on card-body" data-panel="content">{sub_content(ADOPTED)}</div>
    <div class="tab-panel card-body" data-panel="pub">{publish_panel()}</div>
    <div class="tab-panel card-body" data-panel="flow">{adopted_timeline()}</div>
    <div class="tab-panel" data-panel="log">{logs}</div>
  </div>
  <div class="grid" style="align-content:start">
    {card('投稿信息', info_kv(ADOPTED), 'file')}
    {card('稿件状态', '<div class="flex between"><span class="c-muted">流转状态</span>' + tag('已终审采用') + '</div><div class="flex between mt12"><span class="c-muted">统计归档</span>' + tag('计入采用') + '</div><div class="flex between mt12"><span class="c-muted">升华网发布</span><span class="tag tag-gray">待管理员标记</span></div>', 'tag')}
  </div>
</div>'''
    page('submission-detail.html', '稿件档案', body, ['稿件查询', '稿件档案'], active='submissions.html')
    for t in ('视频', '照片', '线索'):
        sub = sample_for(t)
        stage, status = SAMPLE_STAGE[t]
        head = page_head(f'{sub["title"]} {tag(status)}', f'稿件编号 {sub["id"]} · {TYPE_NAME[t]} · {sub["college"]} · 稿件档案永久保存', a_btn('返回查询', 'submissions.html', '', 'arrow-l'))
        page(typed('submission-detail.html', t), '稿件档案', head + full_detail(sub, status, stage), ['稿件查询', '稿件档案'], active='submissions.html')

    # ---------- 已办 ----------
    hist = [
        ('TG2026092702', '学院“算法之星”编程挑战赛精彩瞬间', '照片', '计算机学院', '2026-09-29 15:20', '已通过', '0.6 个工作日', '及时', '构图完整，同意报送。'),
        ('TG2026092601', '湘雅医学院新生开学第一课', '新闻', '湘雅医学院', '2026-09-29 10:05', '已退回', '1.1 个工作日', '及时', '导语过长，请压缩至 150 字以内。'),
        ('TG2026092503', '新生军训风采纪实短片《淬炼》', '视频', '计算机学院', '2026-09-26 17:30', '已通过', '0.4 个工作日', '及时', '视频链接有效，同意报送。'),
        ('TG2026092305', '湘雅医学院“医路同行”义诊进社区', '新闻', '湘雅医学院', '2026-09-26 09:10', '已通过', '3.5 个工作日', '超时', '同意报送。'),
        ('TG2026092203', '“青春志愿行”社区服务周纪实', '新闻', '计算机学院', '2026-09-21 09:20', '已通过', '0.7 个工作日', '及时', '修改到位，同意报送。'),
        ('TG2026091502', ADOPTED['title'], '新闻', '商学院', '2026-09-17 09:40', '已通过', '0.5 个工作日', '及时', '要素齐全。'),
        ('TG2026090909', '化工学院实验室安全月启动', '新闻', '化学化工学院', '2026-09-15 14:20', '已退回', '2 个工作日', '及时', '配图涉及人物肖像，请确认授权。'),
        ('TG2026091304', '资源学院“矿业报国”主题宣讲短片', '视频', '资源与安全工程学院', '2026-09-14 09:30', '已通过', '4 个工作日', '超时', '同意报送。'),
    ]
    drows = [(sid, title, t, NAMES[(i * 7 + 3) % len(NAMES)], col, st, op, time, cost, ok) for i, (sid, title, t, col, time, st, cost, ok, op) in enumerate(hist)]
    body = done_body('ledger', drows, node, 'done-detail.html', ('已通过', '已退回'),
                     [(SID, FEATURED['title'], '新闻', '陈雨桐', '计算机学院', '2026-09-30 16:40')] + new_rows, f'{node}已办记录')
    page('my-ledger.html', '已办', body, ['已办'])

    # ---------- 催办 / 抄送 ----------
    overs = [d for d in wrows if d['lv'] == 'over']
    urges = [(flow_name(d['t'], d['title']), node, '系统（超时自动催办）', d['arrive'], '2026-09-30 09:00') for d in overs]
    urges.append((flow_name('新闻', FEATURED['title']), node, '张静（校团委管理员）', c['arrive'], '2026-09-30 10:15'))
    copies = [(flow_name('新闻', ADOPTED['title']), '三审终审', '张静（校团委管理员）', '2026-09-19 10:30', '已读'),
              (flow_name('照片', '学院“算法之星”编程挑战赛精彩瞬间'), '三审终审', '张静（校团委管理员）', '2026-09-30 11:00', '未读')]
    page('cc.html', '催办/抄送', cc_body(urges, copies, 'review.html', 'done-detail.html'), ['催办/抄送'])

    # ---------- 批量审批 ----------
    page('batch.html', '批量审批', batch_body(wrows, node, 'review.html'), ['批量审批'])

    # ---------- 已办详情 ----------
    body = detail_body(ADOPTED, '已终审采用', 'tag-solid-ok', node_chart('学生', 7), adopted_timeline(), 'my-ledger.html',
                       ADOPTED['time'], ADOPTED['times']['deputy'] if node == '一审' else ADOPTED['times']['r1'], sub_content(ADOPTED))
    page('done-detail.html', '已办详情', body, ['已办', '新闻投稿审核'], active='my-ledger.html')

    # ---------- 消息 ----------
    items = [
        ('inbox', 'blue', f'新的待{node}稿件', f'《{FEATURED["title"]}》已到达{node}环节，请在 3 个工作日内处理', '30 分钟前', 'review.html', True),
        ('alert', 'red', '审核超时预警', f'有 {n_over} 篇稿件已超过审核时限，已记入超时台账，请尽快处理', '今天 09:00', 'todo.html', True),
        ('clock', 'orange', '即将超时提醒', f'有 {n_warn} 篇稿件剩余时限不足 1 个工作日', '今天 09:00', 'todo.html', True),
        ('check-circle', 'green', '您审核的稿件已终审采用', f'《{ADOPTED["title"]}》已由校团委终审采用', '09-19 10:30', 'submission-detail.html'),
        ('bell', 'blue', '系统通知', '国庆假期（10月1日—7日）不计入审核工作日，节后审核时效顺延', '09-26 17:00', 'messages.html'),
    ]
    page('messages.html', '消息通知', messages_page_body(items))


def build():
    build_for('reviewer1')
    build_for('reviewer2')
