import os
import random
import re
import sys
from typing import Dict, List

DAMPING = 0.85 
SAMPLES = 10000
ACCURACY = 0.001 

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


def transition_model(corpus, page, damping_factor) -> Dict[str, float]:
    
    # verify if the current page has links to other pages from the corpus
    curr_page_links = corpus[page] if len(corpus[page]) else corpus.keys()
    randomness = 1-damping_factor/len(curr_page_links)
    equal_probability = 1/len(curr_page_links)

    # probability distribution structure
    pd = dict() 
    
    # every page in the corpus
    for page in corpus.keys():
        if page in curr_page_links:
            pd[page] = randomness + (damping_factor * equal_probability)
        else:
            pd[page] = randomness

    return pd
    
    
def sample_pagerank(corpus, damping_factor, n):
    """
#    Return PageRank values for each page by sampling `n` pages
#    according to transition model, starting with a page at random.
#
#    Return a dictionary where keys are page names, and values are
#    their estimated PageRank value (a value between 0 and 1). All
#    PageRank values should sum to 1.
#    """
    print(corpus)
    print(damping_factor)
    print(n)
    
def iterate_pagerank(corpus : Dict[str, List[str]], damping):
  
    # create the initial pagerank results
    pagerank = dict[str, float]()
    
    link_by = dict[str, list[str]]()
    keys = corpus.keys() 
    
    # feed the pagerank results with pages as keys and the initial probability associated with it (1/N)
    for page_key_i in keys:
        pagerank[page_key_i] = 1/len(corpus)
        link_by[page_key_i] = []
        
        # piece of code that builds the (page-links_to_that_page) structure (different from corpus)
        for page_key_j in keys:
            if page_key_i in corpus[page_key_j] or not len(corpus[page_key_j]):
                link_by[page_key_i].append(page_key_j)

    convergence = set() 
    update(corpus, pagerank, link_by, convergence, damping)

    return pagerank
  

def update(corpus : Dict[str, List[str]], pagerank : dict[str, float], link_by : dict[str, list[str]], convergence : set, damping : float):
      
    #for page_key in corpus.keys():
    #    
    #    # where the source page weight comes in the pr link calculation?
    #    pr = 0
    #    page_pd = transition_model(corpus, page_key, damping_factor=damping)
    #    for link, pd in page_pd.items():
    #        pr = pr + pd 
    #        
    #        curr_pr = pagerank[link]
    #        diff = curr_pr - pr                                      
    #        if abs(diff) <= ACCURACY:
    #            pagerank[link] = pr
    #            convergence.add(link)
    #            
    #            if len(convergence) == len(corpus):
    #                return pagerank
    #        else:
    #            pagerank[link] = pr 

    for page, curr_pr in pagerank.items():    
        pr = 0
        for link in link_by[page]:

            # The code information below could be encoded in the transition_model [theory]
            link_page_pr = pagerank[link]

            # part of the contribution calculation
            num_of_links = len(corpus[link]) if len(corpus[link]) else len(corpus.keys())  
            link_contribution = link_page_pr/num_of_links # probabilistic contribution calculation
            pr = pr + link_contribution
 
        pr = (1-damping)/len(corpus) + damping * pr
        diff = curr_pr - pr 

        if abs(diff) <= ACCURACY:
            pagerank[page] = pr
            convergence.add(page)
            
            if len(convergence) == len(corpus):
                return pagerank
        else:
            pagerank[page] = pr 

    update(corpus, pagerank, link_by, convergence, damping)


if __name__ == "__main__":
    main()
