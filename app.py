from flask import Flask, render_template, request
from rdflib import Graph

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reaction_results = []
    if request.method == "POST":
        reactant1 = request.form["reactant1"]
        reactant2 = request.form["reactant2"]

        # Define the SPARQL query
        query = f"""
        PREFIX : <http://example.org/chemistry.owl#>
        SELECT ?product
        WHERE {{
          ?reaction :has_reactant :{reactant1} .
          ?reaction :has_reactant :{reactant2} .
          ?reaction :has_product ?product .
        }}
        """

        # Load the ontology (change path if necessary)
        g = Graph()
        g.parse("chemical_reactions.owl")

        # Execute the query
        results = g.query(query)

        # Collect the results (showing only product names)
        for row in results:
            # Strip the full URI to just the name (e.g., H2O from the full URI)
            product_name = row[0].split("#")[-1]
            reaction_results.append(product_name)

    return render_template("index.html", results=reaction_results)

if __name__ == "__main__":
    app.run(debug=True)
