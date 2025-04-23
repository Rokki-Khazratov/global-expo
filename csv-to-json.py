import csv
import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Member

# Define the output directory
OUTPUT_DIR = os.path.join(settings.BASE_DIR, 'exports')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Export to CSV
csv_file_path = os.path.join(OUTPUT_DIR, 'members.csv')
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write header
    writer.writerow(['ID', 'Name', 'Company', 'Position', 'Phone', 'Role', 'QR Code', 'Registration Time'])
    # Write data
    for member in Member.objects.all():
        writer.writerow([
            member.id,
            member.name,
            member.company.name if member.company else '',
            member.position.name if member.position else '',
            member.phone,
            member.get_role_display(),
            member.qr_code.url if member.qr_code else '',
            member.registration_time,
        ])

print(f"CSV file created at: {csv_file_path}")

# Export to XLSX
xlsx_file_path = os.path.join(OUTPUT_DIR, 'members.xlsx')
data = []
for member in Member.objects.all():
    data.append({
        'ID': member.id,
        'Name': member.name,
        'Company': member.company.name if member.company else '',
        'Position': member.position.name if member.position else '',
        'Phone': member.phone,
        'Role': member.get_role_display(),
        'QR Code': member.qr_code.url if member.qr_code else '',
        'Registration Time': member.registration_time,
    })

df = pd.DataFrame(data)
df.to_excel(xlsx_file_path, index=False)

print(f"XLSX file created at: {xlsx_file_path}")