# Jira---LeanIX-integration-

Jira <> LeanIX Integration
Owner: @Marques B 
Last Updated: 6/7/2019


# Background

To implement the Jira to LeanIX integration a python script will have to be used that takes an email sent out from Jira once the ticket is completed with specific data. It will be used to create applications within LeanIX following the +Jira Vendor Software Request MVP requirements. The script is using an API token from LeanIX to


# Process

Once a Vendor Service request ticket is closed it will push a type of data link through the methods listed below that will be filtered and organized through the python script. From there, the script contacts LeanIX through the API token and creates an application or business category based on the questions answered in the Vendor Service Request Form.

## Email
| Pros                          | Cons                                                      |
| ----------------------------- | --------------------------------------------------------- |
| Automated push from Jira      | Need to have security allow python script to access inbox |
| Emails can be used to as logs |                                                           |

## CSV Export
| Pros                                                                                                                                                                                                      | Cons                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Easier to configure and setup                                                                                                                                                                             | Manual pull Jira (could be done at EOD) |
| CSV can be used as daily log                                                                                                                                                                              |                                         |
| Can run script on current google sheet<br>to make up to date https://docs.google.com/spreadsheets/d/1Jg46PkSeH6rhsWQU3Px7Cqo3SGkDQwln-H1yuHgWKxc/edit?ouid=117110541779363535038&usp=sheets_home&ths=true |                                         |

# Implementation

Currently the python script is taking a csv export from a Jira filter and parses the data, from there it connects with LeanIX. However, before uploading anything into it LeanIX it pulls data of existing Applications, User Groups, Providers, tags, and Business Capability from LeanIX and compares the information from Jira towards LeanIX. For Applications, Business Capability, User Groups and Providers in LeanIX it checks to see if it already exists based off the information from Jira. If it already exist it skips and moves on in the script, if it doesn’t exist yet it creates the new FactSheet. Whether the FactSheet already exists in LeanIX or not, based on the information in Jira it creates relations between all of these mentioned fields in LeanIX.

Once the FactSheets are created and the relations between all of them towards Application is made it then adds users to Application. The users are listed in Jira by email from the system owner and business owner fields. Users are known as Subscriptions in LeanIX when assigning FactSheets, there are only 2 roles though in LeanIX Responsible and Observer. The system owner is given responsible role while the business owner and anyone else added is given observer role (a person can only be given one role per FactSheet). Also if someone who doesn’t have access or an account in LeanIX is given one of these roles their email will show up with the role category but will not have access to this. The user’s status will be pending and an invite will need to be sent to them but it will only give them Viewer access to LeanIX.

After assigning users to Responsible and Observer the python script will then create tags onto the Application FactSheet (Currently the script is overwriting all tags added and is only allowing the last tag to remain). 

Lastly a Lifecycle is added to the Application FactSheet in LeanIX for when the application is started. There currently is not setting for end date so the lifecycle will continue to run on until the end date is added manually into the Application. The Lifecycle start date for the application is currently based off of the resolved start from Jira which the day in which the ticket is closed.

| Jira Custom Field   | LeanIX Field               |
| ------------------- | -------------------------- |
| Product Name        | Application                |
| Software Category   | Business Capability        |
| Software Vendor     | Provider                   |
| Projected Usage     | User Group                 |
| System Owner        | Subscriptions: Responsible |
| Business Owner      | Subscriptions: Observer    |
| License Type        | Tag                        |
| Data Classification |                            |
| Software Type       |                            |
| Criticality         |                            |
| Authentication      |                            |
| Resolved            | Lifecycle start date       |

