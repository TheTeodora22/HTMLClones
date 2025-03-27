# HTML Clones

## Introduction

We have a dataset with 4 subdirectories in increasing complexity

+ tier 1
+ tier 2
+ tier 3
+ tier 4

The subdirectories contain HTML documents.  We want to group them together based on how similar are they from the perspective of a user who opens them in a web browser.

##

Programming language chosen: Python

Frameworks & Libraries:

+ BeautifulSoup - to parse the HTML documents
+ Scikit-learn - ML algorithms
+ Numpy
+ Os

## Solution

### Reading the data

Using OS library, all files ending in ".html" are read from each directory sequentally and the files are then processed.

### Pre-processing text

+ clean any meta-tags that don't influence appearance

+ parse body tags structure

+ parse all html text

+ parse the css style

+ to all of these, added style, text and tags found in the script section

### TF-IDF Vectorizer

The function "TfidfVectorizer()" from sklearn library helped me to see how "important" each word 
actually is. 

Applying this function to each text, we get a different matrix that will be useful in our next calculations.

### Cosine Similarity

The three matrices, previously calculated, are combined into one by horizontally stacking them, in order to not apply the same function three times.

Instead we call the function "cosine_similarity()" from the sklearn library, to see how similar are the documents based on our criterias.

The result is a matrix of similarities. The numbers are between 0 and 1, with 0 being not similar at all and 1 being the exact same copy.

He are the matrices for each tier of documents:

Tier 1:

![Alt text](.\PozeClone\tier1.png)

Tier 2:

![Alt text](.\PozeClone\tier2.png)

Tier 3:

![Alt text](.\PozeClone\tier3.png)

Tier 4:

![Alt text](.\PozeClone\tier4.png)

### Clustering

1. Flip the similarity matrix
    
    First we take the similarity scores and convert them into distances(how far from 0 are they)
        
            distance = 1 - similarity
    
2. Hierarchical clustering
    
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
[aitoka.shop.html]
[amordevoltarapido.com.br.html]
[amt-avaluos.online.html]
[amyqnliycusz.shop.html]
[anzald.com.html]
[artfay.tv.html]
[ashfordcenter.world.html]
[astroservice.top.html]
[atyourlevel.online.html]
[authologic.io.html]
[celestialkeepsakes.com.html]
[amcun3.online.html, amcun9.online.html]
[championdirect.store.html, golf-saint-cyprien.com.html, sodearif.com.html]
[babubasics.co.uk.html, babubasics.com.html, eonfibre.net.html, paddygower.com.html, scalingspecialists.com.html, stratalaser.com.html, thisisthefuckingnews.com.html]
[badlandsconcerts.com.html, badlandslightfest.com.html, columbiahouse.ca.html, concoursparcscanada.ca.html, couplesdash.com.html, datewithdice.com.html, dudecheck.com.html, fmdistilled.com.html, globewayimmigration.com.html, ilovestubbs.com.html, membranereactor.com.html, nobullheating.com.html, rootsbluesbarbecue.com.html, soultosolesoundspa.com.html, templarsnotary.com.html, wifipresspad.com.html]
[alphamaterialsinc.com.html, americanairless.com.html, angelvisiontravel.com.html, brakeditorial.com.html, citizensagainstsextrafficking.org.html, crazyadsclimber.com.html, doughansonconstruction.com.html, fidexor.com.html, grantiah.com.html, harotzu.com.html, jandptrucking.com.html, keepmybooks.pro.html, keepmybooks.services.html, moneyweedwives.com.html, moneyweedwives.show.html, nounsbverbn.com.html, ordfld.com.html, pvcgs.org.html, pyramidelectric.us.html, rovics.com.html]
[aemails.org.html, aerex.eu.html, aevesdk3.com.html, afro-pari.com.html, ahamconsumerconnections.org.html, ahbynmkkmnfu.shop.html, ai-center.online.html, aigner-haag.at.html, akashinime.guru.html, alessiofalcone.it.html, alhasanfoundation.in.html, alileime.org.html, alimarkets.com.html, alimarkets.it.html, alinahoivatiimi.com.html, alinahoivatiimi.net.html, aliper.com.html, aliper.it.html, alisupermercati.com.html, alisupermercato.eu.html, almacom-gmbh.eu.html, almighty-jezuz.com.html, alwin.ltd.uk.html, amdac-carmichael.com.html, angangintl.com.html, annabeodog.xyz.html, aotvqsuprqnb.shop.html, apco911.com.html, apimco.link.html, app-go88s.biz.html, appleclub.tech.html, approvedfast.com.html, apps-foundry.com.html, arabianchemicalterminals.com.html, arbetslivsmuseer.se.html, arcadeeurope.com.html, argonfinancial.com.html, arttoy.cc.html, asahibeerusa.com.html, asd.net.html, asiafundspace.com.html, audreysweets.xyz.html]

Folder: tier2
[alessiodecurtis.com.html]
[altenheime-essen.de.html]
[petapilot.com.html]
[shopmeds.us.html]
[mariner-energy.com.html, starkwelt.com.html]
[ads-sedlmair.online.html, hanshammer.de.html, hhammer.de.html, kroha.de.html, local-marketing-lab.com.html, techcom-gmbh.de.html]
[acco-semi.com.html, bestcontentwritingservice.com.html, creplace.com.html, djdrinks.co.uk.html, engineeredrss.com.html, fortunatextiles.es.html, healthfly.in.html, mpgsx.com.mx.html, nykei.com.html, tiptopteak.com.html]

Folder: tier3
[ampika.com.html]
[dianessidewalkdeli.com.html]
[omerta-inc.com.html]
[proapremium.id.html]
[coade.icu.html, imzcr.me.html]
[afnanstore.shop.html, bersamaetawalin.site.html, cameliastore28.my.id.html, cosekarang.com.html, dhavinastore.com.html, dvnbysarah.com.html, elitemajesty.com.html, etawalinherbalmilk.site.html, juraganstore.shop.html, masjidrayaalfalah.id.html, parascerah.store.html, rakarta.com.html, susuetawalinkuid.site.html, tulangsendietawalin.site.html]
[1stmortgages.london.html, adeptohomes.com.html, belledermaaesthetics.com.html, columbiacouncilofneighborhoods.com.html, deltadoula.com.html, eastbourne.online.html, fieldtech.info.html, flyerfunnelsuk.com.html, frankieswinebar.com.html, furniturehutuk.com.html, g3rcq.com.html, hycareakarui.com.html, lagustosavaldebebas.com.html, lipolondon.com.html, londonviptaxi.com.html, okcis.info.html, renautautomotive.com.html, renewconsultants.com.html, sophrologue-paris14.com.html, thefoxinnbroadwell.com.html]

Folder: tier4
[assuredrxservices.com.html, coronadynamics.com.html, ecoled.co.in.html, lbgenetics.com.html, morriskamlay.com.html, rmhaddock.com.html, your-pc-guru.com.html]
[altnloyalty.com.html, ascendohio.com.html, lmeloyalty.com.html, nbesloyalty.com.html, novltyclub.com.html, shoalsslty.com.html, tlflhasit1.com.html, tryhrbyloyalty.com.html, visittlfl.com.html, wowlklnd.com.html, zenlfs.com.html]
[1-win-cazinos-club.org.ru.html, 1win-official-site-casinoz.org.ru.html, 1win-sloty.pp.ru.html, 1wincasinoz-vhod.org.ru.html, cazinos-official-1win.net.ru.html, cazinoz1-win.pp.ru.html, fontan-casino.pp.ru.html, fontan-mobile.net.ru.html, fontan-zercalo.net.ru.html, kasinos-1-win.net.ru.html, mirror-wulkan-russia.org.ru.html, vulcan-24kasinos.pp.ru.html]

## Problems and possible improvements

## Helpful Reading Sources

