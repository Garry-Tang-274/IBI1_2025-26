import xml.dom.minidom
from datetime import datetime

def run_dom_parser(filename):
    print("Starting DOM parsing...")
    start_time = datetime.now()
    
    # Dictionary to store the term with max <is_a> count for each namespace
    results = {
        "molecular_function": {"term": None, "count": -1},
        "biological_process": {"term": None, "count": -1},
        "cellular_component": {"term": None, "count": -1}
    }
    
    # Parse the XML file
    doc = xml.dom.minidom.parse(filename)
    terms = doc.getElementsByTagName("term")
    
    for term in terms:
        # Extract namespace
        namespaces = term.getElementsByTagName("namespace")
        if not namespaces or not namespaces[0].firstChild:
            continue
        ns = namespaces[0].firstChild.data.strip()
        
        # Check if it's one of the target namespaces
        if ns in results:
            # Count <is_a> elements
            is_a_elements = term.getElementsByTagName("is_a")
            is_a_count = len(is_a_elements)
            
            if is_a_count > results[ns]["count"]:
                results[ns]["count"] = is_a_count
                # Extract term ID
                ids = term.getElementsByTagName("id")
                if ids and ids[0].firstChild:
                    results[ns]["term"] = ids[0].firstChild.data.strip()
    
    end_time = datetime.now()
    time_taken = end_time - start_time
    
    # Print results
    print("--- DOM API Results ---")
    for ns, data in results.items():
        print(f"Namespace: {ns} | Term: {data['term']} | Max <is_a> count: {data['count']}")
    print(f"Time taken by DOM: {time_taken}")

if __name__ == "__main__":
    run_dom_parser("go_obo.xml")