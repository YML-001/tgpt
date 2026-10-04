# 移动端页面右侧说明：要点 + 业务链路（下一步）
from icons import icon

C = 'mobile/correspondent/'
SUBMIT_NOTE = ['选择学生身份时必须指定指导老师，默认预填上次选择的指导老师，可搜索其他学院',
               '选择教师身份无需指导老师，提交后直接进入校团委一审',
               '内容每 30 秒自动保存，可随时点击“存草稿”',
               '提交前自动做敏感词检测：高危词拦截，低危词提醒后可继续']

NOTES = {
    C + 'home.html': (['欢迎区展示本学年投稿、已采用、审核中、被退回 4 项个人数据',
                       '四宫格直达新闻、视频、照片、线索四类投稿表单；底部“投稿”按钮弹出类型选择',
                       '被退回的稿件置顶提醒，点击直接进入修改重提',
                       '排行榜展示全校前三名学院，本院高亮'],
                      [('新闻投稿', 'submit-news.html'), ('处理被退回稿件', 'resubmit.html'), ('我的投稿', 'my-submissions.html')]),
    C + 'submit-news.html': (SUBMIT_NOTE + ['新闻正文不少于 50 字，配图至少 1 张'],
                             [('提交后：提交成功页', 'submit-success.html?type=新闻&identity=学生'), ('返回首页', 'home.html')]),
    C + 'submit-video.html': (SUBMIT_NOTE[:2] + ['视频时长按“分:秒”格式填写', '必须提供永久有效的云盘链接，临时分享链接会被退回'],
                              [('提交后：提交成功页', 'submit-success.html?type=视频&identity=学生'), ('返回首页', 'home.html')]),
    C + 'submit-photo.html': (SUBMIT_NOTE[:2] + ['支持批量上传原图，单张不超过 30MB', '可为每张照片单独填写备注；无重要领导填写“无”'],
                              [('提交后：提交成功页', 'submit-success.html?type=照片&identity=学生'), ('返回首页', 'home.html')]),
    C + 'submit-clue.html': (SUBMIT_NOTE[:2] + ['线索无需上传图片，重点描述人物、事件与新闻价值', '接受采访时需填写可采访时间段'],
                             [('提交后：提交成功页', 'submit-success.html?type=线索&identity=学生'), ('返回首页', 'home.html')]),
    C + 'submit-success.html': (['展示稿件编号与当前所处审核节点',
                                 '学生稿件显示 5 步流程（含指导老师），教师稿件显示 4 步流程',
                                 '可继续投稿，或进入我的投稿查看新提交的稿件'],
                                [('查看我的投稿（新稿件高亮）', 'my-submissions.html?new=TG2026093005'),
                                 ('切换为教师投稿的效果', 'submit-success.html?type=新闻&identity=教师')]),
    C + 'my-submissions.html': (['顶部分段按草稿、审核中、已退回、已采用、未采用筛选',
                                 '被退回的稿件显示退回意见摘要，点击进入修改重提',
                                 '草稿点击继续编辑，其他稿件进入稿件档案'],
                                [('被退回稿件：修改重提', 'resubmit.html'), ('稿件档案', 'detail.html')]),
    C + 'detail.html': (['顶部红色提示展示最近一次退回意见',
                         '三个页签：稿件内容、流转记录（含每个节点的审核人与意见）、投稿信息',
                         '底部按钮直接进入修改重提'],
                        [('按意见修改并重新提交', 'resubmit.html'), ('返回我的投稿', 'my-submissions.html')]),
    C + 'resubmit.html': (['顶部汇总历次退回意见，修改时对照处理',
                           '重新提交生成新版本（v3），历史版本与意见永久保留',
                           '必须填写修改说明；可更换指导老师',
                           '重新提交后回到指导老师审核环节'],
                          [('重新提交后：我的投稿', 'my-submissions.html?re=1&msg=已重新提交，生成 v3 版本并重新进入审核'),
                           ('查看稿件档案', 'detail.html')]),
    C + 'ranking.html': (['按学年、学期切换，以终审采用数排序',
                          '本院高亮；点击其他学院提示只能查看本院明细（数据隔离）'],
                         [('返回首页', 'home.html'), ('我的', 'profile.html')]),
    C + 'messages.html': (['退回、采用、审核进度、排行榜更新等消息',
                           '未读消息带红点，右上角可全部标记已读',
                           '点击消息跳转到对应稿件或页面'],
                          [('被退回：修改重提', 'resubmit.html'), ('采用：稿件档案', 'detail.html')]),
    C + 'profile.html': (['展示本院本学年投稿统计（仅本院数据）',
                          '投稿须知以底部面板弹出',
                          '可切换到 PC 端或退出登录'],
                         [('我的投稿', 'my-submissions.html'), ('全校排行榜', 'ranking.html')]),
}


def reviewer_notes(folder, node, nxt, pc_desc):
    base = f'mobile/{folder}/'
    NOTES[base + 'todo.html'] = ([pc_desc, '顶部统计待处理、已超时、即将超时数量',
                                  '超时稿件红色标记并排在最前，分段可按时限筛选',
                                  '点击稿件进入审核详情'],
                                 [('审核稿件', 'review.html'), ('审核台账' if folder != 'teacher' else '审核记录',
                                                              'ledger.html' if folder != 'teacher' else 'history.html')])
    ledger = 'ledger.html' if folder != 'teacher' else 'history.html'
    NOTES[base + 'review.html'] = ([f'顶部显示{node}节点时限与剩余时间',
                                    '三个页签：稿件内容（含敏感词检测结果）、流转记录、投稿信息',
                                    '退回必须填写意见，可一键套用意见模板',
                                    f'通过后流转至{nxt}，意见选填'],
                                   [('通过后：回到待办（已移除该稿件）', f'todo.html?done=TG2026092801&msg={node}通过，已流转至{nxt}'),
                                    ('退回后：查看台账记录', f'{ledger}?new=TG2026092801&act=reject')])
    NOTES[base + ledger] = (['统计累计审核数、及时率与超时次数',
                             '每条记录显示审核结果、用时与是否及时',
                             '分段可按通过 / 退回筛选'],
                            [('返回待办', 'todo.html'), ('消息', 'messages.html')])
    NOTES[base + 'messages.html'] = (['新稿件到达、超时预警、即将超时、终审结果等消息',
                                      '点击消息跳转到审核页或待办列表'],
                                     [('新的待审稿件', 'review.html'), ('待办列表', 'todo.html')])


reviewer_notes('teacher', '指导老师审核', '校团委一审', '仅显示指定您为指导老师的学生稿件')
reviewer_notes('reviewer1', '一审', '二审', '只展示分配给本人（一审环节）的稿件')
reviewer_notes('reviewer2', '二审', '三审终审', '只展示分配给本人（二审环节）的稿件')

A = 'mobile/admin/'
NOTES.update({
    A + 'home.html': (['统计看板：投稿总量、终审采用、退回、审核及时率',
                       '待三审、超时未处理可点击进入列表',
                       '稿件类型分布与学院采用排行前三',
                       '完整驾驶舱、升华网素材导出在 PC 端操作'],
                      [('处理待三审稿件', 'final-list.html'), ('PC 端统计驾驶舱', '../../pc/admin/dashboard.html')]),
    A + 'final-list.html': (['二审通过的稿件进入三审终审',
                             '超时稿件红色标记并优先排序',
                             '点击稿件进入终审'],
                            [('终审稿件', 'final-review.html'), ('返回看板', 'home.html')]),
    A + 'final-review.html': (['终审二选一：采用或不采用',
                               '采用计入学院采用统计与排行榜；不采用必须填写终审意见',
                               '新闻线索终审采用后进入 PC 端线索跟进'],
                              [('采用后：回到待三审列表', 'final-list.html?done=TG2026092801&msg=已终审采用，计入学院采用统计'),
                               ('PC 端线索跟进', '../../pc/admin/clue-tracking.html')]),
    A + 'messages.html': (['新的待三审稿件、超时预警、待发布升华网等消息'],
                          [('待三审稿件', 'final-review.html'), ('返回看板', 'home.html')]),
})


def notes_panel(path):
    items, flow = NOTES.get(path, ([], []))
    lis = ''.join(f'<li>{n}</li>' for n in items)
    html = f'<div class="n-path">{path}</div><ul>{lis}</ul></div>'
    if flow:
        links = ''.join(f'<a href="{h}">{icon("arrow-r", 14)}{t}</a>' for t, h in flow)
        html += f'<div class="card flow"><b>业务链路 · 下一步</b>{links}</div>'
    return html
