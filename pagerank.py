import os
import random
import re
import sys
from typing import Dict, List

DAMPING = 0.85
SAMPLES = 10000
ACCURACY = 0.001 # convergence

def main():
    
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    
    #ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    #print(f"PageRank Results from Sampling (n = {SAMPLES})")
    #for page in sorted(ranks):
    #    print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):

    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)

            # all links founded on the .html file except for links to the .html file itself
            pages[filename] = set(links) - {filename} 

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor) -> Dict[str, set]:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    mapped_links = dict[str, set]()

    links = corpus[page]
    dist_sum = 0
    for link in links:
        prob = ((1 - damping_factor)/len(corpus)) + (1/len(links) * damping_factor)
        mapped_links[link] = prob
        dist_sum += prob  

    #prop_dist[page] = 1 - dist_sum
    prop_dist[page] = (1 - damping_factor)/len(corpus) # pode ser que falte atribuir a probabilidade para uma página que não esteja listada como link


    # falta contemplar todas as condições de corpus

    return mapped_links 


def sample_pagerank(corpus, damping_factor, n):
    """
#    Return PageRank values for each page by sampling `n` pages
#    according to transition model, starting with a page at random.
#
#    Return a dictionary where keys are page names, and values are
#    their estimated PageRank value (a value between 0 and 1). All
#    PageRank values should sum to 1.
#    """
    

def iterate_pagerank(corpus : Dict[str, List[str]], _):

    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.  
    """

    print(f"CORPUS -> {corpus}\n\n")
    
    # create the initial pagerank results
    pagerank = dict[str, float]()
    
    link_by = dict[str, list[str]]()
    keys = corpus.keys() # Lista de chaves (string)
    
    print(f"keys: {keys}")

    # feed the pagerank results with pages as keys and the initial probability associated with it (1/N)
    for page_key_i in keys:
        pagerank[page_key_i] = 1/len(corpus)
        link_by[page_key_i] = []
        
        for page_key_j in keys:
            if page_key_i in corpus[page_key_j]:
                link_by[page_key_i].append(page_key_j)
        
        print(f"link_by[page_key_i]: {link_by[page_key_i]}")

        if not len(link_by[page_key_i]):
            link_by[page_key_i] = [*keys]

        #link_by[page_key_i] = [page_key_j if page_key_i in corpus[page_key_j] else (*keys) for page_key_j in keys] 
                                                                             
    # Modify pagerank with no need to return it? (from this current method)
    convergence = set() 
    update(corpus, pagerank, link_by, convergence)

    print(f"final convergence structure: {convergence}")

    return pagerank
  

def update(corpus : Dict[str, List[str]], pagerank : dict[str, float], link_by : dict[str, list[str]], convergence : set):
          
    print(f"linked_by: {link_by}")

    for page, curr_pr in pagerank.items():    
        
        print(f"Calculating pr for page {page} with current pr {curr_pr}")

        pr = 0
        for link in link_by[page]:

            print(f"Link {link} to current iteration page {page}")

            # The code information below could be encoded in the transition_model [theory]
            link_page_pr = pagerank[link] # pagerank of the link (how do pagerank is built?)
            num_of_links = len(corpus[link])

            print(f"num_of_links (link): {num_of_links}")
            
            link_contribution = link_page_pr/num_of_links
            
            print(f"Link contribution: {link_contribution}")
            #pr = pr + (DAMPING * link_contribution)
            pr = pr + link_contribution

        
        print(f"pr before DAMPING (0.15): {pr}")
        pr = (1-DAMPING)/len(corpus) + DAMPING * pr

        print(f"pr: {pr}")
        print(f"curr_pr: {curr_pr}")
        diff = curr_pr - pr 

        print(f"diff: {diff}")
        if abs(diff) <= ACCURACY:

            print(f"REACH CONVERGENCE for page: {page}") 
            pagerank[page] = pr
            convergence.add(page)
            
            if len(convergence) == len(corpus):
                return pagerank
        else:
            pagerank[page] = pr 

    update(corpus, pagerank, link_by, convergence)



if __name__ == "__main__":
    main()
