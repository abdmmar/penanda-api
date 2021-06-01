def register_api(blueprint, view, endpoint, url, primary_key = "id", primary_key_type="int"):
  view_func = view.as_view(endpoint)
  blueprint.add_url_rule(url, defaults={primary_key: None}, view_func=view_func, methods=["GET"])
  blueprint.add_url_rule(url, view_func=view_func, methods=["POST"])
  blueprint.add_url_rule(f'{url}<{primary_key_type}:{primary_key}>', view_func=view_func, methods=["GET", "PUT", "DELETE"])
  
def extractDataToDictionary(data, cursor):
  """merge row and data to be dictionary

  Args:
      data (tuple): tuple of data, ex: (1, 'budi', '1234')
      cursor (cursor()): get every row ex: ('id', 'name', 'password') from the last fetch

  Returns:
      data: data as dictionary ex: {'id': 1, 'name': 'budi', 'password': '1234'}
  """  
  row = [x[0] for x in cursor.description]
  item = {}
  
  for i in range(len(data)):
    item[row[i]] = data[i]
  
  return item