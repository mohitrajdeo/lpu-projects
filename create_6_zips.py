"""
Create exactly 6 separate, submission-ready, zero-bloat ZIP packages for the 3 students:
1. Mohit_12323329_AIOps_DL_Project.zip (INT422)
2. Mohit_12323329_Terraform_Nagios_Project.zip (INT333)
3. Akash_12301625_SWE_DL_Project.zip (INT422)
4. Akash_12301625_Puppet_Nagios_Project.zip (INT333)
5. Saif_12308813_SecOps_DL_Project.zip (INT422)
6. Saif_12308813_Terraform_ALB_Project.zip (INT333)
"""

import os
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
    '.zip'
}

def should_include(path):
    parts = os.path.normpath(path).split(os.sep)
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
    ext = os.path.splitext(path)[1].lower()
    if ext in EXCLUDE_EXTS:
        return False
    return True

def package_project(src_dir, dest_zip_path, root_prefix):
    os.makedirs(os.path.dirname(dest_zip_path), exist_ok=True)
    file_count = 0
    with zipfile.ZipFile(dest_zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(src_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                full_path = os.path.join(root, f)
                if should_include(full_path):
                    rel = os.path.relpath(full_path, src_dir)
                    arcname = os.path.join(root_prefix, rel) if root_prefix else rel
                    zf.write(full_path, arcname)
                    file_count += 1
    size_mb = os.path.getsize(dest_zip_path) / (1024 * 1024)
    print(f"  [+] {os.path.basename(dest_zip_path):<45} : {file_count:>3} files | {size_mb:>6.2f} MB")
    return dest_zip_path, size_mb, file_count

def main():
    hub_dir = r"c:\MOHIT\6_PROJECT_ZIPS"
    os.makedirs(hub_dir, exist_ok=True)
    
    projects = [
        # Student 1: Mohit Raj Deo
        (
            r"c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence",
            os.path.join(hub_dir, "1_Mohit_12323329_INT422_DL_AIOps_Project.zip"),
            r"c:\MOHIT\dl\Mohit_12323329_AIOps_DL_Project.zip",
            "Mohit_12323329_AIOps_DL"
        ),
        (
            r"c:\MOHIT\devops\1_Mohit_Terraform_Nagios",
            os.path.join(hub_dir, "2_Mohit_12323329_INT333_DevOps_Terraform_Nagios.zip"),
            r"c:\MOHIT\devops\Mohit_12323329_Terraform_Nagios_Project.zip",
            "Mohit_12323329_Terraform_Nagios"
        ),
        # Student 2: Akash Choudhary
        (
            r"c:\MOHIT\dl\2_Akash_Autonomous_SWE_System",
            os.path.join(hub_dir, "3_Akash_12301625_INT422_DL_SWE_Project.zip"),
            r"c:\MOHIT\dl\Akash_12301625_SWE_DL_Project.zip",
            "Akash_12301625_SWE_Platform_DL"
        ),
        (
            r"c:\MOHIT\devops\2_Akash_Puppet_Nagios",
            os.path.join(hub_dir, "4_Akash_12301625_INT333_DevOps_Puppet_Nagios.zip"),
            r"c:\MOHIT\devops\Akash_12301625_Puppet_Nagios_Project.zip",
            "Akash_12301625_Puppet_Nagios"
        ),
        # Student 3: Saif Siddique
        (
            r"c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence",
            os.path.join(hub_dir, "5_Saif_12308813_INT422_DL_SecOps_Project.zip"),
            r"c:\MOHIT\dl\Saif_12308813_SecOps_DL_Project.zip",
            "Saif_12308813_SecOps_DL"
        ),
        (
            r"c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios",
            os.path.join(hub_dir, "6_Saif_12308813_INT333_DevOps_Terraform_ALB.zip"),
            r"c:\MOHIT\devops\Saif_12308813_Terraform_ALB_Project.zip",
            "Saif_12308813_Terraform_ALB"
        ),
    ]

    print("==========================================================================")
    print("COMPILING 6 SEPARATE CAPSTONE ZIP PACKAGES (INT422 & INT333)")
    print("==========================================================================")

    results = []
    for src, hub_zip, project_zip, prefix in projects:
        # Build to 6_PROJECT_ZIPS
        zip_path, size_mb, count = package_project(src, hub_zip, prefix)
        # Also copy to project directory
        shutil.copy2(hub_zip, project_zip)
        results.append((os.path.basename(hub_zip), size_mb, count))

    # Mirror to dashboard static directory so they are downloadable via web UI
    dashboard_zips = r"c:\MOHIT\dl\dashboard\static\zips"
    os.makedirs(dashboard_zips, exist_ok=True)
    mirror_map = [
        ("1_Mohit_12323329_INT422_DL_AIOps_Project.zip", "Mohit_12323329_AIOps_DL_Project.zip"),
        ("2_Mohit_12323329_INT333_DevOps_Terraform_Nagios.zip", "Mohit_12323329_Terraform_Nagios.zip"),
        ("3_Akash_12301625_INT422_DL_SWE_Project.zip", "Akash_12301625_SWE_DL_Project.zip"),
        ("4_Akash_12301625_INT333_DevOps_Puppet_Nagios.zip", "Akash_12301625_Puppet_Nagios.zip"),
        ("5_Saif_12308813_INT422_DL_SecOps_Project.zip", "Saif_12308813_SecOps_DL_Project.zip"),
        ("6_Saif_12308813_INT333_DevOps_Terraform_ALB.zip", "Saif_12308813_Terraform_ALB_Nagios.zip"),
    ]
    for src_name, dst_name in mirror_map:
        s = os.path.join(hub_dir, src_name)
        d = os.path.join(dashboard_zips, dst_name)
        shutil.copy2(s, d)

    print("==========================================================================")
    print("SUCCESS: ALL 6 CAPSTONE ZIP PACKAGES CREATED WITH ZERO BLOAT!")
    print(f"Location: {hub_dir}")
    print("==========================================================================")

if __name__ == '__main__':
    main()

