import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Member

def export_members_by_role():
    # Define role mappings (based on the ROLE_CHOICES in the model)
    role_files = {
        1: 'vip_members.xlsx',        # VIP
        2: 'exhibitor_members.xlsx',  # Exhibitor
        3: 'visitor_members.xlsx'     # Visitor
    }
    
    # Get all members
    members = Member.objects.all()
    
    # Create separate data lists for each role
    role_data = {1: [], 2: [], 3: []}
    
    for member in members:
        if member.role in role_data:
            role_data[member.role].append({
                'ID': member.id,
                'Ф.И.О.': member.name,
                'Компания': member.company.name if member.company else '',
                'Должность': member.position.name if member.position else '',
                'Телефон': member.phone,
                'Роль': member.get_role_display(),
                'Время регистрации': member.registration_time,
            })
    
    # Export separate files for each role
    for role_id, data in role_data.items():
        if data:  # Only create file if there is data for this role
            df = pd.DataFrame(data)
            output_file = role_files[role_id]
            df.to_excel(output_file, index=False)
            print(f"Exported {len(data)} {role_files[role_id].split('_')[0]} members to {output_file}")

if __name__ == '__main__':
    export_members_by_role() 