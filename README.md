# Pain
## Goals:

- programmatically query Web of Science
- retrieve abstracts, publication date, and author affiliation for relevant articles
- clean up results into 'tidy' format

## Web of Science
We want to use the Core Collection. We need access to the [premium API](http://wokinfo.com/products_tools/products/related/webservices/). Northwestern University is subscribed and it seems like querying the API from a campus IP works like a "premium" subscription.

Problem #1: doing it by hand is cumbersome and has reproducibility issues (incl. for us in 6 months).

Problem #2: The WoS web services are based on SOAP. SOAP is complicated.

Problem #3: WoS returns either files in either xml or badly formatted Excel or plain text (either key value pairs or tab-delimited tabular in UTF16-LE). Hand-formatting the Excel gets us back to #2. The other two are difficult to work with for non-programmers. We would prefer tidy Excel.

## Examples of WoS results
See directory `examples`.

Example query (used to collect the results in `examples`):

    SO=(PAIN OR "JOURNAL OF PAIN") AND TI=(gender OR women OR sex) AND TS=(gender OR sex OR women)

Example of a plain-text file with key value pairs:

    TI Genetic influence on variability in human acute experimental pain
       sensitivity associated with gender, ethnicity and psychological
       temperament
    SO PAIN
    AB While a variety of cultural, psychological and physiological factors contribute to variability in both clinical and experimental contexts, the role of genetic factors in human pain sensitivity is increasingly recognized as an important element. This study was performed to evaluate genetic influences on variability in human pain sensitivity associated with gender, ethnicity and temperament. Pain sensitivity in response to experimental painful thermal and cold stimuli was measured with visual analogue scale ratings and temperament dimensions of personality were evaluated. Loci in the vanilloid receptor subtype I gene (TRPV1), delta opioid receptor subtype I gene (OPRD2) and catechol O-methyltransferase gene (COMT) were genotyped using 5' nuclease assays. A total of 500 normal participants (306 females and 194 males) were evaluated. The sample composition was 62.0% European American, 17.4% African American, 9.0% Asian American, and 8.6% Hispanic, and 3.0% individuals with mixed racial parentage. Female European Americans with the TRPV1 Val(585) Val allele and males with low harm avoidance showed longer cold withdrawal times based on the classification and regression tree (CART) analysis. CART identified gender, an OPRD1 polymorphism and temperament dimensions of personality as the primary determinants of heat pain sensitivity at 49 degreesC. Our observations demonstrate that gender, ethnicity and temperament contribute to individual variation in thermal and cold pain sensitivity by interactions with TRPV1 and OPRD1 single nucleotide polymorphisms. (C) 2004 Published by Elsevier B.V. on behalf of International Association for the Study of Pain.
    RI Goldman, David/F-9772-2010
    OI Goldman, David/0000-0002-1724-5405

Example of a json file:

    <?xml version="1.0" ?>
    <records>	<REC r_id_disclaimer="ResearcherID data provided by Clarivate Analytics">
            <UID>WOS:000259172200006</UID>
            <static_data>
                <summary>
                    <EWUID>
                        <WUID coll_id="WOS"/>
                        <edition value="WOS.SCI"/>
                    </EWUID>
                    <pub_info coverdate="SEP 2008" has_abstract="Y" issue="9" pubmonth="SEP" pubtype="Journal" pubyear="2008" sortdate="2008-09-01" vol="9">
                        <page begin="813" end="822" page_count="10">813-822</page>
                    </pub_info>
                    <titles count="6">
                        <title type="source">JOURNAL OF PAIN</title>
                        <title type="source_abbrev">J PAIN</title>
                        <title type="abbrev_iso">J. Pain</title>
                        <title type="abbrev_11">J PAIN</title>
                        <title type="abbrev_29">J PAIN</title>
                        <title type="item">Effect of axillary lymph node dissection on prevalence and intensity of chronic and phantom pain after breast cancer surgery</title>
                    </titles>
                    <names count="5">
                        <name addr_no="1" daisng_id="1503908" role="author" seq_no="1">
                            <display_name>Steegers, Monique A.</display_name>

## Existing code
This kind fellow shared his Python SOAP client to query WoS: [Enrico Bacis' gh](https://github.com/enricobacis/wos).

Installing the client allows for two things:

- use a commandline `wos` command to query WoS
- import the module in order to create a client and automate queries

The former works "out-of-the-box" but does not return the same number of results as a manual search with an identical query. It is also not clear whether it queries the 'search' or the 'retrieve' API (probably the latter).

The latter exceeds our Python abilities.
