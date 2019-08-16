import json 
import requests 
import pandas as pd
import time
from jira import JIRA
import os, sys
import smtplib, ssl
import traceback

#Implement GraphQL queries
def call(query):
  data = {"query" : query}
  json_data = json.dumps(data)
  response = requests.post(url=request_url, headers=header, data=json_data)
  response.raise_for_status()
  return response.json()

#Create Application
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
def createBusiness2(business_other):
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: BusinessCapability}) {
        factSheet {
          id
        }
      }
  }
  """ % (business_other)
  print ("Create Business Capability " + business_other)
  response = call(query)
  print (response)

def createBusiness(business_parent, business_child):
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: BusinessCapability}) {
        factSheet {
          id
        }
      }
  }
  """ % (business_child)
  print ("Create Business Capability " + business_child)
  response = call(query)
  print (response)
  query = """
    mutation {
      createFactSheet(input: {name: "%s", type: BusinessCapability}) {
        factSheet {
          id
        }
      }
  }
  """ % (business_parent)
  print ("Create Business Capability " + business_parent)
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

def relationsBusiness2(id2, business_other):
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
    }""" % (business_other)
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

def relationsBusiness(id2, mercy):
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
  """ % (id2, mercy)
  print(query)
  print ("Relations have been created between: towards Application")
  response = call(query)
  print (response)

def childParent(business_parent, business_child):
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
        """ % (business_parent)
  response = call(query)
  print (response)
  parent_code = str(response)
  parent = parent_code.split("'")[17]
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
        """ % (business_child)  
  response = call(query)
  print (response)
  child_code = str(response)
  child = child_code.split("'")[17]
  query = """
    mutation {
        updateFactSheet(id: "%s", patches: [{op: add, path: "/relToChild/new_1", value: "{\\"factSheetId\\":\\"%s\\"}"}]) {
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
  """ % (parent, child)
  print ("Parent Child Relations have been created between")
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
      allTags(filter: {tagGroupName: "License", nameSubstring: "%s"}) {
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

def duplicateTicket(summary, new_issue):
  for issue in jira.search_issues("""summary ~ "%s" and issuetype = "New Feature" ORDER BY created ASC""" % (summary), maxResults=50):
    parent_issue = issue.key
    jira.create_issue_link(type="Duplicate", inwardIssue=new_issue, outwardIssue=parent_issue)

def emailSend(Key, useremail, master_time, lines):
  port = 587  # For starttls
  smtp_server = "smtp.gmail.com"
  #cc = "ea@dropbox.com"
  bcc = "mbutilla@dropbox.com"
  password = str(lines).split("'")[1]
  sender_email = useremail
  Text = """The Python Script For Jira LeanIX has been broken from either over use or Missing information within this a jira ticket please restart.\n   Ran a number of: """ + str(master_time) + """\n   Time and Date of Program Failure: """ + time.ctime() + """\n   Jira ticket failed on: """ + str(Key)
  Subject = "Jira LeanIX Script failed"
  message = 'Subject: {}\n\n{}'.format(Subject, Text)
  context = ssl.create_default_context()
  with smtplib.SMTP(smtp_server, port) as server:
      server.ehlo()  # Can be omitted
      server.starttls(context=context)
      server.ehlo()  # Can be omitted
      server.login(sender_email, password)
      server.sendmail(sender_email, bcc, message)
      #server.sendmail(sender_email, cc, message)
  print("Python script needs to be restarted, email with failue sent")

#Check Jira for existing LeanIX Factsheets
def preExisting():
  for issue in jira.search_issues('project = "Vendor Service Request" AND created >= -1d AND issuetype = "New Feature" AND status not in ("CorpEng Review", "Cancelled", "Done")', maxResults=50):
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
    response = call(query)
    print (response['data'])
    cmd = str(response)
    try:
      if cmd.split("'")[13] == issue.fields.summary:
        print ("Application Already exist within LeanIX")
        id2 = cmd.split("'")[17]
        comment = jira.add_comment(issue.key, """Application already exist within LeanIX, closing out ticket as cancelled.\n https://dropbox.leanix.net/dropboxSandbox/factsheet/Application/"""+ id2)
        jira.transition_issue(issue, '81')
      else:
        print(issue.key,)
        print("Application has not been requested before")
    except IndexError:
      print(issue.key,)
      print("Application has not been requested before")

def changeRequest():
  for issue in jira.search_issues('project = "Vendor Service Request" AND created >= -1d AND issuetype = Support AND status not in ("CorpEng Review", "Cancelled", "Done")', maxResults=50):
    query = """
      allFactSheets(filter: {displayName: "%s"}) {
              totalCount
        edges {
          node {
            displayName
            tags{
              name
              tagGroup {
                name
              }
            }
          }
        }
      }
    }
    """ % (issue.fields.summary)
    response = call(query)
    print (response['data'])
    cmd = str(response)
    print(cmd)
    try:
      if cmd.split("'")[13] == issue.fields.summary:
        print ("Application Already exist within LeanIX")
        id2 = cmd.split("'")[17]
        comment = jira.add_comment(issue.key, """Application already exist within LeanIX, closing out ticket as cancelled.\n https://dropbox.leanix.net/dropboxSandbox/factsheet/Application/"""+ id2)
        summary = issue.fields.summary
        new_issue = issue.key
        duplicateTicket(summary, new_issue)
        jira.transition_issue(issue, '141')
      else:
        print(new_issue)
        print("Application has not been requested before")
    except IndexError:
      print(new_issue)
      print("Application has not been requested before")

print ("Start : " + time.ctime())
master_time = 0
while master_time <= 135:
  with open('secrets/code.txt') as f:
    lines = f.readlines()
    password = str(lines).split("'")[3]
    api_token = str(lines).split("'")[5]
    useremail = str(lines).split("'")[7]
    jira = jira = JIRA(auth=(useremail, password), options={'server': str(lines).split("'")[9]})
    #LeanIX API 
    auth_url = 'https://dropbox.leanix.net/services/mtm/v1/oauth2/token' 
    request_url = 'https://dropbox.leanix.net/services/pathfinder/v1/graphql'

    #API handler
    response = requests.post(auth_url, auth=('apitoken', api_token),
                             data={'grant_type': 'client_credentials'})
    response.raise_for_status() 
    access_token = response.json()['access_token']
    auth_header = 'Bearer ' + access_token
    header = {'Authorization': auth_header}
    try:
      changeRequest()
      print()
      preExisting()
      print()
    except:
      print("No Tickets have been made yet")
    time.sleep(3200)
    master_time += 1
os.execl(sys.executable, sys.executable, *sys.argv)
emailSend(Key, useremail, master_time, lines)
     for issue in jira.search_issues('project = "Vendor Service Request" AND status = Done AND resolved is not EMPTY AND issuetype = "New Feature" AND resolved >= -1d', maxResults=50):
       print(len(issue.fields.summary) )
       if len(issue.fields.summary) == 0:
         print("No Tickets have been made yet.")
         time.sleep(3200)
         os.execl(sys.executable, sys.executable, *sys.argv)
       else:
         print("There are tickets in Jira")
         try:
           Key = issue.key
           Summary = issue.fields.summary
           business_parent = str(issue.fields.customfield_11065.value)
           business_child = str(issue.fields.customfield_11065.child.value)
           Software_Type = str(issue.fields.customfield_11066.value)
           business_other = str(issue.fields.customfield_11100.value)
           Software_Vendor = str(issue.fields.customfield_11060)
           Business_Owner = str(issue.fields.customfield_11074.emailAddress)
           System_Owner = str(issue.fields.customfield_11075.emailAddress)
           Authentication = str(issue.fields.customfield_11079.value)
           Criticality = str(issue.fields.customfield_11071.value)
           Data_Classification = str(issue.fields.customfield_11076.value)
           Data_Types = str(issue.fields.customfield_11060)
           License_Type = str(issue.fields.customfield_11067.value)
           Vendor_Contact = str(issue.fields.customfield_11060)
           Security_Review = str(issue.fields.customfield_11097.value)
           Projected_Usage = str(issue.fields.customfield_11059)
           Resolved = str(issue.fields.resolutiondate)
         except AttributeError:
           emailSend(Key, useremail, master_time, lines)
           sys.exit()
           try:
             createApplication(name = str(Summary))
             time.sleep(15)
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
             """ % (Summary)
             print ("Application in LeanIX as not been listed.")
             response = call(query)
             print (response['data'])
             cmd = str(response)
           except:
             emailSend(Key, useremail, master_time, lines)
             sys.exit()
           if cmd.split("'")[13].lower() == str(Summary).lower():
             print ("split is working")
             id2 = cmd.split("'")[17]
             print (id2)
             if business_parent == "Other":
               createBusiness2(business_other)
               print()
               relationsBusiness2(id2, business_other)
               print()
             else:
               createBusiness(business_parent, business_child)
               print()
               childParent(business_parent, business_child)
               print()
               query = """
                 {
                   allFactSheets(filter: {displayName: "%s / %s"}) {
                     totalCount
                     edges {
                       node {
                         displayName
                         id
                       }
                     }
                   }
                 }
               """ % (business_parent, business_child)
               response = call(query)
               print (response['data'])
               agh = str(response)
               mercy = agh.split("'")[17]
               relationsBusiness(id2, mercy)
             print()
             createProvider(provider_name = str(Software_Vendor))
             print()
             #relationsProvider(provider_name = str(issue.fields.customfield_11114), name = issue.fields.summary)
             #cannot make relatioin between application and provider https://dev.leanix.net/docs/data-model
             print()
             if str(Projected_Usage).split("'")[1] == "All Departments":
               group = "Product, Design, Growth, ITS, Central Services, Co-Founders, Application Eng, Cloud Eng, HelloSign, Black Ops, Comms, Finance, Legal, Office Services, People, Tuck Shop, BD, BSO, CX, Marketing, Sales & Channel"
               ug = 0
               while ug < 120:
                 try:
                   userGroup(group.split(", ")[ug]) 
                   print()
                   relationsUserGroup(id2, group.split(", ")[ug])
                   ug += 1
                 except IndexError:
                   break
             elif is not str(Projected_Usage).split("'")[1]:
               break
             else:
               ug = 1
               while ug < 120:
                 try:
                   userGroup(group = (str(Projected_Usage).split("'")[ug])) 
                   print()
                   relationsUserGroup(id2, (str(Projected_Usage).split("'")[ug]))
                   ug += 4
                 except IndexError:
                   break
             print ()
             addUser(id2, system_owner = str(System_Owner), business_owner= str(Business_Owner))
             print ()
             if str(Data_Classification) == "L1 - User data, Dropbox secrets, PII":
               Data_Classification = "Level-1"
             elif str(Data_Classification) == "L2 - Sensitive company data":
               Data_Classification = "Level-2"
             elif str(Data_Classification) == "L3 - Leveraged data":
              Data_Classification = "Level-3"
             else:
              Data_Classification = "None of the above"
             if str(Authentication) == "Enterprise single sign on":
               Authentication = "SSO Capable"
             elif str() == "Standalone username/password":
               Authentication = "SSO Incapable"
             else:
               Authentication = "No Auth"
             if str(Software_Type) == "Server software hosted on-prem":
               Software_Type = "On-Prem"
             elif str(Software_Type) == "Cloud software":
               Software_Type = "SaaS"
             elif str(Software_Type) == "Desktop software or browser plugin":
              Software_Type = "Standalone Client"
             elif str(Software_Type) == "Hybrid cloud/ on-prem solution":
              Software_Type = "Hybrid" 
             else:
              Software_Type = "no longer used"
             createTag(id2, tag_license = str(License_Type), tag_dc = str(Data_Classification), tag_software = str(Software_Type), tag_crit = str(Criticality), tag_auth = str(Authentication), tag_sec = str(Security_Review))
             print ()
             lifeCycle(id2, start_date = str(Resolved))
             print()
             time.sleep(30)
             print ("End : " + time.ctime())
         except KeyboardInterrupt:
           emailSend(Key, useremail, master_time, lines)
           sys.exit()
         except requests.exceptions.ConnectionError:
           emailSend(Key, useremail, master_time, lines)
           sys.exit()
         except:
           emailSend(Key, useremail, master_time, lines)
           sys.exit()
     try:
       time.sleep(3200)
       master_time += 1
     except KeyboardInterrupt:
       Key = "Script was stopped by a User: mbutilla"
       emailSend(Key, useremail, master_time, lines)
       sys.exit()
 os.execl(sys.executable, sys.executable, *sys.argv)
 emailSend(Key, useremail, master_time, lines)
