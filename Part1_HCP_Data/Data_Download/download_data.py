# download_HCP_1200.py
#
# Author: Joke Durnez (joke.durnez@gmail.com)

# Import packages
import os
import tarfile
import shutil

SERIES_MAP = { 
'MNINonLinear':'MNINonLinear' 
}

x1=0
# Main collect and download function
def collect_and_download(out_dir,
                         subject,
                         series=SERIES_MAP.keys(),
                         tartasks=False
                         ):

    # Import packages

    import pandas
    import boto3
    import botocore
    global x1;

    # Init variables
    s3_bucket_name = 'hcp-openaccess'
    s3_prefix = 'HCP_1200'

    boto3.setup_default_session(profile_name='hcp')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hcp-openaccess')

    s3_keys = bucket.objects.filter(Prefix='HCP_1200/%s/'%subject)
    s3_keylist = [key.key for key in s3_keys]

    prefixes = ["HCP_1200/%s/%s"%(subject,x) for x in SERIES_MAP.values()]
    prefixes = tuple(prefixes)
    s3_keylist = [x for x in s3_keylist if x.startswith(prefixes)]

    # remove png and html and add only the data required
    s3_keylist = [x for x in s3_keylist if not x.endswith(('png','html'))]
    # s3_keylist = [x for x in s3_keylist if (x.endswith('rfMRI_REST1_LR.nii.gz')) or (x.endswith('rfMRI_REST2_LR.nii.gz')) or (x.endswith('.txt')) ]
    s3_keylist = [x for x in s3_keylist if (x.endswith('rfMRI_REST1_LR_hp2000_clean.nii.gz') or x.endswith('rfMRI_REST2_LR_hp2000_clean.nii.gz')) ]
    
    # If output path doesn't exist, create it
    if not os.path.exists(out_dir):
        print 'Could not find %s, creating now...' % out_dir
        os.makedirs(out_dir)

    # Init a list to store paths.
    print 'Collecting images of interest...'

    # And download the items
    total_num_files = len(s3_keylist)
    files_downloaded = len(s3_keylist)
    for path_idx, s3_path in enumerate(s3_keylist):
        rel_path = s3_path.replace(s3_prefix, '')
        rel_path = rel_path.lstrip('/')
        download_file = os.path.join(out_dir, rel_path)
        download_dir = os.path.dirname(download_file)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        try:
            if not os.path.exists(download_file):
                # print 'Downloading to: %s' % download_file
                with open(download_file, 'wb') as f:
                    bucket.download_file(s3_path,download_file)
                # print("FACTS: path: %s, file: %s"%(s3_path, download_file))
                x1=x1+1
                if x1%100==0:
                  print '%.3f%% percent complete' % \
                        (100*(float(path_idx+1)/total_num_files))
            else:
                print 'File %s already exists, skipping...' % download_file
                files_downloaded -= 1
        except Exception as exc:
            print 'There was a problem downloading %s Check and try again.' % s3_path
            print exc

    if tartasks:
        subdir = os.path.join(out_dir,"%s/MNINonLinear/Results/"%subject)
        if os.path.exists(subdir):
            try:
                protocols = [x for x in os.listdir(subdir) if x.startswith('tfMRI') and not x.endswith('tar.gz')]
            except OSError:
                print("OSError")
            else:
                for protocol in protocols:
                    print('tarring protocol %s in subject %s'%(subject,protocol))
                    protocoldir = os.path.join(subdir,protocol)
                    with tarfile.open(protocoldir+".tar.gz","w:gz") as tar:
                        tar.add(protocoldir,arcname=os.path.basename(protocoldir))
                    shutil.rmtree(protocoldir)

    print '%d files downloaded for subject %s.' % (files_downloaded,subject)

    print 'Done!'

# Make module executable
if __name__ == '__main__':
    # Import packages
    import argparse
    import sys

    # Init arparser
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments
    parser.add_argument('-o', '--out_dir', required=True, type=str,
                        help='Path to local folder to download files to')
    parser.add_argument('-s', '--subject', required=True, type=str,
                        help='Subject code')
    # Optional arguments
    parser.add_argument('-t', '--tartasks', required=False, action='store_true',help='To limit number of files: tar together tasks')

    args = parser.parse_args()

    out_dir = os.path.abspath(args.out_dir)
    subject = args.subject

    kwargs = {}
    if args.tartasks:
        kwargs['tartasks'] = args.tartasks

collect_and_download(out_dir=out_dir,subject=subject,**kwargs)
