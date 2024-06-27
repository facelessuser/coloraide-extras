_P='<div class="color-command">{}</div>'
_O='swatch'
_N='transparent'
_M='pycon'
_L='playground'
_K='gamut'
_J='color'
_I='{} {}%'
_H='exceptions'
_G='highlight'
_F='eval'
_E='<string>'
_D=None
_C='class'
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
template='<div class="playground" id="__playground_{el_id}">\n<div class="playground-results" id="__playground-results_{el_id}">\n{results}\n</div>\n<div class="playground-code hidden" id="__playground-code_{el_id}" data-search-exclude>\n<form autocomplete="off">\n<textarea class="playground-inputs" id="__playground-inputs_{el_id}" spellcheck="false">{raw_source}</textarea>\n</form>\n</div>\n<div class="playground-footer" data-search-exclude>\n<hr>\n<button id="__playground-edit_{el_id}" class="playground-edit" title="Edit the current snippet">Edit</button>\n<button id="__playground-share_{el_id}" class="playground-share" title="Copy URL to current snippet">Share</button>\n<button id="__playground-run_{el_id}" class="playground-run hidden" title="Run code (Ctrl + Enter)">Run</button>\n<button id="__playground-cancel_{el_id}" class="playground-cancel hidden" title="Cancel edit (Escape)">Cancel</button>\n<span class=\'gamut\'>Gamut: {gamut}</span>\n</div>\n</div>'
code_id=0
class Ramp(list):0
class Steps(list):0
class Row(list):0
class ColorTuple(namedtuple('ColorTuple',['string',_J])):0
class AtomicString(str):0
class Break(Exception):0
class Continue(Exception):0
HtmlRow=Row
HtmlSteps=Steps
HtmlGradient=Ramp
def _escape(txt):txt=txt.replace('&','&amp;');txt=txt.replace('<','&lt;');txt=txt.replace('>','&gt;');return txt
class StreamOut:
    def __init__(self):self.old=sys.stdout;self.stdout=StringIO();sys.stdout=self.stdout
    def read(self):
        value=''
        if self.stdout is not _D:self.stdout.flush();value=self.stdout.getvalue();self.stdout=StringIO();sys.stdout=self.stdout
        return value
    def __enter__(self):return self
    def __exit__(self,type,value,traceback):sys.stdout=self.old;self.old=_D;self.stdout=_D
def get_colors(result):
    domain=[]
    if isinstance(result,AtomicString):yield find_colors(result)
    if isinstance(result,Row):yield Row([ColorTuple(c.to_string(fit=_A),c.clone())if isinstance(c,Color)else ColorTuple(c,ColorAll(c))for c in result])
    elif isinstance(result,(Steps,Ramp)):t=type(result);yield t([c.clone()if isinstance(c,Color)else ColorAll(c)for c in result])
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
        if mcolor is not _D:colors.append(ColorTuple(text[mcolor.start:mcolor.end],mcolor.color))
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
                for (e,p) in enumerate(node.patterns[:-1]if star else node.patterns):
                    if not compare_match(s[e],g,p):return _A
                if star and node.patterns[-1].name:g[node.patterns[-1].name]=s[l2-1:]
                return _B
        return _A
    elif isinstance(node,ast.MatchMapping):
        if isinstance(s,Mapping):
            star=node.rest;l1,l2=len(s),len(node.patterns)
            if star and l1>=l2 or l1==l2:
                keys=set()
                for (kp,vp) in zip(node.keys,node.patterns):
                    key=eval(compile(ast.Expression(kp),_E,_F),g);keys.add(key)
                    if key not in s:return _A
                    if not compare_match(s[key],g,vp):return _A
                if star:g[star]={k:v for(k,v)in s.items()if k not in keys}
                return _B
        return _A
    elif isinstance(node,ast.MatchClass):
        name=g.get(node.cls.id,_D)
        if name is _D:raise NameError("name '{}' is not defined".format(node.cls.id))
        if not isinstance(s,name):return _A
        ma=getattr(s,'__match_args__',());l1=len(ma);l2=len(node.patterns)
        if l1<l2:raise TypeError('{}() accepts {} positional sub-patterns ({} given)'.format(name,l1,l2))
        for (e,p) in enumerate(node.patterns):
            if not hasattr(s,ma[e]):return _A
            if not compare_match(getattr(s,ma[e]),g,p):return _A
        for (a,p) in zip(node.kwd_attrs,node.kwd_patterns):
            if not hasattr(s,a):return _A
            if not compare_match(getattr(s,a),g,p):return _A
        return _B
    elif isinstance(node,ast.MatchAs):
        if node.name is not _D:g[node.name]=s
        if node.pattern:return compare_match(s,g,node.pattern)
        return _B
    raise RuntimeError('Unknown Match pattern {}'.format(str(node)))
def evaluate_except(node,e,g,loop=_A):
    for n in node.handlers:
        if n.name:g[n.name]=e
        if n.type is _D:
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
                for (e,t) in enumerate(node.target.dims):g[t.id]=x[e]
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
                if m is not _D:
                    for ne in n.body:yield from evaluate(ne,g,loop)
                if e is _D:break
            if e is not _D:raise e
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
    else:_exec=ast.Module([node],[]);exec(compile(_exec,_E,'exec'),g);yield _D
def execute(cmd,no_except=_B,inline=_A,init='',g=_D):
    A='\n';console='';colors=[]
    if g is _D:g={'Ramp':Ramp,'Steps':Steps,'Row':Row,'HtmlRow':HtmlRow,'HtmlSteps':HtmlSteps,'HtmlGradient':HtmlGradient}
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
        import traceback;return '{}'.format(traceback.format_exc()),colors
    for node in tree.body:
        result=[];start=node.lineno;end=node.end_lineno;stmt=lines[start-1:end];command=''
        for (i,line) in enumerate(stmt,0):
            if i==0:stmt[i]='>>> '+line
            else:stmt[i]='... '+line
        command+=A.join(stmt)
        if isinstance(node,AST_BLOCKS):command+='\n... '
        try:
            with StreamOut()as s:
                for x in evaluate(node,g):
                    result.append(x);text=s.read()
                    if text:result.append(AtomicString(text))
                console+=command
        except Exception as e:
            if no_except:
                if not inline:from pymdownx.superfences import SuperFencesException;raise SuperFencesException from e
                else:from pymdownx.inlinehilite import InlineHiliteException;raise InlineHiliteException from e
            import traceback;console+='{}\n{}'.format(command,traceback.format_exc());break
        result_text=A
        for r in result:
            if r is _D:continue
            for clist in get_colors(r):
                if clist:colors.append(clist)
            result_text+='{}{}'.format(repr(r)if isinstance(r,str)and not isinstance(r,AtomicString)else str(r),A if not isinstance(r,AtomicString)else'')
        console+=result_text
    return console,colors
def colorize(src,lang,**options):HtmlFormatter=find_formatter_class('html');lexer=get_lexer_by_name(lang,**options);formatter=HtmlFormatter(cssclass=_G,wrapcode=_B);return highlight(src,lexer,formatter).strip()
def color_command_validator(language,inputs,options,attrs,md):
    valid_inputs={_H,'play','wheel'}
    for (k,v) in inputs.items():
        if k in valid_inputs:options[k]=_B;continue
        attrs[k]=v
    return _B
def _color_command_console(colors,gamut=WEBSPACE):
    B=' ';A='<div class="swatch-bar">{}</div>';el='';bar=_A;values=[]
    for item in colors:
        is_grad=isinstance(item,HtmlGradient);is_steps=isinstance(item,Steps)
        if is_grad or is_steps:
            current=total=percent=last=0
            if isinstance(item,Steps):total=len(item);percent=100/total;current=percent
            if bar:el+=A.format(B.join(values));values=[]
            sub_el1='<div class="swatch-bar"><span class="swatch swatch-gradient">{}</span></div>';style='--swatch-stops: ';stops=[]
            for (e,color) in enumerate(item):
                color.fit(gamut);color_str=color.convert(gamut).to_string()
                if current:
                    if is_steps:stops.append(_I.format(color_str,str(last)));stops.append(_I.format(color_str,str(current)))
                    else:stops.append(color_str)
                    last=current
                    if e<total-1:current+=percent
                    else:current=100
                else:stops.append(color_str)
            if not stops:stops.extend([_N]*2)
            if len(stops)==1:stops.append(stops[0])
            style+=','.join(stops);sub_el2='<span class="swatch-color" style="{}"></span>'.format(style);el+=sub_el1.format(sub_el2);bar=_A
        else:
            is_row=_A
            if isinstance(item,Row):
                is_row=_B
                if bar and values:el+=A.format(B.join(values));values=[]
                bar=_A
            bar=_B
            for color in item:
                base_classes=_O
                if not color.color.in_gamut(gamut):base_classes+=' out-of-gamut'
                color.color.fit(gamut);srgb=color.color.convert(gamut);value1=srgb.to_string(alpha=_A);value2=srgb.to_string();style='--swatch-stops: {} 50%, {} 50%'.format(value1,value2);title=color.string;classes=base_classes;c='<span class="swatch-color" style="{style}"></span>'.format(style=style);c='<span class="{classes}" title="{title}&#013;Copy to clipboard">{color}</span>'.format(classes=classes,color=c,title=title);values.append(c)
            if is_row and values:el+=A.format(B.join(values));values=[];bar=_A
    if bar:el+=A.format(B.join(values));values=[]
    return el
def _color_command_formatter(src='',language='',class_name=_D,options=_D,md='',init='',**kwargs):
    C='</div>';B='formatter';A='fenced_code_block';global code_id;from pymdownx.superfences import SuperFencesException;gamut=kwargs.get(_K,WEBSPACE);wheel=options.get('wheel',_A);play=options.get('play',_A)if options is not _D else _A
    if not play and language==_L:play=_B
    if not play:return md.preprocessors[A].extension.superfences[0][B](src=src,class_name=class_name,language='py',md=md,options=options,**kwargs)
    try:
        if wheel:
            gamut='srgb';exceptions=options.get(_H,_A)if options is not _D else _A;_,colors=execute(src.strip(),not exceptions,init=init);l=len(colors)
            if l not in(12,24,48):raise SuperFencesException('Color wheel requires either 12, 24, or 48 colors')
            colors=[c[0].color for c in colors]
            if l==12:freq=4;offset=6
            elif l==24:freq=8;offset=12
            else:freq=16;offset=24
            primary=colors[::freq][::-1];secondary=(colors[offset::freq]+[colors[offset//3]])[::-1];tertiary=colors[::offset//6][::-1];color_rings=[primary,secondary,tertiary];extra_rings_start='';extra_rings_end=''
            if l>12:extra_rings_start='<div class="tertiary2">';extra_rings_end+=C;color_rings.append(colors[::offset//12][::-1])
            if l>24:extra_rings_start='<div class="tertiary3">'+extra_rings_start;extra_rings_end+=C;color_rings.append(colors[::-1])
            color_stops=''
            for (i,colors) in enumerate(color_rings,1):
                total=len(colors);percent=100/total;current=percent;last=-1;stops=[]
                for (e,color) in enumerate(colors):
                    color.fit(gamut);color_str=color.convert(gamut).to_string()
                    if current:
                        stops.append(_I.format(color_str,str(last)));stops.append(_I.format(color_str,str(current)));last=current
                        if e<total-1:current+=percent
                        else:current=100
                    else:stops.append(color_str)
                color_stops+='--color-wheel-stops{}: {};'.format(i,','.join(stops))
            color_wheel='<div class="color-wheel" style="{}"><div class="wheel">\n{}<div class="tertiary"><div class="secondary"><div class="secondary-inner"><div class="primary"><div class="primary-inner"></div></div></div></div></div></div></div>{}'.format(color_stops,extra_rings_start,extra_rings_end);return color_wheel
        else:
            if len(md.preprocessors[A].extension.stash)==0:code_id=0
            exceptions=options.get(_H,_A)if options is not _D else _A;console,colors=execute(src.strip(),not exceptions,init=init);el=_color_command_console(colors,gamut=gamut);el+=md.preprocessors[A].extension.superfences[0][B](src=console,class_name=_G,language=_M,md=md,options=options,**kwargs);el=_P.format(el);el=template.format(el_id=code_id,raw_source=_escape(src),results=el,gamut=gamut);code_id+=1
    except SuperFencesException:raise
    except Exception:from pymdownx import superfences;import traceback;print(traceback.format_exc());return superfences.fence_code_format(src,'text',class_name,options,md,**kwargs)
    return el
def color_command_formatter(init='',gamut=WEBSPACE):return partial(_color_command_formatter,init=init,gamut=gamut)
def _color_formatter(src='',language='',class_name=_D,md='',exceptions=_B,init='',gamut=WEBSPACE):
    E='backtick';D='title';C='Only one color allowed';B=' 50%';A='span';from pymdownx.inlinehilite import InlineHiliteException
    try:
        result=src.strip()
        try:color=ColorAll(result.strip())
        except Exception as e:
            _,colors=execute(result,exceptions,inline=_B,init=init)
            if len(colors)!=1 or len(colors[0])!=1:
                if exceptions:raise InlineHiliteException(C) from e
                else:raise ValueError(C) from e
            color=colors[0][0].color;result=colors[0][0].string
        el=Etree.Element(A);stops=[]
        if not color.in_gamut(gamut):
            color.fit(gamut);attributes={_C:'swatch out-of-gamut',D:result};sub_el=Etree.SubElement(el,A,attributes);stops.append(color.convert(gamut).to_string(hex=_B,alpha=_A))
            if color[-1]<1.0:stops[-1]+=B;stops.append(color.convert(gamut).to_string(hex=_B)+B)
        else:
            attributes={_C:_O,D:result};sub_el=Etree.SubElement(el,A,attributes);stops.append(color.convert(gamut).to_string(hex=_B,alpha=_A))
            if color[-1]<1.0:stops[-1]+=B;stops.append(color.convert(gamut).to_string(hex=_B)+B)
        if not stops:stops.extend([_N]*2)
        if len(stops)==1:stops.append(stops[0])
        Etree.SubElement(sub_el,A,{_C:'swatch-color','style':'--swatch-stops: {};'.format(','.join(stops))});el.append(md.inlinePatterns[E].handle_code('css-color',result))
    except InlineHiliteException:raise
    except Exception:import traceback;print(traceback.format_exc());el=md.inlinePatterns[E].handle_code('text',src)
    return el
def color_formatter(init='',gamut=WEBSPACE):return partial(_color_formatter,init=init,gamut=gamut)
def _live_color_command_formatter(src,init='',gamut=WEBSPACE):
    try:
        console,colors=execute(src.strip(),_A,init=init);el=_color_command_console(colors,gamut=gamut)
        if not colors:el+='<div class="swatch-bar"></div>'
        el+=colorize(console,_M,**{'python3':_B,'stripnl':_A});el=_P.format(el)
    except Exception:import traceback;return '<div class="color-command"><div class="swatch-bar"></div>{}</div>'.format(colorize(traceback.format_exc(),_M))
    return el
def live_color_command_formatter(init='',gamut=WEBSPACE):return partial(_live_color_command_formatter,init=init,gamut=gamut)
def live_color_command_validator(language,inputs,options,attrs,md):value=color_command_validator(language,inputs,options,attrs,md);options[_H]=_B;return value
def render_console(*args,**kwargs):
    C='.swatch-bar';B='code';A='id_num';from js import document;gamut=kwargs.get(_K,WEBSPACE)
    try:
        inputs=document.getElementById('__playground-inputs_{}'.format(globals()[A]));results=document.getElementById('__playground-results_{}'.format(globals()[A]));footer=document.querySelector('#__playground_{} .gamut'.format(globals()[A]));result=live_color_command_formatter(LIVE_INIT,gamut)(inputs.value);temp=document.createElement('div');temp.innerHTML=result;cmd=results.querySelector('.color-command')
        for el in cmd.querySelectorAll(C):el.remove()
        for el in temp.querySelectorAll(C):cmd.insertBefore(el,cmd.lastChild)
        footer.innerHTML='Gamut: {}'.format(gamut);pre=cmd.querySelector('pre');pre.replaceChild(temp.querySelector(B),pre.querySelector(B));temp.remove();scrollingElement=results.querySelector(B);scrollingElement.scrollTop=scrollingElement.scrollHeight
    except Exception as e:print(e)
def render_notebook(*args,**kwargs):
    c='quote';b='example';a='bug';Z='danger';Y='failure';X='warning';W='question';V='success';U='tip';T='info';S='abstract';R='note';Q='settings';P='new';O='types';N='diagram';M='pymdownx.blocks.tab';L='pymdownx.blocks.details';K='pymdownx.blocks.admonition';J='pymdownx.arithmatex';I='pymdownx.keys';H='pymdownx.magiclink';G='pymdownx.inlinehilite';F='pymdownx.superfences';E='markdown.extensions.smarty';D='markdown.extensions.toc';C='validator';B='format';A='name';import markdown;from pymdownx import slugs,superfences;from js import document;gamut=kwargs.get(_K,WEBSPACE);text=globals().get('content','');extensions=[D,E,'pymdownx.betterem','markdown.extensions.attr_list','markdown.extensions.tables','markdown.extensions.abbr','markdown.extensions.footnotes',F,'pymdownx.highlight',G,H,'pymdownx.tilde','pymdownx.caret','pymdownx.smartsymbols','pymdownx.emoji','pymdownx.escapeall','pymdownx.tasklist','pymdownx.striphtml','pymdownx.snippets',I,'pymdownx.saneheaders',J,K,L,'pymdownx.blocks.html','pymdownx.blocks.definition',M];extension_configs={D:{'slugify':slugs.slugify(case='lower'),'permalink':''},E:{'smart_quotes':_A},J:{'generic':_B,'block_tag':'pre'},F:{'preserve_tabs':_B,'custom_fences':[{A:N,_C:N,B:superfences.fence_code_format},{A:_L,_C:_L,B:color_command_formatter(LIVE_INIT,gamut),C:live_color_command_validator},{A:'python',_C:_G,B:color_command_formatter(LIVE_INIT,gamut),C:live_color_command_validator},{A:'py',_C:_G,B:color_command_formatter(LIVE_INIT,gamut),C:live_color_command_validator}]},G:{'custom_inline':[{A:_J,_C:_J,B:color_formatter(LIVE_INIT,gamut)}]},H:{'repo_url_shortener':_B,'repo_url_shorthand':_B,'social_url_shorthand':_B,'user':'facelessuser','repo':'coloraide'},I:{'separator':'＋'},M:{'alternate_style':_B},K:{O:[P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c]},L:{O:[{A:'details-new',_C:P},{A:'details-settings',_C:Q},{A:'details-note',_C:R},{A:'details-abstract',_C:S},{A:'details-info',_C:T},{A:'details-tip',_C:U},{A:'details-success',_C:V},{A:'details-question',_C:W},{A:'details-warning',_C:X},{A:'details-failure',_C:Y},{A:'details-danger',_C:Z},{A:'details-bug',_C:a},{A:'details-example',_C:b},{A:'details-quote',_C:c}]}}
    try:html=markdown.markdown(text,extensions=extensions,extension_configs=extension_configs)
    except Exception:html=''
    content=document.getElementById('__notebook-render');content.innerHTML=html
