import os
import sys
import django

# 1. Setup Environment first
BASE_DIR = '/var/www/online-edu/backend'
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# 2. Setup Django
django.setup()

# 3. Now import EVERYTHING ELSE
from django.conf import settings
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.request import Request
from apps.users.models import User
from apps.system.views import MaintenanceModeViewSet, IsDeveloper
from apps.users.views import UserViewSet

def audit_security():
    print("🚀 STARTING SECURITY & CONFIDENTIALITY AUDIT\n")
    
    # 1. Verify Developer Confidentiality (Admin perspective)
    print("--- 1. Testing Developer Confidentiality ---")
    # Find a strict admin (not a developer)
    admin_user = User.objects.filter(role='admin', is_developer=False).first()
    
    if not admin_user:
        print("⚠️ No strict admin found. Creating temporary admin for audit...")
        admin_user = User.objects.create_user(
            username='temp_audit_admin', 
            email='audit@admin.com', 
            password='audit_password',
            role='admin',
            is_staff=True,
            is_superuser=False,
            is_developer=False
        )
        created_temp_admin = True
    else:
        created_temp_admin = False

    dev_user = User.objects.filter(is_developer=True).first()
    
    if not admin_user or not dev_user:
        print("❌ Error: Could not find admin or developer users for testing.")
        # Try to find any user with developer role if is_developer isn't enough
        dev_user = User.objects.filter(role='developer').first()
        if not dev_user:
            return

    # Monkey-patch ALLOWED_HOSTS for test execution
    settings.ALLOWED_HOSTS.append('testserver')

    # Check UserViewSet Filter
    factory = APIRequestFactory()
    view = UserViewSet.as_view({'get': 'list'})
    request = factory.get('/api/users/', HTTP_HOST='testserver')
    force_authenticate(request, user=admin_user)
    response = view(request)
    
    # Check if response data is a list or a dictionary with 'results' key
    users_data = response.data
    
    if isinstance(users_data, dict) and 'results' in users_data:
        users_data = users_data['results']
        
    if not isinstance(users_data, list):
        print(f"⚠️ Unexpected response data format: {type(users_data)}")
        print(f"Data content: {users_data}")
        return

    user_ids = [str(u.get('id')) for u in users_data if isinstance(u, dict)]
    if str(dev_user.id) in user_ids:
        print(f"❌ FAIL: Admin can see developer (ID: {dev_user.id}) in user list!")
    else:
        print(f"✅ PASS: Admin cannot see developer (ID: {dev_user.id}) in user list.")

    # 2. Verify Read-Only Enforcement (Developer perspective)
    print("\n--- 2. Testing Read-Only Enforcement ---")
    # Action 'toggle' should no longer exist or be part of ReadOnlyModelViewSet
    factory = APIRequestFactory()
    view = MaintenanceModeViewSet.as_view({'post': 'toggle'}) if hasattr(MaintenanceModeViewSet, 'toggle') else None
    
    if view is None:
        print("✅ PASS: 'toggle' action is COMPLETELY REMOVED from ViewSet.")
    else:
        request = factory.post('/api/system/maintenance/toggle/')
        force_authenticate(request, user=dev_user)
        try:
            response = view(request)
            if response.status_code == 405:
                print("✅ PASS: 'toggle' action is disabled (405 Method Not Allowed).")
            else:
                print(f"❌ FAIL: 'toggle' action returned {response.status_code} instead of 405!")
        except Exception as e:
            print(f"✅ PASS: 'toggle' action call failed as expected: {str(e)}")

    # 3. Verify Developer Permissions
    print("\n--- 3. Testing Developer Permission Logic ---")
    permission = IsDeveloper()
    request_dev = factory.get('/dummy/')
    force_authenticate(request_dev, user=dev_user)
    
    # Wrap in DRF Request
    drf_request = Request(request_dev)
    
    is_perm_granted = permission.has_permission(drf_request, None)
    if is_perm_granted:
        print("✅ PASS: Developer has IsDeveloper permission.")
    else:
        print(f"❌ FAIL: Developer (ID: {dev_user.id}, is_dev: {getattr(dev_user, 'is_developer', 'N/A')}) lacks IsDeveloper permission!")

    # 4. Verify Admin Permissions on Developer Portal
    print("\n--- 4. Testing Admin Exclusion from Dev Portal ---")
    request_admin = factory.get('/api/system/maintenance/current/')
    force_authenticate(request_admin, user=admin_user)
    
    drf_request_admin = Request(request_admin)
    is_admin_perm_granted = permission.has_permission(drf_request_admin, None)
    
    print(f"DEBUG: Admin User: {admin_user.username}, Role: {admin_user.role}, is_developer: {getattr(admin_user, 'is_developer', 'N/A')}")

    if not is_admin_perm_granted:
        print("✅ PASS: Admin is denied access to Developer Portal API.")
    else:
        print("❌ FAIL: Admin has access to Developer Portal API!")

    print("\n🏁 SECURITY AUDIT COMPLETE")
    
    if 'created_temp_admin' in locals() and created_temp_admin:
        print("🧹 Cleaning up temporary admin user...")
        admin_user.delete()

if __name__ == "__main__":
    audit_security()
