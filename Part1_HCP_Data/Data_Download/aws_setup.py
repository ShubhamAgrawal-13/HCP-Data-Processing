#AWS configure part

str1='''[hcp]
AWS_ACCESS_KEY_ID=AKIAXO65CT57PHRSAVVZ
AWS_SECRET_ACCESS_KEY=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
'''

f1=open("/root/.aws/credentials","w")
f1.write(str1);
f1.close()
