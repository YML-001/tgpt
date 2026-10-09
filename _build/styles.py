# 内联样式：设计令牌与组件样式，对齐 design-system.md（中南主色 #3087CC）

BASE_CSS = """
/* ===== 设计令牌 ===== */
:root{--primary:#2A8DC7;--primary-light:#EAF4F9;--primary-dark:#1F77AD;--blue6:#9CCDEB;--blue7:#BADEF3;--blue8:#D6EAF9;
--text:#1E323F;--text-2:#485066;--text-3:#8A94A3;--placeholder:#A8ABB2;--border:#DCDFE6;--line:#E8EAEC;--bg:#E3F1F9;
--success:#19B87A;--success-bg:#E9F9F1;--success-bd:#A9E8CB;--warn:#F59200;--warn-bg:#FFF4E5;--warn-bd:#FFDCA8;
--danger:#F56C6C;--danger-bg:#FEF0F0;--danger-bd:#FBC4C4;--gray-bg:#F4F4F5;
--brace:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='6' viewBox='0 0 32 6'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='1' x2='3.24' y2='13.44' gradientUnits='userSpaceOnUse'%3E%3Cstop stop-color='%23F7CED9'/%3E%3Cstop offset='1' stop-color='%23FA396F'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M30.4 1C30.6 1 31.1333 1 31.6 1.4C32 1.86667 32 2.33333 32 2.6V3.66667H29.3333H21.6667C20 3.66667 18 4.13333 17.3333 5.26667V5.93708H14.6667V5.26667C13.8 4.33333 12.3333 3.66667 11 3.66667H2.66667H0V2.66667C0 2.2 0.133333 1.8 0.466667 1.53333C1 1 1.8 1 2.26667 1H11C12.9333 1 14.8667 1.8 16.2 3.06667C17.7333 1.73333 19.9333 1 21.6667 1H30.4Z' fill='url(%23g)'/%3E%3C/svg%3E");
--radius:4px;--shadow-sm:0 1px 3px rgba(0,0,0,.06);--shadow-md:0 2px 8px rgba(0,0,0,.04);--shadow-lg:0 8px 24px rgba(15,40,80,.10);
--font:'OPPOSans',-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);font-size:14px;color:var(--text);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--primary);text-decoration:none}
button{font-family:inherit;cursor:pointer}
input,select,textarea{font-family:inherit}
img{max-width:100%}
.ic{flex-shrink:0;vertical-align:middle}
.hidden{display:none!important}
.c-primary{color:var(--primary)}.c-success{color:var(--success)}.c-warn{color:var(--warn)}.c-danger{color:var(--danger)}.c-muted{color:var(--text-3)}
.fw{font-weight:600}.num{font-variant-numeric:tabular-nums}
.flex{display:flex;align-items:center}.gap8{gap:8px}.gap12{gap:12px}.between{justify-content:space-between}.ml-auto{margin-left:auto}
.mt8{margin-top:8px}.mt12{margin-top:12px}.mt16{margin-top:16px}.mt20{margin-top:20px}.mt24{margin-top:24px}.mb16{margin-bottom:16px}
:focus-visible{outline:2px solid var(--primary);outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

/* ===== 按钮 ===== */
.btn{height:32px;padding:0 15px;border-radius:var(--radius);border:1px solid var(--primary);background:#fff;color:var(--primary);display:inline-flex;align-items:center;justify-content:center;gap:5px;font-size:14px;font-weight:400;transition:all .15s;white-space:nowrap;text-decoration:none}
.btn:hover{background:var(--primary-light);border-color:var(--primary);color:var(--primary)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-primary{background:var(--primary);border-color:var(--primary);color:#fff}
.btn-primary:hover{background:var(--primary-dark);border-color:var(--primary-dark);color:#fff}
.btn-outline{border-color:var(--primary);color:var(--primary)}
.btn-outline:hover{background:var(--primary-light)}
.btn-success{background:var(--success);border-color:var(--success);color:#fff}
.btn-success:hover{background:#12a063;border-color:#12a063;color:#fff}
.btn-danger{background:var(--danger);border-color:var(--danger);color:#fff}
.btn-danger:hover{background:#c41a20;border-color:#c41a20;color:#fff}
.btn-danger-o{border-color:var(--danger-bd);color:var(--danger);background:#fff}
.btn-danger-o:hover{background:var(--danger-bg);border-color:var(--danger);color:var(--danger)}
.btn-warn{background:var(--warn);border-color:var(--warn);color:#fff}
.btn-warn:hover{background:#d98200;color:#fff;border-color:#d98200}
.btn-lg{height:38px;padding:0 22px;font-size:15px}
.btn-sm{height:26px;padding:0 10px;font-size:12px;border-radius:3px}
.link{color:var(--primary);cursor:pointer;background:none;border:none;font-size:13px;padding:0;display:inline-flex;align-items:center;gap:4px}
.link:hover{color:var(--primary-dark);text-decoration:underline}
.link-danger{color:var(--danger)}.link-danger:hover{color:#b3161c}
.link-muted{color:var(--text-3)}

/* ===== 标签 ===== */
.tag{display:inline-flex;align-items:center;gap:5px;height:22px;padding:0 10px;border-radius:11px;font-size:12px;font-weight:400;border:1px solid;white-space:nowrap;line-height:1}
.tag-success{color:var(--success);background:var(--success-bg);border-color:var(--success-bd)}
.tag-warn{color:var(--warn);background:var(--warn-bg);border-color:var(--warn-bd)}
.tag-danger{color:var(--danger);background:var(--danger-bg);border-color:var(--danger-bd)}
.tag-gray{color:var(--text-3);background:var(--gray-bg);border-color:var(--border)}
.tag-primary{color:var(--primary);background:var(--primary-light);border-color:var(--primary)}
.tag-dot::before{display:none}
.tag-solid{color:#fff;background:var(--primary);border-color:var(--primary)}
.type-tag{display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var(--text-2);background:#F4F6F9;border-radius:4px;padding:2px 8px;white-space:nowrap}

/* ===== 表单控件 ===== */
.input,.select{height:32px;border:1px solid var(--border);border-radius:4px;padding:0 12px;font-size:14px;color:var(--text);background:#fff;outline:none;transition:border-color .15s,box-shadow .15s}
.select{padding-right:30px;appearance:none;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239096A2' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E") no-repeat right 10px center}
.input::placeholder,.textarea::placeholder{color:var(--placeholder)}
.input:focus,.select:focus,.textarea:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(42,141,199,.12)}
.input:disabled,.select:disabled{background:var(--gray-bg);color:var(--text-3)}
.textarea{width:100%;min-height:96px;border:1px solid var(--border);border-radius:4px;padding:10px 12px;font-size:14px;color:var(--text);outline:none;resize:vertical;line-height:1.7;transition:border-color .15s}
.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field.full{grid-column:1/-1}
.lbl{font-size:13px;color:var(--text-2);font-weight:500}
.lbl.req::before{content:'*';color:var(--danger);margin-right:3px}
.hint{font-size:12px;color:var(--text-3)}
.field-error{font-size:12px;color:var(--danger)}
.field.is-error .input,.field.is-error .select,.field.is-error .textarea,.field.is-error .editor-box,.field.is-error .upload{border-color:var(--danger)!important;box-shadow:0 0 0 3px rgba(223,32,39,.08)}
.radio-group{display:flex;gap:10px;flex-wrap:wrap}
.radio-card{border:1px solid var(--border);border-radius:8px;padding:0 16px;height:40px;display:inline-flex;align-items:center;gap:8px;cursor:pointer;transition:all .15s;font-size:14px;background:#fff}
.radio-card:hover{border-color:var(--primary)}
.radio-card input{accent-color:var(--primary)}
.radio-card:has(input:checked){border-color:var(--primary);background:var(--primary-light);color:var(--primary-dark)}
.check{display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-size:14px}
.check input{accent-color:var(--primary);width:15px;height:15px}
input[type=checkbox]{accent-color:var(--primary)}

/* ===== 开关 ===== */
.switch{width:40px;height:22px;border-radius:11px;background:var(--border);position:relative;border:none;transition:background .2s;flex-shrink:0;padding:0}
.switch::after{content:'';position:absolute;left:2px;top:2px;width:18px;height:18px;border-radius:50%;background:#fff;transition:left .2s;box-shadow:0 1px 2px rgba(0,0,0,.2)}
.switch.on{background:var(--primary)}
.switch.on::after{left:20px}

/* ===== 提示条 ===== */
.notice{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border-radius:8px;border:1px solid;font-size:13px;line-height:1.7}
.notice .ic{margin-top:2px}
.notice-info{background:var(--primary-light);border-color:var(--blue7);color:var(--primary-dark)}
.notice-warn{background:var(--warn-bg);border-color:var(--warn-bd);color:#9A5C00}
.notice-danger{background:var(--danger-bg);border-color:var(--danger-bd);color:#A8161B}
.notice-success{background:var(--success-bg);border-color:var(--success-bd);color:#0E7A4C}
.result-bar{display:flex;align-items:center;gap:10px;padding:12px 16px;border-radius:10px;margin-bottom:16px;font-size:14px;border:1px solid;animation:pop .3s ease-out}
.result-bar.success{background:var(--success-bg);border-color:var(--success-bd);color:#0E7A4C}
.result-bar.warn{background:var(--warn-bg);border-color:var(--warn-bd);color:#9A5C00}
.result-bar a{margin-left:auto;font-weight:500}
.rb-x{border:none;background:none;font-size:18px;color:inherit;opacity:.6;margin-left:8px}
.result-bar a+.rb-x{margin-left:8px}
.result-bar span+.rb-x{margin-left:auto}

/* ===== 弹窗 ===== */
.modal{position:fixed;inset:0;background:rgba(20,30,45,.45);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal.open{display:flex;animation:fade .2s}
.modal-box{background:#fff;border-radius:8px;width:560px;max-width:100%;max-height:90vh;display:flex;flex-direction:column;box-shadow:0 20px 50px rgba(0,0,0,.2);animation:pop .25s ease-out}
.modal-sm{width:460px}.modal-lg{width:760px}.modal-xl{width:1000px}
.modal-head{padding:14px 20px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;font-weight:600;font-size:17px;color:var(--text);background:linear-gradient(90deg,#EAF4F9,#fff);border-radius:8px 8px 0 0}
.modal-body{padding:20px 22px;overflow:auto}
.modal-foot{padding:14px 22px;border-top:1px solid var(--line);display:flex;justify-content:flex-end;gap:10px}
.modal-x{border:none;background:none;color:var(--text-3);width:32px;height:32px;border-radius:6px;display:grid;place-items:center}
.modal-x:hover{background:var(--gray-bg);color:var(--text)}
.dlg-text{color:var(--text-2);line-height:1.8}
.dlg-row{display:flex;justify-content:space-between}
.dlg-row .hint{margin-left:auto}
.tpl-title{font-size:12px;color:var(--text-3);margin:14px 0 8px}
.tpl-list{display:flex;flex-direction:column;gap:6px}
.tpl-chip{text-align:left;border:1px dashed var(--blue7);background:#F7FBFE;color:var(--primary-dark);border-radius:6px;padding:7px 10px;font-size:13px;line-height:1.5}
.tpl-chip:hover{background:var(--primary-light);border-style:solid}
.modal .form-grid{grid-template-columns:1fr 1fr}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{from{transform:translateY(10px);opacity:0}to{transform:none;opacity:1}}
@keyframes flash{0%{background:#DDEFFC}100%{background:transparent}}

/* ===== 轻提示 ===== */
.toast-wrap{position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:300;display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none}
.toast{padding:10px 16px;border-radius:8px;border:1px solid;font-size:14px;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow-lg);animation:pop .25s;background:#fff;max-width:520px}
.toast.success{color:#0E7A4C;background:var(--success-bg);border-color:var(--success-bd)}
.toast.warn{color:#9A5C00;background:var(--warn-bg);border-color:var(--warn-bd)}
.toast.danger{color:#A8161B;background:var(--danger-bg);border-color:var(--danger-bd)}
.toast.info{color:var(--primary-dark);background:var(--primary-light);border-color:var(--blue7)}

/* ===== 时间轴 ===== */
.timeline{position:relative;padding-left:26px}
.tl-item{position:relative;padding-bottom:20px}
.tl-item::before{content:'';position:absolute;left:-20px;top:16px;bottom:-2px;width:2px;background:var(--line)}
.tl-item:last-child{padding-bottom:0}
.tl-item:last-child::before{display:none}
.tl-dot{position:absolute;left:-25px;top:5px;width:12px;height:12px;border-radius:50%;border:2px solid var(--border);background:#fff}
.tl-dot.ok{background:var(--success);border-color:var(--success)}
.tl-item:has(.tl-dot.ok)::before{background:var(--success-bd)}
.tl-dot.warn{background:var(--warn);border-color:var(--warn)}
.tl-dot.danger{background:var(--danger);border-color:var(--danger)}
.tl-dot.primary{background:#fff;border-color:var(--primary);box-shadow:0 0 0 4px rgba(48,135,204,.18)}
.tl-head{display:flex;gap:8px;align-items:center;font-weight:600;flex-wrap:wrap}
.tl-meta{font-size:12px;color:var(--text-3);margin-top:2px}
.tl-opinion{margin-top:6px;background:#F7F9FB;border-radius:6px;border-left:3px solid var(--line);padding:8px 10px;font-size:13px;color:var(--text-2);line-height:1.7}
.tl-opinion.danger{background:var(--danger-bg);color:#A8161B;border-left-color:var(--danger)}

/* ===== 其他 ===== */
.chip-input{display:flex;flex-direction:column;gap:10px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 6px 0 10px;border-radius:14px;background:var(--primary-light);color:var(--primary-dark);font-size:13px}
.chip-x{border:none;background:none;color:var(--primary);font-size:15px;width:18px;height:18px;border-radius:50%;line-height:1}
.chip-x:hover{background:#fff}
.progress{height:8px;background:var(--gray-bg);border-radius:4px;overflow:hidden}
.progress i{display:block;height:100%;background:var(--primary);border-radius:4px}
mark.high{background:var(--danger-bg);color:var(--danger);padding:0 2px;border-radius:3px;font-weight:600}
mark.low{background:var(--warn-bg);color:#B86E00;padding:0 2px;border-radius:3px}
.teacher-picker{position:relative}
.picker-list{position:absolute;left:0;right:0;top:calc(100% + 4px);background:#fff;border:1px solid var(--line);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.1);max-height:240px;overflow:auto;z-index:40;display:none;padding:4px}
.picker-list.open{display:block}
.picker-item{padding:8px 10px;border-radius:6px;cursor:pointer;display:flex;flex-direction:column}
.picker-item:hover{background:var(--primary-light)}
.picker-item span{font-size:12px;color:var(--text-3)}
.picker-empty{padding:12px;color:var(--text-3);font-size:13px}
.picker-item.on{background:var(--primary-light)}
.staff-picker{position:relative}
.staff-tip{display:flex;align-items:center;gap:12px;margin-top:6px;font-size:12px;color:var(--text-3);line-height:1.5}
.staff-tip .link{margin-left:auto;flex:none;font-size:12px}
.field .f-range{height:36px;padding:2px 6px;border-color:var(--border)}
.field .f-range .input{height:30px;width:auto;flex:1}
.field.is-error .f-range{border-color:var(--danger)}
.field.is-error .f-range .input{box-shadow:none!important}
.nowrap{white-space:nowrap}
.import-drop{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px}
.import-preview .tbl th,.import-preview .tbl td{padding:8px 10px;font-size:13px}
.import-preview .table-wrap{max-height:260px;overflow:auto}
.import-sum{display:flex;gap:16px;align-items:center;margin-bottom:10px;font-size:13px}
.term-head{display:flex;align-items:center;justify-content:space-between;padding:0 2px 8px;border-bottom:1px solid var(--line)}
.term-all{display:flex;align-items:center;gap:8px;font-weight:500;cursor:pointer}
.term-list{max-height:280px;overflow:auto}
.term-item{display:grid;grid-template-columns:24px 1.1fr 1.6fr 1.4fr 72px;align-items:center;gap:10px;padding:10px 2px;border-bottom:1px solid var(--line);font-size:13px;cursor:pointer}
.term-item b{font-weight:500;color:var(--text)}
.term-item .t-sub{font-size:12px;color:var(--text-3)}
.term-item.leave{background:#FAFAFB}
.term-item.leave b{color:var(--text-3)}
.term-empty{padding:28px 0;text-align:center;color:var(--text-3);font-size:13px}
.dot-ok{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--success);margin-right:6px;vertical-align:middle}
.is-new,.is-new td{animation:flash 2.4s ease-out}
.only-unread .msg-item:not(.unread){display:none}
.test-sum{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.test-text{background:#FAFBFC;border:1px solid var(--line);border-radius:8px;padding:12px 14px;line-height:1.9;white-space:pre-wrap}
"""

PC_CSS = BASE_CSS + """
/* ===== PC 框架（按智慧学工正式系统 1920 设计稿尺寸，脚本按视口等比缩放） ===== */
html{scroll-padding:110px 0 110px}
body{background:#E3F1F9;color:rgba(0,0,0,.85)}
.btn{font-weight:500}
.top{position:fixed;top:0;left:0;right:0;height:80px;z-index:30;box-shadow:0 2px 10px rgba(27,113,188,.18)}
.top-bar{height:80px;background:linear-gradient(90deg,#1B71BC 0%,#2F86D2 45%,#5BA6EA 100%);display:flex;align-items:center;justify-content:flex-end;padding:0 25px 0 560px;position:relative}
.top-bar::before{content:'';position:absolute;inset:0;background:radial-gradient(520px 140px at 72% -30%,rgba(255,255,255,.22),transparent 70%),linear-gradient(160deg,transparent 60%,rgba(255,255,255,.08) 60%,rgba(255,255,255,.08) 70%,transparent 70%);pointer-events:none}
.brand{position:absolute;left:0;top:0;z-index:3;width:540px;height:80px;display:flex;align-items:center;gap:14px;padding:0 0 0 30px;color:#fff;background:linear-gradient(118deg,#155FA4 0%,#1E73BE 55%,#2C87D2 100%);clip-path:polygon(0 0,100% 0,94% 100%,0 100%)}
.brand::after{content:'';position:absolute;right:70px;top:0;bottom:0;width:150px;background:linear-gradient(118deg,transparent 42%,rgba(255,255,255,.07) 42%,rgba(255,255,255,.07) 58%,transparent 58%);pointer-events:none}
.brand-emblem{width:54px;height:54px;border-radius:50%;border:2px solid rgba(255,255,255,.92);box-shadow:inset 0 0 0 4px rgba(255,255,255,.16);display:grid;place-items:center;font-size:24px;font-weight:800;flex:none;background:rgba(255,255,255,.1)}
.brand-txt b{display:block;font-size:28px;letter-spacing:2px;line-height:1.15;font-weight:800}
.brand-txt small{display:flex;align-items:center;gap:10px;font-size:14px;letter-spacing:6px;opacity:.9;margin-top:3px;font-style:italic}
.brand-txt small::before,.brand-txt small::after{content:'';width:46px;height:1px;background:rgba(255,255,255,.7)}
.top-right{display:flex;align-items:center;gap:25px;position:relative;z-index:2}
.top .icon-btn{color:#fff}
.top .icon-btn:hover{background:rgba(255,255,255,.16);color:#fff}
.dot-badge{border-color:#2F86D2!important}
.user-chip{display:flex;align-items:center;gap:8px;padding:0 4px;height:44px;border-radius:22px;cursor:pointer;color:#fff}
.user-chip:hover{background:rgba(255,255,255,.12)}
.user-chip .avatar{width:32px;height:32px;border:1px solid rgba(255,255,255,.8)}
.uc-main{display:flex;flex-direction:column;line-height:1.3}
.uc-main b{font-size:16px;font-weight:700;color:#fff}
.uc-main small{font-size:12px}
.top-pill{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:36px;min-width:128px;padding:0 14px;border-radius:20px;background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.45);color:#fff;font-size:14px}
.top-pill .ic{width:16px;height:16px}
.top-pill:hover{background:rgba(255,255,255,.32)}
.top .dropdown-menu{top:52px;width:320px}
.side{position:fixed;left:20px;top:100px;bottom:51px;width:225px;border-radius:8px;background:#458FD8 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='191' height='297' viewBox='0 0 191 297' fill='none' stroke='white' stroke-opacity='.28' stroke-width='1.2'%3E%3Cpath d='M2 295h187M8 295v-46h175v46M2 249h187l-10-12H12z'/%3E%3Cpath d='M22 237v-26h147v26M16 211h159l-8-10H24z'/%3E%3Cpath d='M80 295v-26a15 15 0 0 1 31 0v26M30 260h16v18H30zM145 260h16v18h-16zM40 222h12v10H40zM139 222h12v10h-12z'/%3E%3Cpath d='M70 201V96h51v105M64 96h63l-6-10H70zM74 86V58h43v28M70 58h51l-25.5-34z'/%3E%3Ccircle cx='95.5' cy='72' r='9'/%3E%3Cpath d='M95.5 72v-5M95.5 72l4 2M95.5 24V4M91 10h9'/%3E%3Cpath d='M82 112h11v18H82zM98 112h11v18H98zM82 142h11v18H82zM98 142h11v18H98zM82 172h11v18H82zM98 172h11v18H98z'/%3E%3C/svg%3E") no-repeat center bottom/191px 297px local;padding:10px 5px 310px;overflow-y:auto;z-index:10;color:#fff;scrollbar-width:none}
.nav-sec+.nav-sec{margin-top:10px}
.nav-group{display:flex;align-items:center;gap:4px;width:100%;height:30px;padding:0 7.5px;border:0;background:none;font-size:12px;font-weight:700;color:#E3F1F9;text-align:left;cursor:pointer}
.nav-group::before{content:'';width:3px;height:12px;border-radius:12px;background:#E3F1F9;flex:none}
.nav-group .ic{margin-left:auto;transition:transform .2s;opacity:.85}
.nav-sec:not(.open) .nav-group .ic{transform:rotate(-90deg)}
.nav-sec:not(.open) .nav-items{display:none}
.nav-group:hover{color:#fff}
.nav a{display:flex;align-items:center;gap:5px;height:34px;padding:0 7.5px;margin-top:5px;border-radius:4px;color:#fff;font-size:14px;font-weight:700;transition:background .15s}
.nav a:hover{background:rgba(255,255,255,.12)}
.nav a.active{background:rgba(255,255,255,.2)}
.nav-ic{width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,.3);display:grid;place-items:center;font-style:normal;flex:none}
.nav-ic .ic{width:12px;height:12px;stroke-width:2.4}
.nav-badge{margin-left:auto;min-width:18px;height:18px;border-radius:9px;background:#FF5A5A;color:#fff;font-size:11px;display:grid;place-items:center;padding:0 5px;font-weight:500}
.msg-pop{width:360px;padding:0;overflow:hidden}
.mp-head{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--line);font-size:14px}
.mp-list{max-height:360px;overflow:auto}
.msg-pop .msg-item{padding:12px 16px 12px 22px;gap:12px}
.msg-pop .msg-item.unread::after{top:20px}
.msg-pop .msg-ic{width:34px;height:34px;border-radius:9px}
.msg-pop .msg-title{font-size:13px}
.msg-pop .msg-desc{font-size:12px;line-height:1.6}
.msg-pop .msg-time{margin-top:2px}
.dropdown-menu a.mp-foot{justify-content:center;gap:4px;padding:11px;border-radius:0;color:var(--primary)}
.main{margin-left:265px;padding:100px 20px 51px 0;display:flex;flex-direction:column}
.vtabs{height:47px;background:#fff;border-radius:8px 8px 0 0;display:flex;align-items:flex-end;padding-left:16px;border-bottom:1px solid #E3F1F9;box-shadow:inset 0 -1px 0 #E4E7ED;flex:none}
.vtabs:has(+ .page > :not(.page-head):not(.wf-search):not(.wf-sheet):first-child){margin-bottom:10px}
.vt-back{height:40px;border:0;background:none;color:#AFAFAF;font-size:14px;display:flex;align-items:center;gap:2px;padding:0 16px}
.vt-back:hover{color:var(--primary)}
.vt{height:40px;padding:0 20px;display:flex;align-items:center;gap:6px;font-size:14px;color:#AFAFAF;border-radius:4px 4px 0 0}
a.vt:hover{color:var(--primary)}
.vt.on{background:#EAF4F9;color:#2A8DC7;font-weight:700;padding:0 24px}
.vt-x{color:inherit;display:grid;place-items:center;width:16px;height:16px;border-radius:50%}
.vt-x:hover{background:#2A8DC7;color:#fff}
.vt-more-wrap{margin-left:auto;align-self:stretch}
.vt-more{width:43px;height:100%;border:0;border-left:1px solid #E4E7ED;background:none;color:#606266;display:grid;place-items:center}
.vt-more:hover{color:var(--primary)}
.vt-more-wrap .dropdown-menu{top:46px;min-width:280px;border-radius:4px}
.top-search{display:flex;align-items:center;gap:6px;height:32px;margin:4px;padding:0 11px;border-radius:4px;box-shadow:0 0 0 1px #DCDFE6 inset;color:#A8ABB2;font-size:14px;cursor:text}
.top-search input{border:none;background:none;outline:none;flex:1;min-width:0;font-size:14px;color:#606266}
.top-search input::placeholder{color:var(--placeholder)}
.icon-btn{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;color:var(--text-2);position:relative;border:none;background:none}
.icon-btn:hover{background:var(--primary-light);color:var(--primary)}
.dot-badge{position:absolute;top:1px;right:-3px;transform:scale(.85);min-width:16px;height:16px;border-radius:8px;background:#FF4D4F;color:#fff;font-size:10px;display:grid;place-items:center;padding:0 4px;border:2px solid #fff;box-sizing:content-box;font-weight:600}
.avatar{width:32px;height:32px;border-radius:50%;object-fit:cover;background:var(--gray-bg)}
.foot{position:fixed;left:0;right:0;bottom:0;height:31px;z-index:20;background:#fff;border-top:1px solid #E4E7ED;display:flex;align-items:center;justify-content:center;font-size:14px;color:rgba(0,0,0,.85)}
.dropdown{position:relative}
.dropdown-menu{position:absolute;right:0;top:44px;background:#fff;border:1px solid #E4E7ED;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.08),0 3px 6px -4px rgba(0,0,0,.12);min-width:260px;padding:6px;display:none;z-index:30}
.dropdown.open .dropdown-menu{display:block;animation:pop .18s}
.dropdown-menu a,.dropdown-menu button.dm-item{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:4px;color:#606266;font-size:14px;width:100%;border:none;background:none;text-align:left}
.dropdown-menu a:hover,.dropdown-menu button.dm-item:hover{background:#EAF4F9;color:#2A8DC7}
.dm-title{font-size:12px;color:var(--text-3);padding:8px 10px 4px}
.dm-sep{height:1px;background:var(--line);margin:6px 0}
.dm-role{display:flex;align-items:center;justify-content:space-between;gap:6px;padding:6px 10px;border-radius:4px}
.dm-role:hover{background:#F7F9FB}
.dm-role b{font-size:14px;font-weight:500}
.dm-role .dm-links{display:flex;gap:4px}
.dm-role .dm-links a{white-space:nowrap;padding:3px 8px;font-size:12px;border:1px solid var(--line);border-radius:4px;color:var(--text-2)}
.dm-role .dm-links a:hover{border-color:var(--primary);color:var(--primary);background:#fff}
.dm-role.cur b{color:var(--primary)}
.page{flex:1;width:100%}
.page-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;gap:16px;flex-wrap:wrap}
.page>.page-head:first-child{background:#fff;border-radius:0 0 8px 8px;padding:15px 24px}
.page-title{font-size:18px;font-weight:600;color:#1E323F;line-height:24px;display:flex;align-items:center;gap:10px;position:relative;padding-bottom:10px}
.page-title::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.page-desc{color:#8A94A3;margin-top:6px;font-size:14px}
.page-actions{display:flex;gap:12px;flex-wrap:wrap}

/* ===== 卡片与布局 ===== */
.card{background:linear-gradient(180deg,#EFF8FF 0,#fff 64px) #fff;border-radius:8px;box-shadow:none;border:0}
.card-head{display:flex;align-items:center;justify-content:space-between;padding:16px 24px 6px;gap:12px}
.card-head>a.link:last-child{background:#E8F5FF;border:1px solid #fff;border-radius:24px;padding:2px 10px;font-size:12px;color:#2A8DC7}
.card-head>a.link:last-child:hover{text-decoration:none;background:#D6EAF9}
.card-title{font-size:18px;font-weight:700;color:#3C444F;display:flex;align-items:center;gap:8px;position:relative;padding-bottom:10px}
.card-title::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.card>.table-wrap,.card>.tab-panel>.table-wrap{padding:0 24px}
.card>.tabs+.tab-panel>.table-wrap,.card>.filters+.table-wrap{padding-top:4px}
.card-title>.ic:first-child{display:none}
.card-body{padding:16px 24px}
.grid{display:grid;gap:10px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g5{grid-template-columns:repeat(5,minmax(0,1fr))}
.g-main{grid-template-columns:minmax(0,1fr) 400px}
.g-main-wide{grid-template-columns:minmax(0,1fr) 460px}
.span2{grid-column:span 2}

/* ===== 统计卡 ===== */
.stat{padding:20px 24px;display:flex;align-items:center;gap:16px;position:relative;overflow:hidden;background:linear-gradient(180deg,#C5E9FF 0%,#fff 80%) #fff;border-radius:8px 8px 4px 4px}
.stat-body{min-width:0}
.stat-ic{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;flex-shrink:0;color:#fff;box-shadow:0 6px 12px rgba(42,141,199,.22)}
.stat-ic.blue{background:linear-gradient(135deg,#7CCBFF,#2A8DC7)}
.stat-ic.green{background:linear-gradient(135deg,#74E3B5,#19B87A);box-shadow:0 6px 12px rgba(25,184,122,.22)}
.stat-ic.orange{background:linear-gradient(135deg,#FFCB78,#F59200);box-shadow:0 6px 12px rgba(245,146,0,.22)}
.stat-ic.red{background:linear-gradient(135deg,#FFA3A3,#F05454);box-shadow:0 6px 12px rgba(240,84,84,.22)}
.stat-ic.gray{background:linear-gradient(135deg,#C9D1DB,#8D99A8);box-shadow:0 6px 12px rgba(100,115,135,.18)}
.stat-num{font-size:28px;font-weight:700;line-height:1.25;color:#2A8DC7;font-variant-numeric:tabular-nums}
.stat-num small{font-size:13px;font-weight:400;color:var(--text-3);margin-left:2px}
.stat-label{color:#3C444F;font-size:14px;font-weight:700}
.stat-trend{font-size:12px;color:var(--text-3)}
a.stat{color:inherit;transition:box-shadow .15s,border-color .15s}
a.stat:hover{box-shadow:0 6px 18px rgba(42,141,199,.16)}

/* ===== 表格（vxe-table 全边框） ===== */
.table-wrap{overflow:auto}
.tbl{width:100%;border-collapse:separate;border-spacing:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,'PingFang SC','Microsoft YaHei',sans-serif;border-left:1px solid #BADEF3}
.tbl th{background:#D6EAF9;color:#2A8DC7;font-weight:700;text-align:left;height:48px;padding:0 10px;font-size:14px;white-space:nowrap;border-right:1px solid #BADEF3;border-top:1px solid #BADEF3;border-bottom:1px solid #BADEF3}
.tbl th:first-child{border-top-left-radius:4px}
.tbl th:last-child{border-top-right-radius:4px}
.tbl th.sortable{cursor:pointer;user-select:none}
.tbl th.sortable::after{content:'↕';margin-left:4px;color:#7FB6DB;font-size:11px}
.tbl th[data-dir=asc]::after{content:'↑';color:var(--primary)}
.tbl th[data-dir=desc]::after{content:'↓';color:var(--primary)}
.tbl td{height:49px;padding:8px 10px;border-bottom:1px solid #E8EAEC;border-right:1px solid #BADEF3;font-size:14px;vertical-align:middle;color:#333}
.tbl td:not(:has(.t-title)){white-space:nowrap}
.tbl tbody tr{transition:background .15s}
.tbl tbody tr:hover td{background:#F3F9FD}
.tbl tr.overdue td{background:#FFFAFA}
.tbl tr.overdue td:first-child{box-shadow:inset 3px 0 0 var(--danger)}
.tbl .t-title{color:#333;font-weight:500;max-width:400px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block}
a.t-title:hover{color:var(--primary)}
.tbl .t-sub{font-size:12px;color:var(--text-3);margin-top:2px}
.tbl .tag{height:24px;padding:0 9px;border-radius:9999px}
.ops{display:flex;gap:0;white-space:nowrap;margin:0 -11px}
.ops .link,.ops>a{font-size:12px;font-weight:500;padding:5px 11px;border-radius:3px}
.ops .link:hover,.ops>a:hover{text-decoration:none;background:#EAF4F9}
.ops .link-danger:hover{background:#FEF0F0}
.pager{display:flex;align-items:center;justify-content:flex-end;gap:0;padding:8px 24px 16px;color:#606266;font-size:14px}
.pager>span{margin-right:16px}
.pager button{min-width:32px;height:32px;padding:0 4px;border:0;background:#fff;border-radius:2px;color:#303133;font-size:14px;font-weight:500}
.pager button[data-pg=prev],.pager button[data-pg=next]{color:#A8ABB2;font-size:18px}
.pager button[data-pg=prev]{margin-left:16px}
.pager button:hover:not(:disabled){color:var(--primary)}
.pager button.on{background:#fff;color:#2A8DC7;font-weight:700}
.pager button:disabled{opacity:.5;cursor:not-allowed}
.pager .select{width:128px;height:32px;font-size:14px;margin-left:16px;border:0;box-shadow:0 0 0 1px #DCDFE6 inset;color:#606266}
.empty{padding:48px 20px;text-align:center;color:var(--text-3)}
.overdue-txt{color:var(--danger);font-weight:500;display:inline-flex;align-items:center;gap:4px}
.remain-txt{color:var(--warn);font-weight:500}
.ok-txt{color:var(--success)}

/* ===== 筛选栏（msearch：四列网格，按钮在末列） ===== */
.filters{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px 16px;align-items:start;padding:16px 24px}
.card>.filters:first-child{border-bottom:10px solid #E3F1F9}
.filters .f-actions{grid-column:4;display:flex;justify-content:flex-end;align-items:center;gap:10px;height:44px}
.filters .f-actions .btn+.btn{margin-left:0}
.f-box{display:flex;align-items:center;height:44px;min-width:0;border:1px solid #E3F1F9;border-radius:4px;background:#fff;padding:5px 8px;transition:border-color .15s}
.f-box:focus-within{border-color:var(--primary)}
.f-lbl{padding:0 12px 0 4px;margin-right:4px;color:#485066;font-size:14px;font-weight:700;white-space:nowrap;position:relative;flex:none}
.f-lbl::after{content:'';position:absolute;right:0;top:50%;width:1px;height:20px;margin-top:-10px;background:#E3F1F9}
.f-box .input,.f-box .select{border:0;height:32px;flex:1;min-width:0;width:auto;box-shadow:none!important;background-color:#fff;color:#606266;padding:0 11px}
.f-box .select{padding-right:28px}
.f-date .input{padding:0 6px;font-size:13px}
.f-to{color:#A8ABB2;padding:0 2px;flex:none}
.search{position:relative;display:inline-flex}
.search .ic{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--placeholder)}
.search .input{padding-left:32px;width:240px}
.date-range{display:inline-flex;align-items:center;gap:6px;color:var(--text-3)}
.date-range .input{width:140px}

/* ===== 标签页 ===== */
.tabs{display:flex;gap:4px;border-bottom:1px solid #E4E7ED;padding:0 24px;overflow-x:auto}
.tab{padding:14px 14px;border:none;background:none;color:#485066;font-size:15px;position:relative;white-space:nowrap}
.tab:hover{color:var(--primary)}
.tab.on{color:var(--primary);font-weight:600}
.tab.on::after{content:'';position:absolute;left:12px;right:12px;bottom:-1px;height:2px;background:var(--primary);border-radius:2px}
.tab .cnt{margin-left:4px;font-size:12px;background:var(--gray-bg);color:var(--text-3);border-radius:9px;padding:0 6px;font-weight:400}
.tab.on .cnt{background:var(--primary-light);color:var(--primary)}
.tab-panel{display:none}.tab-panel.on{display:block}
.seg{display:inline-flex;background:#E3F1F9;border-radius:36px;padding:3px;gap:2px}
.seg button{border:none;background:none;height:28px;padding:0 16px;border-radius:28px;font-size:13px;color:#485066}
.seg button.on{background:var(--primary);color:#fff;font-weight:500}

/* ===== 表单页 ===== */
.form-card{background:#fff;border-radius:8px}
.form-section{padding:16px 24px;border-bottom:1px solid var(--line)}
.form-section:last-of-type{border-bottom:none}
.form-section-title{font-weight:600;font-size:18px;color:#1E323F;margin-bottom:20px;display:flex;align-items:center;gap:8px;position:relative;padding-bottom:10px}
.form-section-title::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.form-section-title .hint{font-weight:400;margin-left:4px}
.form-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 28px}
.form-grid.g3c{grid-template-columns:repeat(3,minmax(0,1fr))}
.field .input,.field .select{width:100%;height:36px}
.form-foot{position:sticky;bottom:31px;background:#fff;border-top:1px solid #E4E7ED;padding:12px 24px;display:flex;justify-content:center;gap:12px;align-items:center;border-radius:0 0 8px 8px;z-index:5}
.draft-status{position:absolute;left:24px;color:var(--text-3);font-size:13px;display:flex;align-items:center}
.link-btn{border:0;background:none;padding:0;font:inherit;cursor:pointer;text-align:left}
.rk-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.rk-sum div{padding:12px 16px;border-radius:4px;background:#F2F9FE;border:1px solid #DCEBF7}
.rk-sum b{display:block;font-size:22px;color:var(--primary);font-variant-numeric:tabular-nums}
.rk-sum span{font-size:12px;color:var(--text-3)}
.type-switch{display:flex;align-items:center;gap:16px;margin-bottom:12px;padding:10px 20px;border-radius:4px;background:#fff}
.type-switch .ts-lbl{font-size:14px;font-weight:700;color:var(--text);flex:none}
.type-switch .radio-group{gap:12px}
.type-switch .radio-card{height:36px;padding:0 16px;border-radius:4px;font-size:14px}
.type-switch .radio-card:has(input:checked){font-weight:700}

/* ===== 富文本编辑器 ===== */
.editor-box{position:relative;border:1px solid var(--border);border-radius:8px;background:#fff}
.editor-bar{display:flex;flex-wrap:wrap;gap:2px;padding:6px 8px;border-bottom:1px solid var(--line);background:#FAFBFC;align-items:center;border-radius:8px 8px 0 0}
.editor-bar button{width:30px;height:30px;border:none;background:none;border-radius:4px;color:var(--text-2);display:grid;place-items:center;cursor:pointer}
.editor-bar button:hover{background:var(--primary-light);color:var(--primary)}
.editor-bar button.on{background:#E3F0FA;color:var(--primary)}
.editor-bar .sep{width:1px;height:18px;background:var(--line);margin:0 6px}
.editor-bar .wc{margin-left:auto;font-size:12px;color:var(--text-3)}
.editor-bar .ed-dd .ed-dd-btn{width:auto;min-width:76px;display:flex;justify-content:space-between;gap:6px;padding:0 8px;font-size:13px;border:1px solid var(--border);background:#fff;height:28px}
.editor-bar .ed-dd .dropdown-menu{left:0;right:auto;top:32px;min-width:140px}
.editor-bar .ed-dd .dropdown-menu .dm-item{width:100%;height:auto;display:flex}
.editor-bar .ed-dd .ed-h2{font-size:18px;font-weight:700}
.editor-bar .ed-dd .ed-h3{font-size:16px;font-weight:700}
.ed-pop{position:absolute;left:8px;top:48px;z-index:20;width:380px;padding:14px;background:#fff;border:1px solid #E4E7ED;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.1);display:flex;flex-direction:column;gap:10px}
.ed-pop[hidden]{display:none}
.ed-pop-title{font-size:14px;font-weight:700;color:var(--text)}
.ed-pop[data-mode=link] .ed-only-image,.ed-pop[data-mode=image] .ed-only-link{display:none}
.ed-img-src{display:flex;align-items:center;gap:14px;font-size:13px}
.ed-local{display:inline-flex;align-items:center;gap:4px;color:var(--primary);cursor:pointer}
.ed-link-btn{border:0;background:none;color:var(--primary);font-size:13px;cursor:pointer;padding:0}
.ed-pop-foot{display:flex;justify-content:flex-end;gap:8px}
.editor{min-height:240px;padding:16px 18px;outline:none;line-height:1.9;font-size:15px}
.editor:empty::before{content:attr(data-placeholder);color:var(--placeholder)}
.editor p{margin-bottom:10px;text-indent:2em}
.editor h2{font-size:20px;font-weight:700;margin:14px 0 8px;line-height:1.5}
.editor h3{font-size:17px;font-weight:700;margin:12px 0 6px;line-height:1.5}
.editor blockquote,.m-editor blockquote{margin:10px 0;padding:8px 14px;border-left:4px solid #2A8DC7;background:#F4F9FD;color:#4A5568}
.editor ul,.editor ol,.m-editor ul,.m-editor ol{padding-left:2em;margin:8px 0}
.editor ul,.m-editor ul{list-style:disc}
.editor ol,.m-editor ol{list-style:decimal}
.editor a,.m-editor a{color:var(--primary);text-decoration:underline}
.editor hr{border:0;border-top:1px dashed var(--border);margin:14px 0}
.editor img{display:block;margin:10px auto;border-radius:6px;max-height:260px;max-width:100%}

/* ===== 上传 ===== */
.upload{border:1.5px dashed var(--border);border-radius:10px;padding:22px;text-align:center;color:var(--text-3);cursor:pointer;background:#FAFCFE;transition:all .15s;position:relative;display:flex;flex-direction:column;align-items:center;gap:6px}
.upload:hover{border-color:var(--primary);background:#F2F9FE;color:var(--primary)}
.upload input{position:absolute;inset:0;opacity:0;cursor:pointer}
.upload b{color:var(--text);font-weight:500}
.files{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.files:not(:empty){margin-top:12px}
.file-item{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff;position:relative}
.file-item img{width:100%;height:108px;object-fit:cover;display:block}
.fi-doc{height:108px;display:grid;place-items:center;background:var(--primary-light);color:var(--primary);font-weight:700}
.fi-meta{padding:6px 8px;font-size:12px;color:var(--text-3);display:flex;flex-direction:column}
.fi-name{color:var(--text-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fi-del{position:absolute;top:6px;right:6px;width:24px;height:24px;border-radius:50%;border:none;background:rgba(0,0,0,.55);color:#fff;display:grid;place-items:center;font-size:15px;line-height:1}
.fi-del:hover{background:var(--danger)}
.file-item input{width:100%;border:none;border-top:1px solid var(--line);padding:7px 8px;font-size:12px;outline:none}

/* ===== 详情 ===== */
.kv{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid #C7E1F0;border-radius:8px;overflow:hidden}
.kv.c2{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.kv.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.kv>div{display:flex;min-height:57px;box-shadow:1px 1px 0 #C7E1F0;min-width:0}
.kv dt{width:130px;flex:none;background:#F1F9FF;color:#3C444F;font-weight:700;font-size:16px;padding:10px 15px;display:flex;align-items:center;border-right:1px solid #C7E1F0}
.kv dd{padding:10px 15px;color:#696F7D;font-size:16px;display:flex;align-items:center;flex-wrap:wrap;gap:6px;min-width:0;word-break:break-all}
.article h2{font-size:22px;line-height:1.5;margin-bottom:10px}
.article-meta{display:flex;gap:16px;flex-wrap:wrap;color:var(--text-3);font-size:13px;padding-bottom:16px;border-bottom:1px solid var(--line);margin-bottom:18px}
.article-body p{text-indent:2em;line-height:2;margin-bottom:12px;font-size:15px;color:#434A55}
.article-body figure{margin:16px 0;text-align:center}
.article-body figure img{border-radius:8px;max-height:340px;width:100%;object-fit:cover}
.article-body figcaption{font-size:12px;color:var(--text-3);margin-top:6px}
.gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.gallery figure{border-radius:8px;overflow:hidden;border:1px solid var(--line);background:#fff}
.gallery img{width:100%;height:120px;object-fit:cover;display:block}
.gallery figcaption{padding:6px 8px;font-size:12px;color:var(--text-3)}
.kv.c1{grid-template-columns:1fr}
.kv.c1 dt{width:108px;font-size:14px}.kv.c1 dd{font-size:14px}.kv.c1>div{min-height:46px}
.kv dd .hint{margin-left:4px}
.att-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.att{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:#fff}
.att-ic{width:38px;height:38px;border-radius:8px;display:grid;place-items:center;color:#fff;font-size:11px;font-weight:700;flex:none}
.att-main{flex:1;min-width:0;display:flex;flex-direction:column}
.att-main b{font-weight:500;color:var(--text);font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.att-main span{font-size:12px;color:var(--text-3)}
.att-empty{padding:14px;border:1px dashed var(--line);border-radius:8px;color:var(--text-3);font-size:13px;text-align:center}
.type-head{display:flex;align-items:center;gap:10px;margin-bottom:14px;color:var(--primary)}
.type-head b{font-size:20px;color:var(--text)}
.cover{border-radius:8px;overflow:hidden;border:1px solid var(--line);background:#fff;margin:0}
.cover img{width:100%;height:190px;object-fit:cover;display:block}
.cover figcaption{padding:8px 10px;font-size:12px;color:var(--text-3);display:flex;align-items:center;gap:4px}
.intro-box{border:1px solid #C7E1F0;border-radius:8px;padding:14px 16px;background:#F7FBFE}
.intro-box b{font-size:15px;color:var(--text)}
.intro-box p{margin-top:6px;line-height:1.9;color:#434A55;font-size:14px}
.photo-gallery{grid-template-columns:repeat(2,1fr)}
.photo-gallery img{height:200px}
.photo-gallery figcaption{display:flex;flex-direction:column;gap:2px;padding:8px 10px}
.photo-gallery figcaption b{color:var(--text);font-weight:500;font-size:13px}
.photo-gallery figcaption em{font-style:normal;color:var(--text-2)}
.sticky-actions{position:sticky;top:100px}
.action-card{padding:18px 20px;display:flex;flex-direction:column;gap:10px}
.action-card .btn{width:100%;height:42px}
.timer{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:10px;background:var(--warn-bg);border:1px solid var(--warn-bd);color:#9A5C00}
.timer.danger{background:var(--danger-bg);border-color:var(--danger-bd);color:#A8161B}
.timer.ok{background:var(--success-bg);border-color:var(--success-bd);color:#0E7A4C}
.timer b{font-size:20px;font-variant-numeric:tabular-nums}
.flow-steps{display:flex;align-items:flex-start;gap:0;padding:4px 0}
.fs{flex:1;display:flex;flex-direction:column;align-items:center;position:relative;text-align:center;font-size:12px;color:var(--text-3)}
.fs::before{content:'';position:absolute;top:13px;left:-50%;right:50%;height:2px;background:var(--line)}
.fs:first-child::before{display:none}
.fs.done::before,.fs.cur::before{background:var(--success)}
.fs i{width:28px;height:28px;border-radius:50%;background:#fff;border:2px solid var(--line);display:grid;place-items:center;font-style:normal;font-weight:600;color:var(--text-3);position:relative;z-index:1;margin-bottom:6px;font-size:12px}
.fs.done i{background:var(--success);border-color:var(--success);color:#fff}
.fs.cur i{border-color:var(--primary);color:var(--primary);box-shadow:0 0 0 4px var(--primary-light)}
.fs.back i{background:var(--danger);border-color:var(--danger);color:#fff}
.fs.cur b{color:var(--primary)}
.fs b{color:var(--text);font-weight:500;font-size:13px}
.sens-card{padding:14px 16px;border-radius:10px;border:1px solid var(--line);background:#FAFBFC}

/* ===== 图表 ===== */
.bars{display:flex;align-items:flex-end;gap:14px;height:200px;padding-top:10px}
.bar-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end}
.bar-stack{width:100%;max-width:34px;display:flex;flex-direction:column-reverse;border-radius:6px 6px 0 0;overflow:hidden}
.bar-stack i{display:block;width:100%}
.bar-col span{font-size:11px;color:var(--text-3);white-space:nowrap}
.bar-col em{font-style:normal;font-size:12px;color:var(--text-2);font-weight:600}
.hbar{display:flex;align-items:center;gap:10px;margin-bottom:12px;font-size:13px}
.hbar .hb-name{width:110px;color:var(--text-2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hbar .hb-track{flex:1;height:10px;background:var(--gray-bg);border-radius:5px;overflow:hidden;display:flex}
.hbar .hb-track i{display:block;height:100%}
.hbar .hb-val{width:64px;text-align:right;color:var(--text);font-weight:600;font-variant-numeric:tabular-nums}
.legend{display:flex;gap:16px;font-size:12px;color:var(--text-2);flex-wrap:wrap}
.legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.donut-wrap{display:flex;align-items:center;gap:20px}
.donut-wrap svg{flex-shrink:0}
.donut-legend{flex:1;display:flex;flex-direction:column;gap:10px}
.donut-legend div{display:flex;align-items:center;gap:8px;font-size:13px;white-space:nowrap}
.donut-legend i{width:10px;height:10px;border-radius:3px}
.donut-legend b{margin-left:auto;font-variant-numeric:tabular-nums}
.rank-no{width:24px;height:24px;border-radius:6px;display:inline-grid;place-items:center;font-weight:700;font-size:12px;background:var(--gray-bg);color:var(--text-2)}
.rank-no.r1{background:linear-gradient(135deg,#FFD66B,#F29100);color:#fff}
.rank-no.r2{background:linear-gradient(135deg,#D7DEE8,#9AA6B6);color:#fff}
.rank-no.r3{background:linear-gradient(135deg,#F3C39B,#C9804A);color:#fff}

/* ===== 消息 ===== */
.msg-item{display:flex;gap:14px;padding:16px 20px;border-bottom:1px solid var(--line);cursor:pointer;transition:background .15s;position:relative}
.msg-item:hover{background:#F9FBFD}
.msg-item.unread::after{content:'';position:absolute;left:8px;top:24px;width:6px;height:6px;border-radius:50%;background:var(--danger)}
.msg-ic{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;flex-shrink:0}
.msg-main{flex:1;min-width:0}
.msg-title{font-weight:600;color:var(--text);display:flex;gap:8px;align-items:center}
.msg-item:not(.unread) .msg-title{font-weight:500;color:var(--text-2)}
.msg-desc{font-size:13px;color:var(--text-3);margin-top:3px}
.msg-time{font-size:12px;color:var(--text-3);white-space:nowrap}
.welcome{padding:22px 26px;border-radius:8px;background:linear-gradient(90deg,#1F7FC1 0%,#4A92DB 100%);color:#fff;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:space-between;gap:20px}
.welcome::after{content:'';position:absolute;right:-70px;top:-90px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.07)}
.welcome::before{content:'';position:absolute;right:160px;bottom:-130px;width:220px;height:220px;border-radius:50%;background:rgba(255,255,255,.05)}
.welcome h1{font-size:20px;font-weight:700}
.welcome p{opacity:.85;margin-top:6px;font-size:13px}
.welcome .btn{background:#fff;color:var(--primary);border-color:#fff;position:relative;z-index:1}
.welcome .btn:hover{background:#F2F9FE}
.welcome .btn-ghost-w{background:rgba(255,255,255,.14);color:#fff;border-color:rgba(255,255,255,.4)}
.welcome .btn-ghost-w:hover{background:rgba(255,255,255,.24);color:#fff}
.todo-item{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px dashed var(--line)}
.todo-item:last-child{border-bottom:none}
.todo-item .ti-main{flex:1;min-width:0}
.todo-item .ti-title{font-weight:500;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.todo-item .ti-sub{font-size:12px;color:var(--text-3)}
.perm-yes{color:var(--success)}.perm-no{color:#C8CAD1}.perm-part{color:var(--warn);font-size:12px}
.diff-del{background:#FDECEC;color:#A8161B;text-decoration:line-through;border-radius:3px;padding:0 2px}
.diff-add{background:#E3F8EE;color:#0E7A4C;border-radius:3px;padding:0 2px}
.zip-tree{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;background:#1F2733;color:#D5DEE8;border-radius:10px;padding:16px 18px;line-height:1.9}
.zip-tree .d{color:#7CC4FA}.zip-tree .c{color:#7C8898}
.clean-text{white-space:pre-wrap;font-size:14px;line-height:1.9;background:#FAFBFC;border:1px solid var(--line);border-radius:10px;padding:16px 18px;max-height:420px;overflow:auto}
.clean-text .ph{color:var(--primary);background:var(--primary-light);border-radius:4px;padding:1px 4px}
.kanban{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.kb-col{background:#EAF4F9;border-radius:8px;padding:12px}
.kb-head{display:flex;align-items:center;gap:8px;font-weight:600;padding:4px 4px 12px}
.kb-card{background:#fff;border-radius:6px;padding:12px 14px;margin-bottom:10px;border:1px solid #DCEBF6}
.kb-card b{display:block;font-size:14px;line-height:1.5;color:var(--text)}
.kb-card .kb-meta{font-size:12px;color:var(--text-3);margin-top:6px}
.forbid{max-width:520px;margin:60px auto;text-align:center}
.forbid .big-ic{width:88px;height:88px;border-radius:50%;background:var(--danger-bg);color:var(--danger);display:grid;place-items:center;margin:0 auto 20px}
.success-box{max-width:640px;margin:20px auto;text-align:center;padding:40px 36px}
.success-box .big-ic{width:80px;height:80px;border-radius:50%;background:var(--success-bg);color:var(--success);display:grid;place-items:center;margin:0 auto 18px}
/* ===== 统一待办（对齐智慧学工“我的待办”） ===== */
.page>.wf-search:first-child,.page>.wf-sheet:first-child{border-radius:0 0 8px 8px}
.wf-search{background:#fff;margin-bottom:10px}
.wf-search .filters,.wf-sheet .filters{padding:16px 24px}
.wf-table{background:#fff;padding-top:16px}
.wf-table>.table-wrap{padding:0 24px}
.wf-sheet{background:#fff;padding-bottom:4px}
.wf-sheet>.tabs{padding:0 24px}
.wf-sheet .tab-panel>.table-wrap{padding:0 24px}
.wf-tools{display:flex;align-items:center;gap:12px;padding:0 24px 10px}
.tbl td.seq,.tbl th.seq-h{width:70px}
.tbl th.tc,.tbl td.tc{text-align:center}
.tbl td.wf-op{max-width:320px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#606266}
.wf-batch{display:grid;grid-template-columns:240px minmax(0,1fr);gap:20px;padding:0 24px}
.wf-batch .wf-tools{padding:0 0 10px}
.wf-batch-main>.table-wrap{padding:0}
.wf-batch-main>.pager{padding-right:0}
.wf-cats{border-right:1px solid #E4E7ED;padding-right:16px;display:flex;flex-direction:column;gap:6px;align-self:stretch}
.wf-cats-title{display:flex;align-items:center;justify-content:space-between;font-size:16px;font-weight:700;color:#1E323F;padding:2px 8px 2px 10px;border-left:3px solid #2A8DC7;margin:4px 0 10px;line-height:20px}
.wf-cats-title em,.wf-cat em{font-style:normal;min-width:20px;height:18px;padding:0 6px;border-radius:9px;font-size:12px;font-weight:500;display:grid;place-items:center}
.wf-cats-title em{background:#F0F2F5;color:#909399}
.wf-cat{display:flex;align-items:center;justify-content:space-between;height:38px;padding:0 10px;border:0;border-radius:4px;background:none;color:#606266;font-size:14px;text-align:left}
.wf-cat:hover{background:#F3F9FD}
.wf-cat.on{background:#EAF4F9;color:#2A8DC7;font-weight:500;box-shadow:inset 3px 0 0 #2A8DC7}
.wf-cat em{background:#409EFF;color:#fff}
.btn-batch-ok{background:#95C6E3;border-color:#95C6E3;color:#fff}
.btn-batch-ok:hover{background:#2A8DC7;border-color:#2A8DC7;color:#fff}
.btn-batch-no{background:#FAB6B6;border-color:#FAB6B6;color:#fff}
.btn-batch-no:hover{background:#F56C6C;border-color:#F56C6C;color:#fff}
.wf-pills{display:flex;gap:8px;padding:16px 24px 0}
.wf-pill{height:36px;padding:0 14px;border:0;border-radius:4px 4px 0 0;background:#F0F2F5;color:#909399;font-size:16px}
.wf-pill:hover{color:#2A8DC7}
.wf-pill.on{background:#EAF4F9;color:#2A8DC7;box-shadow:inset 0 -2px 0 #2A8DC7}
.wf-task{display:flex;align-items:center;justify-content:space-between;gap:16px;margin:0 24px;padding:12px 0;border-bottom:1px solid #EEE}
.wf-task-title{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:12px;color:#444;min-width:0}
.wf-task-title b{font-size:16px;color:#1E323F;margin-right:4px}
.wf-task-title .tag{border:0;border-radius:4px;height:24px;padding:0 9px}
.wf-task-actions{display:flex;gap:10px;flex:none}
.wf-task-actions .btn-lg{height:32px;padding:0 15px;font-size:14px}
.wf-task-actions .btn-success{background:#2A8DC7;border-color:#2A8DC7}
.wf-task-actions .btn-success:hover{background:#1F77AD;border-color:#1F77AD}
.wf-handle>.tab-panel{padding:16px 24px 20px}
.wf-sec+.wf-sec{margin-top:20px}
.section-title{font-size:18px;font-weight:600;color:#1E323F;line-height:24px;position:relative;padding-bottom:10px;margin-bottom:12px}
.section-title::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.bd-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid #C7E1F0;border-radius:8px;overflow:hidden}
.bd-cell{padding:10px;min-height:86px;background:linear-gradient(#EDF8FF 8%,#fff);box-shadow:1px 1px 0 #C7E1F0;min-width:0;display:flex;flex-direction:column;justify-content:center;gap:6px}
.bd-cell span{font-size:16px;color:#627079}
.bd-cell b{font-size:16px;font-weight:700;color:#1E323F;word-break:break-all}
.wf-article{border:1px solid #C7E1F0;border-radius:8px;padding:20px 24px}
.wf-flow-panel{border:1px solid #C7E1F0;border-radius:8px;padding:16px 20px;background:linear-gradient(#EDF8FF 8%,#fff)}
.wf-sub{font-size:14px;font-weight:700;color:#1E323F;border-left:3px solid #2A8DC7;padding-left:8px;line-height:16px;margin-bottom:14px}
.wf-nodes{display:flex;align-items:center;flex-wrap:wrap;gap:10px 0}
.wf-node{display:inline-flex;align-items:center;gap:6px;height:38px;padding:8px 12px;border-radius:8px;border:1px solid #DCDFE6;background:#F5F7FA;font-size:14px;color:#909399}
.wf-node i{font-style:normal;font-size:12px}
.wf-node b{font-weight:600;color:#303133}
.wf-node span{font-size:12px;padding:0 6px;border-radius:4px;background:rgba(255,255,255,.8);line-height:20px}
.wf-node.done{background:#F0F9EB;border-color:#67C23A;color:#67C23A}
.wf-node.cur{background:#EAF4F9;border-color:#2A8DC7;color:#2A8DC7}
.wf-node.back{background:#FEF0F0;border-color:#F56C6C;color:#F56C6C}
.wf-arrow{color:#C0C4CC;margin:0 10px;font-size:16px}
.wf-top{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 15px}
.wf-top .section-title{margin:0}
.wf-sheet-body{margin-top:10px;padding:15px 20px}
.tag.tag-solid-ok{background:#67C23A;border-color:#67C23A;color:#fff;border-radius:4px}
"""

MOBILE_CSS = BASE_CSS + """
/* ===== H5 令牌（对齐智慧学工移动端） ===== */
:root{--primary:#0057F0;--primary-light:#EAF1FF;--primary-dark:#0047C6;--blue7:#BFD4FF;--blue8:#DCE8FF;
--text:#1E323F;--text-2:#55656F;--text-3:#8CA2B6;--line:#E6EEF7;--bg:#F0F7FF;--grad:linear-gradient(118deg,#065CF8 0%,#469FFF 77%)}
.btn{border-radius:22px;border-color:var(--primary);color:var(--primary)}
.btn-primary{background:var(--grad);border:0;color:#fff}
.btn-primary:hover{background:var(--grad);filter:brightness(1.05);color:#fff}
.tag{border:0;border-radius:2px;font-weight:500;height:20px;padding:0 6px}
.tag-warn{background:rgba(255,126,34,.1);color:#F59200}
.tag-primary{background:#EAF1FF;color:var(--primary)}
.tag-success{background:#E6F8EF;color:#12A86B}
.tag-danger{background:#FFEDED;color:#F04848}
.tag-gray{background:#F0F2F5;color:#8A94A3}
.notice{border-radius:8px}
/* ===== 手机外框（桌面预览用） ===== */
body.app-stage{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;gap:40px;padding:36px 20px 60px;background:radial-gradient(1200px 600px at 20% 0%,#DDEBF7 0%,transparent 60%),radial-gradient(900px 500px at 100% 100%,#E6F4EF 0%,transparent 55%),#EEF3F8}
.phone{width:375px;height:812px;background:var(--bg) linear-gradient(180deg,#E5F4FF 0,var(--bg) 220px) no-repeat;border-radius:46px;box-shadow:0 0 0 10px #1E2530,0 0 0 11px #3A4452,0 40px 80px rgba(15,40,80,.28);overflow:hidden;position:relative;display:flex;flex-direction:column;flex:none}
.phone::before{content:'';position:absolute;top:10px;left:50%;transform:translateX(-50%);width:120px;height:32px;border-radius:18px;background:#0B0F14;z-index:40}
.status-bar{height:48px;display:flex;align-items:center;justify-content:space-between;padding:6px 28px 0 34px;font-size:15px;font-weight:600;flex-shrink:0;background:#fff;color:#000;position:relative;z-index:3}
.sb-icons{display:flex;gap:5px;align-items:center}
.sb-icons .ic{stroke-width:2}
.notes{width:340px;flex:none;position:sticky;top:36px;display:flex;flex-direction:column;gap:14px}
.notes .card{background:#fff;border-radius:8px;box-shadow:var(--shadow-sm);border:1px solid #EDF0F4;padding:18px 20px}
.notes .n-role{font-size:12px;color:var(--text-3)}
.notes h3{font-size:18px;margin:2px 0 4px}
.notes .n-path{font-size:12px;color:var(--text-3);margin-bottom:12px;word-break:break-all}
.notes ul{list-style:none;display:grid;gap:8px;font-size:13px;color:var(--text-2)}
.notes li{display:flex;gap:8px;line-height:1.6}
.notes li::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--blue7);margin-top:8px;flex:none}
.notes .flow b{display:block;font-size:14px;margin-bottom:2px}
.notes .flow a{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:8px;background:#F0F7FF;font-size:13px;margin-top:6px;color:var(--text)}
.notes .flow a:hover{background:var(--primary-light);color:var(--primary)}
.notes>.btn{width:100%}
@media (max-width:820px){.notes{display:none}}
.m-header{height:44px;display:flex;align-items:center;justify-content:center;position:relative;background:#fff;flex-shrink:0;z-index:2;padding:0 56px}
.m-header h1{font-size:17px;font-weight:600;color:#000;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.m-back,.m-hr{position:absolute;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:2px;color:var(--text);border:none;background:none;font-size:14px;height:44px;min-width:44px}
.m-back{left:8px}.m-hr{right:12px;justify-content:flex-end;color:var(--primary)}
.m-body{flex:1;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;padding:12px 16px 20px;position:relative}
.m-body::-webkit-scrollbar{display:none}
.tabbar{height:82px;padding-bottom:24px;display:flex;background:linear-gradient(180deg,#FFFFFF 0%,#F4F9FF 100%);border-radius:22px 22px 0 0;flex-shrink:0;box-shadow:0 -4px 16px rgba(0,87,240,.08);position:relative;z-index:3}
.tabbar a{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;color:#696F7D;font-size:10px;position:relative}
.tabbar a.on{color:var(--primary);font-weight:700}
.tabbar a.on .tb-txt{background:linear-gradient(100deg,#065CF8,#469FFF 77%);-webkit-background-clip:text;background-clip:text;color:transparent}
.tabbar a.on .ic{filter:drop-shadow(0 2px 4px rgba(0,87,240,.25))}
.tabbar .tb-btn{flex:1;display:flex;align-items:center;justify-content:center;background:none;border:0;padding:0}
.tabbar .tb-plus{width:54px;height:54px;border-radius:50%;background:var(--grad);color:#fff;display:grid;place-items:center;margin-top:-26px;border:4px solid #fff;box-shadow:0 0 0 1px #CFE0FF,0 8px 16px rgba(0,87,240,.35)}
.tb-badge{position:absolute;top:6px;left:calc(50% + 6px);min-width:16px;height:16px;border-radius:8px;background:var(--danger);color:#fff;font-size:10px;display:grid;place-items:center;padding:0 4px}
.home-ind{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:#1E2530;z-index:6}
.m-foot{padding:10px 16px 30px;background:#fff;display:flex;gap:10px;flex-shrink:0;box-shadow:0 -4px 16px rgba(0,87,240,.06);border-radius:16px 16px 0 0}
.m-foot .btn{flex:1;height:44px;font-size:16px;border-radius:22px}
.m-foot .btn.w-auto{flex:0 0 auto;padding:0 18px}

/* ===== 移动端组件 ===== */
.m-card{background:#fff;border-radius:8px;padding:14px;margin-bottom:12px}
.m-card-title{font-size:18px;font-weight:900;color:#333;display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;position:relative;padding-bottom:9px}
.m-card-title::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.m-card-title a{font-size:12px;font-weight:400;color:var(--primary);background:#E5EFFF;border:1px solid #fff;border-radius:24px;padding:2px 10px}
.m-section{font-size:18px;font-weight:700;color:#333;margin:18px 2px 10px;display:flex;justify-content:space-between;align-items:center;position:relative;padding-bottom:9px}
.m-section::after{content:'';position:absolute;left:0;bottom:0;width:32px;height:6px;background:var(--brace) no-repeat}
.m-section a{font-size:12px;font-weight:400;color:var(--primary);background:#E5EFFF;border:1px solid #fff;border-radius:24px;padding:2px 10px}
.m-hero{border-radius:12px;padding:16px;color:#fff;background:linear-gradient(150deg,#1F6FEA 0%,#3D8BFF 60%,#79B2FF 100%);box-shadow:0 8px 18px rgba(0,87,240,.2);position:relative;overflow:hidden;margin-bottom:12px}
.m-hero::after{content:'';position:absolute;right:-30px;top:-30px;width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,.08)}
.m-hero h2{font-size:18px}
.m-hero p{font-size:12px;opacity:.85;margin-top:4px}
.m-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:14px;position:relative;z-index:1}
.m-stats div{text-align:center}
.m-stats b{display:block;font-size:20px;font-variant-numeric:tabular-nums}
.m-stats span{font-size:11px;opacity:.85}
.m-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.m-grid a{display:flex;flex-direction:column;align-items:center;gap:6px;color:var(--text);font-size:12px;padding:6px 0}
.m-grid .mg-ic{width:44px;height:44px;border-radius:50%;box-shadow:0 4px 10px rgba(0,87,240,.15);display:grid;place-items:center;color:#fff}
.svc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.svc{position:relative;display:block;height:88px;padding:14px 14px 0;border-radius:8px;overflow:hidden;color:var(--text);--c:#3D7BFF;background:linear-gradient(135deg,#E3ECFF 0%,#D3E2FF 100%)}
.svc.green{--c:#1FC28A;background:linear-gradient(135deg,#E2F8EF 0%,#C9F1E0 100%)}
.svc.purple{--c:#7B61FF;background:linear-gradient(135deg,#EEE9FF 0%,#DFD6FF 100%)}
.svc.orange{--c:#FF8A3D;background:linear-gradient(135deg,#FFEDE0 0%,#FFDCC7 100%)}
.svc.pink{--c:#FF5C7C;background:linear-gradient(135deg,#FFE8EC 0%,#FFD3DC 100%)}
.svc b{display:flex;align-items:center;gap:6px;font-size:16px;font-weight:800}
.svc b i{width:18px;height:18px;border-radius:50%;background:var(--c);opacity:.75;color:#fff;display:grid;place-items:center}
.svc small{display:block;font-size:12px;color:rgba(30,50,63,.6);margin-top:4px;padding-right:46px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.svc::after{content:'';position:absolute;right:-18px;bottom:-26px;width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.45)}
.svc-ic{position:absolute;right:12px;bottom:10px;z-index:1;width:40px;height:40px;border-radius:10px;display:grid;place-items:center;color:#fff;background:var(--c);box-shadow:0 6px 12px rgba(0,0,0,.12);transform:rotate(-6deg)}
.m-item{display:block;background:#fff;border-radius:8px;padding:10px;margin-bottom:15px;color:var(--text);position:relative}
.m-item.overdue{box-shadow:inset 3px 0 0 var(--danger),var(--shadow-sm)}
.m-item-top{display:flex;align-items:flex-start;gap:8px;justify-content:space-between;padding:0 4px}
.m-item-title{font-weight:700;font-size:16px;color:var(--text);line-height:1.45;flex:1}
.m-item-meta{display:flex;gap:6px 12px;flex-wrap:wrap;font-size:12px;color:rgba(30,50,63,.7);margin-top:8px;padding:12px 10px;border-radius:8px;background:linear-gradient(0deg,#F9FBFF,#E5EFFF)}
.m-item-foot{display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding:10px 4px 0;border-top:1px solid #E3F1F9;font-size:12px;color:rgba(30,50,63,.7)}
.m-seg{display:flex;gap:8px;overflow-x:auto;padding:2px 0 10px;margin:0 -16px;padding-left:16px;padding-right:16px}
.m-seg::-webkit-scrollbar{display:none}
.m-seg button{flex-shrink:0;height:30px;padding:0 14px;border-radius:15px;border:0;background:#fff;color:rgba(30,50,63,.7);font-size:13px}
.m-seg button.on{background:var(--grad);color:#fff;font-weight:500;box-shadow:0 4px 10px rgba(0,87,240,.2)}
.m-tabs{display:flex;background:var(--bg);margin:-12px -16px 12px;position:sticky;top:-12px;z-index:2}
.m-tabs button{flex:1;height:52px;border:none;background:none;color:rgba(30,50,63,.7);font-size:16px;position:relative}
.m-tabs button+button::before{content:'';position:absolute;left:0;top:50%;height:22px;margin-top:-11px;width:1px;background:rgba(191,208,242,.5)}
.m-tabs button.on{color:var(--text);font-weight:800}
.m-tabs button.on::after{content:'';position:absolute;left:50%;bottom:4px;transform:translateX(-50%);width:32px;height:6px;background:var(--brace) no-repeat}
.tab-panel{display:none}.tab-panel.on{display:block}
.m-form{background:#fff;border-radius:8px;padding:4px 14px;margin-bottom:12px}
.m-form .field{padding:12px 0;border-bottom:1px solid var(--line)}
.m-form .field:last-child{border-bottom:none}
.m-form .input,.m-form .select{height:44px;width:100%;font-size:15px;background-color:#F6F8FC;border-color:#F6F8FC;border-radius:8px}
.m-form .textarea{font-size:15px;background:#F6F8FC;border-color:#F6F8FC;border-radius:8px}
.m-form .input:focus,.m-form .select:focus,.m-form .textarea:focus{background-color:#fff}
.m-form-title{font-size:16px;color:#303133;margin:16px 2px 10px;font-weight:900}
.m-form .radio-card{height:38px;padding:0 12px;flex:1;justify-content:center;border-radius:19px}
.upload{border:1.5px dashed var(--border);border-radius:10px;padding:16px;text-align:center;color:var(--text-3);position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:13px;background:#FAFCFE}
.upload input{position:absolute;inset:0;opacity:0}
.files{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.files:not(:empty){margin-top:10px}
.file-item{border-radius:8px;overflow:hidden;position:relative;border:1px solid var(--line);background:#fff}
.file-item img{width:100%;height:80px;object-fit:cover;display:block}
.fi-doc{height:80px;display:grid;place-items:center;background:var(--primary-light);color:var(--primary);font-weight:700}
.fi-meta{padding:4px 6px;font-size:10px;color:var(--text-3);display:flex;flex-direction:column}
.fi-name{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text-2)}
.fi-del{position:absolute;top:4px;right:4px;width:22px;height:22px;border-radius:50%;border:none;background:rgba(0,0,0,.55);color:#fff;font-size:14px;line-height:1;display:grid;place-items:center}
.file-item input{width:100%;border:none;border-top:1px solid var(--line);padding:5px 6px;font-size:11px;outline:none}
.m-editor{min-height:160px;border:1px solid var(--border);border-radius:8px;padding:10px 12px;outline:none;font-size:15px;line-height:1.8}
.m-editor:empty::before{content:attr(data-placeholder);color:var(--placeholder)}
.type-switch{margin:0 0 12px;padding:8px;border-radius:8px;background:#fff}
.type-switch .ts-lbl{display:none}
.type-switch .radio-group{flex-wrap:nowrap;gap:6px}
.type-switch .radio-card{flex:1;justify-content:center;height:34px;padding:0 4px;gap:3px;border-radius:4px;font-size:13px;white-space:nowrap}
.type-switch .radio-card:has(input:checked){font-weight:700}
.m-ed-box{position:relative;border:1px solid var(--border);border-radius:8px;background:#fff}
.m-ed-box .m-editor{border:0;border-radius:0}
.m-ed-bar{display:flex;align-items:center;gap:2px;padding:4px 6px;border-bottom:1px solid var(--line);background:#FAFBFC;overflow-x:auto;white-space:nowrap;border-radius:8px 8px 0 0;scrollbar-width:none}
.m-ed-bar::-webkit-scrollbar{display:none}
.m-ed-bar button{flex:none;width:32px;height:32px;border:0;background:none;border-radius:6px;color:var(--text-2);display:grid;place-items:center}
.m-ed-bar button.on{background:#E3F0FA;color:var(--primary)}
.m-ed-bar .sep{flex:none;width:1px;height:16px;background:var(--line);margin:0 4px}
.m-ed-box .ed-pop{position:absolute;left:6px;right:6px;top:44px;z-index:20;padding:12px;background:#fff;border:1px solid #E4E7ED;border-radius:8px;box-shadow:0 6px 16px rgba(0,0,0,.12);display:flex;flex-direction:column;gap:10px}
.m-ed-box .ed-pop[hidden]{display:none}
.m-ed-box .ed-pop-title{font-size:14px;font-weight:700}
.m-ed-box .ed-pop[data-mode=link] .ed-only-image,.m-ed-box .ed-pop[data-mode=image] .ed-only-link{display:none}
.m-ed-box .ed-img-src{display:flex;gap:16px;font-size:13px}
.m-ed-box .ed-local{display:inline-flex;align-items:center;gap:4px;color:var(--primary)}
.m-ed-box .ed-link-btn{border:0;background:none;color:var(--primary);font-size:13px;padding:0}
.m-ed-box .ed-pop-foot{display:flex;justify-content:flex-end;gap:8px}
.m-ed-box .ed-pop-foot .btn{height:30px;padding:0 14px}
.m-editor h3{font-size:16px;font-weight:700;margin:8px 0 4px}
.m-editor img{display:block;max-width:100%;margin:8px auto;border-radius:6px}
.m-ed-wc{padding:4px 12px 8px;text-align:right;font-size:12px;color:var(--text-3)}
.m-kv{display:flex;flex-direction:column}
.m-kv div{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:14px}
.m-kv div:last-child{border-bottom:none}
.m-kv dt{color:var(--text-3);flex-shrink:0}
.m-kv dd{text-align:right;color:var(--text)}
.m-article h2{font-size:19px;line-height:1.5;margin-bottom:8px}
.m-article p{font-size:15px;line-height:1.9;text-indent:2em;margin-bottom:10px;color:#434A55}
.m-article img{width:100%;border-radius:8px;margin:6px 0 10px;height:180px;object-fit:cover}
.m-sub-t{font-size:13px;font-weight:600;color:var(--text);margin:12px 0 6px}
.m-att{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)}
.m-att:last-child{border-bottom:none}
.m-att .att-ic{width:34px;height:34px;border-radius:8px;display:grid;place-items:center;color:#fff;font-size:10px;font-weight:700;flex:none}
.m-att .att-main{flex:1;min-width:0;display:flex;flex-direction:column;font-size:13px}
.m-att .att-main b{font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.m-att .att-main span{font-size:12px;color:var(--text-3)}
.m-cover{width:100%;height:170px;object-fit:cover;border-radius:8px;margin:8px 0}
.m-photo{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)}
.m-photo img{width:96px;height:72px;object-fit:cover;border-radius:6px;flex:none}
.m-photo div{display:flex;flex-direction:column;gap:2px;font-size:12px;color:var(--text-3);min-width:0}
.m-photo b{font-size:13px;color:var(--text);font-weight:500}
.m-photo em{font-style:normal;color:var(--text-2)}
.m-list-link{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #E3F1F9;color:#303133;font-size:14px}
.m-card:has(> .m-list-link){border-radius:20px;background:linear-gradient(180deg,#E2F3FF -9%,#fff 11%);border:1px solid #fff;padding:4px 16px 8px}
button.m-list-link{width:100%;background:none;border:0;border-bottom:1px solid #E3F1F9;font:inherit;font-size:14px;text-align:left;cursor:pointer}
.m-list-link:last-child{border-bottom:none}
.m-list-link .ic:last-child{margin-left:auto;color:var(--placeholder)}
.m-list-link .ll-ic{width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:var(--primary-light);color:var(--primary)}
.msg-item{display:flex;gap:12px;padding:14px;background:#fff;border-radius:8px;margin-bottom:10px;position:relative;cursor:pointer}
.msg-item.unread::after{content:'';position:absolute;right:14px;top:16px;width:8px;height:8px;border-radius:50%;background:var(--danger)}
.msg-ic{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;flex-shrink:0}
.msg-main{flex:1;min-width:0}
.msg-title{font-weight:600;font-size:14px;padding-right:14px}
.msg-item:not(.unread) .msg-title{font-weight:500;color:var(--text-2)}
.msg-desc{font-size:12px;color:var(--text-3);margin-top:3px;line-height:1.6}
.msg-time{font-size:11px;color:var(--text-3);margin-top:4px}
.rank-row{display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--line)}
.rank-row:last-child{border-bottom:none}
.rank-row .rr-name{flex:1;font-size:14px}
.rank-row .rr-bar{width:90px;height:6px;background:var(--gray-bg);border-radius:3px;overflow:hidden}
.rank-row .rr-bar i{display:block;height:100%;background:var(--primary);border-radius:3px}
.rank-row b{width:30px;text-align:right;font-variant-numeric:tabular-nums}
.m-hero-btn{margin-top:10px;display:inline-flex;align-items:center;gap:4px;height:30px;padding:0 14px;border-radius:15px;border:1px solid rgba(255,255,255,.7);background:rgba(255,255,255,.18);color:#fff;font-size:13px;position:relative;z-index:1}
.rk-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px}
.rk-sum div{padding:8px 4px;border-radius:8px;background:var(--primary-light);text-align:center}
.rk-sum b{display:block;font-size:17px;color:var(--primary)}
.rk-sum span{font-size:11px;color:var(--text-3)}
.rk-item{padding:10px 0;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:3px}
.rk-item:last-child{border-bottom:0}
.rk-item b{font-size:14px;flex:1;min-width:0}
.rank-row.me{background:var(--primary-light);margin:0 -14px;padding:11px 14px;border-radius:8px}
.rank-no{width:22px;height:22px;border-radius:6px;display:inline-grid;place-items:center;font-weight:700;font-size:12px;background:var(--gray-bg);color:var(--text-2)}
.rank-no.r1{background:linear-gradient(135deg,#FFD66B,#F29100);color:#fff}
.rank-no.r2{background:linear-gradient(135deg,#D7DEE8,#9AA6B6);color:#fff}
.rank-no.r3{background:linear-gradient(135deg,#F3C39B,#C9804A);color:#fff}
.m-timer{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:8px;background:var(--warn-bg);color:#9A5C00;margin-bottom:12px;font-size:13px}
.m-timer.danger{background:var(--danger-bg);color:#A8161B}
.m-timer b{font-size:17px}
.m-result{text-align:center;padding:40px 10px 20px}
.m-result .big-ic{width:76px;height:76px;border-radius:50%;background:var(--success-bg);color:var(--success);display:grid;place-items:center;margin:0 auto 16px}
.m-result h2{font-size:20px}
.m-result p{color:var(--text-3);font-size:13px;margin-top:6px}
.m-steps{display:flex;margin:18px 0 6px}
.m-steps div{flex:1;text-align:center;font-size:11px;color:var(--text-3);position:relative}
.m-steps div::before{content:'';position:absolute;top:9px;left:-50%;right:50%;height:2px;background:var(--line)}
.m-steps div:first-child::before{display:none}
.m-steps div.done::before,.m-steps div.cur::before{background:var(--success)}
.m-steps i{width:20px;height:20px;border-radius:50%;display:block;margin:0 auto 4px;background:#fff;border:2px solid var(--line);position:relative;z-index:1}
.m-steps .done i{background:var(--success);border-color:var(--success)}
.m-steps .cur i{border-color:var(--primary);box-shadow:0 0 0 3px var(--primary-light)}
.m-steps .cur{color:var(--primary);font-weight:600}
.m-profile{display:flex;align-items:center;gap:14px;padding:18px;border-radius:12px;background:linear-gradient(150deg,#1F6FEA 0%,#3D8BFF 60%,#79B2FF 100%);color:#fff;margin-bottom:12px;box-shadow:0 8px 18px rgba(0,87,240,.2)}
.m-profile img{width:56px;height:56px;border-radius:50%;border:2px solid rgba(255,255,255,.6);object-fit:cover}
.m-profile b{font-size:18px;display:block}
.m-profile span{font-size:12px;opacity:.85}
.m-mini-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.m-mini-stats div{background:linear-gradient(180deg,#E8F1FF 0%,#F8FBFF 100%);border-radius:8px;padding:12px;text-align:center}
.m-mini-stats b{display:block;font-size:20px;font-variant-numeric:tabular-nums}
.m-mini-stats span{font-size:11px;color:var(--text-3)}
.btn-block{width:100%;height:44px;font-size:15px;border-radius:22px}
.m-empty{text-align:center;color:#8CA2B6;padding:40px 0;font-size:12px}
.sens-card{padding:12px;border-radius:10px;background:#FAFBFC;border:1px solid var(--line);font-size:13px}

/* 手机内的弹窗改为底部面板 */
.toast-wrap{position:absolute;top:56px}
.toast{font-size:13px;max-width:320px}
.modal{position:absolute;padding:0;align-items:flex-end;z-index:50}
.modal .modal-box{width:100%;border-radius:16px 16px 0 0;max-height:85%;animation:sheetUp .28s ease-out}
.modal.center{align-items:center;padding:24px}
.modal.center .modal-box{border-radius:14px}
.modal-foot{padding-bottom:30px}
.modal-foot .btn{flex:1;height:44px;border-radius:22px}
@keyframes sheetUp{from{transform:translateY(100%)}to{transform:none}}
.result-bar{margin:0 0 12px;font-size:13px;padding:10px 12px}

@media (max-width:480px){
  body.app-stage{padding:0;display:block;background:var(--bg)}
  .phone{width:100%;height:100vh;height:100dvh;border-radius:0;box-shadow:none}
  .phone::before{display:none}
  .status-bar{display:none}
  .home-ind{display:none}
}
"""
