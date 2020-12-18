#AWS configure part

str1='''[hcp]
AWS_ACCESS_KEY_ID=*************\\ enter ur access key id
AWS_SECRET_ACCESS_KEY=******************\\enter your secret access key
'''

f1=open("/root/.aws/credentials","w")
f1.write(str1);
f1.close()
