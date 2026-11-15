"""
Build clean, zero-bloat ZIP packages for all DL and DevOps projects and master packages.
Excludes:
- node_modules
- __pycache__
- .pytest_cache
- .git
- *.pyc
- zips/
"""

import os
import sys
import zipfile
import shutil

EXCLUDE_DIRS = {
    'node_modules',
    '__pycache__',
    '.pytest_cache',
    '.git',
    'zips',
    '.idea',
    '.vscode'
}

EXCLUDE_EXTS = {
    '.pyc',
    '.pyo',
    '.pyd',
    '.zip'  # prevent nesting existing zips
}

def should_include(path, base_folder):
    parts = os.path.normpath(path).split(os.sep)
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
    ext = os.path.splitext(path)[1].lower()
    if ext in EXCLUDE_EXTS:
        return False
    return True

def make_zip(source_dir, output_zip_path, prefix=""):
    print(f"[*] Packaging {os.path.basename(output_zip_path)} from {source_dir}...")
    os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)
    
    file_count = 0
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                full_path = os.path.join(root, file)
                if should_include(full_path, source_dir):
                    rel_path = os.path.relpath(full_path, source_dir)
                    arcname = os.path.join(prefix, rel_path) if prefix else rel_path
                    zipf.write(full_path, arcname)
                    file_count += 1
                    
    size_mb = os.path.getsize(output_zip_path) / (1024 * 1024)
    print(f"    [OK] Packaged {file_count} files -> {size_mb:.2f} MB")

def build_all():
    # 1. Individual DL Zips
    dl_base = r"c:\MOHIT\dl"
    make_zip(os.path.join(dl_base, "1_Mohit_AIOps_Cloud_Intelligence"),
             os.path.join(dl_base, "Mohit_12323329_AIOps_DL_Project.zip"),
             prefix="1_Mohit_AIOps_Cloud_Intelligence")

    make_zip(os.path.join(dl_base, "2_Akash_Autonomous_SWE_System"),
             os.path.join(dl_base, "Akash_12301625_SWE_DL_Project.zip"),
             prefix="2_Akash_Autonomous_SWE_System")

    make_zip(os.path.join(dl_base, "3_Saif_Cyber_Threat_Intelligence"),
             os.path.join(dl_base, "Saif_12308813_SecOps_DL_Project.zip"),
             prefix="3_Saif_Cyber_Threat_Intelligence")

    # 2. DL Master Zip (Everything in dl except dashboard/static/zips)
    make_zip(dl_base,
             os.path.join(dl_base, "ALL_3_INT422_DL_PROJECTS_MASTER.zip"),
             prefix="INT422_Deep_Learning_Suite")

    # 3. Individual DevOps Zips
    devops_base = r"c:\MOHIT\devops"
    make_zip(os.path.join(devops_base, "1_Mohit_Terraform_Nagios"),
             os.path.join(devops_base, "Mohit_12323329_Terraform_Nagios_Project.zip"),
             prefix="1_Mohit_Terraform_Nagios")

    make_zip(os.path.join(devops_base, "2_Akash_Puppet_Nagios"),
             os.path.join(devops_base, "Akash_12301625_Puppet_Nagios_Project.zip"),
             prefix="2_Akash_Puppet_Nagios")

    make_zip(os.path.join(devops_base, "3_Saif_Terraform_ALB_Nagios"),
             os.path.join(devops_base, "Saif_12308813_Terraform_ALB_Project.zip"),
             prefix="3_Saif_Terraform_ALB_Nagios")

    # 4. DevOps Master Zip
    make_zip(devops_base,
             os.path.join(devops_base, "ALL_3_INT333_DEVOPS_PROJECTS_MASTER.zip"),
             prefix="INT333_DevOps_Suite")

    # 5. Mirror to dashboard/static/zips
    dest_zip_dir = r"c:\MOHIT\dl\dashboard\static\zips"
    os.makedirs(dest_zip_dir, exist_ok=True)

    zips_to_copy = [
        (os.path.join(dl_base, "Mohit_12323329_AIOps_DL_Project.zip"), "mohit_dl.zip"),
        (os.path.join(dl_base, "Akash_12301625_SWE_DL_Project.zip"), "akash_dl.zip"),
        (os.path.join(dl_base, "Saif_12308813_SecOps_DL_Project.zip"), "saif_dl.zip"),
        (os.path.join(dl_base, "ALL_3_INT422_DL_PROJECTS_MASTER.zip"), "master_dl.zip"),
        (os.path.join(devops_base, "Mohit_12323329_Terraform_Nagios_Project.zip"), "mohit_devops.zip"),
        (os.path.join(devops_base, "Akash_12301625_Puppet_Nagios_Project.zip"), "akash_devops.zip"),
        (os.path.join(devops_base, "Saif_12308813_Terraform_ALB_Project.zip"), "saif_devops.zip"),
        (os.path.join(devops_base, "ALL_3_INT333_DEVOPS_PROJECTS_MASTER.zip"), "master_devops.zip"),
    ]

    print("[*] Mirroring zips to dashboard download directory...")
    for src, name in zips_to_copy:
        if os.path.exists(src):
            dst = os.path.join(dest_zip_dir, name)
            shutil.copy2(src, dst)
            print(f"    [Copied] {name} ({os.path.getsize(dst) / (1024*1024):.2f} MB)")

if __name__ == '__main__':
    build_all()
    print("[SUCCESS] All projects successfully packaged into zero-bloat ZIPs!")

