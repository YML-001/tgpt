# PC 端 · 副职领导（按职能部门在“副职领导名单”中配置，审核本部门职能部门老师的投稿）
from lib import card, btn, a_btn, pc_page, write
from data import VICE_TODO, VICE_REVIEWED, VICE_NEWS
from common import messages_page_body
from workflow import norm, todo_body, done_body, cc_body, batch_body, detail_body, node_chart, flow_name
from review import review_body, reject_modal, q, type_review_pages
from detail import sub_content, flow_records, sample_for, chart_cur
from query import query_pages

R = 'vice'
P = 'pc/vice/'
SUB = VICE_NEWS
SID = SUB['id']
ROWS = norm(VICE_TODO, 'vice')
TPL_VICE = ['涉及部门工作的数据和表述需与部门正式发布口径一致，请核对后修改。', '稿件涉及的会议或活动信息需补充审批依据，请完善后重新提交。',
            '请删除未公开的内部工作安排，修改后重新提交。']
PASS_MSG = '副职领导审核通过，稿件已报送校团委学生一审'
PASS_NEXT = q('todo.html', done=SID, msg=PASS_MSG, link=q('history.html', new=SID, act='pass'), linkText='查看已办')
REJECT_NEXT = q('todo.html', done=SID, type='warn', msg=f'已退回稿件，系统已通知投稿人{SUB["author"]}', link=q('history.html', new=SID, act='reject'), linkText='查看已办')
SCOPE = card('副职领导审核说明', '<div style="font-size:13px;line-height:1.9;color:var(--text-2)">· 只审核本部门（党委宣传部）职能部门老师的投稿，提交后直接到达。<br>'
                           '· 本部门配置了多名副职领导时，稿件同时出现在每个人的待办中，任一人完成审核即可。<br>'
                           '· 通过后报送校团委学生一审；退回须填写意见，稿件回到投稿人修改。</div>', 'shield')
NEW_ROWS = []


def vice_sub(t):
    sub = dict(VICE_NEWS) if t == '新闻' else sample_for(t, dict(identity='职能部门老师', college='党委宣传部'))
    sub['teacher'] = '—'
    return sub


NEWS_DONE = dict(VICE_NEWS, id='TG2026090918', title='新教工入职培训侧记', time='2026-09-09 10:20', times={})
SAMPLES = [(NEWS_DONE, 'adopted', '已发布'), (vice_sub('视频'), 'adopted', '已终审采用'),
           (vice_sub('照片'), 'adopted', '已终审采用'), (vice_sub('线索'), 'r3', '待三审')]


def page(file, title, body, crumbs=None, modals='', active=None):
    write(P + file, pc_page(R, active or file, title, body, crumbs=crumbs, modals=modals, todo_count=len(ROWS)))


def todo():
    page('todo.html', '待办', todo_body('vTodo', ROWS, '副职领导审核', 'review.html'), ['待办'])


def review(reject=False):
    d = ROWS[[r['sid'] for r in ROWS].index(SID)]
    actions = (btn('通过，报送学生一审', 'btn-success btn-lg', 'check', f'data-action="pass" data-opinion="optional" data-tpl="vice" data-title="副职领导审核通过" data-ok="确认通过" data-msg="{PASS_MSG}" data-next="{PASS_NEXT}"') +
               a_btn('退回修改', 'review-reject.html', 'btn-danger-o btn-lg', 'undo'))
    body = review_body(SUB, '待副职领导审核', '副职领导审核', 1, (d['rem'], d['lv']), flow_records(SUB, 'vice'), actions, 'todo.html',
                       identity='职能部门老师', start=SUB['time'], arrive=d['arrive'], extra_right=SCOPE)
    modals = reject_modal('rejectBox', '退回稿件', '退回意见', TPL_VICE, REJECT_NEXT) if reject else ''
    page('review-reject.html' if reject else 'review.html', '办理', body, ['待办', '新闻投稿审核'], modals, active='todo.html')


def typed_pages():
    global NEW_ROWS
    made = type_review_pages(page, ROWS, '副职领导审核', 'vice', 'todo.html', 'history.html', 'vice', '通过，报送学生一审', PASS_MSG, '待办',
                             extra_right=SCOPE)
    NEW_ROWS = [(sid, title, t, author, col, '2026-09-30 16:50') for sid, title, t, author, col in made.values()]
    for sub, stage, status in SAMPLES[1:]:
        body = detail_body(sub, status, 'tag-solid-ok', node_chart('职能部门老师', chart_cur('职能部门老师', stage)), flow_records(sub, stage),
                           'history.html', sub['time'], sub['time'], sub_content(sub))
        page({'视频': 'done-detail-video.html', '照片': 'done-detail-photo.html', '线索': 'done-detail-clue.html'}[sub['type']], '已办详情', body,
             ['已办', f'{sub["type"]}稿件审核'], active='history.html')


def history():
    rows = [(sid, title, t, author, dept, '已通过' if res == '已通过' else '已退回',
             '已核对部门工作信息，同意报送。' if res == '已通过' else '涉及部门工作的数据和表述需与部门正式发布口径一致，请核对后修改。',
             rtime, '0.5 个工作日', '及时') for sid, title, t, dept, author, ident, d, res, rtime, st in VICE_REVIEWED]
    body = done_body('vHis', rows, '副职领导审核', 'done-detail.html', ('已通过', '已退回'),
                     [(SID, SUB['title'], '新闻', SUB['author'], SUB['college'], '2026-09-30 16:50')] + NEW_ROWS, '副职领导已办记录')
    page('history.html', '已办', body, ['已办'])


def cc():
    urges = [(flow_name('照片', '校园秋景摄影征集精选'), '副职领导审核', '系统（超时自动催办）', '2026-09-25 09:30', '2026-09-30 09:00'),
             (flow_name('视频', '“我和我的祖国”快闪活动视频'), '副职领导审核', '张静（校团委管理员）', '2026-09-28 11:00', '2026-09-30 09:30')]
    copies = [(flow_name('照片', '国庆主题灯光秀照片'), '三审终审', '张静（校团委管理员）', '2026-09-21 10:30', '已读'),
              (flow_name('视频', '迎新季校园宣传片'), '学生一审', '刘子涵（一审员）', '2026-09-28 10:30', '未读')]
    page('cc.html', '催办/抄送', cc_body(urges, copies, 'review.html', 'done-detail.html'), ['催办/抄送'])


def batch():
    page('batch.html', '批量审批', batch_body(ROWS, '副职领导审核', 'review.html', 'vice'), ['批量审批'])


def done_detail():
    body = detail_body(SUB, '已通过', 'tag-solid-ok', node_chart('职能部门老师', 2), flow_records(SUB, 'r1'), 'history.html',
                       SUB['time'], SUB['time'], sub_content(SUB))
    page('done-detail.html', '已办详情', body, ['已办', '新闻投稿审核'], active='history.html')


def messages():
    items = [
        ('inbox', 'blue', '新的待审稿件', f'党委宣传部{SUB["author"]}提交了《{SUB["title"]}》，请在 3 个工作日内审核', '20 分钟前', 'review.html', True),
        ('alert', 'red', '审核超时提醒', '《校园秋景摄影征集精选》已超过审核时限 1 个工作日，已记入超时台账', '今天 09:00', 'todo.html', True),
        ('check-circle', 'green', '您审核的稿件已终审采用', '《国庆主题灯光秀照片》已由校团委终审采用', '09-21 10:30', 'history.html'),
    ]
    page('messages.html', '消息通知', messages_page_body(items))


def build():
    todo(); review(); review(True); typed_pages(); history()
    query_pages(page, '副职领导审核', VICE_REVIEWED, '只显示党委宣传部、您在副职领导审核环节已处理过的职能部门老师稿件；', SAMPLES, '部门')
    cc(); batch(); done_detail(); messages()
