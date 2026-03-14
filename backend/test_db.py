from app.database import SessionLocal
from app import models

db = SessionLocal()

# 1. Create a Client [cite: 109]
new_client = models.Client(name="Bridge Corp", subscription_tier=models.SubscriptionTier.PRO)
db.add(new_client)
db.commit()
db.refresh(new_client)

# 2. Create a Project for that Client [cite: 110]
new_project = models.Project(name="Golden Gate SHM", client_id=new_client.id)
db.add(new_project)
db.commit()

print(f"Success! Created Client ID: {new_client.id} with Project: {new_project.name}")
db.close()
