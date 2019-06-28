import json 
import requests 
import pandas as pd
import csv
import time
import datetime
from jira import JIRA

#Jira connection
passwrd = input("Please enter in Jira password: ")
print ("Start : " + time.ctime())
jira = jira = JIRA(basic_auth=("UserEmail", passwrd), options={'server': '#Link to Jira'})

#LeanIX connection
api_token = ''
auth_url = 'https://(companyname).leanix.net/services/mtm/v1/oauth2/token' 
request_url = 'https://(companyname).leanix.net/services/pathfinder/v1/graphql'

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

def relationsProvider(provider_name, name):
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
      result: updateFactSheet(id: "%s", patches: [{op: replace, path: "/tags", value: "[{\\"tagName\\":\\"%s\\"}]"}], validateOnly: false) {
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
  """ % (id3, name)
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
def createTag(id2, tag_license, tag_dc, tag_software, tag_crit, tag_auth, tag_sec):
#license Type
#query not showing ids but no errors
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
  tagId7 = tcmd.split("'")[25]
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
  tagId6 = tcmd.split("'")[25]
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
  tagId5 = tcmd.split("'")[25]
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
  tagId4 = tcmd.split("'")[25]
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
  tagId3 = tcmd.split("'")[25]
#Security Review tag
  query = """
    {
      allTags(filter: {tagGroupName: "Security Review", nameSubstring: "%s"}) {
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
  """ % (tag_sec)
  response = call(query)
  print (response)
  tcmd2 = str(response)
  tagId2 = tcmd2.split("'")[25]
  query = """
    mutation {
      updateFactSheet(id: "%s", 
        patches: [{op: replace, path: "/tags", value: "[{\\\"tagId\\\":\\\"%s\\\"},{\\\"tagId\\\":\\\"%s\\\"},{\\\"tagId\\\":\\\"%s\\\"}, {\\\"tagId\\\":\\\"%s\\\"}, {\\\"tagId\\\":\\\"%s\\\"}, {\\\"tagId\\\":\\\"%s\\\"}]"}]) {
          factSheet {
          id
        } 
      }
    }
  """ % (id2, tagId2, tagId3, tagId4, tagId5, tagId6, tagId7)
  response = call(query)
  print ("Security Review tag has been created")
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


for issue in jira.search_issues('filter=12002', maxResults=50):
  print('Key: {}'.format(issue.key))
  print('Summary: {}'.format(issue.fields.summary))
  print('Software Category: {}'.format(str(issue.fields.customfield_11119.value)))
  print('Software Type: {}'.format(str(issue.fields.customfield_11123.value)))
  print('Software Vendor: {}'.format(str(issue.fields.customfield_11114)))
  print('Business Owner: {},'.format(str(issue.fields.customfield_11131.emailAddress)))
  print('System Owner: {}'.format(str(issue.fields.customfield_11132.emailAddress)))
  print('Authentication: {}'.format(str(issue.fields.customfield_11136.value)))
  print('Criticality: {}'.format(str(issue.fields.customfield_11128.value)))
  print('Data Classification: {}'.format(str(issue.fields.customfield_11133.value)))
  print('Data Types: {}'.format(str(issue.fields.customfield_11134)))
  print('License Type: {}'.format(str(issue.fields.customfield_11124.value)))
  print('Vendor Contact: {}'.format(str(issue.fields.customfield_11125)))
  print('Security Review: {}'.format(str(issue.fields.customfield_11139.value)))
  print('Projected Usage: {}'.format(str(issue.fields.customfield_11120)))
  print('Resolved: {}'.format(str(issue.fields.resolutiondate)))
  try:
    try:
      createApplication(name = issue.fields.summary)
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
      """ % (issue.fields.summary)
      print ("List of newest created Application in LeanIX :")
      response = call(query)
      print (response['data'])
      cmd = str(response)
    except IndexError:
      break
    if cmd.split("'")[13] == issue.fields.summary:
      print ("split is working")
      id2 = cmd.split("'")[17]
      print (id2)
      createBusiness(business_name = str(issue.fields.customfield_11119.value))
      print()
      relationsBusiness(id2, business_name = str(issue.fields.customfield_11119.value))
      print()
      createProvider(provider_name = str(issue.fields.customfield_11114))
      print()
      #relationsProvider(provider_name = str(issue.fields.customfield_11114), name = issue.fields.summary)
      #cannot make relatioin between application and provider https://dev.leanix.net/docs/data-model 
      print()
      ug = 1
      while ug < 50:
        try:
          userGroup(group = (str(issue.fields.customfield_11120).split("'")[ug])) 
          print()
          relationsUserGroup(id2, (str(issue.fields.customfield_11120).split("'")[ug]))
          ug += 4
        except IndexError:
          break
      print ()
      addUser(id2, system_owner = str(issue.fields.customfield_11132.emailAddress), business_owner= str(issue.fields.customfield_11131.emailAddress))
      print ()
      createTag(id2, tag_license = str(issue.fields.customfield_11124.value), tag_dc = str(issue.fields.customfield_11133.value), tag_software = str(issue.fields.customfield_11123.value), tag_crit = str(issue.fields.customfield_11128.value), tag_auth = str(issue.fields.customfield_11136.value), tag_sec = str(issue.fields.customfield_11139.value))
      print ()
      lifeCycle(id2, start_date = str(issue.fields.resolutiondate))
      print ()
  except KeyboardInterrupt:
    print("Field is empty, end of program.")
    break
print ("End : " + time.ctime())
