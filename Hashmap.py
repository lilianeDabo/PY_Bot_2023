class Hashmap :
  def __init__(self, size):
    self.size = size
    self.buckets = []

    for i in range(size):
      self.buckets.append([])

  def set(self, key, value):
    hashed = hash(key) # we hash
    index = hashed % self.size # we modulo w/ size so we can get index

    #To make sure values are unique
    bucket = self.buckets[index]

    for i in range(len(bucket)):
    #Takes the newest value for said key
       if bucket[i][0] == key:
          del bucket[i]

    self.buckets[index].append((key,value)) # we append

  def get(self, key, string_of_value):
    value = ""

    given_key = (hash(key)) % self.size
   
    bucket = self.buckets[given_key] #the bucket we should be looking for ( it is both where we look ( hashed ) and the key we are looking for ( unhashed ) )

    for k, val in bucket:
        if k == key:
            value = val
        
    # string_of_value permet de voir plus clairement la catégorie de la donnée ( ex : history, dialogue...etc )
    return [f'id: {key}', f'{string_of_value}: {value}'] # Renvoie un string ressemblant plus à une hashmap avec l'id et la valeur entrée en argument

def get_user_value_saved(user_id, value_saved, string_of_value): # Renvoie une hashmap dans laquelle l'utilisateur et la valeur donnée sont associés
    H=Hashmap(100)
    H.set(user_id, value_saved)
    user_and_value = H.get(user_id, string_of_value)
    return user_and_value
  