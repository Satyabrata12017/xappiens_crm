import frappe
from frappe.model.document import Document

def update_lead_with_email(self,method=None):
    email_id=self.get("email_id")
    last_modified_lead=""
    
    # Find the most recently modified lead with the given email_id
    last_modified_leads = frappe.get_all(
        'Lead',
        filters={'email_id': email_id},
        fields=['name'],
        order_by='modified desc',
        limit_page_length=1
    )
    if last_modified_leads:
        last_modified_lead=last_modified_leads[0].name

    if last_modified_lead:
        # Get all leads with the same email_id except the most recently modified one
        leads_to_append = frappe.get_all(
            'Lead',
            filters={'email_id': email_id, 'name': ['!=', last_modified_lead]},
            fields=['*']  # Fetch all fields
        )


        # Load the last modified lead document
        last_lead_doc = frappe.get_doc('Lead', last_modified_lead)
        create_related_lead(last_modified_lead,leads_to_append)

        

        # Delete all leads except the most recently modified one
        # for lead in leads_to_append:
        #     frappe.delete_doc('Lead', lead.name)

        # frappe.db.commit()

# Example usage
# update_lead_with_email('example@example.com')

def create_related_lead(last_lead_doc,leads_to_append):
    exclude_fields = ['name', 'doctype', 'modified', 'owner', 'creation', 'modified_by', 'idx', '_user_tags', '_comments', '_assign', '_liked_by', '_seen']
    for lead in leads_to_append:
        lead_data = {key: value for key, value in lead.items() if key not in exclude_fields}
        frappe.get_doc({
            "doctype":"Related Leads",
            "parent":last_lead_doc,
            "lead_data":str(lead_data),
            "parentfield":"custom_related_leads",
            "parenttype":"Lead"
        }).insert()

    frappe.db.commit()



from datetime import datetime

@frappe.whitelist()
def process_records():
    # Step 1: Fetch all records
    records = frappe.get_all('Lead', fields=['name', 'email_id', 'modified'])

    # Step 2: Group records by email_id
    grouped_records = {}
    for record in records:
        email_id = record['email_id']
        if email_id not in grouped_records:
            grouped_records[email_id] = []
        grouped_records[email_id].append(record)

    # Step 3: Process each group
    for email_id, recs in grouped_records.items():
        # Sort records by 'modified' in descending order
        recs.sort(key=lambda x: x['modified'], reverse=True)
        
        # Last modified record
        last_modified_record = recs[0]
        last_modified_doc = frappe.get_doc('Lead', last_modified_record['name'])
        
        # Append other records to the child table
        # frappe.log_error("recs",recs)
        child_records = recs[1:]
        for child_record in child_records:
            frappe.log_error("recs",child_record)
            last_modified_doc.append('custom_related_leads', {
                'lead_data': child_record
                # Add all required fields from the child records
            })
        
        # Save the changes
        last_modified_doc.save()

        # # Step 4: Delete old records
        # for old_record in recs[1:]:
        #     frappe.delete_doc('Lead', old_record['name'])

    # frappe.db.commit()