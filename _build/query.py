# 稿件查询：审核角色查看本人审核过的稿件（通过 / 退回），与一审“稿件查询”同样的检索与筛选
from lib import tag, type_tag, page_head, btn, a_btn, filter_select, search_box, date_range, filter_bar, table, icon
from data import typed, TYPE_NAME, VIDEO, PHOTO, CLUE, NEWS_DONE
from detail import full_detail

FLOW_STATUS = ['待指导老师审核', '待副书记审核', '待一审', '待二审', '待三审', '已退回', '已终审采用', '已终审不采用', '已发布']
NODE_OF = {'待指导老师审核': '指导老师审核', '待副书记审核': '副书记审核', '待一审': '一审', '待二审': '二审', '待三审': '三审终审',
           '已退回': '退回投稿人修改', '已终审采用': '流程结束', '已终审不采用': '流程结束', '已发布': '流程结束'}
DETAIL_SAMPLES = [(NEWS_DONE, 'adopted', '已终审采用'), (VIDEO, 'adopted', '已终审采用'), (PHOTO, 'adopted', '已终审采用'), (CLUE, 'r3', '待三审')]


def reviewed_query_body(node, rows, scope):
    """rows：编号、标题、类型、学院、投稿人、身份、投稿日期、本人审核结果、审核时间、当前流转状态"""
    tid = 'qTable'
    trs = ''
    for sid, title, t, col, author, ident, d, res, rtime, st in rows:
        h = typed('submission-detail.html', t)
        trs += (f'<tr data-college="{col}" data-type="{t}" data-status="{st}" data-result="{res}" data-identity="{ident}" data-date="{d}">'
                f'<td><a class="t-title" href="{h}">{title}</a><div class="t-sub">{sid}</div></td>'
                f'<td>{type_tag(t)}</td><td>{col}</td><td>{author}<div class="t-sub">{ident}</div></td><td>{d}</td>'
                f'<td>{tag(res)}<div class="t-sub">{rtime}</div></td><td>{tag(st)}<div class="t-sub">当前节点：{NODE_OF[st]}</div></td>'
                f'<td><a class="link" href="{h}">查看档案</a></td></tr>')
    colleges = sorted({r[3] for r in rows}, key=lambda c: (c != '计算机学院', c))
    ctrls = (filter_select(tid, 'college', '全部学院', colleges) + filter_select(tid, 'type', '全部类型', ['新闻', '视频', '照片', '线索']) +
             filter_select(tid, 'status', '全部状态', FLOW_STATUS) + filter_select(tid, 'result', '全部审核结果', ['已通过', '已退回']) +
             filter_select(tid, 'identity', '全部投稿身份', ['学生', '教师']) + date_range(tid) + search_box(tid))
    head = page_head('稿件查询', f'查看本人在“{node}”环节审核过的稿件（含通过与退回），可按学院、类型、状态、审核结果、时间范围组合筛选',
                     btn('导出查询结果', '', 'download', f'data-action="export-csv" data-table="#{tid}" data-filename="{node}稿件查询结果"'))
    note = f'<div class="notice notice-info mb16">{icon("info", 15)}<div>{scope}仍在“待办”中的稿件不在此列表；稿件后续的流转状态实时同步。</div></div>'
    cols = ['稿件', '类型', '投稿学院', '投稿人', ('投稿日期', 'data-sort'), '本人审核结果', '当前流转状态', ('操作', 'class="no-export"')]
    return f'{head}{note}<div class="card">{filter_bar(tid, ctrls)}{table(tid, cols, [trs], page_size=15)}</div>'


def query_pages(page, node, rows, scope):
    page('submissions.html', '稿件查询', reviewed_query_body(node, rows, scope))
    for sub, stage, status in DETAIL_SAMPLES:
        head = page_head(f'{sub["title"]} {tag(status)}', f'稿件编号 {sub["id"]} · {TYPE_NAME[sub["type"]]} · {sub["college"]} · 稿件档案永久保存',
                         a_btn('返回稿件查询', 'submissions.html', '', 'arrow-l'))
        page(typed('submission-detail.html', sub['type']), '稿件档案', head + full_detail(sub, status, stage), ['稿件查询', '稿件档案'], '', 'submissions.html')
