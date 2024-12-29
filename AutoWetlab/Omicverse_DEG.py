import omicverse as ov
import pandas as pd
import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

#设定绘图格式，分辨率300dpi等
ov.utils.ov_plot_set()

data = ov.utils.read('https://raw.githubusercontent.com/Starlitnightly/Pyomic/master/sample/counts.txt',index_col=0,header=1)
data.columns=[i.split('/')[-1].replace('.bam','') for i in data.columns]
data.head()#读取文件并划分区间

ov.utils.download_geneid_annotation_pair()#下载基因对
data=ov.bulk.Matrix_ID_mapping(data,'genesets/pair_GRCm39.tsv')#基因ID比对
data.head()

dds=ov.bulk.pyDEG(data)#创建差异分析对象
print('... drop_duplicates_index success')

treatment_groups=['4-3','4-4'] #输入实验组列名
control_groups=['1--1','1--2'] #输入对照组列名
result=dds.deg_analysis(treatment_groups,control_groups,method='DEseq2')#进行差异分析

print(result.shape)
result=result.loc[result['log2(BaseMean)']>1]
print(result.shape)#筛选低表达基因

dds.foldchange_set(fc_threshold=-1, pval_threshold=0.05, logp_max=10)#可手动输入参数设置过滤阈值


dds.plot_volcano(title='DEG Analysis',figsize=(4,4),plot_genes_num=8,plot_genes_fontsize=12,)#可视化文件
#获得差异基因（上调/下调）

dds.plot_boxplot(genes=['Ckap2','Lef1'],treatment_groups=treatment_groups,control_groups=control_groups,
                 figsize=(2,3),fontsize=12,legend_bbox=(2,0.55))
#获得特定基因对在实验组和对照组的分布
dds.plot_boxplot(genes=['Ckap2'],treatment_groups=treatment_groups,
                control_groups=control_groups,figsize=(2,3),fontsize=12,
                 legend_bbox=(2,0.55))
#获得特定基因在实验组和对照组的分布

ov.utils.download_pathway_database() #GSEA 分析及富集
pathway_dict=ov.utils.geneset_prepare('genesets/WikiPathways_2019_Mouse.txt',organism='Mouse')#导入数据集
rnk=dds.ranking2gsea() #基因打分排序
gsea_obj=ov.bulk.pyGSEA(rnk,pathway_dict)#创建GSEA对象
enrich_res=gsea_obj.enrichment() #计算结果
gsea_obj.enrich_res.head()#显示重要基因
gsea_obj.plot_enrichment(num=10,node_size=[10,20,30],
                        cax_fontsize=12,
                        fig_title='Wiki Pathway Enrichment',fig_xlabel='Fractions of genes',
                        figsize=(2,4),cmap='YlGnBu',
                        text_knock=2,text_maxsize=30,
                        cax_loc=[2.5, 0.45, 0.5, 0.02],
                          bbox_to_anchor_used=(-0.25, -13),node_diameter=10,)
#num=基因个数 node_size=节点大小 cax_loc颜色条位置 cax_fontsize颜色条字体大小
#fig_title标题 #fig_xlabel x轴标题 #figsize轴标题 #

gsea_obj.enrich_res.index[:5]#对基因打分
fig=gsea_obj.plot_gsea(term_num=1,
                  gene_set_title='Matrix Metalloproteinases',
                  figsize=(3,4),
                  cmap='RdBu_r',
                  title_fontsize=14,
                  title_y=0.95)



