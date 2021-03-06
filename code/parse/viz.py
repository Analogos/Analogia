from StoryMatch import *
from graphstyle_node_edge import Digraph
import numpy as np

params = {'penwidth': '5', 'arrowsize': '2', 'format': 'png', 'shape': 'square', 'color': 'black', 'rankdir': 'LR'}
node_num_dict = {}
n_node = 0
n_node_previous_story = 0

def style_node_edge(i_x, i_y, i_r, g, pair=False):
    # in adj matrix, var y causes var x
    x = str(i_x)
    y = str(i_y)
    r = str(i_r)
    if pair == False:  #new nodes and edges
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
    else:  # matched pair, make bold

        if r == "-1":  # "bold node, no relation"
            g.node(x, penwidth=params['penwidth'])
            g.node(y, penwidth=params['penwidth'])

        elif r == "0":  # "causal":
            g.node(y, penwidth=params['penwidth'])
            g.node(x, fillcolor='yellow', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "1":  # "assumed_causal":
            g.node(x, penwidth=params['penwidth'])
            g.node(y, penwidth=params['penwidth'])
            g.edge(y, x, style='dotted', color='orange', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "2":  # "presumption":
            g.node(x, penwidth=params['penwidth'])
            g.node(y, fillcolor='orange', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, style='dotted', color='orange', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "3":  # "abduction":
            g.node(y, penwidth=params['penwidth'])
            g.node(x, fillcolor='greenyellow', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, color='greenyellow', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "4":  # "enablement":
            g.node(x, penwidth=params['penwidth'])
            g.node(y, fillcolor='pink', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, color='pink', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "5":  # "post_hoc_ergo_propter_hoc":
            g.node(x, penwidth=params['penwidth'])
            g.node(y, penwidth=params['penwidth'])
            g.edge(y, x, color='blue', style='dotted', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "6":  # "explicit_cause":
            g.node(x, penwidth=params['penwidth'])
            g.node(y, penwidth=params['penwidth'])
            g.edge(y, x, color='blue', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "7":  # "lead_to":
            g.node(y, penwidth=params['penwidth'])
            g.node(x, fillcolor='lightblue', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, color='lightblue', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "8":  # "strange_lead_to":
            g.node(y, penwidth=params['penwidth'])
            g.node(x, fillcolor='magenta3', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, color='magenta3', penwidth=params['penwidth'], arrowsize=params['arrowsize'])

        elif r == "9":  # "in_order_to":
            g.node(y, penwidth=params['penwidth'])
            g.node(x, fillcolor='grey', style='filled', penwidth=params['penwidth'])
            g.edge(y, x, color='grey', penwidth=params['penwidth'], arrowsize=params['arrowsize'])


def make_node(sent_arr, list_of_relation_mat, g, pair=False):
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
                        style_node_edge(i_x + n_node_previous_story, i_y + n_node_previous_story, i_r, g, pair)
                    i_x += 1
                i_y += 1
            i_r += 1
        n_node_previous_story += (n_node - n_node_previous_story)  # = the increase in num of node

    else:   #visualizing pairs
        i_r = 0
        for relation_mat in list_of_relation_mat:
            i_y = 0
            for y in relation_mat:
                i_x = 0
                for x in y:
                    annotation = "\n[" + str(pair) + "]"
                    if x == 0:
                        i_r = -1  # make nodes bold
                        g.node(str(node_num_dict.get(sent_arr[i_x])), sent_arr[i_x] + annotation)
                        g.node(str(node_num_dict.get(sent_arr[i_y])), sent_arr[i_y] + annotation)
                        # update dict
                        node_num_dict[sent_arr[i_y] + annotation] = node_num_dict.get(sent_arr[i_y])
                        # del old entries
                        del node_num_dict[sent_arr[i_x]]
                        style_node_edge(node_num_dict.get(sent_arr[i_x] + annotation),
                            node_num_dict.get(sent_arr[i_y] + annotation), i_r, g, pair)
                    if x == 1:
                        g.node(str(node_num_dict.get(sent_arr[i_x])), sent_arr[i_x] + annotation)
                        g.node(str(node_num_dict.get(sent_arr[i_y])), sent_arr[i_y] + annotation)
                        # update dict
                        node_num_dict[sent_arr[i_y] + annotation] = node_num_dict.get(sent_arr[i_y])
                        # del old entries
                        del node_num_dict[sent_arr[i_x]]
                        style_node_edge(node_num_dict.get(sent_arr[i_x] + annotation),
                            node_num_dict.get(sent_arr[i_y] + annotation), i_r, g, pair)

                    i_x += 1
                i_y += 1
            i_r += 1

#for prototype
def get_causal_relation_matrix(sent_arr):
    n_nodes = len(sent_arr)
    n_rel = 1  # only causal
    list_of_relation_mat = np.zeros((n_rel, n_nodes, n_nodes))
    for i in range(n_nodes - 1):  # all causal
        list_of_relation_mat[0][i][i + 1] = 1

    return list_of_relation_mat


def get_node_max_size(digraph):
    import re
    heights = [height.split('=')[1] for height in re.findall('height=[0-9.]+', str(digraph))]
    widths = [width.split('=')[1] for width in re.findall('(?:^|\W)width=[0-9.]+', str(digraph))]
    heights.sort(key=float)
    widths.sort(key=float)
    return heights[len(heights) - 1], widths[len(widths) - 1]


def main():
    # gv for extracting height, width
    # strict (bool) – Rendering should merge multi-edges.
    g = Digraph(engine='dot', format='gv', strict=True)  
    g.attr('node', shape=params['shape'], color=params['color'])
    g.graph_attr['rankdir'] = params['rankdir']
    
    #modify here
    given_story = STORY0
    query_story = STORY2
    print("[Given]\n" + "\n".join(given_story) + "\n")
    print("[Query]\n" + "\n".join(query_story) + "\n")

    similar_sentence_pairs = ""
    similar_sentences = get_longest_match(given_story, query_story)

    make_node(given_story, get_causal_relation_matrix(given_story), g)
    make_node(query_story, get_causal_relation_matrix(query_story), g)
    n_pair = 1
    for pair in similar_sentences:
        print("\n%s\n%s\n" % (given_story[pair[0]], query_story[pair[1]]))
        similar_sentence_pairs += "[" + str(n_pair) + "] " + given_story[pair[0]] + "\t" + query_story[pair[1]] + "\n"
        list_of_given_story_pair = [given_story[pair[0]]]
        list_of_query_story_pair = [query_story[pair[1]]]
        make_node(list_of_given_story_pair, get_causal_relation_matrix(list_of_given_story_pair), g, pair=n_pair)
        make_node(list_of_query_story_pair, get_causal_relation_matrix(list_of_query_story_pair), g, pair=n_pair)
        n_pair += 1
    score = round(calc_similarity_score(given_story, query_story, similar_sentences), 2)
    
    print("----- Diagnosis -----")
    print("==> Similarity Score = %f" % score)
    print("==> Verdict = %s" % judge_story(score))
    summary = "Similarity: " + str(score) + "\n" + str(similar_sentence_pairs)
    g.attr(label=summary, fontsize='40')

    # flexible node size
    params['height'], params['width'] = get_node_max_size(g.pipe().decode('utf-8'))
    g.node_attr['width'] = params['width']
    g.node_attr['height'] = params['height']
    g.format = params['format']
    
    #modify file name
    output = "story2.gv"
    g.render(output)
    print("output " + output + "." + params['format'])


if __name__ == '__main__':
    main()
