#### Initial Setup Guide

This guide provides a straightforward approach to interact with your MongoDB databases effectively.

1. **Rename the config_template Directory:**
   Start by renaming the config_template folder to config. This is a crucial step to set up your configuration
   environment.
2. **Generate Configuration Files:**
   Utilize the examples provided within the config_template directory to create your own configuration files. Feel free
   to generate as many configuration files as necessary to suit your needs.

3. **Examine Script Examples:**
   For practical insight, review the transfer_collection.py and transfer_database.py script examples. These scripts
   demonstrate how to transfer collections or entire databases. You can execute these scripts using the following
   commands:
    * To transfer a specific collection:

      ```python transfer_collection.py --source alias_of_your_source_db --target alias_of_your_target_db --collection name_of_the_collection_to_copy```
    * To transfer an entire database:

      ```python transfer_database.py --source alias_of_your_source_db --target alias_of_your_target_db```

2. **Customize Your Data Pipeline:**
   Leverage the functions and classes provided in manager.py and database.py to tailor your data management pipeline.
   These tools are designed to facilitate a range of database operations, allowing for customized data handling and
   manipulation.

By following these steps, you can efficiently set up and manage your MongoDB databases, ensuring a streamlined workflow
for your data management tasks.