import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from .model import topology, route


def plots(c, summary, sweep, folder):
    folder.mkdir(exist_ok=True)
    plt.rcParams.update({'figure.dpi':140, 'font.size':10})
    def finish(name):
        if name == 'topology.png':
            plt.subplots_adjust(top=.88, bottom=.04)
        else:
            plt.tight_layout()
        plt.savefig(folder/name, bbox_inches='tight')
        plt.close()
    g = topology(c,c['conditions']['normal'])
    pos = c['positions']
    plt.figure(figsize=(10,5))
    nx.draw(g,pos,with_labels=True,node_color='#b9dbed',node_size=800)
    nx.draw_networkx_edge_labels(g,pos,edge_labels={(a,b):f"{e['bandwidth_mbps']}M / {e['delay_ms']}ms" for a,b,e in g.edges(data=True)},font_size=7)
    plt.suptitle('12-router topology: bandwidth / propagation + processing delay')
    finish('topology.png')
    fig, axes = plt.subplots(1,3,figsize=(15,4))
    for ax,(name,level) in zip(axes,c['conditions'].items()):
        g = topology(c,level)
        nx.draw(g,pos,ax=ax,with_labels=True,node_color='#dce9ee',node_size=450,edge_color='#cccccc')
        for a,color,width,style in [('baseline','#df8056',5,'solid'),('proposed','#12658b',2,'dashed')]:
            path = route(g,*c['pairs'][0],a)
            nx.draw_networkx_edges(g,pos,edgelist=list(zip(path,path[1:])),ax=ax,edge_color=color,width=width,style=style)
        ax.set_title(name)
    fig.suptitle('R1 to R12: baseline orange solid; proposed blue dashed')
    finish('selected_routes.png')
    for metric,label in [('delay_ms','Mean delivered delay (ms)'),('loss_pct','Packet loss (%)'),
                         ('throughput_mbps','Cohort goodput (Mbps)'),('pdr_pct','Packet delivery ratio (%)'),
                         ('hops','Selected path hops'),('qos_cost','Common QoS path cost')]:
        plt.figure(figsize=(7,4))
        for a,offset,color in [('baseline',-.18,'#df8056'),('proposed',.18,'#12658b')]:
            data = [r for r in summary if r['algorithm']==a]
            plt.bar([i+offset for i in range(3)],[r[metric] for r in data],width=.36,
                    yerr=[r[metric+'_ci95'] for r in data],capsize=4,label=a,color=color)
        plt.xticks(range(3),list(c['conditions']))
        plt.ylabel(label)
        plt.title('Paired experiments; approximate 95% CI')
        plt.legend()
        finish(metric+'.png')
    fig,axes = plt.subplots(1,2,figsize=(10,4))
    for a in ['baseline','proposed']:
        data = [r for r in sweep if r['algorithm']==a]
        for ax,m,label in zip(axes,['delay_ms','loss_pct'],['Delay (ms)','Loss (%)']):
            ax.plot([r['utilization'] for r in data],[r[m] for r in data],'-o',label=a)
            ax.set(xlabel='Core background utilization',ylabel=label)
            ax.legend()
    finish('performance_vs_congestion.png')
