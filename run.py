from neo4j_writer import Neo4jWriter
from entity_models import Person, Patent, Company
from IPStreet import client, query
import configparser



if __name__ == '__main__':

    # Instantiate neo4j writer and IP Street client
    writer = Neo4jWriter()
    client = client.Client('IP_STREET_API_KEY',2)

    # prep and send IP Street query
    query = query.PatentData()
    query.add_owner('Next IT Corp.')
    results = client.send(query)


    # Write all patent nodes
    for patent in results:
        print(patent)
        # Write all patent nodes
        patent_node = Patent()
        patent_node.grant_number = patent['grant_number']
        patent_node.publication_number = patent['publication_number']
        patent_node.title = patent['title']
        patent_node.application_date = patent['application_date']
        writer.write_patent(patent_node)

        inventors = patent['inventor'].split(';')
        for inventor in inventors:
            person_node = Person()
            person_node.full_name = inventor
            writer.write_person(person_node)
            writer.write_person_to_patent(person_node,patent_node)

        companies = patent['owner'].split(';')
        for company in companies:
            company_node = Company()
            company_node.full_name = company
            writer.write_company(company_node)
            writer.write_company_to_patent(company_node,patent_node)

