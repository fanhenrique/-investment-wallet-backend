from django.contrib import admin
from .models import Wallet

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user, assign_perm

# from django.contrib.auth.models import Permission

# permissions = Permission.objects.create(name='permissions_users')


class WalletAdmin(GuardedModelAdmin):
  #ModelAdim
  list_display = ('name', )
  
  #GuardedModelAdminMixin
  user_can_access_owned_objects_only = True

  # rewite of ModelAdmim 
  def has_module_permission(self, request):
    # print('has_module_permission')
    if super().has_module_permission(request):
      return True
    else:
      # print('modelobject')
      return self.get_model_objects(request).exists()

  # rewite of ModelAdmim 
  def get_queryset(self, request):
    # print('get_queryset')
    if request.user.is_superuser:
      return super().get_queryset(request)
    return self.get_model_objects(request)

  def get_model_objects(self, request, action=None, klass=None):
    # print('get_model_objects')
    actions = [action] if action else ['add', 'view', 'change', 'delete']
    klass = klass if klass else self.opts.model
    model_name = klass._meta.model_name
    a = get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)
    print(a)
    return a
  def has_permission(self, request, action, obj=None):
    # print('has_permission')
    code_name = f'{action}_{self.opts.model_name}'
    # assign_perm(request.user, 'view_wallet', obj=obj)
    if obj:
      return request.user.has_perm(f'{self.opts.app_label}.{code_name}', obj)
    else:
      return self.get_model_objects(request).exists()

  # rewite of ModelAdmim (has_view_permission, has_add_permission, has_change_permission, has_delete_permission)
  def has_view_permission(self, request, obj=None):
    
    if request.user.is_superuser:
      return True
    # print('has_view_permission', request.user, obj)  
    return self.has_permission(request=request, action='view', obj=obj)
  
  def has_add_permission(self, request):
    # print('has_add_permission')
    if request.user.is_superuser:
      return True
    return self.has_permission(request=request, action='add')

  def has_change_permission(self, request, obj=None):
    # print('has_change_permission')
    if request.user.is_superuser:
      return True
    return self.has_permission(request=request, action='change', obj=obj)
    
  def has_delete_permission(self, request, obj=None):
    # print('has_delete_permission')
    if request.user.is_superuser:
      return True
    return self.has_permission(request=request, action='delete', obj=obj)

admin.site.register(Wallet)
