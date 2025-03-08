_R='content'
_Q='swatch'
_P='transparent'
_O='session_name'
_N='session'
_M='SESSIONS'
_L='pycon'
_K='playground'
_J='gamut'
_I='exceptions'
_H='color'
_G='highlight'
_F='eval'
_E='<string>'
_D='class'
_C=None
_B=True
_A=False
import xml.etree.ElementTree as Etree
from collections.abc import Sequence,Mapping
from collections import namedtuple
import ast
from io import StringIO
import sys,re
from functools import partial
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import find_formatter_class
from coloraide import Color
from coloraide.interpolate import Interpolator,normalize_domain
try:from coloraide_extras.everything import ColorAll
except ImportError:from coloraide.everything import ColorAll
PY310=(3,10)<=sys.version_info
PY311=(3,11)<=sys.version_info
WEBSPACE='srgb'
AST_BLOCKS=ast.If,ast.For,ast.While,ast.Try,ast.With,ast.FunctionDef,ast.ClassDef,ast.AsyncFor,ast.AsyncWith,ast.AsyncFunctionDef
if PY310:AST_BLOCKS=AST_BLOCKS+(ast.Match,)
if PY311:AST_BLOCKS=AST_BLOCKS+(ast.TryStar,)
RE_INIT=re.compile('^\\s*#\\s*pragma:\\s*init\\n(.*?)#\\s*pragma:\\s*init\\n',re.DOTALL|re.I)
RE_COLOR_START=re.compile('(?i)(?:\\b(?<![-#&$])(?:color|hsla?|lch|lab|hwb|rgba?)\\(|\\b(?<![-#&$])[\\w]{3,}(?![(-])\\b|(?<![&])#)')
LIVE_INIT='\nfrom coloraide import *\nimport coloraide\ntry:\n    import coloraide_extras\n    from coloraide_extras.everything import ColorAll as Color\nexcept ImportError:\n    from coloraide.everything import ColorAll as Color\n'
template='<div class="playground" id="__playground_{el_id}">\n<div class="playground-results" id="__playground-results_{el_id}">\n{results}\n</div>\n<div class="playground-code hidden" id="__playground-code_{el_id}" session="{session}" data-search-exclude>\n<form autocomplete="off">\n<pre class="playground-inputs" id="__playground-inputs_{el_id}" spellcheck="false">{raw_source}</pre>\n</form>\n</div>\n<div class="playground-footer" data-search-exclude>\n<hr>\n<button id="__playground-edit_{el_id}" class="playground-edit" title="Edit the current snippet">Edit</button>\n<button id="__playground-share_{el_id}" class="playground-share" title="Copy URL to current snippet">Share</button>\n<button id="__playground-run_{el_id}" class="playground-run hidden" title="Run code (Ctrl + Enter)">Run</button>\n<button id="__playground-cancel_{el_id}" class="playground-cancel hidden" title="Cancel edit (Escape)">Cancel</button>\n<div class=\'spacer\'></div>\n<div class=\'footer-status\'>\n<span class=\'session\'>{session}</span>\n<span class=\'gamut\'>Gamut: {gamut}</span>\n</div>\n</div>\n</div>'
code_id=0
if _M not in globals()or not globals()[_M]:
    SESSIONS={}
    class Ramp(list):0
    class Steps(list):0
    class Row(list):0
    class Wheel(Steps):
        def __init__(self,iterable):
            if not hasattr(iterable,'__len__'):iterable=list(iterable)
            if len(iterable)not in(3,6,12,24,48):raise ValueError('Wheel only supports iterables of length 3, 6, 12, 24, or 48')
            super().__init__(iterable)
    class ColorTuple(namedtuple('ColorTuple',['string',_H])):0
    class AtomicString(str):0
    class Break(Exception):0
    class Continue(Exception):0
    HtmlRow=Row;HtmlSteps=Steps;HtmlGradient=Ramp
def reset():SESSIONS.clear()
def _escape(txt):txt=txt.replace('&','&amp;');txt=txt.replace('<','&lt;');txt=txt.replace('>','&gt;');return txt
class StreamOut:
    def __init__(self):self.old=sys.stdout;self.stdout=StringIO();sys.stdout=self.stdout
    def read(self):
        value=''
        if self.stdout is not _C:self.stdout.flush();value=self.stdout.getvalue();self.stdout=StringIO();sys.stdout=self.stdout
        return value
    def __enter__(self):return self
    def __exit__(self,type,value,traceback):sys.stdout=self.old;self.old=_C;self.stdout=_C
def get_colors(result):
    domain=[]
    if isinstance(result,AtomicString):yield find_colors(result)
    if isinstance(result,Row):yield Row([ColorTuple(c.to_string(fit=_A),c.clone())if isinstance(c,Color)else ColorTuple(c,ColorAll(c))for c in result])
    elif isinstance(result,(Wheel,Steps,Ramp)):t=type(result);yield t([c.clone()if isinstance(c,Color)else ColorAll(c)for c in result])
    elif isinstance(result,Color):yield[ColorTuple(result.to_string(fit=_A),result.clone())]
    elif isinstance(result,Interpolator):
        if result._domain:domain=result._domain;result.domain(normalize_domain(result._domain))
        grad=Ramp(result.steps(steps=5,max_delta_e=2.3))
        if domain:result._domain=domain;domain=[]
        yield grad
    elif isinstance(result,str):
        try:yield[ColorTuple(result,ColorAll(result))]
        except Exception:pass
    elif isinstance(result,(list,tuple)):
        for r in result:
            for x in get_colors(r):
                if x:yield x
def find_colors(text):
    colors=[]
    for m in RE_COLOR_START.finditer(text):
        start=m.start();mcolor=ColorAll.match(text,start=start)
        if mcolor is not _C:colors.append(ColorTuple(text[mcolor.start:mcolor.end],mcolor.color))
    return colors
def evaluate_with(node,g,loop,index=0):
    l=len(node.items)-1;withitem=node.items[index]
    if withitem.context_expr:
        with eval(compile(ast.Expression(withitem.context_expr),_E,_F),g)as w:
            g[withitem.optional_vars.id]=w
            if index<l:evaluate_with(node,g,loop,index+1)
            else:
                for n in node.body:yield from evaluate(n,g,loop)
    else:
        with eval(compile(ast.Expression(withitem.context_expr),_E,_F),g):
            if index<l:evaluate_with(node,g,loop,index+1)
            else:
                for n in node.body:yield from evaluate(n,g,loop)
def compare_match(s,g,node):
    if isinstance(node,ast.MatchOr):
        for pattern in node.patterns:
            if compare_match(s,g,pattern):return _B
    elif isinstance(node,ast.MatchValue):p=eval(compile(ast.Expression(node.value),_E,_F),g);return s==p
    elif isinstance(node,ast.MatchSingleton):return s is node.value
    elif isinstance(node,ast.MatchSequence):
        if isinstance(s,Sequence):
            star=isinstance(node.patterns[-1],ast.MatchStar);l1,l2=len(s),len(node.patterns)
            if star and l1>=l2-1 or l1==l2:
                for(e,p)in enumerate(node.patterns[:-1]if star else node.patterns):
                    if not compare_match(s[e],g,p):return _A
                if star and node.patterns[-1].name:g[node.patterns[-1].name]=s[l2-1:]
                return _B
        return _A
    elif isinstance(node,ast.MatchMapping):
        if isinstance(s,Mapping):
            star=node.rest;l1,l2=len(s),len(node.patterns)
            if star and l1>=l2 or l1==l2:
                keys=set()
                for(kp,vp)in zip(node.keys,node.patterns):
                    key=eval(compile(ast.Expression(kp),_E,_F),g);keys.add(key)
                    if key not in s:return _A
                    if not compare_match(s[key],g,vp):return _A
                if star:g[star]={k:v for(k,v)in s.items()if k not in keys}
                return _B
        return _A
    elif isinstance(node,ast.MatchClass):
        name=g.get(node.cls.id,_C)
        if name is _C:raise NameError(f"name '{node.cls.id}' is not defined")
        if not isinstance(s,name):return _A
        ma=getattr(s,'__match_args__',());l1=len(ma);l2=len(node.patterns)
        if l1<l2:raise TypeError(f"{name}() accepts {l1} positional sub-patterns ({l2} given)")
        for(e,p)in enumerate(node.patterns):
            if not hasattr(s,ma[e]):return _A
            if not compare_match(getattr(s,ma[e]),g,p):return _A
        for(a,p)in zip(node.kwd_attrs,node.kwd_patterns):
            if not hasattr(s,a):return _A
            if not compare_match(getattr(s,a),g,p):return _A
        return _B
    elif isinstance(node,ast.MatchAs):
        if node.name is not _C:g[node.name]=s
        if node.pattern:return compare_match(s,g,node.pattern)
        return _B
    raise RuntimeError(f"Unknown Match pattern {node!s}")
def evaluate_except(node,e,g,loop=_A):
    for n in node.handlers:
        if n.name:g[n.name]=e
        if n.type is _C:
            for ne in n.body:yield from evaluate(ne,g,loop)
            break
        elif isinstance(e,eval(compile(ast.Expression(n.type),_E,_F),g)):
            for ne in n.body:yield from evaluate(ne,g,loop)
            break
    else:raise
def evaluate(node,g,loop=_A):
    if loop and isinstance(node,ast.Break):raise Break
    if loop and isinstance(node,ast.Continue):raise Continue
    if isinstance(node,ast.Expr):_eval=ast.Expression(node.value);yield eval(compile(_eval,_E,_F),g)
    elif isinstance(node,ast.If):
        if eval(compile(ast.Expression(node.test),_E,_F),g):
            for n in node.body:yield from evaluate(n,g,loop)
        elif node.orelse:
            for n in node.orelse:yield from evaluate(n,g,loop)
    elif isinstance(node,ast.While):
        while eval(compile(ast.Expression(node.test),_E,_F),g):
            try:
                for n in node.body:yield from evaluate(n,g,_B)
            except Break:break
            except Continue:continue
        else:
            for n in node.orelse:yield from evaluate(n,g,loop)
    elif isinstance(node,ast.For):
        for x in eval(compile(ast.Expression(node.iter),_E,_F),g):
            if isinstance(node.target,ast.Tuple):
                for(e,t)in enumerate(node.target.dims):g[t.id]=x[e]
            else:g[node.target.id]=x
            try:
                for n in node.body:yield from evaluate(n,g,_B)
            except Break:break
            except Continue:continue
        else:
            for n in node.orelse:yield from evaluate(n,g,loop)
    elif isinstance(node,ast.Try):
        try:
            for n in node.body:yield from evaluate(n,g,loop)
        except Exception as e:yield from evaluate_except(node,e,g,loop)
        else:
            for n in node.orelse:yield from evaluate(n,g,loop)
        finally:
            for n in node.finalbody:yield from evaluate(n,g,loop)
    elif PY311 and isinstance(node,ast.TryStar):
        try:
            for n in node.body:yield from evaluate(n,g,loop)
        except ExceptionGroup as e:
            for n in node.handlers:
                if n.name:g[n.name]=e
                m,e=e.split(eval(compile(ast.Expression(n.type),_E,_F),g))
                if m is not _C:
                    for ne in n.body:yield from evaluate(ne,g,loop)
                if e is _C:break
            if e is not _C:raise e
        except Exception as e:yield from evaluate_except(node,e,g,loop)
        else:
            for n in node.orelse:yield from evaluate(n,g,loop)
        finally:
            for n in node.finalbody:yield from evaluate(n,g,loop)
    elif PY310 and isinstance(node,ast.Match):
        s=eval(compile(ast.Expression(node.subject),_E,_F),g)
        for c in node.cases:
            if compare_match(s,g,c.pattern):
                if not c.guard or eval(compile(ast.Expression(c.guard),_E,_F),g):
                    for n in c.body:yield from evaluate(n,g,loop)
                    break
    elif isinstance(node,ast.With):yield from evaluate_with(node,g,loop)
    else:_exec=ast.Module([node],[]);exec(compile(_exec,_E,'exec'),g);yield _C
def execute(cmd,no_except=_B,inline=_A,init='',g=_C):
    A='\n';console='';colors=[]
    if g is _C:g={}
    if not g:
        g['Ramp']=Ramp;g['Steps']=Steps;g['Row']=Row;g['Wheel']=Wheel;g['HtmlRow']=HtmlRow;g['HtmlSteps']=HtmlSteps;g['HtmlGradient']=HtmlGradient
        if init:execute(init.strip(),g=g)
    m=RE_INIT.match(cmd)
    if m:block_init=m.group(1);src=cmd[m.end():];execute(block_init,g=g)
    else:src=cmd
    lines=src.split(A)
    try:tree=ast.parse(src)
    except Exception as e:
        if no_except:
            if not inline:from pymdownx.superfences import SuperFencesException;raise SuperFencesException from e
            else:from pymdownx.inlinehilite import InlineHiliteException;raise InlineHiliteException from e
        import traceback;return f"{traceback.format_exc()}",colors
    last=-1
    for node in tree.body:
        result=[];start=node.lineno;end=node.end_lineno;stmt=[];command=''
        for(i,line)in enumerate(lines[start-1:end],0):
            if line!=last:
                if i==0:stmt.append('>>> '+line)
                else:stmt.append('... '+line)
            last=line
        if stmt:command+=A.join(stmt)
        if isinstance(node,AST_BLOCKS):command+='\n... '
        try:
            with StreamOut()as s:
                for x in evaluate(node,g):
                    text=s.read()
                    if text:result.append(AtomicString(text))
                    result.append(x)
                console+=command
        except Exception as e:
            if no_except:
                if not inline:from pymdownx.superfences import SuperFencesException;raise SuperFencesException from e
                else:from pymdownx.inlinehilite import InlineHiliteException;raise InlineHiliteException from e
            import traceback;console+=f"{command}\n{traceback.format_exc()}";break
        result_text=A
        for r in result:
            if r is _C:continue
            for clist in get_colors(r):
                if clist:colors.append(clist)
            result_text+='{}{}'.format(repr(r)if isinstance(r,str)and not isinstance(r,AtomicString)else str(r),A if not isinstance(r,AtomicString)else'')
        if stmt:console+=result_text
    return console,colors
def colorize(src,lang,**options):HtmlFormatter=find_formatter_class('html');lexer=get_lexer_by_name(lang,**options);formatter=HtmlFormatter(cssclass=_G,wrapcode=_B);return highlight(src,lexer,formatter).strip()
def color_command_validator(language,inputs,options,attrs,md):
    valid_inputs={_I,'play'}
    for(k,v)in inputs.items():
        if k==_N:
            if k not in SESSIONS:SESSIONS[k]={}
            options[k]=SESSIONS[k];options[_O]=v;continue
        if k in valid_inputs:options[k]=_B;continue
        attrs[k]=v
    return _B
def _color_command_console(colors,gamut=WEBSPACE):
    C='</div>';B=' ';A='<div class="swatch-bar">{}</div>';el='';bar=_A;values=[]
    for item in colors:
        is_grad=isinstance(item,HtmlGradient);is_steps=isinstance(item,Steps);is_wheel=isinstance(item,Wheel);l=len(item)if is_wheel else 0
        if is_wheel:
            if l>=48:freq=16;offset=24
            elif l>=24:freq=8;offset=12
            elif l>=12:freq=4;offset=6
            elif l>=6:freq=2;offset=3
            else:freq=1;offset=1
            extra_rings_start='';extra_rings_end='';primary=item[::freq][2::-1];color_rings=[primary]
            if l>=6:extra_rings_start='<div class="secondary"><div class="secondary-inner">';extra_rings_end='</div></div>';secondary=(item[offset::freq]+[item[offset//3]])[2::-1];color_rings.append(secondary)
            if l>=12:extra_rings_start='<div class="tertiary">'+extra_rings_start;extra_rings_end+=C;tertiary=item[::offset//6][11::-1];color_rings.append(tertiary)
            if l>=24:extra_rings_start='<div class="tertiary2">'+extra_rings_start;extra_rings_end+=C;color_rings.append(item[::offset//12][23::-1])
            if l>=48:extra_rings_start='<div class="tertiary3">'+extra_rings_start;extra_rings_end+=C;color_rings.append(item[47::-1])
            color_stops=''
            for(i,rcolors)in enumerate(color_rings,1):
                total=len(rcolors);percent=100/total;current=percent;last=-1;stops=[]
                for(e,color)in enumerate(rcolors):
                    color.fit(gamut);color_str=color.convert(gamut).to_string()
                    if current:
                        stops.append(f"{color_str} {last!s}%");stops.append(f"{color_str} {current!s}%");last=current
                        if e<total-1:current+=percent
                        else:current=100
                    else:stops.append(color_str)
                color_stops+='--color-wheel-stops{}: {};'.format(i,','.join(stops))
            color_wheel='<div class="color-wheel" style="{}"><div class="wheel">\n{}<div class="primary"><div class="primary-inner"></div></div></div></div>{}'.format(color_stops,extra_rings_start,extra_rings_end);el+=color_wheel
        elif is_grad or is_steps:
            current=total=percent=last=0
            if is_steps:total=len(item);percent=100/total;current=percent
            if bar:el+=A.format(B.join(values));values=[]
            sub_el1='<div class="swatch-bar"><span class="swatch swatch-gradient">{}</span></div>';style='--swatch-stops: ';stops=[]
            for(e,color)in enumerate(item):
                color.fit(gamut);color_str=color.convert(gamut).to_string()
                if current:
                    if is_steps:stops.append(f"{color_str} {last!s}%");stops.append(f"{color_str} {current!s}%")
                    else:stops.append(color_str)
                    last=current
                    if e<total-1:current+=percent
                    else:current=100
                else:stops.append(color_str)
            if not stops:stops.extend([_P]*2)
            if len(stops)==1:stops.append(stops[0])
            style+=','.join(stops);sub_el2=f'<span class="swatch-color" style="{style}"></span>';el+=sub_el1.format(sub_el2);bar=_A
        else:
            is_row=_A
            if isinstance(item,Row):
                is_row=_B
                if bar and values:el+=A.format(B.join(values));values=[]
                bar=_A
            bar=_B
            for color in item:
                base_classes=_Q
                if not color.color.in_gamut(gamut):base_classes+=' out-of-gamut'
                color.color.fit(gamut);srgb=color.color.convert(gamut);value1=srgb.to_string(alpha=_A);value2=srgb.to_string();style=f"--swatch-stops: {value1} 50%, {value2} 50%";title=color.string;classes=base_classes;c=f'<span class="swatch-color" style="{style}"></span>';c='<span class="{classes}" title="{title}&#013;Copy to clipboard">{color}</span>'.format(classes=classes,color=c,title=title);values.append(c)
            if is_row and values:el+=A.format(B.join(values));values=[];bar=_A
    if bar:el+=A.format(B.join(values));values=[]
    return el
def _color_command_formatter(src='',language='',class_name=_C,options=_C,md='',init='',**kwargs):
    B='formatter';A='fenced_code_block';global code_id;from pymdownx.superfences import SuperFencesException;gamut=kwargs.get(_J,WEBSPACE);play=options.get('play',_A)if options is not _C else _A;session=options.get(_N)if options is not _C else _C;session_name=options.get(_O,'')if options is not _C else''
    if not play and language==_K:play=_B
    if not play:return md.preprocessors[A].extension.superfences[0][B](src=src,class_name=class_name,language='py',md=md,options=options,**kwargs)
    try:
        if len(md.preprocessors[A].extension.stash)==0:code_id=0
        exceptions=options.get(_I,_A)if options is not _C else _A;console,colors=execute(src.strip(),not exceptions,init=init,g=session);el=_color_command_console(colors,gamut=gamut);el+=md.preprocessors[A].extension.superfences[0][B](src=console,class_name=_G,language=_L,md=md,options=options,**kwargs);el=f'<div class="color-command">{el}</div>';el=template.format(el_id=code_id,raw_source=_escape(src),results=el,gamut=gamut,session=f"Session: {session_name}"if session_name else'');code_id+=1
    except SuperFencesException:raise
    except Exception:from pymdownx import superfences;import traceback;print(traceback.format_exc());return superfences.fence_code_format(src,'text',class_name,options,md,**kwargs)
    return el
def color_command_formatter(init='',gamut=WEBSPACE):return partial(_color_command_formatter,init=init,gamut=gamut)
def _color_formatter(src='',language='',class_name=_C,md='',exceptions=_B,init='',gamut=WEBSPACE):
    E='backtick';D='title';C='Only one color allowed';B=' 50%';A='span';from pymdownx.inlinehilite import InlineHiliteException
    try:
        result=src.strip()
        try:color=ColorAll(result.strip())
        except Exception as e:
            _,colors=execute(result,exceptions,inline=_B,init=init)
            if len(colors)!=1 or len(colors[0])!=1:
                if exceptions:raise InlineHiliteException(C)from e
                else:raise ValueError(C)from e
            color=colors[0][0].color;result=colors[0][0].string
        el=Etree.Element(A);stops=[]
        if not color.in_gamut(gamut):
            color.fit(gamut);attributes={_D:'swatch out-of-gamut',D:result};sub_el=Etree.SubElement(el,A,attributes);stops.append(color.convert(gamut).to_string(hex=_B,alpha=_A))
            if color[-1]<1.:stops[-1]+=B;stops.append(color.convert(gamut).to_string(hex=_B)+B)
        else:
            attributes={_D:_Q,D:result};sub_el=Etree.SubElement(el,A,attributes);stops.append(color.convert(gamut).to_string(hex=_B,alpha=_A))
            if color[-1]<1.:stops[-1]+=B;stops.append(color.convert(gamut).to_string(hex=_B)+B)
        if not stops:stops.extend([_P]*2)
        if len(stops)==1:stops.append(stops[0])
        Etree.SubElement(sub_el,A,{_D:'swatch-color','style':'--swatch-stops: {};'.format(','.join(stops))});el.append(md.inlinePatterns[E].handle_code('css-color',result))
    except InlineHiliteException:raise
    except Exception:import traceback;print(traceback.format_exc());el=md.inlinePatterns[E].handle_code('text',src)
    return el
def color_formatter(init='',gamut=WEBSPACE):return partial(_color_formatter,init=init,gamut=gamut)
def _live_color_command_formatter(src,init='',gamut=WEBSPACE,session=''):
    try:
        if session:
            if session not in SESSIONS:SESSIONS[session]={}
            g=SESSIONS.get(session,{})
        else:g={}
        console,colors=execute(src.strip(),_A,init=init,g=g);el=_color_command_console(colors,gamut=gamut)
        if not colors:el+='<div class="swatch-bar"></div>'
        el+=colorize(console,_L,**{'python3':_B,'stripnl':_A});el=f'<div class="color-command">{el}</div>'
    except Exception:import traceback;return'<div class="color-command"><div class="swatch-bar"></div>{}</div>'.format(colorize(traceback.format_exc(),_L))
    return el
def live_color_command_formatter(init='',gamut=WEBSPACE,session=''):return partial(_live_color_command_formatter,init=init,gamut=gamut,session=session)
def live_color_command_validator(language,inputs,options,attrs,md):value=color_command_validator(language,inputs,options,attrs,md);options[_I]=_B;return value
def render_console(*args,**kwargs):
    C='.swatch-bar, .color-wheel';B='id_num';A='code';from js import document;gamut=kwargs.get(_J,WEBSPACE)
    try:
        results=document.getElementById('__playground-results_{}'.format(globals()[B]));footer=document.querySelector('#__playground_{} .gamut'.format(globals()[B]));session=globals()['session_id'];result=live_color_command_formatter(LIVE_INIT,gamut)(globals()[_R],session=session);temp=document.createElement('div');temp.innerHTML=result;cmd=results.querySelector('.color-command')
        for el in cmd.querySelectorAll(C):el.remove()
        for el in temp.querySelectorAll(C):cmd.insertBefore(el,cmd.lastChild)
        footer.innerHTML=f"Gamut: {gamut}";pre=cmd.querySelector('pre');pre.replaceChild(temp.querySelector(A),pre.querySelector(A));temp.remove();scrollingElement=results.querySelector(A);scrollingElement.scrollTop=scrollingElement.scrollHeight
    except Exception as e:print(e)
def render_notebook(*args,**kwargs):
    d='quote';c='example';b='bug';a='danger';Z='failure';Y='warning';X='question';W='success';V='tip';U='info';T='abstract';S='note';R='settings';Q='new';P='types';O='diagram';N='pymdownx.fancylists';M='pymdownx.blocks.tab';L='pymdownx.blocks.details';K='pymdownx.blocks.admonition';J='pymdownx.arithmatex';I='pymdownx.keys';H='pymdownx.magiclink';G='pymdownx.inlinehilite';F='pymdownx.superfences';E='markdown.extensions.smarty';D='markdown.extensions.toc';C='validator';B='format';A='name';import markdown;from pymdownx import slugs,superfences;from js import document;gamut=kwargs.get(_J,WEBSPACE);text=globals().get(_R,'');extensions=[D,E,'pymdownx.betterem','markdown.extensions.attr_list','markdown.extensions.tables','markdown.extensions.abbr','markdown.extensions.footnotes',F,'pymdownx.highlight',G,H,'pymdownx.tilde','pymdownx.caret','pymdownx.smartsymbols','pymdownx.emoji','pymdownx.escapeall','pymdownx.tasklist','pymdownx.striphtml','pymdownx.snippets',I,'pymdownx.saneheaders',J,K,L,'pymdownx.blocks.html','pymdownx.blocks.definition',M,N,'pymdownx.blocks.caption'];extension_configs={D:{'slugify':slugs.slugify(case='lower'),'permalink':''},E:{'smart_quotes':_A},J:{'generic':_B,'block_tag':'pre'},F:{'preserve_tabs':_B,'custom_fences':[{A:O,_D:O,B:superfences.fence_code_format},{A:_K,_D:_K,B:color_command_formatter(LIVE_INIT,gamut),C:live_color_command_validator},{A:'python',_D:_G,B:color_command_formatter(LIVE_INIT,gamut),C:live_color_command_validator},{A:'py',_D:_G,B:color_command_formatter(LIVE_INIT,gamut),C:live_color_command_validator}]},G:{'custom_inline':[{A:_H,_D:_H,B:color_formatter(LIVE_INIT,gamut)}]},H:{'repo_url_shortener':_B,'repo_url_shorthand':_B,'social_url_shorthand':_B,'user':'facelessuser','repo':'coloraide'},I:{'separator':'＋'},M:{'alternate_style':_B},K:{P:[Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d]},N:{'inject_style':_B},L:{P:[{A:'details-new',_D:Q},{A:'details-settings',_D:R},{A:'details-note',_D:S},{A:'details-abstract',_D:T},{A:'details-info',_D:U},{A:'details-tip',_D:V},{A:'details-success',_D:W},{A:'details-question',_D:X},{A:'details-warning',_D:Y},{A:'details-failure',_D:Z},{A:'details-danger',_D:a},{A:'details-bug',_D:b},{A:'details-example',_D:c},{A:'details-quote',_D:d}]}}
    try:html=markdown.markdown(text,extensions=extensions,extension_configs=extension_configs)
    except Exception:html=''
    content=document.getElementById('__notebook-render');content.innerHTML=html