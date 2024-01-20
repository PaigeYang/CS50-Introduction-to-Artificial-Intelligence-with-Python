from heredity import joint_probability, update
people = {'Lily': {"mother": None, "father": None},
          'James': {"mother": None, "father": None},
          'Harry': {"mother": "Lily", "father": "James"}}



one_gene = {'Lily', 'Harry'}
two_genes = {'James' }
have_trait = {'Lily', 'Harry'}

p = joint_probability(people, one_gene, two_genes, have_trait)


print(p)
