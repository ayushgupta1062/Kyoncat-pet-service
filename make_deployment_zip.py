import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in ['.git', '.venv', 'venv', 'venv_new', 'env', '__pycache__', 'staticfiles']]
        
        for file in files:
            if file in ['make_deployment_zip.py', '.DS_Store', 'kyonkat_aws_deploy.zip']:
                continue
            if file.endswith('.pyc'):
                continue
                
            file_path = os.path.join(root, file)
            # Calculate archive name (relative path)
            arcname = os.path.relpath(file_path, os.path.join(path))
            
            print(f"Adding {arcname}")
            ziph.write(file_path, arcname)

if __name__ == '__main__':
    zip_filename = 'kyonkat_aws_deploy.zip'
    print(f"Creating {zip_filename}...")
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
    print(f"Successfully created {zip_filename} ready for AWS Elastic Beanstalk upload!")
