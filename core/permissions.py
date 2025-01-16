from rest_framework import permissions

class GlobalDefaultPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    app_permission_model = self.get_app_permission_model(
      method=request.method,
      view=view,
    )

    if not app_permission_model:
      return False
   
    return request.user.has_perm(app_permission_model)

  def get_app_permission_model(self, method, view):
    try:
      model_name = view.queryset.model._meta.model_name
      app_label = view.queryset.model._meta.app_label
      action = self.get_action_sufix(method)
      return f'{app_label}.{action}_{model_name}'
    except AttributeError:
      return None
  
  def get_action_sufix(self, method):
    method_actions = {
      'GET' : 'view',
      'POST' : 'add',
      'PUT' : 'change',
      'PATCH' : 'change',
      'DELETE' : 'delete',
      'OPTIONS' : 'view',
      'HEAD' : 'view'
    }
    return method_actions.get(method, '')