from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

class ModelAdmin(GuardedModelAdmin):
  #ModelAdim
  list_display = ('name', )
  
  #GuardedModelAdminMixin
  user_can_access_owned_objects_only = True

  # rewite of ModelAdmim 
  def has_module_permission(self, request):
    if super().has_module_permission(request):
      return True
    else:
      return self.get_model_objects(request).exists()

  # rewite of ModelAdmim 
  def get_queryset(self, request):
    if request.user.is_superuser:
      return super().get_queryset(request)
    data = self.get_model_objects(request)
    return data

  def get_model_objects(self, request, action=None, klass=None):
    actions = [action] if action else ['add', 'view', 'change', 'delete']
    klass = klass if klass else self.opts.model
    model_name = klass._meta.model_name
    return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

  def has_permission(self, request, action, obj=None):
    code_name = f'{action}_{self.opts.model_name}'
    if obj:
      return request.user.has_perm(f'{self.opts.app_label}.{code_name}', obj)
    else:
      return self.get_model_objects(request).exists()

  # rewite of ModelAdmim (has_view_permission, has_add_permission, has_change_permission, has_delete_permission)
  def has_view_permission(self, request, obj=None):
    return self.has_permission(request=request, action='view', obj=obj)
  
  def has_add_permission(self, request):
    return self.has_permission(request=request, action='add')

  def has_change_permission(self, request, obj=None):
    return self.has_permission(request=request, action='change', obj=obj)
    
  def has_delete_permission(self, request, obj=None):
    return self.has_permission(request=request, action='delete', obj=obj)
