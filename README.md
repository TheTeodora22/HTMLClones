# HTML Clones 💻

## Introduction 

We have a dataset with 4 subdirectories in increasing complexity

+ tier 1
+ tier 2
+ tier 3
+ tier 4

The subdirectories contain HTML documents.  We want to group them together based on how similar are they from the perspective of a user who opens them in a web browser.

##

Programming language chosen: Python

Libraries used:

+ BeautifulSoup - to parse the HTML documents
+ Scikit-learn - ML algorithms
+ Matplotlib - create Heatmaps
+ Re - regular expressions
+ Scipy
+ Numpy 
+ Os

## Dependencies

### Prerequisites

Python 3.x must be installed on your system

Install dependencies:

        pip install beautifulsoup4 scikit-learn matplotlib scipy numpy

## How to Run

+ Open your terminal

+ Run the script by executing:

```bash
python main.py
```
+ Upon execution, you will be prompted to choose a processing mode:
    -  Enter 1 to process all subdirectories under the root directory.
    - Enter 2 to process a specific subdirectory (e.g., tier1, tier2, etc.).

+ The script will generate output files (groups.txt or groups_all.txt) that list the clustered groups of HTML files.

## Solution 

### Reading the data

Using OS library, all files ending in ".html" are read from each directory sequentally and the files are then processed.

### Preprocessing text

+ clean any meta-tags that don't influence appearance

+ parse body tags structure

+ parse all HTML text

+ parse the CSS style

+ added inline style elements

+ added style elements found in the script section

All the extracted texts are grouped in lists, according to their type.

### TF-IDF Vectorization

The function "TfidfVectorizer()" from sklearn library helped me to see how "important" each word, from each text,
actually is. 

**Why** *TF-IDF* (Term Frequency-Inverse Document Frequency)?

Simple word counts don't highlight the special, unique words, because they include most common words in the calculation(like "the" or "and"). The presence of this common words can interfere with the calculation of similarities.


Applying this function to each text type lists, we get matrices that will be useful in our next calculations.

### Cosine Similarity 

The three matrices, previously calculated, are combined into one by horizontally stacking them, in order to not apply the same function three times.

Cosine similarity is used to measure the similarity between two vectors by calculating the cosine of the angle between them.

We call the function "cosine_similarity()" from the sklearn library, to see how similar are the documents based on our criterias.

**Why** *Cosine Similarity*?

 Cosine similarity focuses on the orientation (or direction) of the vectors rather than their magnitude. This property is particularly useful when document lengths vary, as it measures similarity based on the distribution of terms rather than raw counts.

The result is a matrix of similarities. The numbers are between 0 and 1, with 0 being not similar at all and 1 being the exact same copy.

📊
He are the heatmaps based on the matrices for each tier of documents:

Tier 1:

![Alt text](https://github.com/TheTeodora22/HTMLClones/blob/main/PozeClone/tier1.png)

Tier 2:

![Alt text](https://github.com/TheTeodora22/HTMLClones/blob/main/PozeClone/tier2.png)

Tier 3:

![Alt text](https://github.com/TheTeodora22/HTMLClones/blob/main/PozeClone/tier3.png)

Tier 4:

![Alt text](https://github.com/TheTeodora22/HTMLClones/blob/main/PozeClone/tier4.png)

### Clustering 

**Why** *Agglomerative Clustering*?

Agglomerative Clustering doesn’t need you to specify the number of clusters upfront. It starts with each document as its own cluster and merges the closest ones, making it perfect when you’re unsure how many groups exist.

The dendrogram visually reveals how clusters form, and tweaking the merging threshold lets you easily adjust the level of detail in the final clusters.

***Steps:***

1. Flip the similarity matrix
    
    First we take the similarity scores and convert them into distances(how far from 0 are they)
        
            distance = 1 - similarity
    
2. Hierarchical clustering (via Agglomerative Clustering)
    
    + Each document has its own cluster
    + Repeatedly merges the two closest clusters
    +To decide on closeness, we see how far apart are these groups on average

3. Merging stop

        if average_distance > (1 - threshold)

    e.g Threshold = 0.7 → Stop merging when clusters are >30% apart

4. Final Clusters

    Returns a list of clusters where each cluster has HTML documents similar to each other.

## Result

Folder: tier1

[aitoka.shop.html], [amordevoltarapido.com.br.html], [amt-avaluos.online.html], [amyqnliycusz.shop.html], [anzald.com.html], [artfay.tv.html], [ashfordcenter.world.html], [astroservice.top.html], [atyourlevel.online.html], [authologic.io.html], [celestialkeepsakes.com.html], [amcun3.online.html, amcun9.online.html], [championdirect.store.html, golf-saint-cyprien.com.html, sodearif.com.html], [babubasics.co.uk.html, babubasics.com.html, eonfibre.net.html, paddygower.com.html, scalingspecialists.com.html, stratalaser.com.html, thisisthefuckingnews.com.html], [badlandsconcerts.com.html, badlandslightfest.com.html, columbiahouse.ca.html, concoursparcscanada.ca.html, couplesdash.com.html, datewithdice.com.html, dudecheck.com.html, fmdistilled.com.html, globewayimmigration.com.html, ilovestubbs.com.html, membranereactor.com.html, nobullheating.com.html, rootsbluesbarbecue.com.html, soultosolesoundspa.com.html, templarsnotary.com.html, wifipresspad.com.html], [alphamaterialsinc.com.html, americanairless.com.html, angelvisiontravel.com.html, brakeditorial.com.html, citizensagainstsextrafficking.org.html, crazyadsclimber.com.html, doughansonconstruction.com.html, fidexor.com.html, grantiah.com.html, harotzu.com.html, jandptrucking.com.html, keepmybooks.pro.html, keepmybooks.services.html, moneyweedwives.com.html, moneyweedwives.show.html, nounsbverbn.com.html, ordfld.com.html, pvcgs.org.html, pyramidelectric.us.html, rovics.com.html], [aemails.org.html, aerex.eu.html, aevesdk3.com.html, afro-pari.com.html, ahamconsumerconnections.org.html, ahbynmkkmnfu.shop.html, ai-center.online.html, aigner-haag.at.html, akashinime.guru.html, alessiofalcone.it.html, alhasanfoundation.in.html, alileime.org.html, alimarkets.com.html, alimarkets.it.html, alinahoivatiimi.com.html, alinahoivatiimi.net.html, aliper.com.html, aliper.it.html, alisupermercati.com.html, alisupermercato.eu.html, almacom-gmbh.eu.html, almighty-jezuz.com.html, alwin.ltd.uk.html, amdac-carmichael.com.html, angangintl.com.html, annabeodog.xyz.html, aotvqsuprqnb.shop.html, apco911.com.html, apimco.link.html, app-go88s.biz.html, appleclub.tech.html, approvedfast.com.html, apps-foundry.com.html, arabianchemicalterminals.com.html, arbetslivsmuseer.se.html, arcadeeurope.com.html, argonfinancial.com.html, arttoy.cc.html, asahibeerusa.com.html, asd.net.html, asiafundspace.com.html, audreysweets.xyz.html]

Folder: tier2

[alessiodecurtis.com.html], [altenheime-essen.de.html], [petapilot.com.html], [shopmeds.us.html], [mariner-energy.com.html, starkwelt.com.html], [ads-sedlmair.online.html, hanshammer.de.html, hhammer.de.html, kroha.de.html, local-marketing-lab.com.html, techcom-gmbh.de.html], [acco-semi.com.html, bestcontentwritingservice.com.html, creplace.com.html, djdrinks.co.uk.html, engineeredrss.com.html, fortunatextiles.es.html, healthfly.in.html, mpgsx.com.mx.html, nykei.com.html, tiptopteak.com.html]

Folder: tier3

[ampika.com.html], [dianessidewalkdeli.com.html], [omerta-inc.com.html], [proapremium.id.html], [coade.icu.html, imzcr.me.html], [afnanstore.shop.html, bersamaetawalin.site.html, cameliastore28.my.id.html, cosekarang.com.html, dhavinastore.com.html, dvnbysarah.com.html, elitemajesty.com.html, etawalinherbalmilk.site.html, juraganstore.shop.html, masjidrayaalfalah.id.html, parascerah.store.html, rakarta.com.html, susuetawalinkuid.site.html, tulangsendietawalin.site.html], [1stmortgages.london.html, adeptohomes.com.html, belledermaaesthetics.com.html, columbiacouncilofneighborhoods.com.html, deltadoula.com.html, eastbourne.online.html, fieldtech.info.html, flyerfunnelsuk.com.html, frankieswinebar.com.html, furniturehutuk.com.html, g3rcq.com.html, hycareakarui.com.html, lagustosavaldebebas.com.html, lipolondon.com.html, londonviptaxi.com.html, okcis.info.html, renautautomotive.com.html, renewconsultants.com.html, sophrologue-paris14.com.html, thefoxinnbroadwell.com.html]

Folder: tier4

[assuredrxservices.com.html, coronadynamics.com.html, ecoled.co.in.html, lbgenetics.com.html, morriskamlay.com.html, rmhaddock.com.html, your-pc-guru.com.html], [altnloyalty.com.html, ascendohio.com.html, lmeloyalty.com.html, nbesloyalty.com.html, novltyclub.com.html, shoalsslty.com.html, tlflhasit1.com.html, tryhrbyloyalty.com.html, visittlfl.com.html, wowlklnd.com.html, zenlfs.com.html], [1-win-cazinos-club.org.ru.html, 1win-official-site-casinoz.org.ru.html, 1win-sloty.pp.ru.html, 1wincasinoz-vhod.org.ru.html, cazinos-official-1win.net.ru.html, cazinoz1-win.pp.ru.html, fontan-casino.pp.ru.html, fontan-mobile.net.ru.html, fontan-zercalo.net.ru.html, kasinos-1-win.net.ru.html, mirror-wulkan-russia.org.ru.html, vulcan-24kasinos.pp.ru.html]


## Problems and possible improvements

#### Script-generated HTML

The current implementation parses the static HTML content as-is. If the entire HTML structure is generated dynamically in the script section , the parser may not capture the resulting DOM correctly. 

#### Computational Efficiency

+ Redundant Processing:

    The current approach processes every file each time, even if some documents remain unchanged, leading to inefficiencies in repeated runs.

    **Solution:**

    Implement a mechanism to process only new or changed HTML files, which can be beneficial in a continuously updating dataset.

+ Parallel Processing

    Use multiprocessing or threading to parse and process multiple HTML files concurrently, reducing overall runtime.

#### User Interface

+ Command-Line Interface (CLI)

    Develop a CLI to allow users to easily modify parameters (e.g., weights, thresholds, directories) without altering the code.


## Helpful Reading Sources

+ https://stackoverflow.com/questions/11709079/parsing-html-using-python

+ https://stackoverflow.com/questions/456302/how-to-determine-if-two-web-pages-are-the-same

+ https://scikit-learn.org/stable/user_guide.html

+ https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/

+ https://memgraph.com/blog/cosine-similarity-python-scikit-learn

+ https://alvarotrigo.com/blog/change-css-javascript/

