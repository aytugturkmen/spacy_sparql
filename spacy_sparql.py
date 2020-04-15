from SPARQLWrapper import SPARQLWrapper, JSON
from string import Template
import spacy
terms = []
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en")
# Process whole documents
text = """The entertainment system was belting out the Beatles' "We Can Work It Out" when the phone rang. When Pete answered, his phone turned the sound down by sending a message to all the other local devices that had a volume control. His sister,
Lucy, was on the line from the doctor's office: "Mom needs to see a specialist and then has to have a series of physical therapy sessions. Biweekly or something. I'm going to have my agent set up the appointments." Pete immediately agreed to share the chauffeuring. At the
doctor's office, Lucy instructed her Semantic Web agent through her handheld Web browser. The agent promptly retrieved information about Mom's prescribed treatment from the doctor's agent, looked up several lists of providers, and checked for the ones in-plan for Mom's insurance within a 20-mile radius of her home and with a rating of excellent or very good on trusted rating services. It then began trying to find a match between available appointment times (supplied by the agents of individual providers through their Web sites) and Pete's and Lucy's busy schedules. (The emphasized keywords indicate terms whose semantics, or meaning, were defined for the agent through the Semantic Web.)
In a few minutes the agent presented them with a plan. Pete didn't like it—University Hospital was all the way across town from Mom's place, and he'd be driving back in the middle of rush hour. He set his own agent to redo the search with stricter preferences about location and time. Lucy's agent, having complete trust in Pete's agent in the context of the present task, automatically assisted by supplying access certificates and shortcuts to the data it had already sorted through.
Almost instantly the new plan was presented: a much closer clinic and earlier times—but there were two warning notes. First, Pete would have to reschedule a couple of his less important appointments. He checked what they were—not a problem. The other was something about the insurance company's list failing to include this provider under physical therapists: "Service type and insurance plan status securely verified by other means," the agent reassured him. "(Details?)"
Lucy registered her assent at about the same moment Pete was muttering, "Spare me the details," and it was all set. (Of course, Pete couldn't resist the details and later that night had his agent explain how it had found that provider even though it wasn't on the proper list.)"""
doc = nlp(text)
# Analyze syntax.In addition to detecting named entities, nouns can also be detected. To do so, the noun_chunks attribute is used. 
for noun in doc.noun_chunks:
    if noun.root.pos_ != "PRON":
#lemmatize the text so as to get its root form eg: functions,funtionality as function
        terms.append(noun.root.lemma_.title())
# Find named entities, phrases and concepts.NER(Named Entity Recognition) is the process of getting the entity names.This is where named entity recognition comes to play. To get the named entities from a document, you have to use the ents attribute. Let's retrieve the named entities from the above sentence.
for entity in doc.ents:
#POS tag helps us to know the tags of each word like whether a word is noun, adjective etc.
    if entity.text not in terms and entity.root.pos_ != 'ADV' and entity.root.pos_ != 'NUM':
        terms.append(entity.text.title())
#Delete same items in the list
terms = list(dict.fromkeys(terms))
print("*****TERMS*****\n")
print(terms,"\n")
print("---------------------------------------------------------------------------------------------------------------------\n")

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#Prefix declarations, for abbreviating URIs.Associate URIs with prefixes
#A result clause, identifying what information to return from the query(SELECT)
#The query pattern, specifying what to query for in the underlying dataset(WHERE)
query = Template("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT ?label
    WHERE { $uri rdf:type ?label }
    LIMIT 1""")
try:
    print("*****ENTITY TYPE OF CLASS*****\n")
    for aman in terms:
#Send parameter to query
#Title: convert the first character in each word to Uppercase and remaining characters to Lowercase in string and returns new string.
        sparql.setQuery(query.substitute(uri="""<http://dbpedia.org/ontology/%s>"""%(aman.title())))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
#split() method returns a list of strings after breaking the given string by the specified separator.
            print (aman.title(),"===>",result["label"]["value"].split('#')[-1])
except:
    pass
