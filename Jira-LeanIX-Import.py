import json 
import requests 
import pandas as pd
import csv
import time
import datetime

api_token = 'KfbHuGuSZXkaOmjmjcB9qaGtymXryt8vPDjMWRSc'
auth_url = 'https://dropbox.leanix.net/services/mtm/v1/oauth2/token' 
request_url = 'https://dropbox.leanix.net/services/pathfinder/v1/graphql'

#API handler
response = requests.post(auth_url, auth=('apitoken', api_token),
                         data={'grant_type': 'client_credentials'})
response.raise_for_status() 
access_token = response.json()['access_token']
auth_header = 'Bearer ' + access_token
header = {'Authorization': auth_header}

#Implement GraphQL queries
def call(query):
  data = {"query" : query}
  json_data = json.dumps(data)
  response = requests.post(url=request_url, headers=header, data=json_data)
  response.raise_for_status()
  return response.json()

# Create Application
def createApplication(name):
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: Application}) {
        factSheet {
          id
        }
      }
  }
  """ % (name)
  print ("Create Application " + name)
  response = call(query)
  print (response)

#Create Business Capability
def createBusiness(business_name):
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: BusinessCapability}) {
        factSheet {
          id
        }
      }
  }
  """ % (business_name)
  print ("Create Business Capability " + business_name)
  response = call(query)
  print (response)

#Create Provider
def createProvider(provider_name):
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: Provider}) {
        factSheet {
          id
        }
      }
  }
  """ % (provider_name)
  print ("Create Provider " + provider_name)
  response = call(query)
  print (response)

def relationsProvider(id2, provider_name):
  query = """  
    {
      allFactSheets(filter: {displayName: "%s"}) {
        totalCount
        edges {
          node {
            displayName
            id
          }
        }
      }
    }""" % (provider_name)
  response = call(query)
  print (response)
  bcmd = str(response)
  id3 = bcmd.split("'")[17]
  query = """
    mutation {
      updateFactSheet(id: "%s", patches: [{op: add, path: "/relApplicationToProvider/new_1", value: "{\\"factSheetId\\":\\"%s\\"}"}]) {
        factSheet {
          id
          displayName
          ... on Application {
            relApplicationToProcess {
              edges {
                node {
                  id
                }
              }
            }
          }
        }
      }
    }
  """ % (id2, id3)
  response = call(query)
  print ("Relations have been created between: Provider towards Application")
  print (response)

def relationsBusiness(id2, business_name):
  query = """  
    {
      allFactSheets(filter: {displayName: "%s"}) {
        totalCount
        edges {
          node {
            displayName
            id
          }
        }
      }
    }""" % (business_name)
  response = call(query)
  print (response)
  bcmd = str(response)
  id3 = bcmd.split("'")[17]
  query = """
    mutation {
      updateFactSheet(id: "%s", patches: [{op: add, path: "/relApplicationToBusinessCapability/new_1", value: "{\\"factSheetId\\":\\"%s\\"}"}]) {
        factSheet {
          id
          displayName
          ... on Application {
            relApplicationToProcess {
              edges {
                node {
                  id
                }
              }
            }
          }
        }
      }
    }
  """ % (id2, id3)
  print ("Relations have been created between: towards Application")
  response = call(query)
  print (response)

#User Group
def userGroup(group):
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: UserGroup}) {
        factSheet {
          id
        }
      }
  }
  """ % (group)
  print ("Create User Group ")
  response = call(query)
  print (response)

def relationsUserGroup(id2, group):
  print (group)
  query = """  
    {
      allFactSheets(filter: {displayName: "%s"}) {
        totalCount
        edges {
          node {
            displayName
            id
          }
        }
      }
    }""" % (group)
  response = call(query)
  print (response)
  bcmd = str(response)
  id3 = bcmd.split("'")[17]
  query = """
    mutation {
      updateFactSheet(id: "%s", patches: [{op: add, path: "/relApplicationToUserGroup/new_1", value: "{\\"factSheetId\\":\\"%s\\"}"}]) {
        factSheet {
          id
          displayName
          ... on Application {
            relApplicationToProcess {
              edges {
                node {
                  id
                }
              }
            }
          }
        }
      }
    }
  """ % (id2, id3)
  response = call(query)
  print ("Relations have been created between User Group and Application")
  print (response)
  #data = pd.read_csv("jira_export.csv", index_col ="Custom field (Projected Usage)" ) 
  #data.drop(group, axis = 1, inplace = True)  

#Add user as Owner
def addUser(id2, system_owner, business_owner):
  query = """
    mutation {
    createSubscription(factSheetId: "%s", user: {email: "%s"}, type: RESPONSIBLE, validateOnly: false) {
      id
      user {
        userName
      }
      type
      roles {
        id
        name
        subscriptionType
      }
      createdAt
      factSheet {
        id
      }
    }
  }
  """ % (id2, system_owner)
  print ("User added with Responsible Role " + system_owner)
  response = call(query)
  print (response)
  query = """
    mutation {
    createSubscription(factSheetId: "%s", user: {email: "%s"}, type: OBSERVER, validateOnly: false) {
      id
      user {
        userName
      }
      type
      roles {
        id
        name
        subscriptionType
      }
      createdAt
      factSheet {
        id
      }
    }
  }
  """ % (id2, business_owner)
  print ("User added with Observer Role " + business_owner)
  response = call(query)
  print (response)

#Adding tags
def createTag(id2, tag_license, tag_dc, tag_software, tag_crit, tag_auth):
#license Type
  query = """
    {
      allTags(filter: {tagGroupName: "License Type", nameSubstring: "%s"}) {
        edges {
          node {
            tagGroup {
              name
              id
            }
            name
            id
          }
        }
      }
    }
  """ %(tag_license)
  response = call(query)
  print (response)
  tcmd = str(response)
  tagId = tcmd.split("'")[25]
  query = """
    mutation {
      result: updateFactSheet(id: "%s", patches: [{op: add, path:"/tags", value:"[{\\"tagId\\":\\"%s\\"}]"}], validateOnly: false) {
        factSheet {
          ... on Application {
            rev
            displayName
            tags {
              id
              name
              color
              description
              tagGroup {
                shortName
              }
            }
          }
        }
      }
    }
  """ % (id2, tagId)
  response = call(query)
  print ("License Type tag has been created")
  print (response)
#Data Classifications tag
  query = """
    {
      allTags(filter: {tagGroupName: "Data Classification", nameSubstring: "%s"}) {
        edges {
          node {
            tagGroup {
              name
              id
            }
            name
            id
          }
        }
      }
    }
  """ %(tag_dc)
  response = call(query)
  print (response)
  tcmd = str(response)
  tagId = tcmd.split("'")[25]
  query = """
    mutation {
      result: updateFactSheet(id: "%s", patches: [{op: add, path:"/tags", value:"[{\\"tagId\\":\\"%s\\"}]"}], validateOnly: false) {
        factSheet {
          ... on Application {
            rev
            displayName
            tags {
              id
              name
              color
              description
              tagGroup {
                shortName
              }
            }
          }
        }
      }
    }
  """ % (id2, tagId)
  response = call(query)
  print ("Data Classification tag has been created")
  print (response)
#Hosting tag
  query = """
    {
      allTags(filter: {tagGroupName: "Hosting", nameSubstring: "%s"}) {
        edges {
          node {
            tagGroup {
              name
              id
            }
            name
            id
          }
        }
      }
    }
  """ %(tag_software)
  response = call(query)
  print (response)
  tcmd = str(response)
  tagId = tcmd.split("'")[25]
  query = """
    mutation {
      result: updateFactSheet(id: "%s", patches: [{op: add, path:"/tags", value:"[{\\"tagId\\":\\"%s\\"}]"}], validateOnly: false) {
        factSheet {
          ... on Application {
            rev
            displayName
            tags {
              id
              name
              color
              description
              tagGroup {
                shortName
              }
            }
          }
        }
      }
    }
  """ % (id2, tagId)
  response = call(query)
  print ("Hosting tag has been created")
  print (response)
#Criticality tag
  query = """
    {
      allTags(filter: {tagGroupName: "Criticality", nameSubstring: "%s"}) {
        edges {
          node {
            tagGroup {
              name
              id
            }
            name
            id
          }
        }
      }
    }
  """ %(tag_crit)
  response = call(query)
  print (response)
  tcmd = str(response)
  tagId = tcmd.split("'")[25]
  query = """
    mutation {
      result: updateFactSheet(id: "%s", patches: [{op: add, path:"/tags", value:"[{\\"tagId\\":\\"%s\\"}]"}], validateOnly: false) {
        factSheet {
          ... on Application {
            rev
            displayName
            tags {
              id
              name
              color
              description
              tagGroup {
                shortName
              }
            }
          }
        }
      }
    }
  """ % (id2, tagId)
  response = call(query)
  print ("Criticality tag has been created")
  print (response)
#Authentication tag
  query = """
    {
      allTags(filter: {tagGroupName: "Authentication", nameSubstring: "%s"}) {
        edges {
          node {
            tagGroup {
              name
              id
            }
            name
            id
          }
        }
      }
    }
  """ % (tag_auth)
  response = call(query)
  print (response)
  tcmd = str(response)
  tagId = tcmd.split("'")[25]
  query = """
    mutation {
      result: updateFactSheet(id: "%s", patches: [{op: add, path:"/tags", value:"[{\\"tagId\\":\\"%s\\"}]"}], validateOnly: false) {
        factSheet {
          ... on Application {
            rev
            displayName
            tags {
              id
              name
              color
              description
              tagGroup {
                shortName
              }
            }
          }
        }
      }
    }
  """ % (id2, tagId)
  response = call(query)
  print ("Authentication tag has been created")
  print (response)  

#Lifecycle start date
def lifeCycle(id2, start_date):
  SD = pd.to_datetime(start_date)
  Mark = SD.strftime('%Y-%m-%d')
  query = """mutation {
     result:updateFactSheet(id:"%s", patches: [{op:add, path:"/lifecycle", value: "{\\"phases\\":[{\\"phase\\":\\"plan\\",\\"startDate\\":\\"%s\\"}]}"}], validateOnly:false) { 
       factSheet { 
         ... on Project {rev displayName 
           lifecycle{asString phases{phase startDate}}}
       }
     }
    }""" % (id2, Mark)
  response = call(query)
  print ("Start Date for lifeCycle has been add")
  print (response)

df = pd.read_csv('jira_export.csv',
                           header=0, encoding='ascii', engine='python')
print(df.columns.tolist())
print (df.head())

print ("Start : " + time.ctime())
for index, row in df.iterrows():
  try:
    try:
      createApplication(name = row['Custom field (Product Name)'])
      print()
      query = """
        {
          allFactSheets(filter: {displayName: "%s"}) {
            totalCount
            edges {
              node {
                displayName
                id
              }
            }
          }
        }
      """ % (row['Custom field (Product Name)'])
      print ("List of newest created Application in LeanIX :")
      response = call(query)
      print (response['data'])
      cmd = str(response)
    except IndexError:
      break
    if cmd.split("'")[13] == row['Custom field (Product Name)']:
      print ("split is working")
      id2 = cmd.split("'")[17]
    else:
      print ("sprint is not matching correctly, Application already exists")
      break
    createBusiness(business_name = row['Custom field (Software Category)'])
    print()
    relationsBusiness(id2, business_name = row['Custom field (Software Category)'])
    print()
    createProvider(provider_name = row['Custom field (Software Vendor)'])
    print()
    #######################################
    #userGroup(group = row['Custom field (Projected Usage)']) 
    #Projected Usage is repeated to many times in Excel,script only pulls the first mentioned column
    #print()
    #######################################
    relationsUserGroup(id2, group = row['Custom field (Projected Usage)'])
    print ()
    addUser(id2, system_owner = row['Custom field (System Owner)'], business_owner= row['Custom field (Business Owner)'] )
    print ()
    createTag(id2, tag_license = row['Custom field (License Type)'], tag_dc = row["Custom field (Data Classification)"], tag_software = row['Custom field (Software Type)'], tag_crit = row ['Custom field (Criticality)'], tag_auth = row['Custom field (Authentication)'])
    #Overwrites previous tag
    print ()
    lifeCycle(id2, start_date = row['Resolved'])
    print ()
  except KeyboardInterrupt:
    print("Field is empty, end of program.")
    break
print ("End : " + time.ctime())