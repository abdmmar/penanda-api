def register_api(blueprint, view, endpoint, url, primary_key = "id", primary_key_type="int"):
  view_func = view.as_view(endpoint)
  blueprint.add_url_rule(url, defaults={primary_key: None}, view_func=view_func, methods=["GET"])
  blueprint.add_url_rule(url, view_func=view_func, methods=["POST"])
  blueprint.add_url_rule(f'{url}<{primary_key_type}:{primary_key}>', view_func=view_func, methods=["GET", "PUT", "DELETE"])