import xml.sax
from datetime import datetime

class GOContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_element = ""
        self.is_term = False
        self.buffer = ""
        self.term_id = ""
        self.namespace = ""
        self.is_a_count = 0
        
        self.results = {
            "molecular_function": {"term": None, "count": -1},
            "biological_process": {"term": None, "count": -1},
            "cellular_component": {"term": None, "count": -1}
        }

    def startElement(self, tag, attributes):
        self.current_element = tag
        if tag == "term":
            self.is_term = True
            self.is_a_count = 0
            self.term_id = ""
            self.namespace = ""
        elif tag == "is_a" and self.is_term:
            self.is_a_count += 1
        elif tag in ("id", "namespace"):
            # Re-initialise buffer when starting a new relevant tag
            self.buffer = ""

    def characters(self, content):
        if self.is_term and self.current_element in ("id", "namespace"):
            # Use += format to record all information to handle chunked content
            self.buffer += content

    def endElement(self, tag):
        if tag == "term":
            self.is_term = False
            ns = self.namespace.strip()
            if ns in self.results:
                if self.is_a_count > self.results[ns]["count"]:
                    self.results[ns]["count"] = self.is_a_count
                    self.results[ns]["term"] = self.term_id.strip()
        elif tag == "id" and self.is_term:
            self.term_id = self.buffer
        elif tag == "namespace" and self.is_term:
            self.namespace = self.buffer
        
        self.current_element = ""

def run_sax_parser(filename):
    print("Starting SAX parsing...")
    start_time = datetime.now()
    
    handler = GOContentHandler()
    parser = xml.sax.make_parser()
    # Disable namespaces feature to prevent errors with standard SAX parsing
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(handler)
    
    parser.parse(filename)
    
    end_time = datetime.now()
    time_taken = end_time - start_time
    
    # Print results
    print("--- SAX API Results ---")
    for ns, data in handler.results.items():
        print(f"Namespace: {ns} | Term: {data['term']} | Max <is_a> count: {data['count']}")
    print(f"Time taken by SAX: {time_taken}")

if __name__ == "__main__":
    run_sax_parser("go_obo.xml")
    
    # Comment stating which one ran fastest
    """
    Performance Note:
    The SAX API is generally much faster than the DOM API for large XML files like the Gene Ontology.
    Because SAX is an event-driven parser, it processes the file sequentially and does not load 
    the entire XML structure into memory. DOM loads everything into memory, which slows it down considerably.
    """