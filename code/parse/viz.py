import os
from StoryMatch import *

#os.environ["PATH"] += os.pathsep + 'C:/Users/Re/Anaconda3/Library/bin/graphviz'  # add path, run on server
from graphviz import Digraph
import numpy as np


def viz(i_x, i_y, i_r, g, pair=False):
    """
    0 1 y->x
    1 0
    """
    x = str(i_x)
    y = str(i_y)
    r = str(i_r)
    if pair == False:
        if r == "0":  # "causal":
            g.node(x, fillcolor='yellow', style='filled')
            g.edge(y, x)

        elif r == "1":  # "assumed_causal":
            g.edge(y, x, style='dotted', color='orange')

        elif r == "2":  # "presumption":
            g.node(y, fillcolor='orange', style='filled')
            g.edge(y, x, style='dotted', color='orange')

        elif r == "3":  # "abduction":
            g.node(x, fillcolor='greenyellow', style='filled')
            g.edge(y, x, color='greenyellow')

        elif r == "4":  # "enablement":
            g.node(y, fillcolor='pink', style='filled')
            g.edge(y, x, color='pink')

        elif r == "5":  # "post_hoc_ergo_propter_hoc":
            g.edge(y, x, color='blue', style='dotted')

        elif r == "6":  # "explicit_cause":
            g.edge(y, x, color='blue')

        elif r == "7":  # "lead_to":
            g.node(x, fillcolor='lightblue', style='filled')
            g.edge(y, x, color='lightblue')

        elif r == "8":  # "strange_lead_to":
            g.node(x, fillcolor='magenta3', style='filled')
            g.edge(y, x, color='magenta3')

        elif r == "9":  # "in_order_to":
            g.node(x, fillcolor='grey', style='filled')
            g.edge(y, x, color='grey')
    elif (pair == True):#matched pair

        if r=="-1":  # "bold node, no relation"
            g.node(x, penwidth=PENWIDTH)
            g.node(y, penwidth=PENWIDTH)
        elif r == "0":  # "causal":
            g.node(y, penwidth=PENWIDTH)
            g.node(x, fillcolor='yellow', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "1":  # "assumed_causal":
            g.node(x, penwidth=PENWIDTH)
            g.node(y, penwidth=PENWIDTH)
            g.edge(y, x, style='dotted', color='orange', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "2":  # "presumption":
            g.node(x, penwidth=PENWIDTH)
            g.node(y, fillcolor='orange', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, style='dotted', color='orange', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "3":  # "abduction":
            g.node(y, penwidth=PENWIDTH)
            g.node(x, fillcolor='greenyellow', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, color='greenyellow', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "4":  # "enablement":
            g.node(x, penwidth=PENWIDTH)
            g.node(y, fillcolor='pink', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, color='pink', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "5":  # "post_hoc_ergo_propter_hoc":
            g.node(x, penwidth=PENWIDTH)
            g.node(y, penwidth=PENWIDTH)
            g.edge(y, x, color='blue', style='dotted', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "6":  # "explicit_cause":
            g.node(x, penwidth=PENWIDTH)
            g.node(y, penwidth=PENWIDTH)
            g.edge(y, x, color='blue', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "7":  # "lead_to":
            g.node(y, penwidth=PENWIDTH)
            g.node(x, fillcolor='lightblue', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, color='lightblue', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "8":  # "strange_lead_to":
            g.node(y, penwidth=PENWIDTH)
            g.node(x, fillcolor='magenta3', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, color='magenta3', penwidth=PENWIDTH, arrowsize=ARROWSIZE)

        elif r == "9":  # "in_order_to":
            g.node(y, penwidth=PENWIDTH)
            g.node(x, fillcolor='grey', style='filled', penwidth=PENWIDTH)
            g.edge(y, x, color='grey', penwidth=PENWIDTH, arrowsize=ARROWSIZE)



def make_viz(sent_arr, list_of_relation_mat, g, pair=False):
    global n_node
    global n_node_previous_story
    if pair == False:
        for sent in sent_arr:  # assign # to each new node of sent
            g.node(str(n_node), sent)
            node_num_dict[sent] = n_node
            n_node += 1
        i_r = 0
        for relation_mat in list_of_relation_mat:
            i_y = 0
            for y in relation_mat:
                i_x = 0
                for x in y:
                    if x == 1:
                        viz(i_x + n_node_previous_story, i_y + n_node_previous_story, i_r, g, pair)
                    i_x += 1
                i_y += 1
            i_r += 1
        n_node_previous_story += (n_node - n_node_previous_story)  # = the increase in num of node

    if pair == True:
        i_r = 0
        for relation_mat in list_of_relation_mat:
            i_y = 0
            for y in relation_mat:
                i_x = 0
                for x in y:
                    if x == 0:
                        i_r=-1
                        viz(node_num_dict.get(sent_arr[i_x]), node_num_dict.get(sent_arr[i_y]), i_r, g, pair)
                    if x == 1:
                        viz(node_num_dict.get(sent_arr[i_x]), node_num_dict.get(sent_arr[i_y]), i_r, g, pair)
                    i_x += 1
                i_y += 1
            i_r += 1

def get_causal_relation_matrix(sent_arr):
    n_nodes = len(sent_arr)
    n_rel = 1  # only causal
    list_of_relation_mat = np.zeros((n_rel, n_nodes, n_nodes))
    for i in range(n_nodes - 1):  # all causal
        list_of_relation_mat[0][i][i + 1] = 1
        print("causal made: "+str(i))
    return list_of_relation_mat

def main():
    global n_pair
    n_pair=0
    global PENWIDTH
    PENWIDTH = '5'
    global ARROWSIZE
    ARROWSIZE = '2'
    global n_node #total num of nodes
    global n_node_previous_story
    global node_num_dict
    node_num_dict = {}
    n_node = 0
    n_node_previous_story = 0
    g = Digraph(engine='dot', format='png', strict=True)  # strict (bool) – Rendering should merge multi-edges.
    g.attr('node', shape='circle', color='black')
    g.graph_attr['rankdir'] = 'LR'

    #sent_arr = ["Mary likes John", "Mary sends a gift to John", "They are in love."]
    given_story = STORY0
    query_story = STORY5
    print("[Given]\n" + "\n".join(given_story) + "\n")
    print("[Query]\n" + "\n".join(query_story) + "\n")

    similar_sentence_pairs=""

    similar_sentences = get_longest_match(given_story, query_story)

    make_viz(given_story, get_causal_relation_matrix(given_story), g)
    make_viz(query_story, get_causal_relation_matrix(query_story), g)

    n_pair=1
    for pair in similar_sentences:
        print("\n%s\n%s\n" % (given_story[pair[0]], query_story[pair[1]]))
        similar_sentence_pairs+=str(n_pair)+". "+given_story[pair[0]]+"\t"+query_story[pair[1]]+"\n"
        list_of_given_story_pair=[given_story[pair[0]]]
        list_of_query_story_pair=[query_story[pair[1]]]
        make_viz(list_of_given_story_pair, get_causal_relation_matrix(list_of_given_story_pair), g, pair=True)
        make_viz(list_of_query_story_pair, get_causal_relation_matrix(list_of_query_story_pair), g, pair=True)
        n_pair+=1
    score = calc_similarity_score(given_story, query_story, similar_sentences)
    print("----- Diagnosis -----")
    print("==> Similarity Score = %f" % score)
    print("==> Verdict = %s" % judge_story(score))

    summary="Similarity: "+str(score)+"\n"+str(similar_sentence_pairs)
    g.attr(label=summary, fontsize='40')
    #g.render('StoryMatch.gv', view=True)
    g.render('story5.gv')

if __name__ == '__main__':
    main()
