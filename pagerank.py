import os
import random
import re
import sys
from typing import Dict, List

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename} # all links founded on the .html file except for links to the .html file itself

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

#def sample_pagerank(corpus, damping_factor, n):
#    """
#    Return PageRank values for each page by sampling `n` pages
#    according to transition model, starting with a page at random.
#
#    Return a dictionary where keys are page names, and values are
#    their estimated PageRank value (a value between 0 and 1). All
#    PageRank values should sum to 1.
#    """
#    raise NotImplementedError

# Ex.
# { "1.html": [ "2.html", "3.html" ], "3.html": [ "1.html" ], "2.html": [] }
# PS. It is possible to have a page with no links (look at the algorithm)
def iterate_pagerank(corpus : Dict[str, List[str]], damping_factor: float) -> None:
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set accuracy
    accuracy = 0.001

    # create the initial pagerank results
    page_rank = dict[str, float]()
    
    # feed the pagerank results with pages as keys and the initial probability associated with (1/N)
    for page_key in corpus.keys():
        page_rank[page_key] = 1/len(corpus) 

    for page, _ in page_rank:  
        linked_by = corpus[page]
        page = (1-damping_factor)/len(corpus) + calculate_pr(linked_by)
        
        #tm = transition_model(corpus, page, damping_factor) # what is exactly the transition model?
        
        # What convergence means in this context? (Statistics & Probalistics)

def calculate_pr(linked : List[str]) -> float:
    for link in linked:
        # do something
        print(link)

    return 0.0

#def formula() -> float:
#    return 0.0







        









    raise NotImplementedError


if __name__ == "__main__":
    main()
