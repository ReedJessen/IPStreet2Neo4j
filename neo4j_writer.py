import configparser
from neo4j.v1 import GraphDatabase, basic_auth
import datetime
from entity_models import Person, Patent, Company


class Neo4jWriter():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        user_name = config.get('neo4j credentials', 'user_name')
        password = config.get('neo4j credentials', 'password')
        bolt_host = config.get('neo4j credentials', 'bolt_host')

        self.driver = GraphDatabase.driver(bolt_host,
                              auth=basic_auth( user_name, password))

    def write_person(self, Person):
        Person.full_name = Person.full_name.replace("'", "")
        Person.full_name = Person.full_name.strip()
        print('Creating Person Node:' + str(Person.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                props = Person.__dict__
                props = ', '.join("{!s}: {!r}".format(key, val) for (key, val) in props.items())
                query = 'MERGE (a:Person {' + props + "})"
                print(query)
                write_tx.run(query)
                write_tx.success = True

    def write_patent(self, Patent):
        print('Creating Patent Node:' + str(Patent.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                props = Patent.__dict__
                props = ', '.join("{!s}: {!r}".format(key, val) for (key, val) in props.items())
                query = 'MERGE (a:Patent {' + props + "})"
                print(query)
                write_tx.run(query)
                write_tx.success = True


    def write_company(self, Company):
        Company.full_name =  Company.full_name.strip()
        print('Creating Company Node:' + str(Company.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                props = Company.__dict__
                props = ', '.join("{!s}: {!r}".format(key, val) for (key, val) in props.items())
                query = 'MERGE (a:Company {' + props + "})"
                write_tx.run(query)
                write_tx.success = True

    def write_person_to_patent(self, Person, Patent):
        print('Creating Invention Relationship:' + str(Person.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                query = "MATCH(a:Person {full_name: \'" + str(Person.full_name) + "\'}), (b:Patent {grant_number: \'" + str(
                    Patent.grant_number) + "\'}) MERGE(a)-[:Invented {priority_date: \'" + Patent.application_date + "\'}]->(b)"
                print(query)
                write_tx.run(query)
                write_tx.success = True

    def write_company_to_patent(self,Company,Patent):
        print('Creating Ownership Relationship:' + str(Person.__dict__))
        with self.driver.session() as session:
            with session.begin_transaction() as write_tx:
                query = "MATCH(a:Company {full_name: \'" + str(
                    Company.full_name) + "\'}), (b:Patent {grant_number: \'" + str(
                    Patent.grant_number) + "\'}) MERGE(a)-[:Owns]->(b)"
                print(query)
                write_tx.run(query)
                write_tx.success = True
