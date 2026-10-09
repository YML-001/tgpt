# PC 端 · 校团委管理员（三审终审 + 后台管理）
from lib import icon, tag, type_tag, remain, stat, card, page_head, btn, a_btn, options, filter_select, search_box, \
    date_range, filter_bar, table, field, modal, pc_page, write
from data import R3_TODO, FEATURED, ADOPTED, ARCHIVE, RANKING, TIMEOUTS, COLLEGES, typed, type_of, TYPE_NAME
from common import featured_flow_timeline, adopted_timeline, messages_page_body, article, gallery, info_kv, \
    op_log_table, rank_rows, donut, bars, hbars, college_detail_modal
from review import review_body, reject_modal, q, type_review_pages, SAMPLE_STAGE
from detail import sub_content, full_detail, default_logs, sample_for
from workflow import norm, todo_body, done_body, cc_body, batch_body, flow_name
from publish import publish_panel, export_buttons

R = 'admin'
P = 'pc/admin/'
SID = FEATURED['id']
TPL_FINAL = ['稿件时效性已过，不予采用。', '同类题材近期已有报道，不予采用。', '内容与团学工作关联度不高，不予采用。']


def page(file, title, body, crumbs=None, modals='', active=None, css=''):
    write(P + file, pc_page(R, active or file, title, body, crumbs=crumbs, modals=modals, css=css))


def ops_edit(modal_id, title):
    return (f'<div class="ops"><button class="link" data-action="crud-edit" data-modal="{modal_id}" data-title="{title}">编辑</button>'
            f'<button class="link link-danger" data-action="delete-row">删除</button></div>')


def crud_modal(mid, fields, table_id, tpl_id, size='modal-sm'):
    body = f'<form novalidate><div class="form-grid" style="grid-template-columns:1fr 1fr">{fields}</div></form>'
    foot = (f'<button class="btn" data-close>取消</button>'
            f'<button class="btn btn-primary" data-action="crud-save" data-table="#{table_id}" data-template="#{tpl_id}">保存</button>')
    return modal(mid, '新增', body, foot, size)


TERM_TEXT = {'2026 秋季学期': '2026-09-01 至 2027-01-31', '2026 春季学期': '2026-02-01 至 2026-07-31',
             '2026—2027 学年': '2026-09-01 至 2027-08-31', '2025—2026 学年': '2025-09-01 至 2026-08-31'}


def term_range(start, end, name='term'):
    return (f'<div class="f-box f-date f-range" data-range="{name}">'
            f'<input type="date" class="input" name="{name}From" required data-label="任期开始日期" data-default="{start}" value="{start}" aria-label="任期开始日期">'
            f'<span class="f-to">至</span>'
            f'<input type="date" class="input" name="{name}To" required data-label="任期结束日期" data-default="{end}" value="{end}" aria-label="任期结束日期">'
            f'<input type="hidden" name="{name}"></div>')


STAFF_CSV_HEAD = '姓名,工号,所在学院,职务,任期开始,任期结束'


def staff_fields(college_lbl, duty_key, duty_ph, no_ph, term):
    tip = '输入工号自动回显姓名、学院、职务，也可输入姓名检索'
    lookup = (f'<div class="staff-picker"><input class="input" name="no" required data-staff-lookup data-label="工号" placeholder="请输入工号，如 {no_ph}" autocomplete="off">'
              f'<div class="picker-list"></div></div>'
              f'<div class="staff-tip"><span data-staff-msg data-default-msg="{tip}">{tip}</span>'
              f'<button type="button" class="link" data-action="staff-manual">手动填写</button></div>')
    more = 'js-staff-more'
    return (field('工号', lookup, req=True, full=True) +
            field('姓名', '<input class="input" name="name" required placeholder="请输入姓名">', req=True, cls=more) +
            field(college_lbl, f'<select class="select" name="college" required>{options(COLLEGES, "请选择")}</select>', req=True, cls=more) +
            field('职务', f'<input class="input" name="{duty_key}" required placeholder="{duty_ph}">', req=True, cls=more) +
            field('任期', term_range(*term), req=True, full=True, cls=more))


def switch(on=True, name=''):
    return f'<button class="switch{" on" if on else ""}" aria-label="启用开关" data-on-msg="{name}已启用" data-off-msg="{name}已停用" data-confirm-off="停用后该账号将无法登录并失去相应权限，确认停用吗？"></button>'


# ---------- 1 统计驾驶舱 ----------
def dashboard():
    month = [('3月', [48, 30]), ('4月', [62, 35]), ('5月', [58, 40]), ('6月', [41, 22]), ('7月', [26, 12]), ('8月', [33, 17]), ('9月', [96, 58])]
    colleges = [(c, a, s) for c, s, a, b in RANKING[:10]]
    nodes = [('指导老师审核', 0.8, 3.1, 96.9), ('副书记审核', 0.6, 2.4, 97.6), ('一审', 1.1, 5.4, 94.6), ('二审', 0.9, 4.2, 95.8), ('三审终审', 1.3, 6.0, 94.0)]
    node_html = ''.join(f'<div class="hbar"><span class="hb-name">{n}</span><div class="hb-track"><i style="width:{ok}%;background:#1BB975"></i><i style="width:{100 - ok}%;background:#F6BCBE"></i></div><span class="hb-val">{ok}%</span></div>'
                        f'<div class="hint" style="margin:-8px 0 12px 120px">平均处理 {avg} 个工作日 · 超时率 {over}%</div>' for n, avg, over, ok in nodes)
    kpi = lambda total, news, video, photo, clue, adopt, rej, back, rate: f'''<div class="grid g5">
{stat('layers', 'blue', total, '全校投稿总量', f'新闻 {news} · 视频 {video} · 照片 {photo} · 线索 {clue}', 'archive.html')}
{stat('check-circle', 'green', adopt, '终审采用', f'采用率 {adopt / total * 100:.1f}%', 'archive.html')}
{stat('x-circle', 'gray', rej, '终审不采用', '', 'archive.html')}
{stat('undo', 'red', back, '退回次数', '含多次退回', 'archive.html')}
{stat('clock', 'orange', rate, '审核及时率', '超时 38 次', 'timeout-ledger.html', unit='%')}
</div>'''
    csv = '统计项,数值\\n全校投稿总量,1024\\n新闻,532\\n视频,146\\n照片,248\\n线索,98\\n终审采用,562\\n终审不采用,140\\n退回次数,131\\n审核及时率,94.8%'
    body = f'''{page_head('统计驾驶舱', '全校投稿、采用、退回与审核时效全局统计；数据实时更新', btn('导出统计报表', 'btn-primary', 'download', f'data-action="export-csv" data-csv="{csv}" data-filename="投稿平台统计报表"'))}
<div data-tabs-scope>
<div class="flex between mb16"><div class="seg" data-tabs><button class="on" data-tab="y">2026—2027 学年</button><button data-tab="s">本学期</button><button data-tab="m">本月</button><button data-tab="l">2025—2026 学年</button></div><span class="hint">数据更新于 2026-09-30 16:00</span></div>
<div class="tab-panel on" data-panel="y">{kpi(1024, 532, 146, 248, 98, 562, 140, 131, '94.8')}</div>
<div class="tab-panel" data-panel="s">{kpi(412, 215, 58, 101, 38, 226, 55, 49, '95.3')}</div>
<div class="tab-panel" data-panel="m">{kpi(154, 80, 22, 37, 15, 58, 12, 19, '93.9')}</div>
<div class="tab-panel" data-panel="l">{kpi(2381, 1204, 342, 598, 237, 1320, 356, 301, '92.1')}</div>
</div>
<div class="grid g-main mt16">
  {card('月度投稿与采用趋势', bars(month, ('#3087CC', '#B0CEE4'), 230) + '<div class="legend mt12"><span><i style="background:#3087CC"></i>终审采用</span><span><i style="background:#B0CEE4"></i>其他（审核中 / 未采用）</span></div>', 'trend')}
  {card('稿件类型分布', donut([('新闻投稿', 532, '#3087CC'), ('照片投稿', 248, '#1BB975'), ('视频投稿', 146, '#F29100'), ('新闻线索', 98, '#9CBFDA')], 116, 20, ('1024', '篇稿件')), 'layers')}
</div>
<div class="grid g2 mt16">
  {card('各学院投稿与采用（前 10）', hbars(colleges) + '<div class="legend"><span><i style="background:#3087CC"></i>采用</span><span><i style="background:#B0CEE4"></i>投稿</span></div>', 'chart', '<a class="link" href="ranking.html">完整排行 ›</a>')}
  {card('审核时效统计', node_html + '<div class="legend"><span><i style="background:#1BB975"></i>及时</span><span><i style="background:#F6BCBE"></i>超时</span></div>', 'clock', '<a class="link" href="timeout-ledger.html">超时台账 ›</a>')}
</div>
<div class="grid g3 mt16">
  <a class="card stat" href="final-list.html"><div class="stat-ic orange">{icon('inbox', 22)}</div><div><div class="stat-num">7</div><div class="stat-label">待三审稿件 · 1 篇已超时</div></div>{icon('chev-r', 18, 'ml-auto')}</a>
  <a class="card stat" href="timeout-ledger.html"><div class="stat-ic red">{icon('alert', 22)}</div><div><div class="stat-num">5</div><div class="stat-label">当前超时未处理</div></div>{icon('chev-r', 18, 'ml-auto')}</a>
  <a class="card stat" href="publish-export.html"><div class="stat-ic blue">{icon('globe', 22)}</div><div><div class="stat-num">3</div><div class="stat-label">已采用新闻待发布升华网</div></div>{icon('chev-r', 18, 'ml-auto')}</a>
</div>'''
    page('dashboard.html', '统计驾驶舱', body)


# ---------- 2-4 三审终审 ----------
def final_rows():
    rows = [(SID, FEATURED['title'], '新闻', '计算机学院', '学生', '2026-09-30 09:00', '剩余 3 个工作日', 'ok')] + R3_TODO
    order = {'over': 0, 'warn': 1, 'ok': 2}
    return sorted(rows, key=lambda r: (order[r[7]], r[5]))


def final_list():
    rows = norm(final_rows(), 'r3')
    page('final-list.html', '待办', todo_body('finalTable', rows, '三审终审', 'final-review.html'), ['我的待办', '待办'])


def final_done():
    base = [
        ('TG2026091502', ADOPTED['title'], '新闻', '赵一帆', '商学院', '已采用', '内容质量较高，予以采用，计入学院采用统计。', '2026-09-19 10:30', '1 个工作日', '及时'),
        ('TG2026091805', '学生党支部开展“红色经典诵读”活动', '新闻', '陈雨桐', '计算机学院', '已采用', '同意采用。', '2026-09-19 10:10', '0.8 个工作日', '及时'),
        ('TG2026091706', '地学院“地质之美”标本摄影', '照片', '许若彤', '地球科学与信息物理学院', '不采用', '同类题材近期已有报道，不予采用。', '2026-09-18 16:20', '1.2 个工作日', '及时'),
        ('TG2026091603', '能源学院“双碳”科普志愿行', '新闻', '韩博文', '能源科学与工程学院', '已采用', '同意采用。', '2026-09-17 11:40', '3.4 个工作日', '超时'),
        ('TG2026091508', '体育部秋季运动会筹备纪实', '视频', '高子轩', '体育教研部', '不采用', '稿件时效性已过，不予采用。', '2026-09-16 09:30', '0.6 个工作日', '及时'),
    ]
    body = done_body('finalDone', base, '三审终审', 'archive-detail.html', ('已采用', '不采用'), export_name='三审终审已办记录')
    page('final-done.html', '已办', body, ['我的待办', '已办'])


def final_cc():
    rows = norm(final_rows(), 'r3')
    urges = [(flow_name(d['t'], d['title']), '三审终审', '系统（超时自动催办）', d['arrive'], '2026-09-30 09:00') for d in rows if d['lv'] == 'over']
    copies = [(flow_name('新闻', '“青春志愿行”社区服务周纪实'), '二审', '周明轩（二审员）', '2026-09-22 14:18', '已读'),
              (flow_name('线索', '校友返校讲述“北斗”研发故事'), '一审', '刘子涵（一审员）', '2026-09-25 10:20', '未读')]
    page('final-cc.html', '催办/抄送', cc_body(urges, copies, 'final-review.html', 'archive-detail.html'), ['我的待办', '催办/抄送'])


def final_batch():
    page('final-batch.html', '批量审批', batch_body(norm(final_rows(), 'r3'), '三审终审', 'final-review.html', 'final'), ['我的待办', '批量审批'])


def final_review(reject=False):
    adopt_next = q('final-list.html', done=SID, msg='已终审采用，稿件计入计算机学院采用统计', link='archive-detail.html', linkText='查看稿件档案')
    reject_next = q('final-list.html', done=SID, type='warn', msg='已终审不采用，不计入采用统计，已通知投稿人')
    actions = (btn('终审采用', 'btn-success btn-lg', 'check', f'data-action="pass" data-opinion="optional" data-tpl="final" data-title="终审采用" data-label="终审意见" data-ok="确认采用" data-msg="已终审采用，计入学院采用统计" data-next="{adopt_next}"') +
               a_btn('终审不采用', 'final-reject.html', 'btn-danger-o btn-lg', 'x-circle'))
    extra = card('终审规则', f'<div style="font-size:13px;line-height:1.9;color:var(--text-2)">· 采用：流转状态变为【已终审采用】，统计归档属性为【计入采用】，参与学院排行榜。<br>· 不采用：必须填写终审意见，状态为【已终审不采用】，不计入采用统计。<br>· 新闻类采用稿件可导出升华网发布素材。</div>', 'book')
    body = review_body(FEATURED, '待三审', '三审终审', 5, ('剩余 3 个工作日', 'ok'), featured_flow_timeline('r3'), actions, 'final-list.html', extra_right=extra,
                       start=FEATURED['time'], arrive='2026-09-30 09:00')
    modals = reject_modal('rejectBox', '终审不采用', '终审意见', TPL_FINAL, reject_next, ok='确认不采用', cancel='final-review.html') if reject else ''
    page('final-reject.html' if reject else 'final-review.html', '办理', body, ['待办', '新闻投稿审核'], modals, active='final-list.html')
    if not reject:
        type_review_pages(page, norm(final_rows(), 'r3'), '三审终审', 'r3', 'final-list.html', 'final-done.html', 'final', '终审采用',
                          '已终审采用，计入学院采用统计', '待办', reject_title='终审不采用', reject_label='终审意见', reject_text='终审不采用',
                          reject_icon='x-circle', reject_msg='已终审不采用，不计入采用统计，已通知投稿人', handle='final-review.html', extra_right=extra)


# ---------- 5-6 稿件档案库 ----------
def archive():
    trs = ''
    for sid, title, t, col, author, ident, d, st in ARCHIVE:
        adopt = '计入采用' if st in ('已终审采用', '已发布') else '不计入采用'
        pub = '<a class="link" href="publish-export.html">发布素材</a>' if t == '新闻' and st == '已终审采用' else ''
        trs += (f'<tr data-college="{col}" data-type="{t}" data-status="{st}" data-adopt="{adopt}" data-identity="{ident}" data-date="{d}">'
                f'<td><input type="checkbox" class="row-check" aria-label="选择"></td><td><a class="t-title" href="{typed("archive-detail.html", t)}">{title}</a><div class="t-sub">{sid}</div></td>'
                f'<td>{type_tag(t)}</td><td>{col}</td><td>{author}</td><td>{ident}</td><td>{d}</td><td>{tag(st)}</td><td>{tag(adopt)}</td>'
                f'<td><div class="ops"><a class="link" href="{typed("archive-detail.html", t)}">档案</a>{pub}</div></td></tr>')
    ctrls = (search_box('archTable', '标题 / 编号 / 投稿人') + filter_select('archTable', 'college', '全部学院', COLLEGES) +
             filter_select('archTable', 'type', '全部类型', ['新闻', '视频', '照片', '线索']) +
             filter_select('archTable', 'status', '审核流转状态', ['待指导老师审核', '待副书记审核', '待一审', '待二审', '待三审', '已退回', '已终审采用', '已终审不采用', '已发布']) +
             filter_select('archTable', 'adopt', '是否终审采用', ['计入采用', '不计入采用']) + filter_select('archTable', 'identity', '投稿身份', ['学生', '教师']) + date_range('archTable'))
    body = f'''{page_head('稿件档案库', '全校所有稿件永久存档，支持跨学年历史查询与多条件组合检索', btn('导出', '', 'download', 'data-open="exportModal"'))}
<div class="grid g5 mb16">{stat('archive', 'blue', 1024, '本学年档案')}{stat('file', 'blue', 532, '新闻')}{stat('video', 'orange', 146, '视频')}{stat('image', 'green', 248, '照片')}{stat('bulb', 'orange', 98, '线索')}</div>
<div class="card">{filter_bar('archTable', ctrls)}
{table('archTable', [('<input type="checkbox" class="check-all" aria-label="全选">', 'class="no-export" style="width:36px"'), '稿件', '类型', '学院', '投稿人', '身份', ('投稿日期', 'data-sort'), '流转状态', '统计归档', ('操作', 'class="no-export"')], [trs])}</div>'''
    page('archive.html', '稿件档案库', body, ['稿件与数据', '稿件档案库'], export_modal())


def archive_detail():
    logs = op_log_table(default_logs(ADOPTED, 'adopted')[:1] + [('2026-09-15 16:52', '赵一帆（投稿人 · 学生）', '编辑稿件：修改标题（“挑战杯获奖” → 现标题）', '10.12.40.77')]
                        + default_logs(ADOPTED, 'adopted')[1:])
    versions = f'''<table class="tbl"><thead><tr><th>版本</th><th>提交时间</th><th>标题</th><th>说明</th></tr></thead><tbody>
<tr><td><span class="tag tag-primary">v1 当前</span></td><td>2026-09-15 16:40</td><td>{ADOPTED["title"]}</td><td>首次提交即通过全部审核</td></tr></tbody></table>
<div class="notice notice-info mt16">{icon('info', 15)}<div>稿件档案禁止直接覆盖旧内容，每次修改都保留版本记录。</div></div>'''
    body = f'''{page_head(f'{ADOPTED["title"]} <span id="pubTag">{tag("已终审采用")}</span>', f'稿件编号 {ADOPTED["id"]} · 新闻投稿 · 商学院 · 档案永久保存', a_btn('返回档案库', 'archive.html', '', 'arrow-l') + export_buttons())}
<div class="grid g-main-wide">
  <div class="card" data-tabs-scope>
    <div class="tabs" data-tabs><button class="tab on" data-tab="content">稿件内容</button><button class="tab" data-tab="pub">升华网发布素材</button><button class="tab" data-tab="flow">完整流转记录</button><button class="tab" data-tab="ver">修改历史</button><button class="tab" data-tab="log">操作日志</button></div>
    <div class="tab-panel on card-body" data-panel="content">{sub_content(ADOPTED)}</div>
    <div class="tab-panel card-body" data-panel="pub">{publish_panel()}</div>
    <div class="tab-panel card-body" data-panel="flow">{adopted_timeline()}</div>
    <div class="tab-panel card-body" data-panel="ver">{versions}</div>
    <div class="tab-panel" data-panel="log">{logs}</div>
  </div>
  <div class="grid" style="align-content:start">
    <div class="card action-card"><b>稿件状态管理</b>
      <div class="flex between"><span class="c-muted">流转状态</span><span class="js-pub">{tag('已终审采用')}</span></div>
      <div class="flex between"><span class="c-muted">统计归档</span>{tag('计入采用')}</div>
      <div class="flex between"><span class="c-muted">升华网发布</span><span class="tag tag-gray" id="pubState">未发布</span></div>
      {btn('标记为已发布', 'btn-primary', 'globe', 'id="markPub" data-action="set-status" data-target="#pubTag .tag, .js-pub .tag, #pubState" data-value="已发布" data-hide="#markPub" data-title="标记为已发布" data-confirm="请确认已在升华网完成该新闻的发布。标记后稿件状态将变为【已发布】。" data-log="标记稿件为已发布"')}
      <div class="hint">完成升华网发布后，需在此将稿件标记为【已发布】。</div>
    </div>
    {card('投稿信息', info_kv(ADOPTED), 'file')}
  </div>
</div>'''
    page('archive-detail.html', '稿件档案详情', body, ['稿件档案库', '稿件档案详情'], active='archive.html')
    for t in ('视频', '照片', '线索'):
        sub = sample_for(t)
        stage, status = SAMPLE_STAGE[t]
        if t == '线索':
            side = card('线索处置', f'<div class="flex between"><span class="c-muted">流转状态</span>{tag(status)}</div><div class="hint mt12">终审采用后进入线索跟进：待跟进 → 已跟进 → 已转为正式新闻。</div>'
                        + a_btn('打开线索跟进', 'clue-tracking.html', 'btn-primary mt12', 'bulb', 'style="width:100%"'), 'bulb')
            acts = a_btn('三审终审', 'final-review-clue.html', 'btn-primary', 'award')
        else:
            side = card('稿件状态', f'<div class="flex between"><span class="c-muted">流转状态</span>{tag(status)}</div><div class="flex between mt12"><span class="c-muted">统计归档</span>{tag("计入采用")}</div>'
                        '<div class="hint mt12">视频、照片类稿件不导出升华网正文，原图 / 云盘链接可在“稿件内容”中查看。</div>', 'tag')
            acts = ''
        head = page_head(f'{sub["title"]} {tag(status)}', f'稿件编号 {sub["id"]} · {TYPE_NAME[t]} · {sub["college"]} · 档案永久保存',
                         a_btn('返回档案库', 'archive.html', '', 'arrow-l') + acts)
        page(typed('archive-detail.html', t), '稿件档案详情', head + full_detail(sub, status, stage, side=side), ['稿件档案库', '稿件档案详情'], active='archive.html')


# ---------- 7 升华网发布素材 ----------
def publish_export():
    pending = [
        (ADOPTED['id'], ADOPTED['title'], '商学院', '2026-09-19', '未发布'),
        ('TG2026091805', '计算机学院学生党支部开展“红色经典诵读”活动', '计算机学院', '2026-09-24', '未发布'),
        ('TG2026090610', '土木学院教授获詹天佑奖', '土木工程学院', '2026-09-11', '未发布'),
        ('TG2026090411', '冶金学院新生入学教育', '冶金与环境学院', '2026-09-08', '已发布'),
        ('TG2026090113', '自动化学院暑期实践总结会', '自动化学院', '2026-09-05', '已发布'),
    ]
    trs = ''
    for i, (sid, title, col, d, st) in enumerate(pending):
        cur = ' style="background:#F2F9FE"' if i == 0 else ''
        st_html = f'<span class="tag tag-primary">已发布</span>' if st == '已发布' else f'<span class="tag tag-warn {"js-row-pub" if i == 0 else ""}">待发布</span>'
        op = '<span class="c-muted">当前选中</span>' if i == 0 else ('<a class="link" href="archive-detail.html">查看</a>' if st == '已发布' else '<a class="link" href="archive-detail.html">处理</a>')
        trs += f'<tr{cur} data-status="{st}"><td><a class="t-title" href="archive-detail.html">{title}</a><div class="t-sub">{sid}</div></td><td>{col}</td><td>{d}</td><td>{st_html}</td><td>{op}</td></tr>'
    logs = op_log_table([('2026-09-29 15:02', '周明轩（二审员）', '导出升华网素材包（TG2026090411）', '10.12.8.66'),
                         ('2026-09-29 14:58', '周明轩（二审员）', '复制升华网可用正文（TG2026090411）', '10.12.8.66')])
    body = f'''{page_head('升华网发布素材', '已终审采用的新闻稿件，可复制清洗后的正文或导出素材包，人工发布到升华网（博达站群）后标记为已发布')}
<div class="card mb16"><div class="card-head"><div class="card-title">{icon('list', 18)}已采用新闻稿件</div>{filter_select('pubTable', 'status', '全部发布状态', ['未发布', '已发布'])}</div>
{table('pubTable', ['稿件', '学院', '终审日期', '发布状态', '操作'], [trs], pager=False)}</div>
<div class="card"><div class="card-head"><div class="card-title">{icon('globe', 18)}{ADOPTED["title"]}</div>
{btn('标记为已发布', 'btn-success', 'check', 'id="markPub2" data-action="set-status" data-target=".js-row-pub" data-value="已发布" data-hide="#markPub2" data-title="标记为已发布" data-confirm="请确认已在升华网完成该新闻的发布。标记后稿件状态将变为【已发布】。" data-log="标记稿件为已发布（TG2026091502）"')}</div>
<div class="card-body">{publish_panel()}</div></div>
<div class="card mt16"><div class="card-head"><div class="card-title">{icon('terminal', 18)}素材复制 / 导出日志</div><span class="hint">复制、导出、标记发布行为实时记入日志</span></div>{logs}</div>'''
    page('publish-export.html', '升华网发布素材', body, ['稿件与数据', '升华网发布素材'])


# ---------- 8 线索跟进 ----------
def clue_tracking():
    clues = [
        ('TG2026092004', '校友返校讲述“北斗”研发故事', '计算机学院', '陈雨桐', '是', '10月8日—15日 下午', '待跟进', '—'),
        ('TG2026092910', '土木学院学子获全国结构设计竞赛一等奖', '土木工程学院', '何静怡', '是', '工作日 14:00—17:00', '待跟进', '—'),
        ('TG2026092806', '交通学院志愿者服务国庆返乡专列', '交通运输工程学院', '李一航', '是', '10月1日—7日', '已跟进', '刘子涵'),
        ('TG2026091201', '湘雅医学院援疆医疗队返校', '湘雅医学院', '孙雅婷', '否', '—', '已跟进', '周明轩'),
        ('TG2026090610', '土木学院教授获詹天佑奖', '土木工程学院', '何静怡', '是', '已完成采访', '已转为正式新闻', '张静'),
        ('TG2026082715', '数学学院学霸宿舍专访', '数学与统计学院', '杨柳', '是', '—', '无需处理', '张静'),
    ]
    opts = ['待跟进', '已跟进', '已转为正式新闻', '无需处理']
    trs = ''
    link_attr = ' data-open="linkModal"'
    for sid, title, col, who, iv, when, st, owner in clues:
        sel = ''.join(f'<option value="{o}"{" selected" if o == st else ""}{link_attr if o == "已转为正式新闻" else ""}>{o}</option>' for o in opts)
        trs += (f'<tr data-status="{st}"><td><a class="t-title" href="archive-detail-clue.html">{title}</a><div class="t-sub">{sid}</div></td><td>{col}</td><td>{who}</td>'
                f'<td>{iv}</td><td>{when}</td><td><span class="tag js-tag {("tag-warn" if st == "待跟进" else "tag-primary" if st == "已跟进" else "tag-success" if st == "已转为正式新闻" else "tag-gray")}">{st}</span></td><td>{owner}</td>'
                f'<td><div class="flex gap8"><select class="select" style="height:30px;font-size:12px;min-width:120px" data-set-tag aria-label="修改处置状态">{sel}</select>'
                f'<button class="link" data-open="followModal">跟进记录</button></div></td></tr>')
    news = options([f'{r[0]} {r[1]}' for r in ARCHIVE if r[2] == '新闻' and r[7] in ('已终审采用', '已发布')], '请选择已采用的正式新闻稿件')
    news_field = field('正式新闻稿件', f'<select class="select" required>{news}</select>', req=True)
    follow_field = field('新增跟进记录', '<textarea class="textarea" required placeholder="记录本次跟进的情况，如联系结果、采访安排"></textarea>', req=True)
    modals = modal('linkModal', '关联正式新闻', f'<form novalidate><div class="notice notice-info mb16">{icon("link", 15)}<div>线索状态改为“已转为正式新闻”时，请关联由该线索采写形成的正式稿件。</div></div>{news_field}</form>',
                   '<button class="btn" data-close>稍后关联</button><button class="btn btn-primary" data-action="save" data-msg="已关联正式新闻，线索状态更新为“已转为正式新闻”">确认关联</button>', 'modal-sm') + \
        modal('followModal', '线索跟进记录', f'''<div class="timeline mb16"><div class="tl-item"><span class="tl-dot ok"></span><div class="tl-head">已联系线索提供人</div><div class="tl-meta">刘子涵 · 2026-09-29 15:00</div><div class="tl-opinion">已电话确认采访时间，计划 10 月 9 日下午赴学院采访。</div></div>
<div class="tl-item"><span class="tl-dot primary"></span><div class="tl-head">线索审核通过，进入跟进</div><div class="tl-meta">系统 · 2026-09-27 10:00</div></div></div>
<form novalidate>{follow_field}</form>''',
                  '<button class="btn" data-close>关闭</button><button class="btn btn-primary" data-action="save" data-msg="跟进记录已保存">保存记录</button>')
    body = f'''{page_head('线索跟进', '新闻线索类稿件的处置追踪：待跟进 → 已跟进 → 已转为正式新闻；状态修改记入操作日志')}
<div class="grid g4 mb16">{stat('bulb', 'orange', 2, '待跟进')}{stat('users', 'blue', 2, '已跟进')}{stat('check-circle', 'green', 1, '已转为正式新闻')}{stat('minus', 'gray', 1, '无需处理')}</div>
<div class="card"><div class="filters">{filter_select('clueTable', 'status', '全部处置状态', opts)}{search_box('clueTable', '搜索线索标题 / 学院')}</div>
{table('clueTable', ['线索', '学院', '提供人', '接受采访', '可采访时间', '处置状态', '跟进人', ('操作', 'class="no-export"')], [trs])}</div>'''
    page('clue-tracking.html', '线索跟进', body, ['审核管理', '线索跟进'], modals)


# ---------- 9 超时台账 ----------
def timeout_ledger():
    trs = ''
    for sid, title, nd, who, arrive, done, over, st in TIMEOUTS:
        op = f'<button class="link" data-toast="已向 {who} 发送催办提醒（站内消息 + 移动端推送）" data-toast-type="success">催办</button>' if st == '处理中' else '<span class="c-muted">—</span>'
        trs += (f'<tr data-node="{nd}" data-who="{who}" data-status="{st}"><td><a class="t-title" href="{typed("archive-detail.html", type_of(sid, title))}">{title}</a><div class="t-sub">{sid}</div></td>'
                f'<td>{nd}</td><td>{who}</td><td>{arrive}</td><td>{done}</td><td class="overdue-txt">{over}</td><td>{tag(st)}</td><td>{op}</td></tr>')
    nodes = [('指导老师审核', 12, 386), ('副书记审核', 5, 342), ('一审', 14, 259), ('二审', 8, 190), ('三审终审', 4, 67)]
    nh = ''.join(f'<div class="hbar"><span class="hb-name">{n}</span><div class="hb-track"><i style="width:{o / t * 100 * 8:.0f}%;background:#DF2027"></i></div><span class="hb-val">{o / t * 100:.1f}%</span></div>' for n, o, t in nodes)
    ctrls = filter_select('toTable', 'node', '全部节点', ['指导老师审核', '副书记审核', '一审', '二审', '三审']) + filter_select('toTable', 'who', '全部审核人', sorted(set(t[3] for t in TIMEOUTS))) + \
        filter_select('toTable', 'status', '全部状态', ['处理中', '已处理']) + search_box('toTable', '搜索稿件')
    body = f'''{page_head('审核超时台账', '稿件到达审核节点后超过 3 个工作日未处理即记为超时；时限可在“业务参数”中调整', btn('导出超时台账', 'btn-primary', 'download', 'data-action="export-csv" data-format="Excel" data-table="#toTable" data-filename="审核超时台账"'))}
<div class="grid g5 mb16">{stat('alert', 'red', 38, '本学年超时次数')}{stat('clock', 'orange', 5, '当前超时未处理', '', None)}{stat('check', 'gray', 33, '超时后已处理')}{stat('check-circle', 'green', '94.8', '审核及时率', unit='%')}{stat('trend', 'red', '5.2', '审核超时率', unit='%')}</div>
<div class="grid g-main">
  <div class="card">{filter_bar('toTable', ctrls)}{table('toTable', ['稿件', '超时节点', '审核人', ('到达节点时间', 'data-sort'), '处理时间', '超时时长', '状态', ('操作', 'class="no-export"')], [trs])}</div>
  <div class="grid" style="align-content:start">{card('各节点超时率', nh + '<div class="hint">超时率 = 超时次数 / 节点处理总数</div>', 'chart')}
  {card('超时最多的审核人', ''.join(f'<div class="todo-item"><span class="rank-no{" r" + str(i + 1) if i < 3 else ""}">{i + 1}</span><div class="ti-main"><div class="ti-title">{n}</div><div class="ti-sub">{r}</div></div><b class="c-danger">{c} 次</b></div>' for i, (n, r, c) in enumerate([('刘子涵', '一审员', 6), ('王海峰', '指导老师', 4), ('周明轩', '二审员', 3), ('杨振华', '副书记', 2), ('陈思琪', '一审员', 2)])), 'users')}</div>
</div>'''
    page('timeout-ledger.html', '超时台账', body, ['审核管理', '超时台账'])


# ---------- 10 排行榜 ----------
def ranking():
    heads = [('排名', 'data-sort'), '学院', ('投稿量', 'data-sort'), ('采用量', 'data-sort'), ('退回量', 'data-sort'), ('采用率', 'data-sort'), '操作']
    mid = {c: f'rkDetail{i}' for i, (c, *_) in enumerate(RANKING)}
    link = lambda c: f'<button type="button" class="t-title link-btn" data-open="{mid[c]}">{c}</button>'
    act = lambda c: btn('查看明细', 'btn-sm', 'list', f'data-open="{mid[c]}"')
    sem = [(c, int(s * .45), int(a * .42), int(b * .5)) for c, s, a, b in RANKING]
    body = f'''{page_head('学院排行榜', '按终审采用数量排序，统计周期可在“业务参数”中配置；点击学院名称或“查看明细”在当前页查看该院稿件', btn('导出排行榜统计表', 'btn-primary', 'download', 'data-action="export-csv" data-format="Excel" data-table="#rankY" data-filename="学院排行榜统计表"'))}
<div class="card" data-tabs-scope>
  <div class="card-head"><div class="seg" data-tabs><button class="on" data-tab="year">2026—2027 学年</button><button data-tab="sem">2026 秋季学期</button><button data-tab="last">2025—2026 学年</button></div><span class="hint">仅统计“计入采用”的稿件</span></div>
  <div class="tab-panel on" data-panel="year">{table('rankY', heads, rank_rows(link, own='', action=act), page_size=20)}</div>
  <div class="tab-panel" data-panel="sem">{table('rankS', heads, rank_rows(link, own='', data=sem, action=act), page_size=20)}</div>
  <div class="tab-panel" data-panel="last">{table('rankL', heads, rank_rows(link, own='', data=[(c, s * 2 + 7, a * 2 + 3, b * 2) for c, s, a, b in RANKING], action=act), page_size=20)}</div>
</div>'''
    modals = ''.join(college_detail_modal(mid[c], c, (s, a, b)) for c, s, a, b in RANKING)
    page('ranking.html', '学院排行榜', body, ['稿件与数据', '学院排行榜'], modals=modals)


# ---------- 数据导出弹窗（档案库“导出”按钮） ----------
def export_modal():
    def csv_of(rows, head):
        return '\\n'.join([','.join(head)] + [','.join(str(x) for x in r) for r in rows])
    head = ['稿件编号', '标题', '类型', '学院', '投稿人', '身份', '投稿日期', '状态']
    all_csv = csv_of(ARCHIVE, head)
    col_csv = csv_of([r for r in ARCHIVE if r[3] == '计算机学院'], head)
    kinds = ('<div class="radio-group" style="flex-direction:column;align-items:stretch">'
             '<label class="radio-card"><input type="radio" name="expKind" value="cur" checked>当前筛选结果（<b data-total-for="archTable">0</b> 条）</label>'
             f'<label class="radio-card"><input type="radio" name="expKind" value="all">全校稿件总表（含状态与统计归档属性，{len(ARCHIVE)} 条）</label>'
             '<label class="radio-card"><input type="radio" name="expKind" value="college">分学院稿件明细表</label></div>')
    col_sel = f'<div class="field hidden" data-show-when="expKind=college"><label class="lbl">选择学院</label><select class="select" data-toast-change="已选择学院">{options(COLLEGES)}</select></div>'
    period = f'<select class="select" data-toast-change="统计周期已切换">{options(["2026—2027 学年", "2026 秋季学期", "2025—2026 学年", "自定义时间段"])}</select>'
    body = f'''<div class="notice notice-info mb16">{icon('info', 15)}<div>学院排行榜、超时审核台账可在对应页面直接导出；所有导出行为均记入操作日志。</div></div>
<div class="grid" style="gap:16px">{field('导出内容', kinds)}{col_sel}{field('统计周期', period)}
<div class="field"><label class="lbl">最近导出</label><div class="hint">2026-09-28 17:20 · 全校稿件总表 · Excel · 1024 条<br>2026-09-25 09:12 · 超时审核台账 · CSV · 36 条</div></div></div>'''
    def pair(attrs, kind):
        a = f'{attrs} data-show-when="expKind={kind}"'
        h = '' if kind == 'cur' else 'hidden'
        return btn('导出 CSV', h, 'download', a) + btn('导出 Excel', ('btn-primary ' + h).strip(), 'download', a + ' data-format="Excel"')
    foot = ('<button class="btn" data-close>取消</button>' +
            pair('data-action="export-csv" data-table="#archTable" data-filename="稿件档案检索结果" data-log="导出稿件档案检索结果"', 'cur') +
            pair(f'data-action="export-csv" data-csv="{all_csv}" data-filename="全校稿件总表" data-log="导出全校稿件总表"', 'all') +
            pair(f'data-action="export-csv" data-csv="{col_csv}" data-filename="分学院稿件明细表" data-log="导出分学院稿件明细表"', 'college'))
    return modal('exportModal', '导出稿件数据', body, foot, 'modal-sm')


# ---------- 12-15 人员名单 ----------
def reviewer_manage(level):
    is1 = level == 1
    members = [('刘子涵', '8209230115', '计算机学院', '宣传部干事', '2026 秋季学期', 186, True),
               ('陈思琪', '8208220321', '商学院', '宣传部干事', '2026 秋季学期', 142, True),
               ('王嘉乐', '8210230408', '文学院', '宣传部干事', '2026 秋季学期', 97, True),
               ('李梓萌', '8211240112', '外国语学院', '宣传部干事', '2026 秋季学期', 12, True),
               ('赵晨阳', '8209230533', '自动化学院', '宣传部干事', '2026 春季学期', 164, False),
               ('孙可欣', '8208220219', '法学院', '宣传部干事', '2026 春季学期', 131, False)] if is1 else \
              [('周明轩', '8207210118', '机电工程学院', '宣传部副部长', '2026—2027 学年', 158, True),
               ('吴雨桐', '8207210502', '湘雅医学院', '宣传部副部长', '2026—2027 学年', 121, True),
               ('郑浩然', '8207210233', '土木工程学院', '新媒体中心主任', '2026—2027 学年', 88, True),
               ('黄子轩', '8206200107', '资源与安全工程学院', '宣传部部长', '2025—2026 学年', 302, False)]
    mid, tid, tpl = f'r{level}Modal', f'r{level}Table', f'r{level}Tpl'
    trs = ''
    for name, no, col, duty, term, cnt, on in members:
        st = '在任' if on else '已离任'
        trs += (f'<tr data-status="{st}"><td><input type="checkbox" class="row-check" aria-label="选择"></td><td data-key="name" class="fw" style="color:var(--text)">{name}</td><td data-key="no">{no}</td><td data-key="college">{col}</td>'
                f'<td data-key="duty">{duty}</td><td data-key="term" class="nowrap">{TERM_TEXT[term]}</td><td class="num" data-key="count">{cnt}</td><td><span class="tag js-tag {"tag-success" if on else "tag-gray"}" data-on="在任" data-off="已离任">{st}</span></td>'
                f'<td>{switch(on, name)}</td><td>{ops_edit(mid, "编辑" + ("一审员" if is1 else "二审员"))}</td></tr>')
    tpl_row = (f'<template id="{tpl}"><tr data-status="在任"><td><input type="checkbox" class="row-check"></td><td data-key="name" class="fw" style="color:var(--text)">{{name}}</td><td data-key="no">{{no}}</td><td data-key="college">{{college}}</td>'
               f'<td data-key="duty">{{duty}}</td><td data-key="term" class="nowrap">{{term}}</td><td class="num" data-key="count">0</td><td><span class="tag js-tag tag-success" data-on="在任" data-off="已离任">在任</span></td>'
               f'<td>{switch(True)}</td><td>{ops_edit(mid, "编辑")}</td></tr></template>')
    fields = staff_fields('所在学院', 'duty', '如：宣传部干事' if is1 else '如：宣传部副部长', '8209230207' if is1 else '8208220101',
                          ('2026-09-01', '2027-01-31') if is1 else ('2026-09-01', '2027-08-31'))
    modals = crud_modal(mid, fields, tid, tpl)
    role = '一审员' if is1 else '二审员'
    sample = ('林书瑶,8209230207,数学与统计学院,宣传部干事,2026-09-01,2027-01-31\\n唐可馨,8210240316,交通运输工程学院,宣传部干事,2026-09-01,2027-01-31' if is1 else
              '李明远,8208220101,商学院,宣传部副部长,2026-09-01,2027-08-31\\n许嘉诚,8207210645,电子信息学院,新媒体中心副主任,2026-09-01,2027-08-31')
    tmpl_csv = f'{STAFF_CSV_HEAD}\\n{sample}'
    modals += modal(f'r{level}Import', f'批量导入{role}', f'''<div class="notice notice-info mb16">{icon('info', 15)}<div>请下载模板，按列填写 <b>姓名、工号、所在学院、职务、任期开始、任期结束</b>（日期格式 2026-09-01，UTF-8 编码 CSV）。已在名单中的工号、缺少字段的行会自动跳过，不会重复导入。</div></div>
<div class="flex gap8 mb16">{btn('下载导入模板', '', 'download', f'data-action="export-csv" data-csv="{tmpl_csv}" data-filename="{role}导入模板" data-keep="1"')}</div>
<label class="upload import-drop">{icon('upload', 26)}<b data-import-name>选择填写好的 CSV 文件</b><span class="hint">仅支持 .csv，选择后在下方预览校验结果</span><input type="file" accept=".csv,text/csv" data-import-file data-table="#{tid}"></label>
<div class="import-preview mt16" data-import-preview></div>''',
                    '<button class="btn" data-close>取消</button>' + btn('确认导入', 'btn-primary', 'check', f'data-action="staff-import" data-table="#{tid}" data-template="#{tpl}"'), 'modal-lg')
    new_term = ('2027-02-01', '2027-07-31') if is1 else ('2027-09-01', '2028-08-31')
    modals += modal(f'r{level}Term', f'{role}学年换届', f'''<div class="notice notice-warn mb16">{icon('alert', 15)}<div>勾选的人员<b>续任</b>：任期更新为新任期，保持在任；取消勾选的人员<b>离任</b>：标记“已离任”并停用账号，任期结束日改为新任期开始前一天。历史审核记录永久保留。</div></div>
<form novalidate><div class="form-grid" style="grid-template-columns:1fr 1fr">{field('新任期', term_range(*new_term, 'newTerm'), req=True, full=True, hint='开始日期即换届生效日期，结束日期须晚于开始日期')}</div></form>
<div class="term-head mt16"><label class="term-all"><input type="checkbox" data-term-all checked>全部续任</label><span class="hint" data-term-sum></span></div>
<div class="term-list" data-term-list></div>''',
                    '<button class="btn" data-close>取消</button>' + btn('确认换届', 'btn-primary', 'repeat', f'data-action="term-apply" data-table="#{tid}"'), 'modal-lg')
    extra_btn = (btn('导入', '', 'upload', f'data-action="staff-import-open" data-modal="r{level}Import"') +
                 btn('导出', '', 'download', f'data-action="export-staff" data-table="#{tid}" data-filename="{role}名单"') +
                 btn('学年换届', 'btn-outline', 'repeat', f'data-action="term-open" data-modal="r{level}Term" data-table="#{tid}"'))
    title = '一审员名单' if is1 else '二审员名单'
    desc = '一审由校团委宣传部学生干部承担，人员经常更换，可随时增减并启用 / 停用' if is1 else '二审由高年级学生干部承担，一年一换，支持按学年批量换届'
    body = f'''{page_head(title, desc, extra_btn + btn('批量停用', 'btn-danger-o', 'x-circle', f'data-action="batch" data-table="#{tid}" data-value="已离任" data-danger="1" data-confirm="确认停用选中的 {{n}} 名审核人员吗？停用后将收回审核权限。" data-msg="已停用 {{n}} 名审核人员"') + btn('新增' + ("一审员" if is1 else "二审员"), 'btn-primary', 'plus', f'data-action="crud-add" data-modal="{mid}" data-title="新增{"一审员" if is1 else "二审员"}"'))}
<div class="notice notice-info mb16">{icon('shield', 15)}<div>{"一审员仅可处理“待一审”稿件，不能操作二审和三审。" if is1 else "二审员仅可处理“待二审”稿件；三审终审仅限校团委管理员（宣传部老师）。"}审核权限可在“角色权限配置”中调整。</div></div>
<div class="card"><div class="filters">{filter_select(tid, 'status', '全部状态', ['在任', '已离任'])}{search_box(tid, '搜索姓名 / 工号 / 学院')}</div>
{table(tid, [('<input type="checkbox" class="check-all" aria-label="全选">', 'class="no-export" style="width:36px"'), '姓名', '工号', '所在学院', '职务', '任期', ('累计审核', 'data-sort'), '状态', '启用', ('操作', 'class="no-export"')], [trs])}</div>{tpl_row}'''
    page(f'reviewer{level}-manage.html', title, body, ['人员与权限', title], modals)


def teacher_manage():
    y1, y2 = '2026-09-01 至 2027-08-31', '2025-09-01 至 2027-08-31'
    teachers = [('王海峰', '200108', '计算机学院', '辅导员', 36, y2), ('李晓琳', '201532', '计算机学院', '辅导员', 21, y1), ('赵明哲', '199921', '商学院', '团委书记', 28, y2),
                ('孙雅婷', '201877', '湘雅医学院', '辅导员', 33, y1), ('周建国', '200356', '机电工程学院', '团委书记', 19, y2), ('吴芳芳', '201244', '文学院', '辅导员', 15, y1),
                ('郑一鸣', '201609', '外国语学院', '团委副书记', 17, y1), ('钱慧敏', '200988', '法学院', '辅导员', 12, y1), ('冯启航', '201713', '自动化学院', '团委书记', 22, y2),
                ('何静怡', '202015', '土木工程学院', '辅导员', 26, y1)]
    trs = ''.join(f'<tr data-college="{c}"><td data-key="name" class="fw" style="color:var(--text)">{n}</td><td data-key="no">{no}</td><td data-key="college">{c}</td><td data-key="title">{t}</td>'
                  f'<td data-key="term" class="nowrap">{term}</td><td class="num">{k}</td><td><span class="tag js-tag tag-success">启用</span></td><td>{switch(True, n)}</td><td>{ops_edit("tModal", "编辑指导老师")}</td></tr>'
                  for n, no, c, t, k, term in teachers)
    tpl = (f'<template id="tTpl"><tr><td data-key="name" class="fw" style="color:var(--text)">{{name}}</td><td data-key="no">{{no}}</td><td data-key="college">{{college}}</td><td data-key="title">{{title}}</td>'
           f'<td data-key="term" class="nowrap">{{term}}</td><td class="num">0</td><td><span class="tag js-tag tag-success">启用</span></td><td>{switch(True)}</td><td>{ops_edit("tModal", "编辑指导老师")}</td></tr></template>')
    fields = staff_fields('所属学院', 'title', '如：辅导员', '202103', ('2026-09-01', '2027-08-31'))
    tmpl_csv = '工号,姓名,所属学院,职务,任期开始日期,任期结束日期\\n200000,示例老师,计算机学院,辅导员,2026-09-01,2027-08-31'
    modals = crud_modal('tModal', fields, 'tTable', 'tTpl') + modal('importModal', '批量导入指导老师', f'''<div class="notice notice-info mb16">{icon('info', 15)}<div>请先下载导入模板，按模板填写后上传。工号重复的记录将自动更新。</div></div>
<div class="flex gap8 mb16">{btn('下载导入模板', '', 'download', f'data-action="export-csv" data-csv="{tmpl_csv}" data-filename="指导老师导入模板"')}</div>
<form novalidate>{'<div class="upload-field"><label class="upload">' + icon('upload', 26) + '<b>上传填写好的模板</b><span class="hint">支持 .xlsx / .csv</span><input type="file" accept=".xlsx,.csv" data-upload="doc" data-required data-min-files="1" data-label="导入文件"></label><div class="files"></div></div>'}</form>''',
                                                                   '<button class="btn" data-close>取消</button><button class="btn btn-primary" data-action="save" data-msg="导入成功：新增 12 名、更新 3 名指导老师">开始导入</button>')
    body = f'''{page_head('指导老师名单', '学生投稿只能从该名单中选择指导老师；投稿时默认预填上次选择的指导老师，也可搜索其他学院老师', btn('批量导入', '', 'upload', 'data-open="importModal"') + btn('新增指导老师', 'btn-primary', 'plus', 'data-action="crud-add" data-modal="tModal" data-title="新增指导老师"'))}
<div class="card"><div class="filters">{filter_select('tTable', 'college', '全部学院', COLLEGES)}{search_box('tTable', '搜索姓名 / 工号')}</div>
{table('tTable', ['姓名', '工号', '所属学院', '职务', '任期', ('指导稿件数', 'data-sort'), '状态', '启用', ('操作', 'class="no-export"')], [trs])}</div>{tpl}'''
    page('teacher-manage.html', '指导老师名单', body, ['人员与权限', '指导老师名单'], modals)


# ---------- 16 角色权限配置 ----------
PERM_ROLES = ['投稿人（全校师生）', '指导老师', '副书记（学工系统）', '一审员', '二审员', '校团委管理员']
DEPUTY_COL = 2
ADMIN_COL = 5
PERMS = [
    ('投稿', [('四类稿件投稿 / 草稿', [1, 0, 0, 0, 0, 0]), ('修改退回稿件并重提', [1, 0, 0, 0, 0, 0])]),
    ('审核', [('指导老师审核（学生稿件）', [0, 1, 0, 0, 0, 0]), ('副书记审核（本院稿件）', [0, 0, 1, 0, 0, 0]), ('一审', [0, 0, 0, 1, 0, 0]), ('二审', [0, 0, 0, 0, 1, 0]),
              ('三审终审', [0, 0, 0, 0, 0, 1]), ('填写 / 维护审核意见模板', [0, 0, 0, 0, 0, 1])]),
    ('查看', [('查看本人稿件与审核意见', [1, 1, 1, 1, 1, 1]), ('查看本院稿件明细与统计', [1, 1, 1, 0, 0, 1]), ('浏览全校稿件档案', [0, 0, 0, 1, 1, 1]), ('查看全校排行榜', [1, 1, 1, 1, 1, 1]), ('查看超时台账与操作日志', [0, 0, 0, 0, 0, 1])]),
    ('导出', [('导出本院稿件数据', [1, 0, 0, 0, 0, 1]), ('导出全校稿件台账', [0, 0, 0, 0, 0, 1]), ('升华网素材复制 / 导出', [0, 0, 0, 1, 1, 1]), ('标记稿件已发布', [0, 0, 0, 0, 0, 1])]),
    ('管理', [('人员名单与账号管理', [0, 0, 0, 0, 0, 1]), ('角色权限配置', [0, 0, 0, 0, 0, 1]), ('业务参数 / 敏感词配置', [0, 0, 0, 0, 0, 1])]),
]


def role_permission():
    rows = ''
    for group, items in PERMS:
        rows += f'<tr><td colspan="{len(PERM_ROLES) + 1}" style="background:#FAFBFC;font-weight:600;color:var(--text)">{group}</td></tr>'
        for name, flags in items:
            cells = ''
            for i, f in enumerate(flags):
                lock = ' disabled title="核心权限，不可取消"' if i == ADMIN_COL and name in ('三审终审', '角色权限配置') else ''
                if i == DEPUTY_COL:
                    lock = ' disabled title="副书记取自学工系统，无需配置"'
                cells += f'<td style="text-align:center"><input type="checkbox" aria-label="{PERM_ROLES[i]} - {name}"{" checked" if f else ""}{lock} data-toast-change="权限已修改，保存后生效"></td>'
            rows += f'<tr><td style="color:var(--text)">{name}</td>{cells}</tr>'
    scope = ''.join(f'<tr><td style="color:var(--text)">{r}</td><td><select class="select" data-toast-change="数据范围已修改，保存后生效">{options(s, selected=d)}</select></td><td class="c-muted">{h}</td></tr>'
                    for r, s, d, h in [('投稿人（全校师生）', ['本人', '本院', '全校'], '本院', '只能看本院稿件明细，看不到其他学院稿件详情'),
                                       ('指导老师', ['本人指导的稿件', '本院'], '本人指导的稿件', '仅审核指定自己为指导老师的学生稿件'),
                                       ('副书记（学工系统）', ['本院'], '本院', '待办只展示本院稿件的副书记审核环节；取自学工系统，无需配置'),
                                       ('一审员', ['分配给本人的环节', '全校'], '分配给本人的环节', '待办只展示一审环节稿件，可浏览全部稿件档案'),
                                       ('二审员', ['分配给本人的环节', '全校'], '分配给本人的环节', '待办只展示二审环节稿件，可浏览全部稿件档案'),
                                       ('校团委管理员', ['全校'], '全校', '全部稿件、审核记录与统计数据')])
    heads = ''.join(f'<th style="text-align:center">{r}</th>' for r in PERM_ROLES)
    body = f'''{page_head('角色权限配置', '所有审核与数据权限均在后台配置，不在代码中写死', btn('恢复默认', '', 'refresh', 'data-toast="已恢复为系统默认权限配置（尚未保存）"') + btn('保存配置', 'btn-primary', 'save', 'data-action="save" data-confirm="保存后权限立即生效，并记入操作日志。确认保存吗？" data-msg="权限配置已保存并生效，变更已记入操作日志"'))}
<div class="notice notice-info mb16">{icon('users', 15)}<div><b>投稿人（全校师生）无需单独开通账号：</b>全校教职工和学生通过统一身份认证登录即可投稿，所属学院取自统一身份认证。</div></div>
<div class="notice notice-info mb16">{icon('user', 15)}<div><b>副书记取自学工系统，无需配置：</b>副书记为投稿人所在学院的副书记，是学工系统的固定角色，本平台不维护名单、不分配人员；稿件按投稿人所在学院自动路由（学生稿件指导老师通过后、教师稿件提交后到达）。副书记的权限列已锁定。</div></div>
<div class="notice notice-warn mb16">{icon('shield', 15)}<div>规则约束：学生干部（一审员、二审员）不能操作三审；三审终审仅限校团委管理员（宣传部老师）。带锁的核心权限不可取消。</div></div>
<div class="card" data-tabs-scope><div class="tabs" data-tabs><button class="tab on" data-tab="func">功能权限</button><button class="tab" data-tab="data">数据范围</button></div>
<div class="tab-panel on" data-panel="func"><div class="table-wrap"><table class="tbl"><thead><tr><th>权限项</th>{heads}</tr></thead><tbody>{rows}</tbody></table></div></div>
<div class="tab-panel" data-panel="data"><div class="table-wrap"><table class="tbl"><thead><tr><th>角色</th><th style="width:220px">可查看数据范围</th><th>说明</th></tr></thead><tbody>{scope}</tbody></table></div></div></div>'''
    page('role-permission.html', '角色权限配置', body, ['人员与权限', '角色权限配置'])


# ---------- 17 业务参数 ----------
def params():
    types = ''.join(f'<tr><td class="fw" style="color:var(--text)">{n}</td><td>{d}</td><td>{switch(True, n)}</td></tr>' for n, d in
                    [('新闻投稿', '文字 + 图片，支持升华网素材导出'), ('视频投稿', '永久云盘链接'), ('照片投稿', '批量原图 + 单张备注'), ('新闻线索', '含线索处置状态')])
    periods = ''.join(f'<span class="chip">{p}<button type="button" class="chip-x" aria-label="移除">×</button></span>' for p in ['2026—2027 学年', '2026 秋季学期', '2027 春季学期', '2025—2026 学年'])
    holidays = ''.join(f'<span class="chip">{p}<button type="button" class="chip-x" aria-label="移除">×</button></span>' for p in ['2026-10-01 至 10-07 国庆节', '2027-01-15 至 02-25 寒假', '2027-04-05 清明节'])
    num = lambda v, n: f'<div class="flex gap8"><input type="number" class="input" name="{n}" min="1" max="15" step="0.5" value="{v}" required style="width:120px"><span class="c-muted">个工作日</span></div>'
    body = f'''{page_head('业务参数配置', '业务规则全部通过参数配置，修改后即时生效并记入操作日志', btn('保存全部参数', 'btn-primary', 'save', 'data-action="save" data-form="#paramForm" data-confirm="参数修改将影响后续所有稿件的审核计时与统计，确认保存吗？" data-msg="业务参数已保存并生效，已记入操作日志"'))}
<form id="paramForm" novalidate class="grid">
<div class="card"><div class="card-head"><div class="card-title">{icon('clock', 18)}审核时效</div><span class="hint">稿件到达节点开始计时，超时自动记入超时台账</span></div>
<div class="card-body"><div class="form-grid" style="grid-template-columns:repeat(5,1fr)">{field('指导老师审核时限', num(3, 't0'), req=True)}{field('副书记审核时限', num(3, 'td'), req=True)}{field('一审时限', num(3, 't1'), req=True)}{field('二审时限', num(3, 't2'), req=True)}{field('三审时限', num(3, 't3'), req=True)}</div>
<div class="form-grid mt16">{field('超时预警提前量', '<div class="flex gap8"><input type="number" class="input" value="1" min="0" step="0.5" style="width:120px" required><span class="c-muted">个工作日（剩余时限低于该值时标记“即将超时”）</span></div>', req=True)}
{field('节假日（不计入工作日）', f'<div class="chip-input"><div class="chips">{holidays}</div><div class="flex gap8"><input class="input" placeholder="如：2027-05-01 至 05-05 劳动节" style="flex:1"><button type="button" class="btn" data-action="add-chip">{icon("plus", 14)}添加</button></div></div>')}</div></div></div>
<div class="grid g2">
<div class="card"><div class="card-head"><div class="card-title">{icon('calendar', 18)}排行榜统计周期字典</div></div><div class="card-body"><div class="chip-input"><div class="chips">{periods}</div><div class="flex gap8"><input class="input" placeholder="新增统计周期，如 2027—2028 学年" style="flex:1"><button type="button" class="btn" data-action="add-chip">{icon("plus", 14)}添加</button></div></div>
<div class="mt16">{field('默认统计周期', f'<select class="select">{options(["2026—2027 学年", "2026 秋季学期"])}</select>')}</div></div></div>
<div class="card"><div class="card-head"><div class="card-title">{icon('layers', 18)}稿件类型字典</div></div><div class="table-wrap"><table class="tbl"><thead><tr><th>类型</th><th>说明</th><th>启用</th></tr></thead><tbody>{types}</tbody></table></div></div>
</div>
<div class="card"><div class="card-head"><div class="card-title">{icon('upload', 18)}文件上传限制</div></div><div class="card-body"><div class="form-grid g3c">
{field('单张图片大小上限', '<div class="flex gap8"><input type="number" class="input" value="20" required style="width:120px"><span class="c-muted">MB</span></div>', req=True)}
{field('允许的图片格式', '<input class="input" value="JPG, JPEG, PNG" required>', req=True)}
{field('原图存储', '<select class="select"><option>保存原图，不做压缩</option></select>', hint='升华网素材包需要原始图片')}</div></div></div>
</form>'''
    page('params.html', '业务参数', body, ['系统配置', '业务参数'])


# ---------- 18 审核意见模板 ----------
def opinion_templates():
    data = [('指导老师审核', '稿件导语不够精炼，请突出活动核心亮点后重新提交。', 42), ('指导老师审核', '配图数量不足或清晰度不够，请补充 3 张以上高清原图。', 37),
            ('指导老师审核', '活动时间、地点等要素缺失，请补全新闻五要素。', 29), ('副书记审核', '稿件政治导向需进一步把关，请修改相关表述后重新提交。', 9),
            ('副书记审核', '活动信息需与学院官方发布保持一致，请补充核实来源。', 6), ('一审 / 二审', '标题过长，请控制在 30 字以内并突出新闻点。', 88),
            ('一审 / 二审', '正文存在错别字和标点不规范问题，请仔细校对。', 64), ('一审 / 二审', '图片涉及人物肖像，请确认已取得本人同意。', 21),
            ('一审 / 二审', '云盘链接为临时分享链接，请更换为永久有效链接。', 18), ('三审终审', '稿件时效性已过，不予采用。', 15), ('三审终审', '同类题材近期已有报道，不予采用。', 12)]
    trs = ''.join(f'<tr data-scope="{s}"><td data-key="scope">{s}</td><td data-key="content" style="color:var(--text)">{c}</td><td class="num">{n}</td><td>{ops_edit("tplModal", "编辑意见模板")}</td></tr>' for s, c, n in data)
    tpl = f'<template id="tplTpl"><tr><td data-key="scope">{{scope}}</td><td data-key="content" style="color:var(--text)">{{content}}</td><td class="num">0</td><td>{ops_edit("tplModal", "编辑意见模板")}</td></tr></template>'
    fields = (field('适用环节', '<select class="select" name="scope" required><option value="">请选择</option><option>指导老师审核</option><option>副书记审核</option><option>一审 / 二审</option><option>三审终审</option></select>', req=True, full=True) +
              field('意见内容', '<textarea class="textarea" name="content" required maxlength="200" placeholder="请输入常用审核意见"></textarea>', req=True, full=True))
    body = f'''{page_head('审核意见模板', '维护常用审核意见，审核人员在退回 / 终审时可一键插入，提升审核效率', btn('新增模板', 'btn-primary', 'plus', 'data-action="crud-add" data-modal="tplModal" data-title="新增意见模板"'))}
<div class="card"><div class="filters">{filter_select('tplTable', 'scope', '全部环节', ['指导老师审核', '副书记审核', '一审 / 二审', '三审终审'])}{search_box('tplTable', '搜索意见内容')}</div>
{table('tplTable', ['适用环节', '意见内容', ('使用次数', 'data-sort'), ('操作', 'class="no-export"')], [trs])}</div>{tpl}'''
    page('opinion-templates.html', '审核意见模板', body, ['系统配置', '审核意见模板'], crud_modal('tplModal', fields, 'tplTable', 'tplTpl'))


# ---------- 19-20 敏感词 ----------
def sensitive_words():
    sets = {
        'high': ('高危敏感词', '命中后拦截提交', [('翻墙', '系统词库'), ('赌博', '系统词库'), ('代考', '系统词库'), ('枪支', '系统词库'), ('办证', '系统词库'), ('替考', '自定义'), ('博彩', '自定义')]),
        'low': ('低危敏感词', '命中后提示，不拦截', [('内部资料', '系统词库'), ('最牛', '自定义'), ('第一名校', '自定义'), ('绝对', '系统词库'), ('国家级', '系统词库')]),
        'white': ('白名单', '包含以下词组时不触发检测', [('国家级一流本科专业', '自定义'), ('国家级大学生创新创业训练计划', '自定义'), ('绝对值', '自定义')]),
    }
    tabs = ''
    panels = ''
    modals = ''
    for i, (k, (name, desc, words)) in enumerate(sets.items()):
        tabs += f'<button class="tab{" on" if i == 0 else ""}" data-tab="{k}">{name}<span class="cnt">{len(words)}</span></button>'
        trs = ''.join(f'<tr><td data-key="word" class="fw" style="color:var(--text)">{w}</td><td data-key="source">{s}</td><td>张静</td><td>2026-09-{10 + j:02d} 10:00</td><td>{ops_edit(k + "Modal", "编辑" + name)}</td></tr>' for j, (w, s) in enumerate(words))
        tpl = f'<template id="{k}Tpl"><tr><td data-key="word" class="fw" style="color:var(--text)">{{word}}</td><td data-key="source">自定义</td><td>张静</td><td>{{now}}</td><td>{ops_edit(k + "Modal", "编辑" + name)}</td></tr></template>'
        panels += f'''<div class="tab-panel{" on" if i == 0 else ""}" data-panel="{k}"><div class="filters">{search_box(k + "Table", "搜索敏感词")}<span class="hint">{desc}</span>
<div class="f-actions">{btn('批量导入', '', 'upload', 'data-toast="请上传 .txt 或 .xlsx 词表文件（每行一个词），演示环境已模拟导入 20 个词" data-toast-type="success"')}{btn('新增' + name, 'btn-primary', 'plus', f'data-action="crud-add" data-modal="{k}Modal" data-title="新增{name}"')}</div></div>
{table(k + "Table", ['敏感词', '来源', '创建人', '更新时间', ('操作', 'class="no-export"')], [trs])}{tpl}</div>'''
        modals += crud_modal(f'{k}Modal', field('词语', '<input class="input" name="word" required placeholder="请输入词语">', req=True, full=True), k + 'Table', k + 'Tpl')
    body = f'''{page_head('敏感词库', '系统内置市面通用敏感词库，并支持自定义高危词、低危词与白名单', btn('检测设置', '', 'settings', 'data-open="settingsModal"'))}
<div class="grid g4 mb16">{stat('shield', 'blue', '12,860', '通用词库词条', '最近更新 2026-09-01')}{stat('alert', 'red', 7, '自定义高危词')}{stat('info', 'orange', 5, '自定义低危词')}{stat('check-circle', 'green', 3, '白名单词组')}</div>
<div class="card" data-tabs-scope><div class="tabs" data-tabs>{tabs}</div>{panels}</div>'''
    page('sensitive-words.html', '敏感词库', body, ['系统配置', '敏感词库'], modals + settings_modal())


def settings_modal():
    body = f'''<div class="grid g2">
<div class="card" style="box-shadow:none"><div class="card-head"><div class="card-title">{icon('settings', 18)}检测规则</div></div><div class="card-body grid" style="gap:20px">
{field('检测模式', '<div class="radio-group"><label class="radio-card"><input type="radio" name="mode" value="semantic" checked>语义匹配</label><label class="radio-card"><input type="radio" name="mode" value="exact">精准匹配</label></div>', hint='语义匹配可识别“翻 墙”“替考”等变体写法；精准匹配只识别完全一致的词语')}
{field('通用敏感词库', f'<div class="flex gap12">{switch(True, "通用敏感词库")}<span class="c-muted">启用市面通用敏感词过滤库（v2026.09，12,860 条）</span></div>')}
{field('检测范围', '<div class="flex gap12" style="flex-wrap:wrap"><label class="check"><input type="checkbox" checked>标题</label><label class="check"><input type="checkbox" checked>正文</label><label class="check"><input type="checkbox" checked>活动简介</label><label class="check"><input type="checkbox" checked>图片备注</label><label class="check"><input type="checkbox">云盘链接</label></div>')}
{field('高危词处理', '<select class="select"><option>拦截提交，要求修改</option><option>允许提交，审核页醒目提示</option></select>')}
{field('低危词处理', '<select class="select"><option>提示投稿人，允许继续提交</option><option>仅在审核页提示</option></select>')}
</div></div>
<div class="card" style="box-shadow:none"><div class="card-head"><div class="card-title">{icon('search', 18)}检测试测</div><span class="hint">使用左侧当前选择的检测模式</span></div><div class="card-body">
<textarea class="textarea" id="testText" style="min-height:140px">我校获批国家级一流本科专业建设点，这是学院最牛的成绩。另外有同学咨询替考和翻 墙软件的问题。</textarea>
<div class="flex gap8 mt12">{btn('开始检测', 'btn-primary', 'search', 'data-action="sensitive-test" data-source="#testText" data-result="#testResult"')}<span class="hint">试试切换“精准匹配”后再检测，对比变体词识别效果</span></div>
<div id="testResult" class="mt16"><div class="empty" style="padding:24px">点击“开始检测”查看命中结果</div></div></div></div>
</div>'''
    foot = '<button class="btn" data-close>取消</button>' + btn('保存设置', 'btn-primary', 'save', 'data-action="save" data-msg="检测设置已保存并生效，已记入操作日志"')
    return modal('settingsModal', '敏感词检测设置', body, foot, 'modal-xl')


# ---------- 21 操作日志 ----------
def operation_logs():
    logs = [
        ('2026-09-30 16:02', '张静', '管理员', '修改业务参数', '—', '10.12.8.10', '一审时限：3 → 3；节假日新增“国庆节”'),
        ('2026-09-30 15:40', '周明轩', '二审员', '导出升华网素材包', 'TG2026091502', '10.12.8.66', '—'),
        ('2026-09-30 15:38', '周明轩', '二审员', '复制升华网正文', 'TG2026091502', '10.12.8.66', '—'),
        ('2026-09-30 14:20', '刘子涵', '一审员', '一审通过', 'TG2026092702', '10.12.8.51', '待一审 → 待二审'),
        ('2026-09-30 11:05', '张静', '管理员', '权限变更', '—', '10.12.8.10', '二审员：新增“升华网素材导出”'),
        ('2026-09-30 10:24', '陈雨桐', '投稿人', '提交投稿', 'TG2026092801', '10.12.34.21', '草稿 → 待指导老师审核'),
        ('2026-09-30 09:12', '陈雨桐', '投稿人', '新建草稿', 'TG2026093001', '10.12.34.21', '—'),
        ('2026-09-29 17:40', '张静', '管理员', '三审终审：采用', 'TG2026091805', '10.12.8.10', '待三审 → 已终审采用；不计入采用 → 计入采用'),
        ('2026-09-29 16:12', '王海峰', '指导老师', '指导老师审核退回', 'TG2026092601', '10.12.30.8', '待指导老师审核 → 已退回'),
        ('2026-09-29 10:30', '张静', '管理员', '数据导出', '—', '10.12.8.10', '导出全校稿件总表（1024 条）'),
        ('2026-09-28 16:35', '杨振华', '副书记', '副书记审核通过', 'TG2026092801', '10.12.30.2', '待副书记审核 → 待一审'),
        ('2026-09-28 14:10', '王海峰', '指导老师', '指导老师审核通过', 'TG2026092801', '10.12.30.8', '待指导老师审核 → 待副书记审核'),
        ('2026-09-22 14:18', '周明轩', '二审员', '二审退回', 'TG2026092203', '10.12.8.66', '待二审 → 已退回'),
        ('2026-09-20 11:40', '陈雨桐', '投稿人', '重新提交', 'TG2026092203', '10.12.34.21', '已退回 → 待指导老师审核；生成 v2'),
        ('2026-09-20 11:35', '陈雨桐', '投稿人', '稿件编辑修改', 'TG2026092203', '10.12.34.21', '标题：“青春志愿行社区服务周活动圆满结束” → “‘青春志愿行’社区服务周纪实”'),
    ]
    trs = ''.join(f'<tr data-act="{a}" data-date="{t[:10]}"><td>{t}</td><td style="color:var(--text)">{u}</td><td>{r}</td><td><span class="type-tag">{a}</span></td><td>{sid}</td><td>{ip}</td><td style="max-width:320px">{d}</td></tr>' for t, u, r, a, sid, ip, d in logs)
    acts = sorted(set(l[3] for l in logs))
    ctrls = filter_select('logsTable', 'act', '全部操作类型', acts) + date_range('logsTable') + search_box('logsTable', '搜索操作人 / 稿件编号')
    body = f'''{page_head('操作日志', '记录稿件新建、提交、编辑、重提、各级审核、退回、权限变更、数据导出等全部行为；日志只读，不可删除', btn('导出日志', '', 'download', 'data-action="export-csv" data-table="#logsTable" data-filename="投稿平台操作日志"'))}
<div class="notice notice-info mb16">{icon('lock', 15)}<div>日志字段包含操作人账号、身份、操作时间、IP 地址、操作对象稿件编号与操作行为；修改类操作记录修改前后的关键信息。</div></div>
<div class="card">{filter_bar('logsTable', ctrls)}{table('logsTable', [('操作时间', 'data-sort'), '操作人', '身份', '操作行为', '对象稿件', 'IP 地址', '修改前后 / 详情'], [trs])}</div>'''
    page('operation-logs.html', '操作日志', body, ['系统配置', '操作日志'])


def messages():
    items = [
        ('inbox', 'blue', '新的待三审稿件', f'《{FEATURED["title"]}》已通过二审，等待您终审', '15 分钟前', 'final-review.html', True),
        ('alert', 'red', '审核超时预警', '当前有 6 篇稿件超时未处理，涉及指导老师、副书记、一审、二审、三审节点', '今天 09:00', 'timeout-ledger.html', True),
        ('clock', 'orange', '三审即将超时', '《校友返校讲述“北斗”研发故事》剩余 0.5 个工作日', '今天 09:00', 'final-list.html', True),
        ('globe', 'blue', '待发布升华网', '有 3 篇已采用新闻尚未标记为已发布', '昨天 17:00', 'publish-export.html', True),
        ('bell', 'blue', '系统通知', '通用敏感词库已更新至 v2026.09，新增 326 条', '09-01 08:00', 'sensitive-words.html'),
    ]
    page('messages.html', '消息通知', messages_page_body(items))


def build():
    dashboard(); final_list(); final_done(); final_cc(); final_batch(); final_review(); final_review(True); archive(); archive_detail(); publish_export()
    clue_tracking(); timeout_ledger(); ranking(); reviewer_manage(1); reviewer_manage(2)
    teacher_manage(); role_permission(); params(); opinion_templates()
    sensitive_words(); operation_logs(); messages()
