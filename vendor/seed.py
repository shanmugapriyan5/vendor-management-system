from faker import Faker
from .models import Vendor

# Initialize Faker for generating fake data
fake = Faker()

def seed_db(n=5)->None:
    """
    Seed the database with randomly generated Vendor instances.

    Args:
    - n (int): Number of Vendor instances to create (default is 5).

    Returns:
    - None
    """
    for _ in range(n):
        # Generate fake data for each Vendor instance
        name = fake.name()
        contact_details = f"Phone number: {fake.phone_number()}, email: {fake.profile('mail')}"
        address = fake.address()
        vendor_code = fake.bothify(text=f"{name.split()[0]}-#####")

        # Create Vendor instances with the generated fake data
        vendor = Vendor.objects.create(
            name = name,
            contact_details = contact_details,
            address = address,
            vendor_code = vendor_code
        )
